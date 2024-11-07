# from segment_anything import sam_model_registry
from PIL import Image
from torchvision import transforms
import torch
import numpy as np
import cv2
from scipy.optimize import linear_sum_assignment
import open_clip
from pathlib import Path
from datetime import datetime
import mediapipe as mp
from image_similarity_measures.evaluate import evaluation
import io
from super_image import PanModel, ImageLoader
import tempfile

# Load the SAM model
# model_type = "vit_h"
# sam = sam_model_registry[model_type](checkpoint=os.path.join(os.path.dirname(__file__), "sam_vit_h_4b8939.pth"))
# sam.to(device="cuda" if torch.cuda.is_available() else "cpu")

# Extract the image encoder
# image_encoder = sam.image_encoder
mp_selfie_segmentation = mp.solutions.selfie_segmentation
segment = mp_selfie_segmentation.SelfieSegmentation(model_selection = 0)
model = PanModel.from_pretrained('eugenesiow/pan-bam', scale=3)


def segment_subject(img):
    results = segment.process(img)
    mask = results.segmentation_mask
    threshold = 0.25
    binary_mask = mask > threshold
    if np.sum(binary_mask) != 0:
        img = img*binary_mask[:,:,np.newaxis]
    # cv2.imwrite(f"segmented+{datetime.now()}.png", img)
    return img

# Load the MobileCLIP model
# clip_model, _, clip_preprocess = open_clip.create_model_and_transforms('MobileCLIP-B', pretrained="datacompdr_lt")

def match_tracks(cost_matrix, threshold=0.4):
    # Replace costs above the threshold with a large number to make them undesirable
    modified_cost_matrix = np.where(cost_matrix < threshold, cost_matrix, 1e9)
    
    # Use the Hungarian algorithm to find the optimal assignment
    row_indices, col_indices = linear_sum_assignment(modified_cost_matrix)
    
    # Filter out assignments that have a cost above the threshold
    matches = []
    for row, col in zip(row_indices, col_indices):
        if cost_matrix[row, col] < threshold:
            matches.append((row, col))
    
    return matches

def async_rematch(oldtracks, newtracks, frame, callback, threshold=0.5):
    # embed newtracks and oldtracks
    # old_embeds = clip_embed([track for track in oldtracks], new=False)
    # new_embeds = clip_embed([track for track in newtracks], new=True)

    # perform matching between oldtracks and newtracks
    # cost_matrix = np.zeros((len(old_embeds), len(new_embeds)))
    # for i, old in enumerate(old_embeds):
    #     for j, new in enumerate(new_embeds):
    #         cost_matrix[i, j] = 1 - abs(np.dot(old, new) / (np.linalg.norm(old) * np.linalg.norm(new)))

    # print("Rematching: ", [track.external_track_id for track in oldtracks], [track.external_track_id for track in newtracks])
    cost_matrix = image_similarity_matrix(oldtracks, newtracks)
    # print("cost_matrix: ", cost_matrix)

    matches = match_tracks(cost_matrix, threshold)
    resmatches = [(oldtracks[i].external_track_id, newtracks[j].external_track_id) for i, j in matches]
    # print("Matches: ", resmatches)

    # change newtracks id to matching oldtrack id; return newtracks that matched

    callback(resmatches)

def tracks_to_patches(tracks, new=False):
    imgs = []
    for track in tracks:
        patch = track.patch if not new else track.new_patch
        patch = model(ImageLoader.load_image(Image.fromarray(cv2.cvtColor(patch, cv2.COLOR_BGR2RGB))))#[0].detach().cpu().numpy().transpose(1, 2, 0).astype(np.uint8)
        patch = ImageLoader._process_image_to_save(patch)
        patch = cv2.convertScaleAbs(patch)
        img = segment_subject(patch)
        imgs.append(img)
    return imgs

def image_similarity_matrix(tracks_a, tracks_b):
    imgs_a = tracks_to_patches(tracks_a, new=False)
    imgs_b = tracks_to_patches(tracks_b, new=True)
    if len(imgs_a) == 0 or len(imgs_b) == 0:
        return np.zeros((len(imgs_a), len(imgs_b)))
    H = max([img.shape[0] for img in [*imgs_a, *imgs_b]])
    W = max([img.shape[1] for img in [*imgs_a, *imgs_b]])
    # pad images to be the same size
    imgs_a = [cv2.copyMakeBorder(img,0,H - img.shape[0],0,W - img.shape[1],cv2.BORDER_CONSTANT,value=[0,0,0]) for img in imgs_a]
    imgs_b = [cv2.copyMakeBorder(img,0,H - img.shape[0],0,W - img.shape[1],cv2.BORDER_CONSTANT,value=[0,0,0]) for img in imgs_b]
    sim_matrix = np.zeros((len(imgs_a), len(imgs_b)))
    with tempfile.TemporaryDirectory() as tmpdirname:
        for i in range(len(imgs_a)):
            for j in range(len(imgs_b)):
                cv2.imwrite(f"{tmpdirname}/img_a_{i}.png", imgs_a[i])
                cv2.imwrite(f"{tmpdirname}/img_b_{j}.png", imgs_b[j])
                # print("im sum:",np.sum(imgs_a[i]), np.sum(imgs_b[j]))
                eval = evaluation(f"img_a_{i}.png", f"img_b_{j}.png", metrics=["rmse"])
                eval = [val for val in eval.values() if abs(val) < 1000]
                image_similarity = sum(eval) / len(eval)
                mask_iou = binaryMaskIOU(imgs_a[i], imgs_b[j])
                sim_matrix[i, j] = image_similarity / (mask_iou if mask_iou != 0 else 1)
    return sim_matrix

def binaryMaskIOU(mask1, mask2):   # From the question.
    mask1_area = np.count_nonzero(mask1 > 0)
    mask2_area = np.count_nonzero(mask2 > 0)
    if mask1_area == 0 or mask2_area == 0:
        return 0
    intersection = np.count_nonzero(np.logical_and( mask1>0,  mask2>0 ))
    iou = intersection/(mask1_area+mask2_area-intersection)
    return iou

def clip_embed(predictions, new=False):
    res = []
    patches = []
    for track in predictions:
        patch = track.patch if not new else track.new_patch
        img = segment_subject(patch)
        img = Image.fromarray(img).convert('RGB')
        patches.append(clip_preprocess(img))
    if patches == []:
        return []
    patches_tensor = torch.stack(patches)
    with torch.no_grad(), torch.cuda.amp.autocast():
        embeddings = clip_model.encode_image(patches_tensor)
    for i, embedding in enumerate(embeddings):
        track = predictions[i]
        track.embedding = embedding
        res.append(embedding)

    return res

def upscale_patches(patches):
    out = []
    for patch in patches:
        out.append(cv2.pyrUp(patch))
    return out



# pred: [(x1, y1), (x2, y2), ..., (xn, yn)] for n keypoints
# Keypoints order in COCO 2017 Keypoint Challenge annotation format:
# 1. Nose
# 2. Left Eye
# 3. Right Eye
# 4. Left Ear
# 5. Right Ear
# 6. Left Shoulder
# 7. Right Shoulder
# 8. Left Elbow
# 9. Right Elbow
# 10. Left Wrist
# 11. Right Wrist
# 12. Left Hip
# 13. Right Hip
# 14. Left Knee
# 15. Right Knee
# 16. Left Ankle
# 17. Right Ankle
def pose_embed(preds):
    # norm key points by finding dist from center of hips
    embeddings = []
    for pred in preds:
        hx = (pred[12][0] + pred[13][0]) / 2
        hy = (pred[12][1] + pred[13][1]) / 2
        normed = [(x - hx, y - hy) for x, y in pred]
        embedding = np.array([x for x, y in normed])#np.array(normed).flatten()
        embeddings.append(embedding)
    return embeddings

def pose_cost(atracks, btracks):
    a_embeds = pose_embed([a.pose for a in atracks])
    b_embeds = pose_embed([b.pose for b in btracks])

    cost_matrix = np.zeros((len(a_embeds), len(b_embeds)))
    for i, a in enumerate(a_embeds):
        for j, b in enumerate(b_embeds):
            if np.sum(b) == 0 or np.sum(a) == 0:
                cost_matrix[i, j] = 1
            else:
                cost_matrix[i, j] = 1 - abs(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    return cost_matrix


if __name__=="__main__": 
    # img = cv2.imread("test_balls.jpg")
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # print(img.shape)
    # embeddings = sam_embed(img, [[0, 0, 533, 400], [533, 0, 1066, 400], [0, 400, 533, 800]])
    # print(embeddings)
    # similarity = np.dot(embeddings[0], embeddings[1]) / (np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1]))
    # print(similarity)
    # similarity = np.dot(embeddings[0], embeddings[2]) / (np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[2]))
    # print(similarity)

    v1 = [0.5, 1, -0.5, 1, 1, 0.5, -1, 0.5, 1, 0, -1, 0, 0.5, 0, -0.5, 0, 1, -1, -1, -1, 1, -2, -1, -2]
    v1 = [x for i,x in enumerate(v1) if i % 2 == 0]
    v2 = [0, 1, 0.5, 1, -0.5, 0.5, 1, 0.5, -1, 0.5, 1, 0, -0.5, 0, 0.5, 0, 0.5, -1, 0, -1, 0.5, -2, -1, -2]
    v2 = [x for i,x in enumerate(v2) if i % 2 == 0]
    sim = np.dot(np.array(v1), np.array(v2))/(np.linalg.norm(np.array(v1)) * np.linalg.norm(np.array(v2)))
    # print(sim)
    