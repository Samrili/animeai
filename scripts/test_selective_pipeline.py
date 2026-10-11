import numpy as np
import cv2
import torch

h, w = 768, 432
img = np.ones((h, w, 3), dtype=np.uint8) * 130
# Add watermark in top-left
cv2.putText(img, '@watermark', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
# Add game text in center
cv2.putText(img, 'Level - 01', (100, 350), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
# Add red arrow
cv2.arrowedLine(img, (150, 200), (250, 300), (0, 0, 255), 5)

from rapidocr_onnxruntime import RapidOCR
engine = RapidOCR()
results, _ = engine(img)

inpaint_mask = np.zeros((h, w), dtype=np.uint8)
preserve_mask = np.zeros((h, w), dtype=np.uint8)

for item in results:
    box, text, score = item[0], item[1], item[2]
    pts = np.array(box, dtype=np.float32)
    cx, cy = np.mean(pts[:, 0]), np.mean(pts[:, 1])
    
    is_delete = (cx < w * 0.5 and cy < h * 0.35) or ('@' in text) # top-left watermark
    
    # Extract letter mask
    roi_mask = np.zeros((h, w), dtype=np.uint8)
    cv2.fillPoly(roi_mask, [np.array(box, dtype=np.int32)], 255)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pixels = gray[roi_mask > 0]
    thresh_val, _ = cv2.threshold(pixels, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, text_thresh = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
    letter_mask = cv2.bitwise_and(text_thresh, roi_mask)
    letter_mask = cv2.dilate(letter_mask, np.ones((5, 5), np.uint8))
    
    if is_delete:
        print(f"DELETING: '{text}' with letter-level precision (not restoring in overlay)")
        inpaint_mask = cv2.bitwise_or(inpaint_mask, letter_mask)
    else:
        print(f"PRESERVING: '{text}' (will be restored crisp on anime video)")
        # For preserved text, use box or smart
        inpaint_mask = cv2.bitwise_or(inpaint_mask, roi_mask)
        preserve_mask = cv2.bitwise_or(preserve_mask, roi_mask)

# Watermark in preserve_mask should be 0 (NOT preserved)
watermark_roi = preserve_mask[20:80, 10:200]
print("Watermark pixels in preserve_mask (should be 0):", np.count_nonzero(watermark_roi))
assert np.count_nonzero(watermark_roi) == 0

# Center text in preserve_mask should be > 0 (preserved)
center_roi = preserve_mask[300:400, 80:300]
print("Center text pixels in preserve_mask (should be > 0):", np.count_nonzero(center_roi))
assert np.count_nonzero(center_roi) > 0

print("Selective text removal logic verified 100%!")
