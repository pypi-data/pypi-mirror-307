def run():
    print(""" EXP 6 video classification
import cv2
import torch
import torchvision.transforms as transforms
from torchvision import models
from collections import Counter
# Load a pre-trained ResNet model
model = models.resnet50(pretrained=True)
model.eval()
# Define image transformations
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
# Helper function to get labels for ImageNet classes
def load_labels():
    with open("imagenet-simple-labels.txt") as f:
        labels = [line.strip() for line in f.readlines()]
    return labels

labels = load_labels()
# Function to classify a single frame
def classify_frame(frame):
    frame = transform(frame)
    frame = frame.unsqueeze(0)
    with torch.no_grad():
        outputs = model(frame)
    _, predicted = outputs.max(1)
    label = labels[predicted.item()]
    return label

# Function to extract frames and classify video
def classify_video(video_path, frame_interval=30):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    classifications = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            label = classify_frame(frame)
            classifications.append(label)

        frame_count += 1

    cap.release()
    return classifications
# Determine the most common classification
classifications = classify_video("/content/video2.mp4")
common_label = Counter(classifications).most_common(1)[0][0]
print(common_label)
# Usage example
video_path = "/content/video2.mp4"
category = classify_video(video_path)
print(f"Predicted category: {category}")
""")