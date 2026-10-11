import numpy as np
import cv2
from rapidocr_onnxruntime import RapidOCR

h, w = 768, 432
img = np.ones((h, w, 3), dtype=np.uint8) * 140
cv2.putText(img, '@watermark', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
cv2.putText(img, 'Level - 01', (120, 350), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
cv2.putText(img, 'Subtitles', (130, 700), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

engine = RapidOCR()
results, _ = engine(img)

print("Detected items:")
for item in results:
    box, text, score = item[0], item[1], item[2]
    pts = np.array(box, dtype=np.float32)
    cx, cy = np.mean(pts[:, 0]), np.mean(pts[:, 1])
    print(f"Text: '{text}' at center ({cx:.1f}, {cy:.1f}), score: {score:.2f}")
