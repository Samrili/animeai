import sys
sys.path.append('ComfyUI/custom_nodes/ComfyUI-AutoTextCleaner')
import cv2
import torch
import numpy as np
from auto_text_cleaner import AutoTextCleaner

cap = cv2.VideoCapture('ComfyUI/input/asd.mp4')
ret, frame = cap.read()
cap.release()

cleaner = AutoTextCleaner()
img_tensor = torch.from_numpy(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0).unsqueeze(0)

cleaned, preserve_mask = cleaner.clean_text(
    img_tensor,
    enabled=True,
    mask_mode="Smart (Harf Bazli - Kusursuz)",
    min_confidence=0.40,
    mask_dilation=4,
    inpaint_radius=5,
    inpaint_method="Telea",
    delete_region_mode="Custom (Ozel Bolge veya Kelime)",
    delete_custom_zones="",
    delete_keywords="MIRI BOXING",
    letter_level_cleaning=True,
    protect_red_shapes=True,
    shape_color_mode="Red (Kirmizi Halka ve Oklar)",
    shape_sensitivity=0.60,
    shape_dilation=4,
    shape_padding=8,
    clean_mode="Inpaint Background (Arka Plani Temizle - Onerilen)"
)

# Convert cleaned to BGR
cleaned_np = (cleaned[0].cpu().numpy() * 255.0).clip(0, 255).astype(np.uint8)
cleaned_bgr = cv2.cvtColor(cleaned_np, cv2.COLOR_RGB2BGR)

# Find MIRI BOXING location
from rapidocr_onnxruntime import RapidOCR
engine = RapidOCR()
res, _ = engine(frame)
miri_box = [item[0] for item in res if 'MIRI' in item[1].upper()][0]
pts = np.array(miri_box, dtype=np.int32)
x1, y1 = np.min(pts, axis=0)
x2, y2 = np.max(pts, axis=0)

orig_crop = frame[max(0, y1-10):min(frame.shape[0], y2+10), max(0, x1-10):min(frame.shape[1], x2+10)]
clean_crop = cleaned_bgr[max(0, y1-10):min(frame.shape[0], y2+10), max(0, x1-10):min(frame.shape[1], x2+10)]

cv2.imwrite('orig_miri.png', orig_crop)
cv2.imwrite('clean_miri.png', clean_crop)

diff = np.abs(orig_crop.astype(int) - clean_crop.astype(int))
print(f"Mean pixel diff in MIRI BOXING area: {np.mean(diff):.2f}")
print(f"Max pixel diff: {np.max(diff)}")
res_cleaned, _ = engine(cleaned_bgr)
cleaned_miri = [item[1] for item in (res_cleaned or []) if 'MIRI' in item[1].upper() or 'BOXING' in item[1].upper()]
print("Detected MIRI/BOXING in cleaned image:", cleaned_miri)
