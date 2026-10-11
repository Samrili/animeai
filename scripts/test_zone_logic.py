import numpy as np
import cv2

def is_box_in_delete_zone(box, h, w, mode, custom_zones_str, keywords_str, text):
    pts = np.array(box, dtype=np.float32)
    cx, cy = float(np.mean(pts[:, 0])), float(np.mean(pts[:, 1]))
    
    # 1. Keyword check
    if keywords_str:
        kws = [k.strip().lower() for k in keywords_str.split(',') if k.strip()]
        text_lower = text.lower()
        if any(kw in text_lower for kw in kws):
            return True
            
    if mode == "None (Tümünü Koru - Silme Yapma)":
        return False
    if mode == "All (Tüm Yazıları Sil - Harf Bazlı Pürüzsüz)":
        return True
        
    # Check preset modes
    if "Top-Left" in mode and (cx < w * 0.5 and cy < h * 0.35):
        return True
    if "Top-Right" in mode and (cx >= w * 0.5 and cy < h * 0.35):
        return True
    if "Bottom-Left" in mode and (cx < w * 0.5 and cy >= h * 0.65):
        return True
    if "Bottom-Right" in mode and (cx >= w * 0.5 and cy >= h * 0.65):
        return True
    if "Top-Bar" in mode and (cy < h * 0.25):
        return True
    if "Bottom-Bar" in mode and (cy >= h * 0.75):
        return True
        
    # Check custom_zones_str
    if custom_zones_str:
        zones = [z.strip().lower() for z in custom_zones_str.split(',') if z.strip()]
        for z in zones:
            if "top-left" in z and (cx < w * 0.5 and cy < h * 0.35):
                return True
            if "top-right" in z and (cx >= w * 0.5 and cy < h * 0.35):
                return True
            if "bottom-left" in z and (cx < w * 0.5 and cy >= h * 0.65):
                return True
            if "bottom-right" in z and (cx >= w * 0.5 and cy >= h * 0.65):
                return True
            # Check coordinate format: "x1, y1, x2, y2" or "x, y, w, h"
            parts = [p.strip() for p in z.split() if p.strip()]
            if len(parts) == 4:
                try:
                    coords = [float(p) for p in parts]
                    x1, y1, x2, y2 = coords[0], coords[1], coords[2], coords[3]
                    # Check if x2, y2 is w, h or right, bottom
                    if x2 < x1 or y2 < y1:
                        x2, y2 = x1 + x2, y1 + y2
                    if x1 <= cx <= x2 and y1 <= cy <= y2:
                        return True
                except ValueError:
                    pass

    return False

# Test cases
h, w = 768, 432
box_top_left = [[10, 20], [100, 20], [100, 50], [10, 50]]
box_center = [[150, 350], [250, 350], [250, 390], [150, 390]]
box_bottom = [[100, 700], [200, 700], [200, 740], [100, 740]]

# Case 1: Delete Top-Left watermark
assert is_box_in_delete_zone(box_top_left, h, w, "Top-Left (Sol Üst Köşe - Filigran/Kullanıcı Adı Sil)", "", "", "@user") == True
assert is_box_in_delete_zone(box_center, h, w, "Top-Left (Sol Üst Köşe - Filigran/Kullanıcı Adı Sil)", "", "", "Level 1") == False

# Case 2: Delete by keyword "@"
assert is_box_in_delete_zone(box_top_left, h, w, "None (Tümünü Koru - Silme Yapma)", "", "@, tiktok", "@user") == True
assert is_box_in_delete_zone(box_center, h, w, "None (Tümünü Koru - Silme Yapma)", "", "@, tiktok", "Level 1") == False

# Case 3: Multiple zones
assert is_box_in_delete_zone(box_top_left, h, w, "Custom (Özel Koordinat veya Kelime)", "top-left, bottom-right", "", "@user") == True
assert is_box_in_delete_zone(box_center, h, w, "Custom (Özel Koordinat veya Kelime)", "top-left, bottom-right", "", "Level 1") == False

print("All zone and keyword tests passed successfully!")
