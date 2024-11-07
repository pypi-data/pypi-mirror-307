from typing import List, Tuple

import numpy as np

from supervision.detection.core import Detections
from supervision.detection.utils import box_iou_batch
from smart_reid import matching
from smart_reid.basetrack import BaseTrack, TrackState
from smart_reid.kalman_filter import KalmanFilter
from smart_reid.strack import STrack
from smart_reid.sam_cost import async_rematch
from threading import Thread


def detections2boxes(detections: Detections) -> np.ndarray:
    """
    Convert Supervision Detections to numpy tensors for further computation.
    Args:
        detections (Detections): Detections/Targets in the format of sv.Detections.
    Returns:
        (np.ndarray): Detections as numpy tensors as in
            `(x_min, y_min, x_max, y_max, confidence, class_id)` order.
    """
    return np.hstack(
        (
            detections.xyxy,
            detections.confidence[:, np.newaxis],
            detections.class_id[:, np.newaxis],
        )
    )

class SmartTrackConfig:
    rematch_new_tracks: bool = True
    rematch_swapped_tracks: bool = True
    track_activation_threshold: float = 0.25
    lost_track_buffer: int = 30
    minimum_matching_threshold: float = 0.8
    frame_rate: int = 30
    minimum_consecutive_frames: int = 1
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class SmartTrack:
    """
    Initialize the ByteTrack object.

    <video controls>
        <source src="https://media.roboflow.com/supervision/video-examples/how-to/track-objects/annotate-video-with-traces.mp4" type="video/mp4">
    </video>

    Parameters:
        track_activation_threshold (float, optional): Detection confidence threshold
            for track activation. IncreasinRematched lostg track_activation_threshold improves accuracy
            and stability but might miss true detections. Decreasing it increases
            completeness but risks introducing noise and instability.
        lost_track_buffer (int, optional): Number of frames to buffer when a track is lost.
            Increasing lost_track_buffer enhances occlusion handling, significantly
            reducing the likelihood of track fragmentation or disappearance caused
            by brief detection gaps.
        minimum_matching_threshold (float, optional): Threshold for matching tracks with detections.
            Increasing minimum_matching_threshold improves accuracy but risks fragmentation.
            Decreasing it improves completeness but risks false positives and drift.
        frame_rate (int, optional): The frame rate of the video.
        minimum_consecutive_frames (int, optional): Number of consecutive frames that an object must
            be tracked before it is considered a 'valid' track.
            Increasing minimum_consecutive_frames prevents the creation of accidental tracks from
            false detection or double detection, but risks missing shorter tracks.
    """  # noqa: E501 // docs

    def __init__(
        self,
        config: SmartTrackConfig
    ):
        self.configure(config)
        

        self.frame_id = 0
        self.kalman_filter = KalmanFilter()

        self.tracked_tracks: List[STrack] = []
        self.lost_tracks: List[STrack] = []
        self.removed_tracks: List[STrack] = []
        self.all_matched = True
        self.last_tracks = 0
        self.singleton_id = None

    def configure(self, config: SmartTrackConfig):
        self.track_activation_threshold = config.track_activation_threshold
        self.lost_track_buffer = config.lost_track_buffer
        self.minimum_matching_threshold = config.minimum_matching_threshold
        self.frame_rate = config.frame_rate
        self.minimum_consecutive_frames = config.minimum_consecutive_frames
        self.max_time_lost = int(self.frame_rate / 30.0 * self.lost_track_buffer)
        self.det_thresh = self.track_activation_threshold + 0.1
        self.rematch_new_tracks = config.rematch_new_tracks
        self.rematch_swapped_tracks = config.rematch_swapped_tracks

    def update_with_detections(self, detections: Detections, frame) -> Detections:
        """
        Updates the tracker with the provided detections and returns the updated
        detection results.

        Args:
            detections (Detections): The detections to pass through the tracker.

        Example:
            ```python
            import supervision as sv
            from ultralytics import YOLO

            model = YOLO(<MODEL_PATH>)
            tracker = sv.ByteTrack()

            bounding_box_annotator = sv.BoundingBoxAnnotator()
            label_annotator = sv.LabelAnnotator()

            def callback(frame: np.ndarray, index: int) -> np.ndarray:
                results = model(frame)[0]
                detections = sv.Detections.from_ultralytics(results)
                detections = tracker.update_with_detections(detections)

                labels = [f"#{tracker_id}" for tracker_id in detections.tracker_id]

                annotated_frame = bounding_box_annotator.annotate(
                    scene=frame.copy(), detections=detections)
                annotated_frame = label_annotator.annotate(
                    scene=annotated_frame, detections=detections, labels=labels)
                return annotated_frame

            sv.process_video(
                source_path=<SOURCE_VIDEO_PATH>,
                target_path=<TARGET_VIDEO_PATH>,
                callback=callback
            )
            ```
        """

        tensors = detections2boxes(detections=detections)
        tracks = self.update_with_tensors(tensors=tensors, frame=frame)

        if len(tracks) > 0:
            detection_bounding_boxes = np.asarray([det[:4] for det in tensors])
            track_bounding_boxes = np.asarray([track.tlbr for track in tracks])

            ious = box_iou_batch(detection_bounding_boxes, track_bounding_boxes)

            iou_costs = 1 - ious

            matches, _, _ = matching.linear_assignment(iou_costs, 0.5)
            detections.tracker_id = np.full(len(detections), -1, dtype=int)
            for i_detection, i_track in matches:
                detections.tracker_id[i_detection] = int(
                    tracks[i_track].external_track_id
                )
            detections = detections[detections.tracker_id != -1]
            detections.tracker_id = detections.tracker_id[detections.tracker_id != -1]

            return detections

        else:
            detections = Detections.empty()
            detections.tracker_id = np.array([], dtype=int)
            detections.confidence = np.array([])
            detections.class_id = np.array([])
            detections["class_name"] = []

            return detections

    def reset(self):
        """
        Resets the internal state of the ByteTrack tracker.

        This method clears the tracking data, including tracked, lost,
        and removed tracks, as well as resetting the frame counter. It's
        particularly useful when processing multiple videos sequentially,
        ensuring the tracker starts with a clean state for each new video.
        """
        self.frame_id = 0
        self.tracked_tracks: List[STrack] = []
        self.lost_tracks: List[STrack] = []
        self.removed_tracks: List[STrack] = []
        BaseTrack.reset_counter()
        STrack.reset_external_counter()

    def update_with_tensors(self, tensors: np.ndarray, frame) -> List[STrack]:
        """
        Updates the tracker with the provided tensors and returns the updated tracks.

        Parameters:
            tensors: The new tensors to update with.

        Returns:
            List[STrack]: Updated tracks.
        """
        self.frame_id += 1
        # print(f"Updating with frame: {self.frame_id}")
        activated_starcks = []
        refind_stracks = []
        lost_stracks = []
        removed_stracks = []

        class_ids = tensors[:, 5]
        scores = tensors[:, 4]
        bboxes = tensors[:, :4]

        remain_inds = scores > self.track_activation_threshold
        inds_low = scores > 0.1
        inds_high = scores < self.track_activation_threshold

        inds_second = np.logical_and(inds_low, inds_high)
        dets_second = bboxes[inds_second]
        dets = bboxes[remain_inds]
        scores_keep = scores[remain_inds]
        scores_second = scores[inds_second]

        class_ids_keep = class_ids[remain_inds]
        class_ids_second = class_ids[inds_second]

        if len(dets) > 0:
            #print(dets[0])
            """Detections"""
            detections = [
                STrack(STrack.tlbr_to_tlwh(tlbr), s, c, self.minimum_consecutive_frames, frame[int(tlbr[1]):int(tlbr[3]), int(tlbr[0]):int(tlbr[2])])
                for (tlbr, s, c) in zip(dets, scores_keep, class_ids_keep)
            ]
        else:
            detections = []

        """ Add newly detected tracklets to tracked_stracks"""
        unconfirmed = []
        tracked_stracks = []  # type: list[STrack]

        for track in self.tracked_tracks:
            if not track.is_activated:
                unconfirmed.append(track)
            else:
                tracked_stracks.append(track)

        """ Step 2: First association, with high score detection boxes"""
        strack_pool = joint_tracks(tracked_stracks, self.lost_tracks)
        # Predict the current location with KF
        STrack.multi_predict(strack_pool)
        dists = matching.iou_distance(strack_pool, detections)

        dists = matching.fuse_score(dists, detections)
        matches, u_track, u_detection = matching.linear_assignment(
            dists, thresh=self.minimum_matching_threshold
        )

        for itracked, idet in matches:
            track = strack_pool[itracked]
            det = detections[idet]
            if track.state == TrackState.Tracked:
                track.update(detections[idet], self.frame_id, update_patch=len(self.tracked_tracks) > 1)
                # track.patch = [t for t in strack_pool if t.external_track_id == track.external_track_id][0].patch
                activated_starcks.append(track)
            else:
                track.re_activate(det, self.frame_id, new_id=False)
                # track.patch = [t for t in strack_pool if t.external_track_id == track.external_track_id][0].patch
                refind_stracks.append(track)
            
        """ Step 3: Second association, with low score detection boxes"""
        # association the untrack to the low score detections
        if len(dets_second) > 0:
            """Detections"""
            detections_second = [
                STrack(STrack.tlbr_to_tlwh(tlbr), s, c, self.minimum_consecutive_frames, frame[int(tlbr[1]):int(tlbr[3]), int(tlbr[0]):int(tlbr[2])])
                for (tlbr, s, c) in zip(dets_second, scores_second, class_ids_second)
            ]
        else:
            detections_second = []
        r_tracked_stracks = [
            strack_pool[i]
            for i in u_track
            if strack_pool[i].state == TrackState.Tracked
        ]
        dists = matching.iou_distance(r_tracked_stracks, detections_second)

        matches, u_track, u_detection_second = matching.linear_assignment(
            dists, thresh=0.5
        )
        for itracked, idet in matches:
            track = r_tracked_stracks[itracked]
            det = detections_second[idet]
            if track.state == TrackState.Tracked:
                track.update(det, self.frame_id, update_patch=len(self.tracked_tracks) > 1)
                # track.patch = [t for t in strack_pool if t.external_track_id == track.external_track_id][0].patch
                activated_starcks.append(track)
            else:
                track.re_activate(det, self.frame_id, new_id=False)
                # track.patch = [t for t in strack_pool if t.external_track_id == track.external_track_id][0].patch
                refind_stracks.append(track)

        for it in u_track:
            track = r_tracked_stracks[it]
            if not track.state == TrackState.Lost:
                track.mark_lost()
                lost_stracks.append(track)

        """Deal with unconfirmed tracks, usually tracks with only one beginning frame"""
        detections = [detections[i] for i in u_detection]
        if len(detections) > 0:
            '''print(f"Unconfirmed: {len(detections)}")'''
        dists = matching.iou_distance(unconfirmed, detections)

        dists = matching.fuse_score(dists, detections)
        
        matches, u_unconfirmed, u_detection = matching.linear_assignment(
            dists, thresh=0.7
        )
        for itracked, idet in matches:
            unconfirmed[itracked].update(detections[idet], self.frame_id, update_patch=len(self.tracked_tracks) > 1)
            activated_starcks.append(unconfirmed[itracked])
        for it in u_unconfirmed:
            track = unconfirmed[it]
            track.mark_removed()
            removed_stracks.append(track)

        """ Step 4: Init new stracks"""
        # embed tracks which have not been matched with any detections
        new_stracks = []
        for i in u_detection:
            track = detections[i]
            if track.score < self.det_thresh:
                continue
            track.activate(self.kalman_filter, self.frame_id)
            activated_starcks.append(track)  
            new_stracks.append(track)

        if len(u_detection) == 1 and len(self.lost_tracks) >= 1:
            best_lost_track = min(self.lost_tracks, key=lambda x: x.external_track_id)
            i_id = new_stracks[0].internal_track_id
            e_id = new_stracks[0].external_track_id
            new_stracks[0].external_track_id = best_lost_track.external_track_id
            new_stracks[0].internal_track_id = best_lost_track.internal_track_id
            best_lost_track.external_track_id = e_id
            best_lost_track.internal_track_id = i_id


            

        """ Step 5: Update state"""
        for track in self.lost_tracks:
            if self.frame_id - track.end_frame > self.max_time_lost:
                track.mark_removed()
                removed_stracks.append(track)
                # print(f"Removed track {track.external_track_id} due to time lost")

        

        # run sam reid if one detection shares significant iou with multiple tracks
        if len(lost_stracks) > 0:
            self.all_matched = False
        if self.rematch_swapped_tracks and len(lost_stracks) == 0 and len(self.lost_tracks) > 0 and len(self.tracked_tracks) > 0 and not self.all_matched:
            # print("Rematching swapped tracks")
            self.all_matched = True
            track_pool = joint_tracks(joint_tracks(self.tracked_tracks, self.lost_tracks), self.removed_tracks)
            track_dists = matching.iou_distance(track_pool, self.tracked_tracks)
            dt = track_dists
            dets_to_rematch = []
            tracks_to_rematch = []
            for idet in range(dt.shape[0]):
                to_match = []
                for itrack in range(dt.shape[1]):
                    if dt[idet, itrack] < self.minimum_matching_threshold:
                        to_match.append(itrack)
                    if len(to_match) > 1:
                        dets_to_rematch.append(track_pool[idet])
                        tracks_to_rematch.extend([self.tracked_tracks[tm] for tm in to_match])

            rematch_thread = Thread(target=async_rematch, args=(tracks_to_rematch, dets_to_rematch, frame, lambda x: self.rematch_tracks_swapped(x), 0.4))
            rematch_thread.start()

        self.tracked_tracks = [
            t for t in self.tracked_tracks if t.state == TrackState.Tracked
        ]
        self.tracked_tracks = joint_tracks(self.tracked_tracks, new_stracks)
        self.tracked_tracks = joint_tracks(self.tracked_tracks, activated_starcks)
        self.tracked_tracks = joint_tracks(self.tracked_tracks, refind_stracks)

        # prevent from changing single tracked tack's id while only one track is present
        # if len(self.tracked_tracks) > 1:
        #     self.singleton_id = None
        # if len(self.tracked_tracks) == 1 and self.singleton_id is None:
        #     self.singleton_id = self.tracked_tracks[0].external_track_id
        # if len(self.tracked_tracks) == 1 and self.singleton_id is not None:
        #     self.tracked_tracks[0].external_track_id = self.singleton_id

        # update patches of tracked tracks if there are two tracks
        # if len(self.tracked_tracks) > 1:
        #     for i in range(len(self.tracked_tracks)):
        #         for j in range(i+1, len(self.tracked_tracks)):
        #             self.tracked_tracks[i].patch = self.tracked_tracks[j].new_patch

        # if self.rematch_new_tracks and len(self.tracked_tracks) > self.last_tracks:
        #     print("Rematching new tracks")
        #     rematch_thread = Thread(target=async_rematch, args=(self.lost_tracks, self.tracked_tracks, frame, lambda x: self.rematch_tracks_lost(x), 0.4))
        #     rematch_thread.start()
        self.lost_tracks.extend(lost_stracks)
        self.lost_tracks = sub_tracks(self.lost_tracks, self.tracked_tracks)
        self.lost_tracks = sub_tracks(self.lost_tracks, self.removed_tracks)
        self.removed_tracks = removed_stracks
        self.last_tracks = len(self.tracked_tracks)

        if len(self.tracked_tracks) > 1 and self.rematch_new_tracks and len(new_stracks) > 0:
            # asynchronously rematch the tracks
            # print("Rematching new tracks")
            rematch_thread = Thread(target=async_rematch, args=([track for track in self.tracked_tracks if track not in new_stracks],  self.tracked_tracks, frame, lambda x: self.rematch_tracks_lost(x)))
            rematch_thread.start()

        ids = [t.external_track_id for t in self.tracked_tracks]
        # print("IDS", ids)
        ids_not_included = [i for i in [1, 2] if i not in ids]
        total_tracks = [t for t in joint_tracks(joint_tracks(self.tracked_tracks, self.lost_tracks), self.removed_tracks) if t.external_track_id not in [1,2]]
        #  print("ID NOT INCLUDED", ids_not_included)
        if len(ids_not_included) > 0 and len(self.tracked_tracks) > 1:
            # find the track with the lowest external id
            # print("TOTAL TRACKS", len(total_tracks))
            for i in ids_not_included:
                avail_tracks = [t for t in self.tracked_tracks if t.external_track_id not in [1,2]]
                if len(avail_tracks) == 0:
                    continue
                min_track = min(avail_tracks, key=lambda x: x.external_track_id)
                min_track.activate(self.kalman_filter, self.frame_id)
                min_track.external_track_id = i
                # print("MIN TRACK", min_track.external_track_id)
                self.tracked_tracks = joint_tracks(self.tracked_tracks, [min_track])
                # print("TRACKED TRACKS", len(self.tracked_tracks))
                total_tracks = sub_tracks(total_tracks, [min_track])
                lost_id_tracks = [t for t in self.lost_tracks if t.external_track_id == i]
                lost_id_track = lost_id_tracks[0] if lost_id_tracks else None
                if lost_id_track:
                    self.lost_tracks = sub_tracks(self.lost_tracks, [lost_id_track])
                    total_tracks = sub_tracks(total_tracks, [lost_id_track])
                removed_id_tracks = [t for t in self.removed_tracks if t.external_track_id == i]
                removed_id_track = removed_id_tracks[0] if removed_id_tracks else None
                if removed_id_track:
                    self.removed_tracks = sub_tracks(self.removed_tracks, [removed_id_track])
                    total_tracks = sub_tracks(total_tracks, [removed_id_track])
                # print("TOTAL TRACKS", len(total_tracks))

        output_stracks = [track for track in self.tracked_tracks if track.is_activated]
        # for track in output_stracks:
            # print(f"Track {track.external_track_id} has {track.continuous_track_count} continuous track count")
        # print(f"Tracked: {len(self.tracked_tracks)} Lost: {len(self.lost_tracks)} Removed: {len(self.removed_tracks)} New: {len(new_stracks)}")

        return output_stracks
    
    def rematch_tracks_lost(self, matches):
        matches = [(i, j) for i, j in matches if i != j]
        for i, j in matches:
            i_tracks = [t for t in joint_tracks(joint_tracks(self.tracked_tracks, self.lost_tracks), self.removed_tracks) if t.external_track_id == i]
            if len(i_tracks) == 0:
                continue
            i_track = i_tracks[0]
            j_tracks = [t for t in joint_tracks(joint_tracks(self.tracked_tracks, self.lost_tracks), self.removed_tracks) if t.external_track_id == j]
            if len(j_tracks) == 0:
                continue
            j_track = j_tracks[0]
            j_track.external_track_id = i
            j_internal = j_track.internal_track_id
            j_patch = j_track.patch
            j_state = j_track.state
            j_track.internal_track_id = i_track.internal_track_id
            j_track.state = i_track.state
            j_track.patch = i_track.patch
            j_track.continuous_track_count = 0
            i_track.external_track_id = j
            i_track.patch = j_patch
            i_track.state = j_state
            i_track.internal_track_id = j_internal
            i_track.continuous_track_count = 0
            self.tracked_tracks = joint_tracks(self.tracked_tracks, [j_track])
            self.tracked_tracks = sub_tracks(self.tracked_tracks, [i_track])
            if i_track.state == TrackState.Lost:
                self.lost_tracks = sub_tracks(self.lost_tracks, [i_track])
            elif j_track.state == TrackState.Lost:
                self.lost_tracks = sub_tracks(self.lost_tracks, [j_track])
            else:
                self.tracked_tracks = joint_tracks(self.tracked_tracks, [i_track])



    def rematch_tracks_swapped(self, matches):
        matches = [(i, j) for i, j in matches if i != j]
        for x, m in enumerate(matches):
            i, j = m
            i_in = False
            j_in = False
            for t in self.tracked_tracks:
                if j == t.external_track_id:
                    j_in = True
                if i == t.external_track_id:
                    i_in = True
            if i_in and j_in and (j, i) not in matches:
                matches.remove(m)

        for i, j in matches:
            i_tracks = [t for t in joint_tracks(joint_tracks(self.tracked_tracks, self.lost_tracks), self.removed_tracks) if t.external_track_id == i]
            if len(i_tracks) == 0:
                continue
            i_track = i_tracks[0]
            j_tracks = [t for t in joint_tracks(joint_tracks(self.tracked_tracks, self.lost_tracks), self.removed_tracks) if t.external_track_id == j]
            if len(j_tracks) == 0:
                continue
            j_track = j_tracks[0]
            j_track.external_track_id = i
            j_internal = j_track.internal_track_id
            j_patch = j_track.patch
            j_state = j_track.state
            j_track.internal_track_id = i_track.internal_track_id
            j_track.state = i_track.state
            j_track.patch = i_track.patch
            j_track.continuous_track_count = 0
            i_track.external_track_id = j
            i_track.patch = j_patch
            i_track.state = j_state
            i_track.internal_track_id = j_internal
            i_track.continuous_track_count = 0


def joint_tracks(
    track_list_a: List[STrack], track_list_b: List[STrack]
) -> List[STrack]:
    """
    Joins two lists of tracks, ensuring that the resulting list does not
    contain tracks with duplicate internal_track_id values.

    Parameters:
        track_list_a: First list of tracks (with internal_track_id attribute).
        track_list_b: Second list of tracks (with internal_track_id attribute).

    Returns:
        Combined list of tracks from track_list_a and track_list_b
            without duplicate internal_track_id values.
    """
    seen_track_ids = set()
    result = []

    for track in track_list_a + track_list_b:
        if track.internal_track_id not in seen_track_ids:
            seen_track_ids.add(track.internal_track_id)
            result.append(track)

    return result


def sub_tracks(track_list_a: List, track_list_b: List) -> List[int]:
    """
    Returns a list of tracks from track_list_a after removing any tracks
    that share the same internal_track_id with tracks in track_list_b.

    Parameters:
        track_list_a: List of tracks (with internal_track_id attribute).
        track_list_b: List of tracks (with internal_track_id attribute) to
            be subtracted from track_list_a.
    Returns:
        List of remaining tracks from track_list_a after subtraction.
    """
    tracks = {track.internal_track_id: track for track in track_list_a}
    track_ids_b = {track.internal_track_id for track in track_list_b}

    for track_id in track_ids_b:
        tracks.pop(track_id, None)

    return list(tracks.values())


def remove_duplicate_tracks(tracks_a: List, tracks_b: List) -> Tuple[List, List]:
    pairwise_distance = matching.iou_distance(tracks_a, tracks_b)
    matching_pairs = np.where(pairwise_distance < 0.15)

    duplicates_a, duplicates_b = set(), set()
    for track_index_a, track_index_b in zip(*matching_pairs):
        time_a = tracks_a[track_index_a].frame_id - tracks_a[track_index_a].start_frame
        time_b = tracks_b[track_index_b].frame_id - tracks_b[track_index_b].start_frame
        if time_a > time_b:
            duplicates_b.add(track_index_b)
        else:
            duplicates_a.add(track_index_a)

    result_a = [
        track for index, track in enumerate(tracks_a) if index not in duplicates_a
    ]
    result_b = [
        track for index, track in enumerate(tracks_b) if index not in duplicates_b
    ]

    return result_a, result_b
