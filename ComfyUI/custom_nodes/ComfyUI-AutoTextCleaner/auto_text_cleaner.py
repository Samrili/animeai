import os
import torch
import torch.nn.functional as F
import numpy as np
import cv2
import re
from PIL import Image, ImageDraw, ImageFont
from rapidocr_onnxruntime import RapidOCR

# Lazy singleton OCR engine to avoid reloading ONNX models on every queue
_ocr_engine = None

def get_ocr_engine():
    global _ocr_engine
    if _ocr_engine is None:
        _ocr_engine = RapidOCR()
    return _ocr_engine


def normalize_text(text):
    """
    OCR bazen Türkçe veya özel karakterleri yanlış tanır.
    Hem orijinal hem normalleştirilmiş metin eşleştirmesi yapar.
    """
    if not text:
        return ""
    # Küçük harfe çevir
    t = text.lower().strip()
    # Türkçe karakterleri normalize et (OCR genellikle ASCII döndürür)
    t = t.replace('ı', 'i').replace('ş', 's').replace('ğ', 'g')
    t = t.replace('ü', 'u').replace('ö', 'o').replace('ç', 'c')
    # Noktalama ve boşlukları normalize et
    t = re.sub(r'[^a-z0-9\s@#_.-]', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t


def keyword_matches(text, keywords_str):
    """
    Verilen metinde anahtar kelimelerin geçip geçmediğini kontrol eder.
    Boşluksuz ve küçük/büyük harf duyarsız arama yapar ("MUSTYYBOXING" ile "M U S T Y Y B O X I N G" eşleşir).
    Tek harfli anahtar sözcüklerin tüm kelimeleri yanlışlıkla silmesini engeller.
    """
    if not keywords_str or not text:
        return False
    kws_raw = [k.strip() for k in keywords_str.split(',') if k.strip()]
    if not kws_raw:
        return False

    text_lower = text.lower().strip()
    text_nospace = text_lower.replace(" ", "")
    text_norm = normalize_text(text)
    text_norm_nospace = text_norm.replace(" ", "")

    for kw in kws_raw:
        kw_lower = kw.lower().strip()
        kw_nospace = kw_lower.replace(" ", "")
        kw_norm = normalize_text(kw)
        kw_norm_nospace = kw_norm.replace(" ", "")

        if not kw_nospace:
            continue

        # Tek harfli anahtar kelimeler yanlışlıkla tüm kelimeleri silmesin!
        # Örneğin kullanıcı 'O' yazarsa 'CROSS' veya 'HOOK' silinmemelidir.
        if len(kw_nospace) <= 1:
            if text_lower == kw_lower or kw_lower in text_lower.split():
                return True
            continue

        # 1. Boşluksuz doğrudan eşleştirme ("mustyyboxing" == "mustyyboxing")
        if kw_nospace in text_nospace or kw_norm_nospace in text_norm_nospace:
            return True
        if text_nospace in kw_nospace or text_norm_nospace in kw_norm_nospace:
            return True

        # 2. Normalize edilmiş alt-dize eşleştirme
        if kw_norm and (kw_norm in text_norm or text_norm in kw_norm):
            return True

        # 3. Kelime parça eşleştirme: "tiktok" -> "t1kt0k" gibi OCR hataları için
        if kw_norm_nospace and len(kw_norm_nospace) >= 4:
            def ocr_normalize(s, one_as):
                return (s.replace('0', 'o')
                         .replace('1', one_as)
                         .replace('3', 'e')
                         .replace('4', 'a')
                         .replace('5', 's')
                         .replace('8', 'b'))
            text_ocr_l = ocr_normalize(text_norm_nospace, 'l')
            kw_ocr_l   = ocr_normalize(kw_norm_nospace,   'l')
            if kw_ocr_l in text_ocr_l or text_ocr_l in kw_ocr_l:
                return True
            text_ocr_i = ocr_normalize(text_norm_nospace, 'i')
            kw_ocr_i   = ocr_normalize(kw_norm_nospace,   'i')
            if kw_ocr_i in text_ocr_i or text_ocr_i in kw_ocr_i:
                return True

    return False


def is_box_in_delete_zone(box, h, w, mode, custom_zones_str, keywords_str, text):
    """
    Belirli bir metin kutusunun kullanıcının silmek istediği bölgede veya kelimede olup olmadığını kontrol eder.
    """
    pts = np.array(box, dtype=np.float32).reshape((-1, 2))
    cx, cy = float(np.mean(pts[:, 0])), float(np.mean(pts[:, 1]))

    # 1. Kelime / anahtar sözcük kontrolü (örn. "@watermark", "tiktok")
    # 1. Kelime / anahtar sözcük kontrolü (örn. "@watermark", "tiktok")
    # Bu kontrol her zaman önce yapılır, mode="None" olsa bile keyword eşleşirse siler
    if keyword_matches(text, keywords_str):
        return True

    if "None" in mode or "Yok" in mode:
        return False
    if "All" in mode or "Tüm Yazıları" in mode:
        return True

    # 2. Sosyal medya filigranı preseti (@, tiktok, capcut, watermark, reels, douyin vb.)
    if "Sosyal Medya" in mode or "Social" in mode:
        social_kw = "tiktok, capcut, @, watermark, reels, kwai, douyin"
        if keyword_matches(text, social_kw) or "@" in text:
            return True
        # Köşe filigranları (sol üst veya sağ alt köşe)
        if (cx < w * 0.45 and cy < h * 0.30) or (cx >= w * 0.55 and cy >= h * 0.70):
            if len(text.strip().split()) <= 4 and len(text.strip()) <= 25:
                return True

    # 3. Hazır preset bölgeleri (Köşeler / Şeritler)
    if ("Top-Left" in mode or "Sol Ust" in mode or "Sol Üst" in mode) and (cx < w * 0.5 and cy < h * 0.35):
        return True
    if ("Top-Right" in mode or "Sag Ust" in mode or "Sağ Üst" in mode) and (cx >= w * 0.5 and cy < h * 0.35):
        return True
    if ("Bottom-Left" in mode or "Sol Alt" in mode) and (cx < w * 0.5 and cy >= h * 0.65):
        return True
    if ("Bottom-Right" in mode or "Sag Alt" in mode or "Sağ Alt" in mode) and (cx >= w * 0.5 and cy >= h * 0.65):
        return True
    if ("Top-Bar" in mode or "Ust Serit" in mode or "Üst Şerit" in mode) and (cy < h * 0.25):
        return True
    if ("Bottom-Bar" in mode or "Alt Serit" in mode or "Alt Şerit" in mode) and (cy >= h * 0.75):
        return True

    # 3. Özel bölgeler (Metin: "top-left, bottom-right" veya koordinat: "x1 y1 x2 y2")
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
            if "top-bar" in z and (cy < h * 0.25):
                return True
            if "bottom-bar" in z and (cy >= h * 0.75):
                return True

            parts = [p.strip() for p in z.split() if p.strip()]
            if len(parts) == 4:
                try:
                    coords = [float(p) for p in parts]
                    zx1 = coords[0] * w if coords[0] <= 1.0 else coords[0]
                    zy1 = coords[1] * h if coords[1] <= 1.0 else coords[1]
                    zx2 = coords[2] * w if coords[2] <= 1.0 else coords[2]
                    zy2 = coords[3] * h if coords[3] <= 1.0 else coords[3]
                    if zx2 < zx1: zx1, zx2 = zx2, zx1
                    if zy2 < zy1: zy1, zy2 = zy2, zy1
                    if zx1 <= cx <= zx2 and zy1 <= cy <= zy2:
                        return True
                except ValueError:
                    pass

    return False


def extract_smart_letter_mask(img_bgr, pts_int, h, w, dilation=3):
    """
    Kutu/dikdörtgen şeklinde değil, SADECE harflerin/rakamların kendi piksellerini çıkartır.
    Açık arka plan üzerindeki koyu yazıları (ve koyu arka plandaki açık yazıları) otomatik algılar.
    Böylece arka plan dokusu korunur ve inpaint yapıldığında silinen yer kesinlikle belli olmaz.
    """
    mask_roi = np.zeros((h, w), dtype=np.uint8)
    cv2.fillPoly(mask_roi, [pts_int], 255)
    mask_roi_dilated = cv2.dilate(mask_roi, np.ones((7, 7), np.uint8))

    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    pixels_in_roi = gray[mask_roi_dilated > 0]
    if len(pixels_in_roi) == 0:
        return mask_roi

    # ROI sınır piksellerinden arka plan parlaklığını belirle
    x, y, bw, bh = cv2.boundingRect(pts_int)
    pad = 4
    x1, y1 = max(0, x - pad), max(0, y - pad)
    x2, y2 = min(w, x + bw + pad), min(h, y + bh + pad)
    roi_crop = gray[y1:y2, x1:x2]

    border_pixels = np.concatenate([
        roi_crop[0, :], roi_crop[-1, :], roi_crop[:, 0], roi_crop[:, -1]
    ])
    is_light_bg = border_pixels.mean() > 128

    if is_light_bg:
        # Açık zemin üstünde koyu yazı (örn. beyaz kart / kağıt üstünde siyah yazı)
        thresh_val, _ = cv2.threshold(pixels_in_roi, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        _, letter_thresh = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY_INV)
    else:
        # Koyu zemin üstünde açık yazı (örn. koyu sahnede beyaz altyazı)
        thresh_val, _ = cv2.threshold(pixels_in_roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        thresh_val = min(thresh_val, 160)
        _, letter_thresh = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
        # Renkli / sarı yazılar için doygunluk kontrolü
        hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
        sat = hsv[:, :, 1]
        _, sat_thresh = cv2.threshold(sat, 80, 255, cv2.THRESH_BINARY)
        letter_thresh = cv2.bitwise_or(letter_thresh, sat_thresh)

    letter_mask = cv2.bitwise_and(letter_thresh, mask_roi_dilated)

    if dilation > 0:
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilation * 2 + 1, dilation * 2 + 1))
        letter_mask = cv2.dilate(letter_mask, k, iterations=1)

    return letter_mask


def detect_annotations_and_shapes(img_bgr, mode="Red (Kirmizi Halka ve Oklar)", sensitivity=0.60, dilation=4):
    """
    Videolardaki kırmızı halka, ok, işaret ve vurgu şekillerini otomatik tespit eder.
    Halka içi boşsa sadece halkanın kendisini (çizgisini) maskeler, böylece halkanın
    içindeki odak noktası animeye dönüşürken kırmızı halka/ok kristal netlikte korunur.
    """
    h, w = img_bgr.shape[:2]
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    sat_thresh = int(np.clip(255 * (1.0 - sensitivity * 0.55), 75, 210))
    val_thresh = int(np.clip(255 * (1.0 - sensitivity * 0.50), 65, 200))

    if "Yellow" in mode:
        mask1 = cv2.inRange(hsv, np.array([0, sat_thresh, val_thresh]), np.array([35, 255, 255]))
        mask2 = cv2.inRange(hsv, np.array([165, sat_thresh, val_thresh]), np.array([180, 255, 255]))
        color_mask = cv2.bitwise_or(mask1, mask2)
    elif "All" in mode:
        color_mask = cv2.inRange(hsv, np.array([0, sat_thresh, val_thresh]), np.array([180, 255, 255]))
    else:  # Red
        mask1 = cv2.inRange(hsv, np.array([0, sat_thresh, val_thresh]), np.array([10, 255, 255]))
        mask2 = cv2.inRange(hsv, np.array([165, sat_thresh, val_thresh]), np.array([180, 255, 255]))
        color_mask = cv2.bitwise_or(mask1, mask2)

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(color_mask, connectivity=8)
    max_pixels = int(h * w * 0.40)
    min_pixels = 15

    clean_mask = np.zeros((h, w), dtype=np.uint8)
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        if min_pixels <= area <= max_pixels:
            clean_mask[labels == i] = 255

    if dilation > 0 and np.any(clean_mask > 0):
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilation * 2 + 1, dilation * 2 + 1))
        clean_mask = cv2.dilate(clean_mask, k, iterations=1)

    return clean_mask


class AutoTextCleaner:
    """
    ComfyUI Node: Auto Text & Shape Cleaner
    Her karedeki metinleri, logoları, kırmızı halka ve okları akıllıca tespit eder.
    Kullanıcının istediği bölgedeki veya anahtar kelimedeki yazıları KUTUSUZ (harf bazlı)
    şekilde pürüzsüzce siler; diğer yazıları ve şekilleri ise koruyarak anime videosunun
    üzerine giydirir.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "mode": ([
                    "Akıllı Silme ve Koruma (Seçilenleri Sil, Kalanı Koru)",
                    "Tüm Yazıları Sil (Arka Plana Göm / Temizle)",
                    "Tümünü Koru (Hiçbir Şey Silme)",
                    "Devre Dışı (Bypass)"
                ], {"default": "Akıllı Silme ve Koruma (Seçilenleri Sil, Kalanı Koru)"}),
                "delete_zone": ([
                    "Yok (Sadece kelimelere göre sil veya silme yapma)",
                    "Sosyal Medya Filigranları (@, TikTok, CapCut, Logo)",
                    "Sol Üst Köşe (Top-Left Watermark / Logo)",
                    "Sağ Üst Köşe (Top-Right Watermark / Logo)",
                    "Sol Alt Köşe (Bottom-Left)",
                    "Sağ Alt Köşe (Bottom-Right)",
                    "Üst Şerit (Top-Bar)",
                    "Alt Şerit (Bottom-Bar - Altyazılar)",
                    "Özel Koordinat (Custom Zone)"
                ], {"default": "Yok (Sadece kelimelere göre sil veya silme yapma)"}),
                "delete_keywords": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Örn: tiktok, @watermark, mustyy (virgülle ayırın)"
                }),
                "shape_protection": ([
                    "Kırmızı Halka ve Okları Koru (Red Shapes)",
                    "Kırmızı ve Sarı Şekilleri Koru (Red + Yellow)",
                    "Tüm Canlı Renkli Şekilleri Koru (All Vibrant)",
                    "Şekilleri Koruma / Kapat (Disabled)"
                ], {"default": "Kırmızı Halka ve Okları Koru (Red Shapes)"}),
            },
            "optional": {
                "custom_zones": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Sadece Özel Koordinat seçildiğinde: x1 y1 x2 y2"
                }),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("images", "text_mask")
    FUNCTION = "clean_text"
    CATEGORY = "AnimeAI/Video"

    def clean_text(self, images,
                   mode="Akıllı Silme ve Koruma (Seçilenleri Sil, Kalanı Koru)",
                   delete_zone="Yok (Sadece kelimelere göre sil veya silme yapma)",
                   delete_keywords="",
                   shape_protection="Kırmızı Halka ve Okları Koru (Red Shapes)",
                   custom_zones="",
                   **kwargs):
        # 1. Geriye dönük uyumluluk: eski boolean 'enabled' veya 'Devre Dışı' kontrolü
        if isinstance(mode, bool):
            is_enabled = mode
            mode_str = "Akıllı Silme ve Koruma (Seçilenleri Sil, Kalanı Koru)" if is_enabled else "Devre Dışı (Bypass)"
        else:
            mode_str = str(mode)

        if "Devre Dışı" in mode_str or "Bypass" in mode_str or kwargs.get("enabled") is False:
            b, h, w, _ = images.shape
            empty_mask = torch.zeros((b, h, w), dtype=torch.float32, device=images.device)
            return (images, empty_mask)

        # 2. Silme kurallarını çözümle
        if "Tüm Yazıları Sil" in mode_str or kwargs.get("delete_region_mode") == "All":
            effective_zone = "All"
            effective_keywords = ""
        elif "Tümünü Koru" in mode_str:
            effective_zone = "None"
            effective_keywords = ""
        else:
            effective_zone = kwargs.get("delete_region_mode") or delete_zone
            effective_keywords = kwargs.get("delete_keywords") if "delete_keywords" in kwargs else delete_keywords

        effective_custom_zones = kwargs.get("delete_custom_zones") if "delete_custom_zones" in kwargs else custom_zones

        # 3. Şekil koruma kurallarını çözümle
        sp = kwargs.get("shape_color_mode") or shape_protection
        if "Disabled" in str(sp) or "Kapat" in str(sp) or kwargs.get("protect_red_shapes") is False:
            protect_red_shapes = False
            shape_color_mode = "Disabled"
        elif "Yellow" in str(sp) or "Sarı" in str(sp):
            protect_red_shapes = True
            shape_color_mode = "Red + Yellow (Kirmizi ve Sari)"
        elif "Vibrant" in str(sp) or "Canlı" in str(sp):
            protect_red_shapes = True
            shape_color_mode = "All Vibrant (Tum Canli Renkler)"
        else:
            protect_red_shapes = True
            shape_color_mode = "Red (Kirmizi Halka ve Oklar)"

        # 4. Hiperparametreler (en ideal test edilmiş sabitler, gerekirse kwargs ile ezilebilir)
        min_confidence = float(kwargs.get("min_confidence", 0.40))
        mask_dilation = int(kwargs.get("mask_dilation", 4))
        inpaint_radius = int(kwargs.get("inpaint_radius", 5))
        inpaint_method = str(kwargs.get("inpaint_method", "Telea"))
        shape_sensitivity = float(kwargs.get("shape_sensitivity", 0.60))
        shape_dilation = int(kwargs.get("shape_dilation", 4))
        shape_padding = int(kwargs.get("shape_padding", 8))
        letter_level_cleaning = bool(kwargs.get("letter_level_cleaning", True))
        mask_mode = str(kwargs.get("mask_mode", "Box (Tum Kutu ve Sekil Koruma)"))
        clean_mode = str(kwargs.get("clean_mode", "Inpaint Background (Arka Plani Temizle - Onerilen)"))

        engine = get_ocr_engine()
        batch_size, h, w, c = images.shape

        cleaned_list = []
        preserve_masks_list = []

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (mask_dilation * 2 + 1, mask_dilation * 2 + 1)) if mask_dilation > 0 else None
        do_inpaint = ("Inpaint" in clean_mode)

        # Keyword modu için daha düşük güven eşiği kullan
        kw_confidence = min(min_confidence, 0.20) if effective_keywords.strip() else min_confidence

        for i in range(batch_size):
            img_tensor = images[i]
            img_np = (img_tensor.cpu().numpy() * 255.0).clip(0, 255).astype(np.uint8)
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

            # 1. Metin Tespiti (RapidOCR) - Kucuk veya genis aralikli filigranlar icin otomatik olcekleme
            ocr_scale = 1.0
            if max(h, w) <= 800:
                ocr_scale = 2.0
            elif max(h, w) <= 1200:
                ocr_scale = 1.5

            if ocr_scale != 1.0:
                ocr_img = cv2.resize(img_bgr, (int(w * ocr_scale), int(h * ocr_scale)), interpolation=cv2.INTER_LANCZOS4)
            else:
                ocr_img = img_bgr

            raw_ocr_result, _ = engine(ocr_img)
            ocr_result = []
            if raw_ocr_result:
                for item in raw_ocr_result:
                    box, text, score = item[0], item[1], item[2]
                    if ocr_scale != 1.0:
                        scaled_box = (np.array(box, dtype=np.float32) / ocr_scale).tolist()
                    else:
                        scaled_box = box
                    ocr_result.append((scaled_box, text, score))

            inpaint_frame_mask = np.zeros((h, w), dtype=np.uint8)
            preserve_frame_mask = np.zeros((h, w), dtype=np.uint8)
            has_inpaint = False

            # Dogrudan koordinatli silme bolgeleri (OCR'a bagli kalmaksizin kesin silme)
            if effective_custom_zones:
                for z in [item.strip().lower() for item in effective_custom_zones.split(',') if item.strip()]:
                    parts = [p for p in z.split() if p]
                    if len(parts) == 4:
                        try:
                            c = [float(p) for p in parts]
                            zx1 = int(c[0] * w if c[0] <= 1.0 else c[0])
                            zy1 = int(c[1] * h if c[1] <= 1.0 else c[1])
                            zx2 = int(c[2] * w if c[2] <= 1.0 else c[2])
                            zy2 = int(c[3] * h if c[3] <= 1.0 else c[3])
                            zx1, zx2 = min(zx1, zx2), max(zx1, zx2)
                            zy1, zy2 = min(zy1, zy2), max(zy1, zy2)
                            zx1, zy1 = max(0, zx1), max(0, zy1)
                            zx2, zy2 = min(w, zx2), min(h, zy2)
                            inpaint_frame_mask[zy1:zy2, zx1:zx2] = 255
                            has_inpaint = True
                        except Exception:
                            pass

            # Şeffaf Bilgilendirme: İlk karede tespit edilen ve silinen/korunan öğeleri temizce özetle
            if i == 0:
                if ocr_result:
                    del_items = []
                    keep_items = []
                    for itm in ocr_result:
                        bx, txt, sc = itm[0], itm[1], itm[2]
                        if is_box_in_delete_zone(bx, h, w, effective_zone, effective_custom_zones, effective_keywords, txt):
                            del_items.append(txt)
                        else:
                            keep_items.append(txt)

                    del_str = f"'{del_items[0]}' (+{len(del_items)-1})" if len(del_items) > 1 else (f"'{del_items[0]}'" if del_items else "yok")
                    keep_str = f"'{keep_items[0]}' (+{len(keep_items)-1})" if len(keep_items) > 1 else (f"'{keep_items[0]}'" if keep_items else "yok")
                    print(f"[AutoTextCleaner] Kare 1: {len(ocr_result)} metin bulundu -> Silinen: [{del_str}], Korunan: [{keep_str}]")
                else:
                    print(f"[AutoTextCleaner] Kare 1: Metin bulunamadı (temiz sahne).")

            has_delete_rules = (effective_keywords.strip() != "") or ("None" not in effective_zone and "Yok" not in effective_zone) or (effective_custom_zones.strip() != "")

            if ocr_result:
                for item in ocr_result:
                    box, text, score = item[0], item[1], item[2]

                    # Keyword eşleşmesi varsa daha düşük güven eşiğini kullan
                    is_keyword_match = keyword_matches(text, effective_keywords) if effective_keywords.strip() else False
                    effective_threshold = kw_confidence if is_keyword_match else min_confidence
                    if score < effective_threshold:
                        continue

                    pts_float = np.array(box, dtype=np.float32).reshape((-1, 2))
                    pts_int = pts_float.astype(np.int32).reshape((-1, 1, 2))

                    # Bu metin silinmek istenen bölgede mi veya anahtar kelimede mi?
                    should_delete = is_box_in_delete_zone(
                        box, h, w,
                        effective_zone,
                        effective_custom_zones,
                        effective_keywords,
                        text
                    )

                    if should_delete:
                        # KULLANICI BU YAZIYI SİLMEK İSTİYOR:
                        if letter_level_cleaning:
                            del_mask = extract_smart_letter_mask(img_bgr, pts_int, h, w, dilation=max(2, mask_dilation // 2))
                        else:
                            del_mask = np.zeros((h, w), dtype=np.uint8)
                            cv2.fillPoly(del_mask, [pts_int], 255)
                            if kernel is not None:
                                del_mask = cv2.dilate(del_mask, kernel, iterations=1)

                        # Arka plandan silinmesi için inpaint maskesine ekle,
                        # preserve_frame_mask'e KESİNLİKLE ekleme (geri giydirilmesin!)
                        inpaint_frame_mask = cv2.bitwise_or(inpaint_frame_mask, del_mask)
                        has_inpaint = True
                    else:
                        # KULLANICI BU YAZIYI KORUMAK İSTİYOR:
                        if "Box" in mask_mode:
                            x_min, y_min = np.min(pts_float, axis=0)
                            x_max, y_max = np.max(pts_float, axis=0)
                            pad = max(0, shape_padding)
                            x1 = max(0, int(x_min - pad))
                            y1 = max(0, int(y_min - pad))
                            x2 = min(w, int(x_max + pad))
                            y2 = min(h, int(y_max + pad))
                            item_mask = np.zeros((h, w), dtype=np.uint8)
                            cv2.rectangle(item_mask, (x1, y1), (x2, y2), 255, -1)
                            if kernel is not None:
                                item_mask = cv2.dilate(item_mask, kernel, iterations=1)
                        else:
                            item_mask = extract_smart_letter_mask(img_bgr, pts_int, h, w, dilation=mask_dilation)

                        preserve_frame_mask = cv2.bitwise_or(preserve_frame_mask, item_mask)
                        # Sadece genel altyazı temizliği modundaysa (silme kuralı yokken) anime öncesi arkaplan inpaint'i yapılır.
                        # Özel bir silme kuralı (keyword veya bölge) tanımlandıysa korunan öğeler KESİNLİKLE inpaint edilip bozulmaz!
                        if do_inpaint and not has_delete_rules:
                            inpaint_frame_mask = cv2.bitwise_or(inpaint_frame_mask, item_mask)
                            has_inpaint = True

            # 2. Kırmızı Halka, Ok ve Şekil Tespiti (Korunacak Öğeler)
            if protect_red_shapes and shape_color_mode != "Disabled":
                shape_mask = detect_annotations_and_shapes(
                    img_bgr,
                    mode=shape_color_mode,
                    sensitivity=shape_sensitivity,
                    dilation=shape_dilation
                )
                if np.any(shape_mask > 0):
                    preserve_frame_mask = cv2.bitwise_or(preserve_frame_mask, shape_mask)
                    if do_inpaint and not has_delete_rules:
                        inpaint_frame_mask = cv2.bitwise_or(inpaint_frame_mask, shape_mask)
                        has_inpaint = True

            # 3. Arka Planı Temizleme (Inpainting)
            if has_inpaint and np.any(inpaint_frame_mask > 0):
                if inpaint_method == "Telea":
                    cleaned_bgr = cv2.inpaint(img_bgr, inpaint_frame_mask, inpaintRadius=inpaint_radius, flags=cv2.INPAINT_TELEA)
                else:
                    cleaned_bgr = cv2.inpaint(img_bgr, inpaint_frame_mask, inpaintRadius=inpaint_radius, flags=cv2.INPAINT_NS)
                cleaned_rgb = cv2.cvtColor(cleaned_bgr, cv2.COLOR_BGR2RGB)
            else:
                cleaned_rgb = img_np

            cleaned_float = cleaned_rgb.astype(np.float32) / 255.0
            cleaned_list.append(cleaned_float)
            preserve_masks_list.append(preserve_frame_mask.astype(np.float32) / 255.0)

        cleaned_tensor = torch.from_numpy(np.stack(cleaned_list, axis=0)).to(images.device)
        mask_tensor = torch.from_numpy(np.stack(preserve_masks_list, axis=0)).to(images.device)

        return (cleaned_tensor, mask_tensor)


class AutoTextShapeOverlay:
    """
    ComfyUI Node: Auto Text & Shape Preserver (Overlay)
    Orijinal videodaki net yazıları, kırmızı halkaları, okları ve logoları,
    AnimateDiff/KSampler tarafından üretilen anime videosunun üzerine kusursuzca giydirir.
    Böylece anime stili korunurken yazılar, halkalar ve oklar asla bozulmaz ve kristal netlikte kalır.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "anime_images": ("IMAGE",),
                "original_images": ("IMAGE",),
                "text_mask": ("MASK",),
                "blend_feather": ("INT", {"default": 2, "min": 0, "max": 15, "step": 1}),
                "opacity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.05}),
            },
            "optional": {
                "user_mask": ("MASK",),  # Kullanici tarafindan secilen koruma bolgesi (LoadImage MASK slotu)
                "user_mask_image": ("IMAGE",),  # Alternatif: Dogrudan IMAGE slotu baglamak isteyenler icin
                "cleaned_images": ("IMAGE",),  # AutoTextCleaner'dan gelen temizlenmis kareler (silinen yazilar temizlenmis)
                "watermark_text": ("STRING", {"default": "@ringpulseofficial"}),
                "watermark_opacity": ("FLOAT", {"default": 0.40, "min": 0.0, "max": 1.0, "step": 0.05}),
                "watermark_position": (["Bottom-Center", "Bottom-Right", "Bottom-Left", "Top-Right", "Top-Left", "None"], {"default": "Bottom-Center"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "overlay_text_and_shapes"
    CATEGORY = "AnimeAI/Video"

    @staticmethod
    def _feather_mask_chunked(m, blend_feather, device, chunk_size=16):
        if blend_feather <= 0 or m is None or torch.count_nonzero(m) == 0:
            return m
        k_size = blend_feather * 2 + 1
        kernel = (torch.ones((1, 1, k_size, k_size), device=device) / (k_size * k_size)).float()

        # Eger tek karelik statik maskeyse, sadece tek kareyi feather et (milisaniyeler surer ve MB bellek harcar)
        if m.shape[0] == 1:
            m_padded = F.pad(m.unsqueeze(1), (blend_feather, blend_feather, blend_feather, blend_feather), mode='replicate')
            return F.conv2d(m_padded, kernel).squeeze(1)

        # Cok kareli maskelerde devasa bellek patlamasini onlemek icin parca parca (chunk) isle
        feathered_chunks = []
        for i in range(0, m.shape[0], chunk_size):
            chunk = m[i:i+chunk_size]
            chunk_padded = F.pad(chunk.unsqueeze(1), (blend_feather, blend_feather, blend_feather, blend_feather), mode='replicate')
            feathered_chunks.append(F.conv2d(chunk_padded, kernel).squeeze(1))
        return torch.cat(feathered_chunks, dim=0)

    @staticmethod
    def _blend_images_chunked(img_a, img_b, weight, chunk_size=32):
        B = img_a.shape[0]
        if B <= chunk_size:
            return img_a * (1.0 - weight) + img_b * weight
        outputs = []
        is_single_weight = (weight.shape[0] == 1)
        for i in range(0, B, chunk_size):
            w_chunk = weight if is_single_weight else weight[i:i+chunk_size]
            a_chunk = img_a[i:i+chunk_size]
            b_chunk = img_b[i:i+chunk_size]
            outputs.append(a_chunk * (1.0 - w_chunk) + b_chunk * w_chunk)
        return torch.cat(outputs, dim=0)

    @staticmethod
    def _render_video_watermark(images, watermark_text="@ringpulseofficial", watermark_opacity=0.40, watermark_position="Bottom-Center"):
        """
        Videoya hafif, sik, yari saydam 'dark glass pill' stilinde watermark ekler.
        Vectorized slice-blending kullandigi icin 360 karelik tam videoda yalnizca ~15-20 ms surer!
        Bellek tuketimi 0 MB, kalite kaybi 0 (pill disindaki tum pikseller %100 dokunulmamis kalir).
        """
        if not watermark_text or not str(watermark_text).strip() or watermark_opacity <= 0.0 or str(watermark_position).lower() in ("none", ""):
            return images

        text = str(watermark_text).strip()
        B, H, W, C = images.shape
        s = W / 1080.0
        font_size = max(13, int(21 * s))

        # Font secimi: Rajdhani-Bold veya sistem fontlari
        font = None
        font_candidates = [
            os.path.join(os.path.dirname(__file__), "..", "..", "fonts", "Rajdhani-Bold.ttf"),
            os.path.join(os.getcwd(), "fonts", "Rajdhani-Bold.ttf"),
            "fonts/Rajdhani-Bold.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/arial.ttf"
        ]
        for fpath in font_candidates:
            if os.path.exists(fpath):
                try:
                    font = ImageFont.truetype(fpath, font_size)
                    break
                except Exception:
                    continue
        if font is None:
            try:
                font = ImageFont.load_default()
            except Exception:
                return images

        # Yazi olculeri ve pill boyutlandirmasi
        dummy = Image.new("RGBA", (10, 10))
        d_dummy = ImageDraw.Draw(dummy)
        bbox = d_dummy.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

        pad_x = int(14 * s)
        pad_y = int(5 * s)
        dot_r = max(2, int(3 * s))
        dot_offset_x = int(6 * s)
        text_start_x = int(14 * s)

        pill_w = tw + pad_x * 2
        pill_h = th + pad_y * 2

        if pill_w >= W or pill_h >= H or pill_w <= 0 or pill_h <= 0:
            return images

        pos = str(watermark_position).lower()
        if "center" in pos:
            px = (W - pill_w) // 2
            py = H - pill_h - int(70 * s)
        elif "bottom-right" in pos:
            px = W - pill_w - int(40 * s)
            py = H - pill_h - int(90 * s)
        elif "bottom-left" in pos:
            px = int(40 * s)
            py = H - pill_h - int(90 * s)
        elif "top-right" in pos:
            px = W - pill_w - int(40 * s)
            py = int(70 * s)
        elif "top-left" in pos:
            px = int(40 * s)
            py = int(70 * s)
        else:
            px = (W - pill_w) // 2
            py = H - pill_h - int(70 * s)

        px = max(0, min(px, W - pill_w))
        py = max(0, min(py, H - pill_h))

        # Yari saydam, modern dark glass pill cizimi
        pill_img = Image.new("RGBA", (pill_w, pill_h), (0, 0, 0, 0))
        d_pill = ImageDraw.Draw(pill_img)

        eff_opacity = float(watermark_opacity)
        bg_alpha = int(180 * eff_opacity)
        border_alpha = int(220 * eff_opacity)
        text_alpha = int(255 * eff_opacity)

        d_pill.rounded_rectangle(
            [0, 0, pill_w - 1, pill_h - 1],
            radius=max(3, int(6 * s)),
            fill=(10, 14, 20, bg_alpha),
            outline=(200, 220, 255, border_alpha),
            width=1
        )
        dot_y = (pill_h - dot_r * 2) // 2
        d_pill.ellipse(
            [dot_offset_x, dot_y, dot_offset_x + dot_r * 2, dot_y + dot_r * 2],
            fill=(0, 235, 255, text_alpha)
        )
        d_pill.text((text_start_x, pad_y - 1), text, fill=(245, 250, 255, text_alpha), font=font)

        pill_np = np.array(pill_img).astype(np.float32) / 255.0
        pill_rgb = torch.from_numpy(pill_np[..., :3]).to(images.device)
        pill_a = torch.from_numpy(pill_np[..., 3:4]).to(images.device)

        # Vectorized slice blending: Devasa bellek harcamadan milisaniyeler icinde yalnizca watermark bolgesini gunceller
        try:
            sub = images[:, py:py+pill_h, px:px+pill_w]
            images[:, py:py+pill_h, px:px+pill_w] = sub * (1.0 - pill_a) + pill_rgb * pill_a
            return images
        except Exception:
            out = images.clone()
            sub = out[:, py:py+pill_h, px:px+pill_w]
            out[:, py:py+pill_h, px:px+pill_w] = sub * (1.0 - pill_a) + pill_rgb * pill_a
            return out

    def overlay_text_and_shapes(self, anime_images, original_images, text_mask, blend_feather=2, opacity=1.0, user_mask=None, user_mask_image=None, cleaned_images=None, watermark_text="@ringpulseofficial", watermark_opacity=0.40, watermark_position="Bottom-Center"):
        batch_size, target_h, target_w, _ = anime_images.shape
        device = anime_images.device

        # 1. Orijinal kareleri hazirla (yazilarin ve sekillerin geri giydirilmesi icin kaynak)
        orig = original_images.to(device)
        if orig.shape[0] < batch_size:
            orig = orig.repeat((batch_size // orig.shape[0] + 1, 1, 1, 1))[:batch_size]
        elif orig.shape[0] > batch_size:
            orig = orig[:batch_size]

        if orig.shape[1] != target_h or orig.shape[2] != target_w:
            orig_perm = orig.permute(0, 3, 1, 2)
            orig_resized = F.interpolate(orig_perm, size=(target_h, target_w), mode='bilinear', align_corners=False)
            orig = orig_resized.permute(0, 2, 3, 1)

        # 2. Temizlenmis kareleri hazirla (koruma alaninda animeyi engelleyip gercek videoyu tutmak icin kaynak)
        # Eger cleaned_images baglanmadiysa, orig kullanilir.
        if cleaned_images is not None:
            cleaned = cleaned_images.to(device)
            if cleaned.shape[0] < batch_size:
                cleaned = cleaned.repeat((batch_size // cleaned.shape[0] + 1, 1, 1, 1))[:batch_size]
            elif cleaned.shape[0] > batch_size:
                cleaned = cleaned[:batch_size]

            if cleaned.shape[1] != target_h or cleaned.shape[2] != target_w:
                cleaned_perm = cleaned.permute(0, 3, 1, 2)
                cleaned_resized = F.interpolate(cleaned_perm, size=(target_h, target_w), mode='bilinear', align_corners=False)
                cleaned = cleaned_resized.permute(0, 2, 3, 1)
        else:
            cleaned = orig

        # 3. Yazi ve Sekil koruma maskesi (AutoTextCleaner ciktisi)
        mask = text_mask.to(device)
        if mask.ndim == 2:
            mask = mask.unsqueeze(0)
        if mask.ndim == 4:
            mask = mask.squeeze(1)

        if mask.shape[1] != target_h or mask.shape[2] != target_w:
            mask_4d = mask.unsqueeze(1)
            mask_resized = F.interpolate(mask_4d, size=(target_h, target_w), mode='bilinear', align_corners=False)
            mask = mask_resized.squeeze(1)

        # Tek kare ise batch'e genisletmeden tut (broadcasting yapilacak); cok kareliyse uyum sagla
        if mask.shape[0] > 1 and mask.shape[0] < batch_size:
            mask = mask.repeat((batch_size // mask.shape[0] + 1, 1, 1))[:batch_size]
        elif mask.shape[0] > batch_size:
            mask = mask[:batch_size]

        # 4. Kullanici koruma maskesi (user_mask veya user_mask_image)
        # Beyaz (1.0) = animeyi engelle (gercek videoyu koru), Siyah (0.0) = anime uygula
        um = None
        if user_mask is not None:
            um = user_mask.to(device)
            if um.ndim == 4:
                if um.shape[-1] in (1, 3, 4):
                    um = um[..., :3].mean(dim=-1)
                elif um.shape[1] == 1:
                    um = um.squeeze(1)
            elif um.ndim == 2:
                um = um.unsqueeze(0)
        elif user_mask_image is not None:
            umi = user_mask_image.to(device)
            if umi.ndim == 4:
                um = umi[..., :3].mean(dim=-1)
            elif umi.ndim == 3:
                um = umi.mean(dim=-1).unsqueeze(0)

        # Akilli Yedek Kurtarma: Eger user_mask baglandiysa fakat ici tamamen 0 ciktiysa (opak PNG sorunu),
        # ComfyUI/input/protection_mask.png dosyasindaki RGB beyaz piksellerden otomatik maske cikar
        if um is not None and torch.count_nonzero(um) == 0:
            try:
                import os
                from PIL import Image
                candidates = ["ComfyUI/input/protection_mask.png", "input/protection_mask.png"]
                for c_path in candidates:
                    if os.path.exists(c_path):
                        p_img = Image.open(c_path)
                        p_arr = np.array(p_img.convert("RGB")).astype(np.float32) / 255.0
                        p_mask = (p_arr[..., 0] > 0.5).astype(np.float32)
                        if np.count_nonzero(p_mask) > 0:
                            um = torch.from_numpy(p_mask).unsqueeze(0).to(device)
                            print(f"[AutoTextShapeOverlay] Bilgi: LoadImage MASK bos gorundu, ancak protection_mask.png dosyasindan {int(np.count_nonzero(p_mask))} koruma pikseli basariyla kurtarildi!")
                            break
            except Exception:
                pass

        if um is not None and torch.count_nonzero(um) > 0:
            if um.shape[1] != target_h or um.shape[2] != target_w:
                um_4d = um.unsqueeze(1)
                um_resized = F.interpolate(um_4d, size=(target_h, target_w), mode='bilinear', align_corners=False)
                um = um_resized.squeeze(1)

            # Cok kareli maskeyse ve batch'ten azsa uyarla
            if um.shape[0] > 1 and um.shape[0] < batch_size:
                um = um.repeat((batch_size // um.shape[0] + 1, 1, 1))[:batch_size]

        # ADIM A: Anime vs Gercek Video Bilesimi (Kullanici Koruma Alani)
        # Korunan alanlarda (um == 1.0) 'cleaned' (gercek video, silinen yazilar temizlenmis) kullanilir.
        # Korunmayan alanlarda (um == 0.0) 'anime_images' kullanilir.
        if um is not None and torch.count_nonzero(um) > 0:
            um_feathered = self._feather_mask_chunked(um, blend_feather, device, chunk_size=16)
            um_weight = torch.clamp(um_feathered, 0.0, 1.0).unsqueeze(-1)
            base_images = self._blend_images_chunked(anime_images, cleaned, um_weight, chunk_size=32)
            print(f"[AutoTextShapeOverlay] Koruma maskesi aktif: {int(torch.count_nonzero(um[0]).item())} piksel gercek videodan (anime engellenerek) korundu.")
        else:
            base_images = anime_images

        # ADIM B: Yazi & Sekil Koruma Giydirmesi (AutoTextCleaner tarafindan saklanan yazilar/sekiller)
        # mask (text_mask) icindeki pikseller orig'den alinip base_images uzerine keskin sekilde giydirilir.
        # Kullanici bir yaziyi sil dediyse, text_mask icinde yer almaz; bu sayede koruma alani icinde olsa dahi silinmis kalir!
        if mask is not None and torch.count_nonzero(mask) > 0:
            mask_feathered = self._feather_mask_chunked(mask, blend_feather, device, chunk_size=16)
            mask_weight = torch.clamp(mask_feathered * opacity, 0.0, 1.0).unsqueeze(-1)
            output_images = self._blend_images_chunked(base_images, orig, mask_weight, chunk_size=32)
        else:
            output_images = base_images

        # ADIM C: Video Watermark Giydirmesi (Subtle Glass Pill)
        output_images = self._render_video_watermark(
            output_images,
            watermark_text=watermark_text,
            watermark_opacity=watermark_opacity,
            watermark_position=watermark_position
        )

        return (output_images,)


NODE_CLASS_MAPPINGS = {
    "AutoTextCleaner": AutoTextCleaner,
    "AutoTextShapeOverlay": AutoTextShapeOverlay,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AutoTextCleaner": "Auto Text and Subtitle Cleaner",
    "AutoTextShapeOverlay": "Auto Text & Shape Preserver (Overlay)",
}

# --- ComfyUI Server Routes for Mask Tool & Auto-Save ---
try:
    import server
    from aiohttp import web
    import folder_paths

    @server.PromptServer.instance.routes.get("/studio")
    @server.PromptServer.instance.routes.get("/studio.html")
    async def serve_studio(request):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(curr_dir, "..", "..", ".."))
        html_path = os.path.join(root_dir, "studio.html")
        if not os.path.exists(html_path):
            html_path = os.path.join(root_dir, "index.html")
        if os.path.exists(html_path):
            return web.FileResponse(html_path)
        return web.Response(text="studio.html bulunamadi", status=404)

    @server.PromptServer.instance.routes.get("/mask_tool")
    @server.PromptServer.instance.routes.get("/mask_tool.html")
    async def serve_mask_tool(request):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(curr_dir, "..", "..", ".."))
        html_path = os.path.join(root_dir, "tools", "mask_tool.html")
        if not os.path.exists(html_path):
            html_path = os.path.join(root_dir, "mask_tool.html")
        if os.path.exists(html_path):
            return web.FileResponse(html_path)
        return web.Response(text="mask_tool.html bulunamadi", status=404)

    @server.PromptServer.instance.routes.get("/poster_tool")
    @server.PromptServer.instance.routes.get("/poster_tool.html")
    async def serve_poster_tool(request):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(curr_dir, "..", "..", ".."))
        html_path = os.path.join(root_dir, "tools", "poster_tool.html")
        if not os.path.exists(html_path):
            html_path = os.path.join(root_dir, "poster_tool.html")
        if os.path.exists(html_path):
            return web.FileResponse(html_path)
        return web.Response(text="poster_tool.html bulunamadi", status=404)

    @server.PromptServer.instance.routes.post("/animeai/save_mask")
    async def save_mask_endpoint(request):
        post = await request.post()
        image = post.get("image")
        if image:
            input_dir = folder_paths.get_input_directory()
            target_path = os.path.join(input_dir, "protection_mask.png")
            content = image.file.read() if hasattr(image, "file") else image
            with open(target_path, "wb") as f:
                f.write(content)
            return web.json_response({"status": "success", "file": target_path})
        return web.Response(status=400)

    import time
    SERVER_INSTANCE_ID = str(int(time.time() * 1000))

    @server.PromptServer.instance.routes.get("/animeai/info")
    async def serve_animeai_info(request):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(curr_dir, "..", "..", ".."))
        wf_path = os.path.join(root_dir, "workflows", "animeai_workflow.json")
        if not os.path.exists(wf_path):
            wf_path = os.path.join(root_dir, "animeai_workflow.json")
        return web.json_response({
            "status": "ready",
            "server_id": SERVER_INSTANCE_ID,
            "has_workflow": os.path.exists(wf_path)
        })

    @server.PromptServer.instance.routes.get("/animeai/workflow")
    async def serve_animeai_workflow(request):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(curr_dir, "..", "..", ".."))
        wf_path = os.path.join(root_dir, "workflows", "animeai_workflow.json")
        if not os.path.exists(wf_path):
            wf_path = os.path.join(root_dir, "animeai_workflow.json")
        if os.path.exists(wf_path):
            return web.FileResponse(wf_path)
        return web.Response(text="animeai_workflow.json bulunamadi", status=404)
except Exception:
    pass
