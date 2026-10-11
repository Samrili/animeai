import sys
import os
sys.path.append('ComfyUI/custom_nodes/ComfyUI-AutoTextCleaner')
import cv2
import numpy as np
from rapidocr_onnxruntime import RapidOCR
from auto_text_cleaner import is_box_in_delete_zone, extract_smart_letter_mask

cap = cv2.VideoCapture('ComfyUI/input/asd.mp4')
engine = RapidOCR()
frame_idx = 0

print("Analyzing asd.mp4 for 'MIRI BOXING'...")
while cap.isOpened() and frame_idx < 30:
    ret, frame = cap.read()
    if not ret:
        break
    res, _ = engine(frame)
    if res:
        miri_items = [item for item in res if 'MIRI' in item[1].upper() or 'BOXING' in item[1].upper()]
        if miri_items:
            for item in miri_items:
                box, text, score = item[0], item[1], item[2]
                h, w = frame.shape[:2]
                to_del = is_box_in_delete_zone(box, h, w, "Custom (Ozel Bolge veya Kelime)", "", "MIRI BOXING", text)
                
                # Test extract_smart_letter_mask
                pts_float = np.array(box, dtype=np.float32).reshape((-1, 2))
                pts_int = pts_float.astype(np.int32).reshape((-1, 1, 2))
                letter_m = extract_smart_letter_mask(frame, pts_int, h, w, dilation=2)
                
                print(f"F{frame_idx}: text='{text}', score={score:.2f}, to_delete={to_del}, letter_mask_pixels={np.count_nonzero(letter_m)}")
        else:
            print(f"F{frame_idx}: MIRI BOXING NOT DETECTED by RapidOCR! Total detected texts: {len(res)}")
            for item in res[:3]:
                print(f"     other: '{item[1]}'")
    else:
        print(f"F{frame_idx}: No text detected at all!")
    frame_idx += 1
cap.release()
