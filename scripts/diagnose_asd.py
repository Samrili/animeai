import cv2
import torch
import numpy as np

cap = cv2.VideoCapture('ComfyUI/input/asd.mp4')
ret, frame = cap.read()
cap.release()

if not ret:
    print("Could not read frame from asd.mp4")
    exit(1)

import sys
sys.path.append('ComfyUI/custom_nodes/ComfyUI-AutoTextCleaner')
from auto_text_cleaner import AutoTextCleaner

cleaner = AutoTextCleaner()
img_tensor = torch.from_numpy(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0).unsqueeze(0)

# Exact parameters from user screenshot:
# enabled: True
# mask_mode: "Smart (Harf Bazli - Kusursuz)"
# min_confidence: 0.40
# mask_dilation: 4
# inpaint_radius: 5
# inpaint_method: "Telea"
# delete_region_mode: "Custom (Ozel Bolge veya Kelime)"
# delete_custom_zones: ""
# delete_keywords: "MIRI BOXING"
# letter_level_cleaning: True
# protect_red_shapes: True
# shape_color_mode: "Red (Kirmizi Halka ve Oklar)"
# shape_sensitivity: 0.60
# shape_dilation: 4
# shape_padding: 8
# clean_mode: "Inpaint Background (Arka Plani Temizle - Onerilen)"

cleaned, mask = cleaner.clean_text(
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

# Now check what was detected on frame:
from rapidocr_onnxruntime import RapidOCR
engine = RapidOCR()
res, _ = engine(frame)

print("OCR detected items on frame 0:")
for item in res:
    box, text, score = item[0], item[1], item[2]
    # Check is_box_in_delete_zone
    from auto_text_cleaner import is_box_in_delete_zone
    h, w = frame.shape[:2]
    to_del = is_box_in_delete_zone(box, h, w, "Custom (Ozel Bolge veya Kelime)", "", "MIRI BOXING", text)
    try:
        print(f"Text: '{text}' | score: {score:.2f} | to_delete: {to_del}")
    except:
        print(f"Text (non-ascii) | score: {score:.2f} | to_delete: {to_del}")
