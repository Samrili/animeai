import numpy as np
import cv2

h, w = 768, 432
# Create a textured background (e.g. gradient/pattern)
img = np.zeros((h, w, 3), dtype=np.uint8)
for y in range(h):
    for x in range(w):
        img[y, x] = [int(100 + 40 * np.sin(x / 30.0)), int(120 + 30 * np.cos(y / 40.0)), 140]

# Add watermark text at top-left
cv2.putText(img, '@watermark', (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
# Add game level text at center
cv2.putText(img, 'Level - 01', (100, 350), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

# Now extract letter-level mask for '@watermark' only
box = [[25, 35], [210, 35], [210, 70], [25, 70]]
roi_mask = np.zeros((h, w), dtype=np.uint8)
cv2.fillPoly(roi_mask, [np.array(box, dtype=np.int32)], 255)

# Smart letter extraction inside ROI
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
pixels = gray[roi_mask > 0]
thresh_val, _ = cv2.threshold(pixels, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
_, text_thresh = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
letter_mask = cv2.bitwise_and(text_thresh, roi_mask)

# Dilate by 2px to cover font anti-aliased edge
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
letter_mask_dilated = cv2.dilate(letter_mask, kernel, iterations=1)

# Inpaint ONLY the letter strokes (NOT the box!)
cleaned = cv2.inpaint(img, letter_mask_dilated, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

# Calculate difference in ROI outside of letters
outside_letters = (roi_mask > 0) & (letter_mask_dilated == 0)
diff = np.abs(cleaned[outside_letters].astype(int) - img[outside_letters].astype(int))
print(f"Mean change outside letters in the ROI: {np.mean(diff):.4f} (should be 0.0 - background untouched!)")
print(f"Max change outside letters: {np.max(diff)} (0 means zero box residue!)")
assert np.max(diff) == 0
print("Letter-level extraction completely preserves surrounding background with ZERO box trace!")
