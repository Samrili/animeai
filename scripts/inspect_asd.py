import cv2
from rapidocr_onnxruntime import RapidOCR

cap = cv2.VideoCapture('ComfyUI/input/asd.mp4')
engine = RapidOCR()
frame_idx = 0
found_any = False

print("Inspecting asd.mp4 frames...")
while cap.isOpened() and frame_idx < 40:
    ret, frame = cap.read()
    if not ret:
        break
    res, _ = engine(frame)
    if res:
        print(f"Frame {frame_idx}:")
        for item in res:
            box, text, score = item[0], item[1], item[2]
            print(f"   Detected text: '{text}' (score: {score:.2f})")
            found_any = True
    frame_idx += 1
cap.release()

if not found_any:
    print("No text detected in first 40 frames!")
