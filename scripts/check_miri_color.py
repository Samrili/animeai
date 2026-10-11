import cv2
import numpy as np

cap = cv2.VideoCapture('ComfyUI/input/asd.mp4')
ret, frame = cap.read()
cap.release()

from rapidocr_onnxruntime import RapidOCR
engine = RapidOCR()
res, _ = engine(frame)

for item in res:
    box, text, score = item[0], item[1], item[2]
    if 'MIRI' in text.upper():
        pts = np.array(box, dtype=np.int32)
        x_min, y_min = np.min(pts, axis=0)
        x_max, y_max = np.max(pts, axis=0)
        crop = frame[y_min:y_max, x_min:x_max]
        hsv_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        print(f"Crop shape: {crop.shape}")
        print(f"Mean BGR: {np.mean(crop, axis=(0,1))}")
        print(f"Mean HSV: {np.mean(hsv_crop, axis=(0,1))}")
        
        # Check if detect_annotations_and_shapes catches it!
        from auto_text_cleaner import detect_annotations_and_shapes
        shape_mask = detect_annotations_and_shapes(frame, "Red (Kirmizi Halka ve Oklar)", 0.60, 4)
        overlap = shape_mask[y_min:y_max, x_min:x_max]
        print(f"Overlap of shape_mask with MIRI BOXING: {np.count_nonzero(overlap)} pixels!")
