from typing import Any, Dict, List, Literal, Optional, Type, Union

from pydantic import AliasChoices, ConfigDict, Field

from inference.core.workflows.execution_engine.entities.base import (
    Batch,
    OutputDefinition,
    WorkflowImageData,
)
from inference.core.workflows.execution_engine.entities.types import (
    OBJECT_DETECTION_PREDICTION_KIND,
    ImageInputField,
    StepOutputImageSelector,
    WorkflowImageSelector,
    StepOutputSelector
)
from inference.core.workflows.prototypes.block import (
    BlockResult,
    WorkflowBlock,
    WorkflowBlockManifest,
)
from smart_reid.core import SmartTrack, SmartTrackConfig

LONG_DESCRIPTION = """
Detect the location of barcodes in an image.

This block is useful for manufacturing and consumer packaged goods projects where you 
need to detect a barcode region in an image. You can then apply Crop block to isolate 
each barcode then apply further processing (i.e. OCR of the characters on a barcode).
"""


class BlockManifest(WorkflowBlockManifest):
    model_config = ConfigDict(
        json_schema_extra={
            "name": "Smart ReID",
            "short_description": "Track and ReID objects across frames.",
            "long_description": LONG_DESCRIPTION,
            "license": "Enterprise",
            "block_type": "tracker",
        }
    )
    type: Literal["SmartReID", "SmartReID"]
    images: Union[WorkflowImageSelector, StepOutputImageSelector] = ImageInputField
    predictions: StepOutputSelector(
        kind=[
           OBJECT_DETECTION_PREDICTION_KIND,
        ]
    ) = Field(
        title="Bounding Boxes",
        description="The output of a detection model describing the bounding boxes that will be used to track the objects.",
        examples=["$steps.my_object_detection_model.predictions"],
        validation_alias=AliasChoices("predictions", "detections"),
    )
    rematch_new_tracks: bool = Field(
        title="Rematch New Tracks",
        description="Whether to attempt to rematch new tracks to previous tracks.",
        default=True,
    )
    rematch_swapped_tracks: bool = Field(
        title="Rematch Swapped Tracks",
        description="Whether to attempt to rematch swapped tracks to previous tracks.",
        default=True,
    )
    track_activation_threshold: float = Field(
        title="Track Activation Threshold",
        description="The threshold for activating a track.",
        default=0.1,
    )
    lost_track_buffer: int = Field(
        title="Lost Track Buffer",
        description="The number of frames to wait before declaring a track lost.",
        default=1000,
    )
    minimum_matching_threshold: float = Field(
        title="Minimum Matching Threshold",
        description="The minimum threshold for matching tracks to detections.",
        default=0.99,
    )
    frame_rate: int = Field(
        title="Frame Rate",
        description="The frame rate of the video.",
        default=60,
    )
    minimum_consecutive_frames: int = Field(
        title="Minimum Consecutive Frames",
        description="The minimum number of consecutive frames a track must be visible for.",
        default=1,
    )



    @classmethod
    def accepts_batch_input(cls) -> bool:
        return True

    @classmethod
    def describe_outputs(cls) -> List[OutputDefinition]:
        return [
            OutputDefinition(
                name="tracks", kind=[OBJECT_DETECTION_PREDICTION_KIND]
            )
        ]

class SmartReIDBlock(WorkflowBlock):
    tracker = None
    def __init__(self):
        if self.tracker is None:
            self.tracker = SmartTrack(SmartTrackConfig(
                track_activation_threshold=0.1,
            lost_track_buffer=1000,
            minimum_matching_threshold=0.99,
            frame_rate=60)
        )

    @classmethod
    def get_manifest(cls) -> Type[WorkflowBlockManifest]:
        return BlockManifest
    
    def run(
        self,
        images: Batch[WorkflowImageData],
        predictions: OBJECT_DETECTION_PREDICTION_KIND,
        rematch_new_tracks: bool,
        rematch_swapped_tracks: bool,
        track_activation_threshold: float,
        lost_track_buffer: int,
        minimum_matching_threshold: float,
        frame_rate: int,
        minimum_consecutive_frames: int,
    ) -> BlockResult:
        # apply configuration settings
        config = SmartTrackConfig(
            rematch_new_tracks=rematch_new_tracks,
            rematch_swapped_tracks=rematch_swapped_tracks,
            track_activation_threshold=track_activation_threshold,
            lost_track_buffer=10000,#lost_track_buffer,
            minimum_matching_threshold=minimum_matching_threshold,
            frame_rate=frame_rate,
            minimum_consecutive_frames=minimum_consecutive_frames,
        )
        self.tracker.configure(config)
        inference_images = [i.to_inference_format(numpy_preferred=True).get("value") for i in images]
        results = []
        for image, prediction in zip(inference_images, predictions):
            tracks = self.tracker.update_with_detections(prediction, image)
            results.append(tracks)
        return [{"tracks": tracks} for tracks in results]
    
def load_blocks() -> List[Type[WorkflowBlock]]:
    return [SmartReIDBlock]
