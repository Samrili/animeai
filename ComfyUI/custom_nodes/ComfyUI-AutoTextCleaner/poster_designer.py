import os
import random
import torch
import numpy as np
from PIL import Image, ImageDraw, ImageFont

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(CURRENT_DIR, "fonts")

def get_font(font_name, size, fallback="arialbd.ttf"):
    path = os.path.join(FONTS_DIR, font_name)
    if os.path.exists(path):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    win_path = os.path.join("C:/Windows/Fonts", fallback)
    if os.path.exists(win_path):
        try:
            return ImageFont.truetype(win_path, size)
        except Exception:
            pass
    return ImageFont.load_default()

def fit_single_line_font(draw, text, font_name, max_w, target_size, min_size=18, fallback="impact.ttf"):
    """
    Dynamically scales down font size until text fits on a single line within max_w.
    Guarantees no horizontal overflow.
    """
    for sz in range(target_size, min_size - 1, -2):
        f = get_font(font_name, sz, fallback)
        bbox = draw.textbbox((0, 0), text, font=f)
        if (bbox[2] - bbox[0]) <= max_w:
            return f, sz
    return get_font(font_name, min_size, fallback), min_size

def draw_adaptive_title(draw, text, font_name, x, y, max_w, target_size, min_size=36, max_lines=2, fill=(255,255,255,255), shadow=True, fallback="impact.ttf", line_spacing=1.02):
    """
    Intelligently fits title into max_w either on 1 line or wrapped cleanly across max_lines.
    Returns (bottom_y, used_font, lines).
    """
    # 1. Check if it fits on a single line with acceptable size (>= 72% target_size)
    f_single, sz_single = fit_single_line_font(draw, text, font_name, max_w, target_size, min_size=int(target_size * 0.72), fallback=fallback)
    bbox_single = draw.textbbox((0, 0), text, font=f_single)
    if (bbox_single[2] - bbox_single[0]) <= max_w:
        if shadow:
            for dx, dy in [(-3,0),(3,0),(0,-3),(0,3),(4,4)]:
                draw.text((x+dx, y+dy), text, fill=(0,0,0,230), font=f_single)
        draw.text((x, y), text, fill=fill, font=f_single)
        t_box = draw.textbbox((x, y), text, font=f_single)
        return t_box[3], f_single, [text]
    
    # 2. Multi-line wrap if max_lines >= 2
    words = text.split(' ')
    best_lines = []
    best_font = None
    
    for sz in range(int(target_size * 0.85), min_size - 1, -2):
        f_try = get_font(font_name, sz, fallback)
        lines = []
        curr = []
        for w in words:
            test = ' '.join(curr + [w])
            bbox = draw.textbbox((0, 0), test, font=f_try)
            if (bbox[2] - bbox[0]) <= max_w or not curr:
                curr.append(w)
            else:
                lines.append(' '.join(curr))
                curr = [w]
        if curr:
            lines.append(' '.join(curr))
            
        if len(lines) <= max_lines:
            all_fit = all((draw.textbbox((0, 0), l, font=f_try)[2] - draw.textbbox((0, 0), l, font=f_try)[0]) <= max_w for l in lines)
            if all_fit:
                best_lines = lines
                best_font = f_try
                break
                
    if not best_lines:
        f_fallback = get_font(font_name, min_size, fallback)
        best_lines = [text]
        best_font = f_fallback
        
    line_h = int((best_font.size if hasattr(best_font, 'size') else min_size) * line_spacing)
    last_bottom = y
    for idx, line in enumerate(best_lines):
        ly = y + idx * line_h
        if shadow:
            for dx, dy in [(-2,0),(2,0),(0,-2),(0,2),(3,3)]:
                draw.text((x+dx, ly+dy), line, fill=(0,0,0,230), font=best_font)
        draw.text((x, ly), line, fill=fill, font=best_font)
        l_box = draw.textbbox((x, ly), line, font=best_font)
        last_bottom = max(last_bottom, l_box[3])
        
    return last_bottom, best_font, best_lines

def draw_wrapped_text(draw, text, font, fill, x, y, max_width, line_spacing=1.24, max_height=None, font_name="Rajdhani-SemiBold.ttf", fallback="arial.ttf", min_font_size=13):
    """
    Wraps text with auto-scaling to strictly prevent height and width overflows in card containers.
    """
    words = text.split(' ')
    current_size = font.size if hasattr(font, 'size') else 20
    curr_font = font
    
    # If max_height is given, search for font size that fits cleanly within max_height
    if max_height is not None:
        for sz in range(current_size, min_font_size - 1, -1):
            f_test = get_font(font_name, sz, fallback)
            test_lines = []
            test_curr = []
            for word in words:
                test_str = ' '.join(test_curr + [word])
                bbox = draw.textbbox((0, 0), test_str, font=f_test)
                if (bbox[2] - bbox[0]) <= max_width or not test_curr:
                    test_curr.append(word)
                else:
                    test_lines.append(' '.join(test_curr))
                    test_curr = [word]
            if test_curr:
                test_lines.append(' '.join(test_curr))
            
            test_lh = int(sz * line_spacing)
            if len(test_lines) * test_lh <= max_height:
                curr_font = f_test
                break
        else:
            curr_font = get_font(font_name, min_font_size, fallback)
            
    # Wrap text with curr_font
    lines = []
    curr_line = []
    for word in words:
        test_line = ' '.join(curr_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=curr_font)
        w = bbox[2] - bbox[0]
        if w <= max_width or not curr_line:
            curr_line.append(word)
        else:
            lines.append(' '.join(curr_line))
            curr_line = [word]
    if curr_line:
        lines.append(' '.join(curr_line))
        
    curr_size = curr_font.size if hasattr(curr_font, 'size') else 20
    line_h = int(curr_size * line_spacing)
    
    # If max_height is set, clamp lines so text never extends past container boundary
    if max_height is not None:
        max_possible_lines = max(1, int(max_height // line_h))
        if len(lines) > max_possible_lines:
            lines = lines[:max_possible_lines]
            if len(lines[-1]) > 3:
                lines[-1] = lines[-1][:-3] + "..."
                
    for i, line in enumerate(lines):
        draw.text((x, y + i * line_h), line, fill=fill, font=curr_font)
        
    return len(lines) * line_h

class FighterPosterDesigner:
    """
    Renders high-impact combat infographic posters in 1080x1350 (4:5 Feed Post)
    and 1080x1920 (9:16 Story/Reel) with 8 distinct layout archetypes,
    tactical combat info modules (Critical Flaw, Combat Range, Target Anatomy),
    bulletproof zero-overlap relative positioning, dynamic font auto-fitting,
    and a single sleek ringpulseofficial watermark.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "title": ("STRING", {"default": "THE LEAD HOOK", "multiline": False}),
                "tagline": ("STRING", {"default": "EXPLOSIVE ROTATIONAL POWER & ANGLE CUTTING", "multiline": False}),
                "protocol_badge": ("STRING", {"default": "[ COMBAT LAB // PROTOCOL 01 ]", "multiline": False}),
                "watermark": ("STRING", {"default": "@ringpulseofficial", "multiline": False}),
                "card_title": ("STRING", {"default": "/// EXECUTION KEYPOINTS", "multiline": False}),
                "target_zone": ("STRING", {"default": "V_TARGET: CHIN // TEMPLE", "multiline": False}),
                "tip_1_tag": ("STRING", {"default": "KINETIC TORQUE", "multiline": False}),
                "tip_1_desc": ("STRING", {"default": "Pivot lead foot 90° on the ball. Whip hips and core synchronously to generate maximum centrifugal force.", "multiline": True}),
                "tip_2_tag": ("STRING", {"default": "HORIZONTAL LOCK", "multiline": False}),
                "tip_2_desc": ("STRING", {"default": "Keep elbow horizontally locked level with the fist. Never drop the elbow below shoulder line at impact.", "multiline": True}),
                "tip_3_tag": ("STRING", {"default": "IRON COUNTER GUARD", "multiline": False}),
                "tip_3_desc": ("STRING", {"default": "Keep rear glove glued to the cheekbone. Slip head slightly off the center line to evade return fire.", "multiline": True}),
                "theme_color": (["Crimson Red", "Cyber Cyan", "UFC Gold", "Golden Bronze", "Emerald Green", "Toxic Emerald", "Electric Violet", "Solar Amber", "Ice Cobalt", "Bloodline Ruby", "Random Palette"], {"default": "Crimson Red"}),
                "layout_archetype": ([
                    "Random Layout Archetype",
                    "Floating Tactical Callouts (Left/Right)",
                    "Side Editorial Column (Magazine)",
                    "Cyberpunk Target Lock HUD",
                    "Classic Bottom Card",
                    "Dual-Wing Symmetrical Frame",
                    "Diagonal Kinetic Slash",
                    "Tactical Blueprint Dossier",
                    "Minimalist Brutalist Combat"
                ], {"default": "Random Layout Archetype"}),
                "resolution_mode": (["1080x1350 (4:5 Feed Post)", "1080x1920 (9:16 Story/Reel)", "1080x1350", "1080x1920", "Scale to 1080w", "Preserve Original"], {"default": "1080x1350 (4:5 Feed Post)"}),
                "caution_flaw": ("STRING", {"default": "DROPPING REAR GUARD ON ROTATION", "multiline": False}),
                "range_class": ("STRING", {"default": "INFIGHTING / POCKET [0.5M]", "multiline": False}),
            }
        }
        
    RETURN_TYPES = ("IMAGE", "IMAGE")
    RETURN_NAMES = ("poster_image", "clean_image")
    FUNCTION = "generate_poster"
    CATEGORY = "AnimeAI/Poster"

    def generate_poster(
        self, image, title, tagline, protocol_badge, watermark, card_title, target_zone,
        tip_1_tag, tip_1_desc, tip_2_tag, tip_2_desc, tip_3_tag, tip_3_desc,
        theme_color, layout_archetype, resolution_mode,
        caution_flaw="DROPPING REAR GUARD ON ROTATION", range_class="INFIGHTING / POCKET [0.5M]",
        **kwargs
    ):
        themes = {
            "Crimson Red": {
                "primary": (255, 38, 70, 255),
                "secondary": (0, 235, 255, 255),
                "gold": (255, 195, 0, 255),
                "border": (255, 38, 70, 170),
            },
            "Cyber Cyan": {
                "primary": (0, 235, 255, 255),
                "secondary": (255, 38, 70, 255),
                "gold": (255, 195, 0, 255),
                "border": (0, 235, 255, 170),
            },
            "UFC Gold": {
                "primary": (255, 195, 0, 255),
                "secondary": (0, 235, 255, 255),
                "gold": (255, 38, 70, 255),
                "border": (255, 195, 0, 170),
            },
            "Golden Bronze": {
                "primary": (255, 195, 0, 255),
                "secondary": (0, 235, 255, 255),
                "gold": (255, 38, 70, 255),
                "border": (255, 195, 0, 170),
            },
            "Emerald Green": {
                "primary": (0, 230, 130, 255),
                "secondary": (255, 195, 0, 255),
                "gold": (255, 230, 120, 255),
                "border": (0, 230, 130, 170),
            },
            "Toxic Emerald": {
                "primary": (0, 230, 130, 255),
                "secondary": (255, 195, 0, 255),
                "gold": (255, 230, 120, 255),
                "border": (0, 230, 130, 170),
            },
            "Electric Violet": {
                "primary": (185, 75, 251, 255),
                "secondary": (0, 235, 255, 255),
                "gold": (255, 215, 0, 255),
                "border": (185, 75, 251, 170),
            },
            "Solar Amber": {
                "primary": (255, 145, 0, 255),
                "secondary": (255, 220, 0, 255),
                "gold": (255, 240, 180, 255),
                "border": (255, 145, 0, 170),
            },
            "Ice Cobalt": {
                "primary": (0, 170, 255, 255),
                "secondary": (0, 255, 210, 255),
                "gold": (255, 220, 100, 255),
                "border": (0, 170, 255, 170),
            },
            "Bloodline Ruby": {
                "primary": (220, 20, 60, 255),
                "secondary": (255, 110, 140, 255),
                "gold": (255, 215, 0, 255),
                "border": (220, 20, 60, 170),
            }
        }
        
        if theme_color == "Random Palette" or theme_color not in themes:
            chosen_key = random.choice(list(themes.keys()))
            palette = themes[chosen_key]
        else:
            palette = themes[theme_color]
            
        layout_options = [
            "Floating Tactical Callouts (Left/Right)",
            "Side Editorial Column (Magazine)",
            "Cyberpunk Target Lock HUD",
            "Classic Bottom Card",
            "Dual-Wing Symmetrical Frame",
            "Diagonal Kinetic Slash",
            "Tactical Blueprint Dossier",
            "Minimalist Brutalist Combat"
        ]
        if layout_archetype == "Random Layout Archetype" or layout_archetype not in layout_options:
            chosen_layout = random.choice(layout_options)
        else:
            chosen_layout = layout_archetype

        tips = [
            ("01", tip_1_tag, tip_1_desc),
            ("02", tip_2_tag, tip_2_desc),
            ("03", tip_3_tag, tip_3_desc),
        ]
        wm_clean = watermark.strip()
        if not wm_clean.startswith("@"):
            wm_clean = "@" + wm_clean

        meta = {
            "title": title,
            "tagline": tagline,
            "protocol": protocol_badge,
            "watermark": wm_clean.upper(),
            "card_title": card_title,
            "target": target_zone,
            "caution": caution_flaw if caution_flaw else "DROPPING REAR GUARD ON ROTATION",
            "range": range_class if range_class else "INFIGHTING / POCKET [0.5M]"
        }

        b, h_orig, w_orig, c = image.shape
        out_tensors = []
        clean_tensors = []

        for i in range(b):
            frame_np = (image[i].cpu().numpy() * 255.0).clip(0, 255).astype(np.uint8)
            pil_img = Image.fromarray(frame_np).convert("RGBA")
            
            if "1350" in resolution_mode:
                target_w, target_h = 1080, 1350
                img_aspect = pil_img.width / pil_img.height
                target_aspect = target_w / target_h
                if img_aspect > target_aspect:
                    new_h = target_h
                    new_w = int(target_h * img_aspect)
                    pil_img = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    crop_x = (new_w - target_w) // 2
                    pil_img = pil_img.crop((crop_x, 0, crop_x + target_w, target_h))
                else:
                    new_w = target_w
                    new_h = int(target_w / img_aspect)
                    pil_img = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    crop_y = (new_h - target_h) // 2
                    pil_img = pil_img.crop((0, crop_y, target_w, crop_y + target_h))
            elif "1920" in resolution_mode:
                target_w, target_h = 1080, 1920
                img_aspect = pil_img.width / pil_img.height
                target_aspect = target_w / target_h
                if img_aspect > target_aspect:
                    new_h = target_h
                    new_w = int(target_h * img_aspect)
                    pil_img = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    crop_x = (new_w - target_w) // 2
                    pil_img = pil_img.crop((crop_x, 0, crop_x + target_w, target_h))
                else:
                    new_w = target_w
                    new_h = int(target_w / img_aspect)
                    pil_img = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    crop_y = (new_h - target_h) // 2
                    pil_img = pil_img.crop((0, crop_y, target_w, crop_y + target_h))
            elif resolution_mode == "Scale to 1080w":
                target_w = 1080
                target_h = int(1080 * (pil_img.height / pil_img.width))
                pil_img = pil_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            else:
                target_w, target_h = pil_img.width, pil_img.height

            # Clean art with watermark & sleek social CTA (no big headers, no tip cards, no flaw box)
            clean_poster = pil_img.copy()
            clean_poster = self._render_clean_watermark(clean_poster, target_w, target_h, palette, meta)
            clean_poster = self._render_social_cta(clean_poster, target_w, target_h, palette, meta, chosen_layout, is_clean_art=True)
            clean_rgb = clean_poster.convert("RGB")
            clean_np = (np.array(clean_rgb, dtype=np.float32) / 255.0)
            clean_tensors.append(torch.from_numpy(clean_np))

            # Dispatch layout renderer across 8 distinct archetypes
            if chosen_layout == "Floating Tactical Callouts (Left/Right)":
                poster = self._render_floating_callouts(pil_img, target_w, target_h, palette, tips, meta)
            elif chosen_layout == "Side Editorial Column (Magazine)":
                poster = self._render_side_column(pil_img, target_w, target_h, palette, tips, meta)
            elif chosen_layout == "Cyberpunk Target Lock HUD":
                poster = self._render_reticle_hud(pil_img, target_w, target_h, palette, tips, meta)
            elif chosen_layout == "Classic Bottom Card":
                poster = self._render_classic_bottom(pil_img, target_w, target_h, palette, tips, meta)
            elif chosen_layout == "Dual-Wing Symmetrical Frame":
                poster = self._render_dual_wing(pil_img, target_w, target_h, palette, tips, meta)
            elif chosen_layout == "Diagonal Kinetic Slash":
                poster = self._render_diagonal_slash(pil_img, target_w, target_h, palette, tips, meta)
            elif chosen_layout == "Tactical Blueprint Dossier":
                poster = self._render_blueprint_dossier(pil_img, target_w, target_h, palette, tips, meta)
            elif chosen_layout == "Minimalist Brutalist Combat":
                poster = self._render_brutalist_combat(pil_img, target_w, target_h, palette, tips, meta)
            else:
                poster = self._render_classic_bottom(pil_img, target_w, target_h, palette, tips, meta)

            # Render dynamic social media Call-To-Action (Like, Follow, Share)
            poster = self._render_social_cta(poster, target_w, target_h, palette, meta, chosen_layout)

            poster_rgb = poster.convert("RGB")
            out_np = (np.array(poster_rgb, dtype=np.float32) / 255.0)
            out_tensor = torch.from_numpy(out_np)
            out_tensors.append(out_tensor)

        final_tensor = torch.stack(out_tensors, dim=0)
        final_clean = torch.stack(clean_tensors, dim=0)
        return (final_tensor, final_clean)

    # ----------------- 1. FLOATING CALLOUTS (ADAPTIVE 1350/1920) -----------------
    def _render_floating_callouts(self, base, w, h, p, tips, meta):
        primary, secondary, gold = p["primary"], p["secondary"], p["gold"]
        is_compact = (h <= 1400)
        s = w / 1080.0
        
        vig = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        vdraw = ImageDraw.Draw(vig)
        top_h = int(280 if is_compact else 360)
        for y in range(top_h):
            a = int(220 * (1.0 - (y/float(top_h))**0.7))
            vdraw.line([(0, y), (w, y)], fill=(8, 10, 14, a))
        poster = Image.alpha_composite(base, vig)
        draw = ImageDraw.Draw(poster)
        
        max_title_w = int(960 * s)
        f_title, _ = fit_single_line_font(draw, meta["title"], "BebasNeue-Regular.ttf", max_title_w, int((115 if is_compact else 136) * s), min_size=int(55*s))
        f_badge = get_font("Rajdhani-Bold.ttf", int((22 if is_compact else 26) * s), "arialbd.ttf")
        f_tag = get_font("Rajdhani-Bold.ttf", int(24 * s), "arialbd.ttf")
        f_body = get_font("Rajdhani-SemiBold.ttf", int((20 if is_compact else 23) * s), "arial.ttf")
        f_wm = get_font("Rajdhani-Bold.ttf", int(22 * s), "arialbd.ttf")
        
        hy = int((38 if is_compact else 48) * s)
        max_badge_w = int(w * 0.46)
        f_badge_fit, _ = fit_single_line_font(draw, meta["protocol"], "Rajdhani-Bold.ttf", max_badge_w, int((22 if is_compact else 25) * s), min_size=int(14*s))
        draw.text((int(60*s), hy), meta["protocol"], fill=secondary, font=f_badge_fit)
        
        tx = int(60 * s)
        ty = int((75 if is_compact else 90) * s)
        for dx, dy in [(-3,0),(3,0),(0,-3),(0,3),(4,4)]:
            draw.text((tx+dx, ty+dy), meta["title"], fill=(0,0,0,230), font=f_title)
        draw.text((tx, ty), meta["title"], fill=(255,255,255,255), font=f_title)
        
        t_box = draw.textbbox((tx, ty), meta["title"], font=f_title)
        title_bottom = t_box[3]
        
        bar_y = title_bottom + int(12 * s)
        draw.line([(int(60*s), bar_y), (int(380*s), bar_y)], fill=primary, width=int(6*s))
        draw.line([(int(390*s), bar_y), (int(460*s), bar_y)], fill=gold, width=int(6*s))
        
        tagline_y = bar_y + int(12 * s)
        f_sub, _ = fit_single_line_font(draw, meta["tagline"], "Rajdhani-Bold.ttf", max_title_w, int((28 if is_compact else 34) * s), min_size=int(18*s))
        draw.text((int(60*s), tagline_y), meta["tagline"], fill=gold, font=f_sub)
        
        if is_compact:
            b1_y1, b1_y2 = int(480*s), int(670*s)
            b2_y1, b2_y2 = int(700*s), int(890*s)
            b3_y1, b3_y2 = int(920*s), int(1110*s)
            flaw_y = int(1135*s)
        else:
            b1_y1, b1_y2 = int(820*s), int(1040*s)
            b2_y1, b2_y2 = int(1120*s), int(1340*s)
            b3_y1, b3_y2 = int(1420*s), int(1640*s)
            flaw_y = int(1690*s)
            
        # Box 1 (Left)
        b1_x1, b1_x2 = int(50*s), int(520*s)
        b1_max_h = (b1_y2 - b1_y1) - int(56*s)
        draw.rounded_rectangle([b1_x1, b1_y1, b1_x2, b1_y2], radius=int(10*s), fill=(10, 14, 22, 225), outline=primary, width=2)
        draw.polygon([(b1_x1, b1_y1), (b1_x1+int(30*s), b1_y1), (b1_x1, b1_y1+int(30*s))], fill=primary)
        draw.text((b1_x1+int(36*s), b1_y1+int(16*s)), f"01 // {tips[0][1]}", fill=gold, font=f_tag)
        draw_wrapped_text(draw, tips[0][2], f_body, (215, 225, 240, 255), b1_x1+int(24*s), b1_y1+int(52*s), int(420*s), 1.25, max_height=b1_max_h)
        draw.line([(b1_x2, b1_y1+int(40*s)), (b1_x2+int(50*s), b1_y1+int(40*s)), (b1_x2+int(90*s), b1_y1+int(90*s))], fill=primary, width=2)
        draw.ellipse([b1_x2+int(86*s), b1_y1+int(86*s), b1_x2+int(94*s), b1_y1+int(94*s)], fill=primary)
        
        # Box 2 (Right)
        b2_x1, b2_x2 = int(560*s), int(1030*s)
        b2_max_h = (b2_y2 - b2_y1) - int(56*s)
        draw.rounded_rectangle([b2_x1, b2_y1, b2_x2, b2_y2], radius=int(10*s), fill=(10, 14, 22, 225), outline=secondary, width=2)
        draw.polygon([(b2_x2, b2_y1), (b2_x2-int(30*s), b2_y1), (b2_x2, b2_y1+int(30*s))], fill=secondary)
        draw.text((b2_x1+int(24*s), b2_y1+int(16*s)), f"02 // {tips[1][1]}", fill=gold, font=f_tag)
        draw_wrapped_text(draw, tips[1][2], f_body, (215, 225, 240, 255), b2_x1+int(24*s), b2_y1+int(52*s), int(420*s), 1.25, max_height=b2_max_h)
        draw.line([(b2_x1, b2_y1+int(40*s)), (b2_x1-int(50*s), b2_y1+int(40*s)), (b2_x1-int(90*s), b2_y1-int(20*s))], fill=secondary, width=2)
        draw.ellipse([b2_x1-int(94*s), b2_y1-int(24*s), b2_x1-int(86*s), b2_y1-int(16*s)], fill=secondary)
        
        # Box 3 (Left-bottom)
        b3_x1, b3_x2 = int(50*s), int(520*s)
        b3_max_h = (b3_y2 - b3_y1) - int(56*s)
        draw.rounded_rectangle([b3_x1, b3_y1, b3_x2, b3_y2], radius=int(10*s), fill=(10, 14, 22, 225), outline=primary, width=2)
        draw.polygon([(b3_x1, b3_y2), (b3_x1+int(30*s), b3_y2), (b3_x1, b3_y2-int(30*s))], fill=primary)
        draw.text((b3_x1+int(24*s), b3_y1+int(16*s)), f"03 // {tips[2][1]}", fill=gold, font=f_tag)
        draw_wrapped_text(draw, tips[2][2], f_body, (215, 225, 240, 255), b3_x1+int(24*s), b3_y1+int(52*s), int(420*s), 1.25, max_height=b3_max_h)
        
        # Flaw pod (Never overflows right screen edge)
        flaw_text = f"[ ! ] CRITICAL FLAW: {meta.get('caution', 'DROPPING REAR GUARD ON ROTATION')}"
        flaw_x = int(560*s)
        flaw_max_w = int(w - flaw_x - int(50*s))
        f_flaw, _ = fit_single_line_font(draw, flaw_text, "Rajdhani-Bold.ttf", flaw_max_w - int(36*s), int((19 if is_compact else 22) * s), min_size=int(13*s))
        flaw_box = draw.textbbox((0, 0), flaw_text, font=f_flaw)
        flaw_w = flaw_box[2] - flaw_box[0]
        actual_pod_w = min(flaw_max_w, flaw_w + int(36*s))
        draw.rounded_rectangle([flaw_x, flaw_y, flaw_x + actual_pod_w, flaw_y + int(46*s)], radius=int(6*s), fill=(28, 8, 12, 235), outline=(255, 45, 65, 200), width=1)
        draw.text((flaw_x + int(18*s), flaw_y + int(10*s)), flaw_text, fill=(255, 95, 110, 255), font=f_flaw)
        
        bbox_f = draw.textbbox((0, 0), meta["watermark"], font=f_wm)
        fw = bbox_f[2] - bbox_f[0]
        fx = (w - fw) // 2
        wy = h - int(55*s)
        draw.rounded_rectangle([fx-int(22*s), wy-int(10*s), fx+fw+int(22*s), wy+int(35*s)], radius=int(6*s), fill=(10, 14, 20, 210), outline=(primary[0], primary[1], primary[2], 140), width=1)
        draw.text((fx, wy), meta["watermark"], fill=(235, 245, 255, 255), font=f_wm)
        return poster

    # ----------------- 2. SIDE EDITORIAL COLUMN (ADAPTIVE 1350/1920) -----------------
    def _render_side_column(self, base, w, h, p, tips, meta):
        primary, secondary, gold = p["primary"], p["secondary"], p["gold"]
        is_compact = (h <= 1400)
        s = w / 1080.0
        
        col_w = int(510 * s)
        ribbon = Image.new("RGBA", (w, h), (0,0,0,0))
        rdraw = ImageDraw.Draw(ribbon)
        for x in range(col_w):
            a = int(240 * (1.0 - (x/float(col_w))**2.8))
            rdraw.line([(x, 0), (x, h)], fill=(8, 11, 18, a))
        poster = Image.alpha_composite(base, ribbon)
        draw = ImageDraw.Draw(poster)
        
        max_col_w = int(410 * s)
        hy = int((40 if is_compact else 55) * s)
        badge_str = f"{meta['protocol']} // {meta.get('range', 'MID-RANGE [1.2M]')}"
        f_badge, _ = fit_single_line_font(draw, badge_str, "Rajdhani-Bold.ttf", max_col_w, int((22 if is_compact else 24)*s), min_size=int(14*s))
        draw.text((int(50*s), hy), badge_str, fill=secondary, font=f_badge)
        
        ty = int((75 if is_compact else 95) * s)
        title_bottom, f_title, _ = draw_adaptive_title(draw, meta["title"], "BebasNeue-Regular.ttf", int(50*s), ty, max_w=max_col_w, target_size=int((96 if is_compact else 110)*s), min_size=int(38*s), max_lines=2)
        
        bar_y = title_bottom + int(12 * s)
        draw.line([(int(50*s), bar_y), (int(360*s), bar_y)], fill=primary, width=int(5*s))
        
        tagline_y = bar_y + int(10 * s)
        f_sub, _ = fit_single_line_font(draw, meta["tagline"], "Rajdhani-Bold.ttf", max_col_w, int((24 if is_compact else 28)*s), min_size=int(16*s))
        draw.text((int(50*s), tagline_y), meta["tagline"], fill=gold, font=f_sub)
        tag_bottom = tagline_y + int((f_sub.size if hasattr(f_sub, 'size') else 22) * 1.25)
        
        curr_y = max(int((265 if is_compact else 340) * s), tag_bottom + int(18*s))
        card_h = int((235 if is_compact else 320) * s)
        gap = int((14 if is_compact else 30) * s)
        
        f_tag = get_font("Rajdhani-Bold.ttf", int((22 if is_compact else 25) * s), "arialbd.ttf")
        f_body = get_font("Rajdhani-SemiBold.ttf", int((19 if is_compact else 22) * s), "arial.ttf")
        f_num = get_font("BebasNeue-Regular.ttf", int((56 if is_compact else 68) * s), "impact.ttf")
        f_wm = get_font("Rajdhani-Bold.ttf", int(22 * s), "arialbd.ttf")
        
        card_max_text_h = card_h - int(80 * s)
        for num, tag, desc in tips:
            draw.rounded_rectangle([int(45*s), curr_y, int(475*s), curr_y + card_h], radius=int(12*s), fill=(12, 16, 26, 225), outline=primary, width=2)
            draw.text((int(65*s), curr_y + int(14*s)), num, fill=primary, font=f_num)
            draw.text((int(135*s), curr_y + int(24*s)), tag, fill=gold, font=f_tag)
            draw_wrapped_text(draw, desc, f_body, (215, 225, 240, 255), int(65*s), curr_y + int(74*s), int(390*s), 1.25, max_height=card_max_text_h)
            curr_y += card_h + gap
            
        flaw_str = f"[ ! ] FLAW: {meta.get('caution', 'DROPPING HAND')}"
        f_flaw, _ = fit_single_line_font(draw, flaw_str, "Rajdhani-Bold.ttf", int(410*s), int((18 if is_compact else 21)*s), min_size=int(13*s))
        draw.rounded_rectangle([int(45*s), curr_y, int(475*s), curr_y + int(46*s)], radius=int(6*s), fill=(26, 8, 12, 230), outline=(255, 45, 65, 180), width=1)
        draw.text((int(65*s), curr_y + int(11*s)), flaw_str, fill=(255, 110, 125, 255), font=f_flaw)
        
        bbox_f = draw.textbbox((0, 0), meta["watermark"], font=f_wm)
        fw = bbox_f[2] - bbox_f[0]
        fx = w - fw - int(60*s)
        wy = h - int(55*s)
        draw.rounded_rectangle([fx-int(18*s), wy-int(10*s), fx+fw+int(18*s), wy+int(35*s)], radius=int(6*s), fill=(10, 14, 20, 210), outline=(primary[0], primary[1], primary[2], 140), width=1)
        draw.text((fx, wy), meta["watermark"], fill=(235, 245, 255, 255), font=f_wm)
        return poster

    # ----------------- 3. CYBERPUNK TARGET LOCK HUD (ADAPTIVE 1350/1920) -----------------
    def _render_reticle_hud(self, base, w, h, p, tips, meta):
        primary, secondary, gold = p["primary"], p["secondary"], p["gold"]
        is_compact = (h <= 1400)
        s = w / 1080.0
        
        vig = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        vdraw = ImageDraw.Draw(vig)
        top_h = int(270 if is_compact else 350)
        for y in range(top_h):
            a = int(220 * (1.0 - (y/float(top_h))**0.7))
            vdraw.line([(0, y), (w, y)], fill=(8, 10, 14, a))
        bot_start = int(h - (240 if is_compact else 370))
        for y in range(bot_start, h):
            a = int(230 * (((y-bot_start)/float(h-bot_start))**0.8))
            vdraw.line([(0, y), (w, y)], fill=(6, 8, 12, a))
        poster = Image.alpha_composite(base, vig)
        draw = ImageDraw.Draw(poster)
        
        max_title_w = int(960 * s)
        f_title, _ = fit_single_line_font(draw, meta["title"], "BebasNeue-Regular.ttf", max_title_w, int((115 if is_compact else 136) * s), min_size=int(55*s))
        f_badge = get_font("Rajdhani-Bold.ttf", int((22 if is_compact else 26) * s), "arialbd.ttf")
        f_tag = get_font("Rajdhani-Bold.ttf", int(24 * s), "arialbd.ttf")
        f_body = get_font("Rajdhani-SemiBold.ttf", int((20 if is_compact else 23) * s), "arial.ttf")
        f_wm = get_font("Rajdhani-Bold.ttf", int(22 * s), "arialbd.ttf")
        
        hy = int((38 if is_compact else 48) * s)
        max_badge_w = int(w * 0.46)
        f_badge_fit, _ = fit_single_line_font(draw, meta["protocol"], "Rajdhani-Bold.ttf", max_badge_w, int((22 if is_compact else 26) * s), min_size=int(14*s))
        draw.text((int(60*s), hy), meta["protocol"], fill=secondary, font=f_badge_fit)
        
        tx = int(60 * s)
        ty = int((75 if is_compact else 90) * s)
        for dx, dy in [(-3,0),(3,0),(0,-3),(0,3),(4,4)]:
            draw.text((tx+dx, ty+dy), meta["title"], fill=(0,0,0,230), font=f_title)
        draw.text((tx, ty), meta["title"], fill=(255,255,255,255), font=f_title)
        
        t_box = draw.textbbox((tx, ty), meta["title"], font=f_title)
        title_bottom = t_box[3]
        
        bar_y = title_bottom + int(12 * s)
        draw.line([(int(60*s), bar_y), (int(420*s), bar_y)], fill=primary, width=int(6*s))
        
        tagline_y = bar_y + int(12 * s)
        f_sub, _ = fit_single_line_font(draw, meta["tagline"], "Rajdhani-Bold.ttf", max_title_w, int((28 if is_compact else 34) * s), min_size=int(18*s))
        draw.text((int(60*s), tagline_y), meta["tagline"], fill=gold, font=f_sub)
        
        cx = int(540*s)
        cy = int(410*s if is_compact else 730*s)
        rad = int(75*s if is_compact else 90*s)
        draw.arc([cx-rad, cy-rad, cx+rad, cy+rad], start=0, end=360, fill=primary, width=2)
        draw.arc([cx-int(rad*0.67), cy-int(rad*0.67), cx+int(rad*0.67), cy+int(rad*0.67)], start=45, end=135, fill=secondary, width=3)
        draw.arc([cx-int(rad*0.67), cy-int(rad*0.67), cx+int(rad*0.67), cy+int(rad*0.67)], start=225, end=315, fill=secondary, width=3)
        draw.line([(cx-rad-int(20*s), cy), (cx-rad+int(20*s), cy)], fill=primary, width=2)
        draw.line([(cx+rad-int(20*s), cy), (cx+rad+int(20*s), cy)], fill=primary, width=2)
        draw.line([(cx, cy-rad-int(20*s)), (cx, cy-rad+int(20*s))], fill=primary, width=2)
        draw.line([(cx, cy+rad-int(20*s)), (cx, cy+rad+int(20*s))], fill=primary, width=2)
        
        target_str = f"[ LOCK: {meta['target']} ]"
        f_target_lbl, _ = fit_single_line_font(draw, target_str, "Rajdhani-Bold.ttf", int(360*s), int((18 if is_compact else 20)*s), min_size=int(13*s))
        tb = draw.textbbox((0, 0), target_str, font=f_target_lbl)
        tw = tb[2] - tb[0]
        draw.text((cx - tw//2, cy-rad-int(48*s)), target_str, fill=gold, font=f_target_lbl)
        
        flaw_hud_str = f"[ ! ] FLAW: {meta.get('caution', 'OVER-EXTENSION')}"
        f_flaw_lbl, _ = fit_single_line_font(draw, flaw_hud_str, "Rajdhani-Bold.ttf", int(400*s), int((17 if is_compact else 19)*s), min_size=int(12*s))
        fb = draw.textbbox((0, 0), flaw_hud_str, font=f_flaw_lbl)
        fw_hud = fb[2] - fb[0]
        hud_box_y = cy + rad + int(30*s)
        draw.rounded_rectangle([cx - fw_hud//2 - int(10*s), hud_box_y, cx + fw_hud//2 + int(10*s), hud_box_y + int(34*s)], radius=int(4*s), fill=(24, 6, 10, 220), outline=(255, 45, 65, 180), width=1)
        draw.text((cx - fw_hud//2, hud_box_y + int(6*s)), flaw_hud_str, fill=(255, 95, 110, 255), font=f_flaw_lbl)
        
        if is_compact:
            p1_y1, p1_y2 = int(550*s), int(730*s)
            p2_y1, p2_y2 = int(760*s), int(940*s)
            p3_y1, p3_y2 = int(970*s), int(1150*s)
        else:
            p1_y1, p1_y2 = int(980*s), int(1220*s)
            p2_y1, p2_y2 = int(1260*s), int(1500*s)
            p3_y1, p3_y2 = int(1540*s), int(1760*s)
            
        p1_max_h = (p1_y2 - p1_y1) - int(54*s)
        draw.polygon([(int(50*s), p1_y1), (int(490*s), p1_y1), (int(520*s), p1_y1+int(30*s)), (int(520*s), p1_y2), (int(50*s), p1_y2)], fill=(10, 14, 22, 225), outline=primary)
        draw.text((int(70*s), p1_y1+int(14*s)), f"01 // {tips[0][1]}", fill=gold, font=f_tag)
        draw_wrapped_text(draw, tips[0][2], f_body, (215, 225, 240, 255), int(70*s), p1_y1+int(50*s), int(420*s), 1.25, max_height=p1_max_h)
        
        p2_max_h = (p2_y2 - p2_y1) - int(54*s)
        draw.polygon([(int(560*s), p2_y1), (int(1030*s), p2_y1), (int(1030*s), p2_y2), (int(590*s), p2_y2), (int(560*s), p2_y2-int(30*s))], fill=(10, 14, 22, 225), outline=secondary)
        draw.text((int(590*s), p2_y1+int(14*s)), f"02 // {tips[1][1]}", fill=gold, font=f_tag)
        draw_wrapped_text(draw, tips[1][2], f_body, (215, 225, 240, 255), int(590*s), p2_y1+int(50*s), int(420*s), 1.25, max_height=p2_max_h)
        
        p3_max_h = (p3_y2 - p3_y1) - int(54*s)
        draw.polygon([(int(50*s), p3_y1), (int(1030*s), p3_y1), (int(1030*s), p3_y2), (int(50*s), p3_y2)], fill=(10, 14, 22, 225), outline=primary)
        draw.text((int(70*s), p3_y1+int(14*s)), f"03 // {tips[2][1]}", fill=gold, font=f_tag)
        draw_wrapped_text(draw, tips[2][2], f_body, (215, 225, 240, 255), int(70*s), p3_y1+int(50*s), int(930*s), 1.25, max_height=p3_max_h)
        
        bbox_f = draw.textbbox((0, 0), meta["watermark"], font=f_wm)
        fw = bbox_f[2] - bbox_f[0]
        fx = (w - fw) // 2
        wy = h - int(55*s)
        draw.rounded_rectangle([fx-int(22*s), wy-int(10*s), fx+fw+int(22*s), wy+int(35*s)], radius=int(6*s), fill=(10, 14, 20, 210), outline=primary, width=1)
        draw.text((fx, wy), meta["watermark"], fill=(235, 245, 255, 255), font=f_wm)
        return poster

    # ----------------- 4. CLASSIC BOTTOM CARD (APEX COMBAT CONSOLE) -----------------
    def _render_classic_bottom(self, base, w, h, p, tips, meta):
        primary, secondary, gold = p["primary"], p["secondary"], p["gold"]
        is_compact = (h <= 1400)
        s = w / 1080.0
        
        # Smooth Vignette keeping the upper 55-60% of fighter artwork completely clear
        vignette = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        vig_draw = ImageDraw.Draw(vignette)
        top_h = int(h * (0.20 if is_compact else 0.25))
        for y_pos in range(top_h):
            ratio = y_pos / float(top_h)
            alpha = int(220 * (1.0 - ratio**0.6))
            vig_draw.line([(0, y_pos), (w, y_pos)], fill=(8, 10, 15, alpha))
            
        bottom_start = int(h * (0.50 if is_compact else 0.55))
        bottom_h = h - bottom_start
        for y_pos in range(bottom_start, h):
            ratio = (y_pos - bottom_start) / float(bottom_h)
            alpha = int(245 * (ratio**0.75))
            vig_draw.line([(0, y_pos), (w, y_pos)], fill=(6, 8, 12, alpha))
            
        poster = Image.alpha_composite(base, vignette)
        draw = ImageDraw.Draw(poster)
        
        # Header Typography
        max_title_w = int(960 * s)
        f_title, _ = fit_single_line_font(draw, meta["title"], "BebasNeue-Regular.ttf", max_title_w, int((115 if is_compact else 138) * s), min_size=int(55*s))
        f_sub, _ = fit_single_line_font(draw, meta["tagline"], "Rajdhani-Bold.ttf", max_title_w, int((28 if is_compact else 34) * s), min_size=int(18*s))
        f_card_head = get_font("Rajdhani-Bold.ttf", int((23 if is_compact else 26) * s), "arialbd.ttf")
        f_target_pill = get_font("Rajdhani-Bold.ttf", int((18 if is_compact else 20) * s), "arialbd.ttf")
        f_tip_num = get_font("Rajdhani-Bold.ttf", int((20 if is_compact else 22) * s), "arialbd.ttf")
        f_tip_tag = get_font("Rajdhani-Bold.ttf", int((22 if is_compact else 24) * s), "arialbd.ttf")
        f_tip_body = get_font("Rajdhani-SemiBold.ttf", int((19 if is_compact else 22) * s), "arial.ttf")
        f_wm = get_font("Rajdhani-Bold.ttf", int(22 * s), "arialbd.ttf")
        
        # 1. Top Header: Only protocol pill clamped to left side (leaves top-right 100% free for CTA!)
        hy = int((36 if is_compact else 46) * s)
        max_badge_w = int(w * 0.46)
        f_badge_fit, _ = fit_single_line_font(draw, meta["protocol"], "Rajdhani-Bold.ttf", max_badge_w, int((22 if is_compact else 25) * s), min_size=int(14*s))
        draw.text((int(50*s), hy), meta["protocol"], fill=secondary, font=f_badge_fit)
        
        # 2. Main Title with deep 3D shadow
        tx, ty = int(50 * s), int((72 if is_compact else 90) * s)
        for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3), (4, 4)]:
            draw.text((tx + dx, ty + dy), meta["title"], fill=(0, 0, 0, 230), font=f_title)
        draw.text((tx, ty), meta["title"], fill=(255, 255, 255, 255), font=f_title)
        
        t_box = draw.textbbox((tx, ty), meta["title"], font=f_title)
        title_bottom = t_box[3]
        
        # 3. Triple Neon Accent Bar
        bar_y = title_bottom + int(10 * s)
        draw.line([(int(50*s), bar_y), (int(340*s), bar_y)], fill=primary, width=int(6 * s))
        draw.line([(int(350*s), bar_y), (int(440*s), bar_y)], fill=gold, width=int(6 * s))
        draw.line([(int(450*s), bar_y), (int(510*s), bar_y)], fill=secondary, width=int(6 * s))
        
        # 4. Tagline
        tagline_y = bar_y + int(10 * s)
        draw.text((int(50*s), tagline_y), meta["tagline"], fill=gold, font=f_sub)
        
        # 5. Apex Combat Console (Compact, Snug & Ergonomic Geometry)
        card_x1 = int(45 * s)
        card_x2 = w - int(45 * s)
        card_w = card_x2 - card_x1
        
        tile_w = card_w - int(40 * s)
        tile_x = card_x1 + int(20 * s)
        tile_h = int((74 if is_compact else 95) * s)
        tile_gap = int((8 if is_compact else 12) * s)
        telem_h = int((26 if is_compact else 30) * s)
        flaw_h = int((28 if is_compact else 32) * s)
        head_h = int((32 if is_compact else 36) * s)
        
        inner_content_h = head_h + int(12 * s) + (tile_h * 3 + tile_gap * 2) + int(8 * s) + telem_h + int(8 * s) + flaw_h + int(16 * s)
        card_y2 = h - int((65 if is_compact else 80) * s)
        card_y1 = card_y2 - inner_content_h
        
        chamfer = int(28 * s)
        console_poly = [
            (card_x1, card_y1),
            (card_x2 - chamfer, card_y1),
            (card_x2, card_y1 + chamfer),
            (card_x2, card_y2),
            (card_x1 + chamfer, card_y2),
            (card_x1, card_y2 - chamfer)
        ]
        # High-tech frosted glass fill with neon tech border
        draw.polygon(console_poly, fill=(10, 14, 22, 215), outline=(primary[0], primary[1], primary[2], 210))
        
        # Corner brackets [+]
        blen = int(22 * s)
        bwidth = max(2, int(3 * s))
        draw.line([(card_x1, card_y1), (card_x1 + blen, card_y1)], fill=primary, width=bwidth)
        draw.line([(card_x1, card_y1), (card_x1, card_y1 + blen)], fill=primary, width=bwidth)
        draw.line([(card_x2, card_y1 + chamfer), (card_x2, card_y1 + chamfer + blen)], fill=secondary, width=bwidth)
        draw.line([(card_x2, card_y2), (card_x2 - blen, card_y2)], fill=primary, width=bwidth)
        draw.line([(card_x2, card_y2), (card_x2, card_y2 - blen)], fill=primary, width=bwidth)
        draw.line([(card_x1, card_y2 - chamfer), (card_x1, card_y2 - chamfer - blen)], fill=secondary, width=bwidth)
        
        # 6. Console Header
        head_y = card_y1 + int(14 * s)
        head_tag = meta.get("card_title", "/// COMBAT ANALYSIS").upper()
        draw.text((card_x1 + int(24 * s), head_y), head_tag, fill=(255, 255, 255, 255), font=f_card_head)
        
        # Right Target Pill [ [+] TARGET: LIVER / RIBS ]
        target_str = f"[+] TARGET: {meta.get('target', 'CENTRAL MASS')}"
        t_box = draw.textbbox((0, 0), target_str, font=f_target_pill)
        tw = t_box[2] - t_box[0]
        th = t_box[3] - t_box[1]
        tp_w = tw + int(20 * s)
        tp_h = th + int(10 * s)
        tp_x = card_x2 - tp_w - int(20 * s)
        tp_y = head_y - int(1 * s)
        draw.rounded_rectangle([tp_x, tp_y, tp_x + tp_w, tp_y + tp_h], radius=int(5*s), fill=(18, 26, 38, 230), outline=(gold[0], gold[1], gold[2], 180), width=1)
        draw.text((tp_x + int(10 * s), tp_y + int(4 * s)), target_str, fill=gold, font=f_target_pill)
        
        # Header separator line
        sep_y = head_y + int((30 if is_compact else 34) * s)
        draw.line([(card_x1 + int(20 * s), sep_y), (card_x2 - int(20 * s), sep_y)], fill=(255, 255, 255, 35), width=1)
        
        # 7. Three Modular Glass Keypoint Tiles
        curr_tile_y = sep_y + int(10 * s)
        
        for num, tag, desc in tips:
            # Modular tile background
            draw.rounded_rectangle(
                [tile_x, curr_tile_y, tile_x + tile_w, curr_tile_y + tile_h],
                radius=int(6 * s),
                fill=(16, 22, 34, 195),
                outline=(primary[0], primary[1], primary[2], 75),
                width=1
            )
            # Left neon indicator bar
            draw.rounded_rectangle(
                [tile_x, curr_tile_y, tile_x + int(5 * s), curr_tile_y + tile_h],
                radius=int(3 * s),
                fill=primary
            )
            # Step Badge [ 01 ]
            badge_poly = [
                (tile_x + int(14 * s), curr_tile_y + int(8 * s)),
                (tile_x + int(56 * s), curr_tile_y + int(8 * s)),
                (tile_x + int(60 * s), curr_tile_y + int(32 * s)),
                (tile_x + int(18 * s), curr_tile_y + int(32 * s))
            ]
            draw.polygon(badge_poly, fill=primary)
            draw.text((tile_x + int(24 * s), curr_tile_y + int(10 * s)), num, fill=(0, 0, 0, 255), font=f_tip_num)
            
            # Tag Title
            draw.text((tile_x + int(72 * s), curr_tile_y + int(8 * s)), tag.upper(), fill=gold, font=f_tip_tag)
            
            # Description text (auto-wrapped and snug)
            draw_wrapped_text(
                draw, desc, f_tip_body, (220, 230, 245, 255),
                tile_x + int(72 * s), curr_tile_y + int(32 * s),
                tile_w - int(84 * s), 1.22,
                max_height=tile_h - int(36 * s)
            )
            curr_tile_y += tile_h + tile_gap
            
        # 8. Tactical Telemetry Strip (Rich combat metrics)
        telem_y = curr_tile_y + int(2 * s)
        range_val = meta.get("range", "INFIGHTING [0.5M]")
        telem_str = f"LETHALITY: [ 88% // HIGH ]   //   RANGE: {range_val}   //   RECOVERY: [ 0.18S OPTIMAL ]"
        f_telem, _ = fit_single_line_font(draw, telem_str, "Rajdhani-Bold.ttf", tile_w - int(10*s), int((16 if is_compact else 18) * s), min_size=int(11*s))
        draw.rounded_rectangle(
            [tile_x, telem_y, tile_x + tile_w, telem_y + int((26 if is_compact else 30) * s)],
            radius=int(4 * s),
            fill=(8, 12, 18, 230),
            outline=(secondary[0], secondary[1], secondary[2], 120),
            width=1
        )
        draw.text((tile_x + int(14 * s), telem_y + int(4 * s)), telem_str, fill=secondary, font=f_telem)
        
        # 9. Critical Flaw / Vulnerability Alert Bar
        flaw_y = telem_y + int((30 if is_compact else 36) * s)
        flaw_str = f"[ ! ] CRITICAL VULNERABILITY: {meta.get('caution', 'DROPPING REAR GUARD ON ROTATION')}"
        f_flaw, _ = fit_single_line_font(draw, flaw_str, "Rajdhani-Bold.ttf", tile_w - int(24*s), int((17 if is_compact else 20) * s), min_size=int(12*s))
        draw.rounded_rectangle(
            [tile_x, flaw_y, tile_x + tile_w, flaw_y + int((28 if is_compact else 32) * s)],
            radius=int(4 * s),
            fill=(28, 8, 12, 240),
            outline=(255, 45, 65, 230),
            width=1
        )
        draw.text((tile_x + int(14 * s), flaw_y + int(5 * s)), flaw_str, fill=(255, 95, 110, 255), font=f_flaw)
        
        # 10. Watermark Pill Centered at Bottom
        bbox_f = draw.textbbox((0, 0), meta["watermark"], font=f_wm)
        fw = bbox_f[2] - bbox_f[0]
        fx = (w - fw) // 2
        wy = h - int(45 * s)
        draw.rounded_rectangle([fx - int(22*s), wy - int(10*s), fx + fw + int(22*s), wy + int(35*s)], radius=int(6*s), fill=(10, 14, 20, 220), outline=(primary[0], primary[1], primary[2], 150), width=1)
        draw.text((fx, wy), meta["watermark"], fill=(235, 245, 255, 255), font=f_wm)
        return poster

    # ----------------- 5. DUAL-WING SYMMETRICAL FRAME (NEW) -----------------
    def _render_dual_wing(self, base, w, h, p, tips, meta):
        primary, secondary, gold = p["primary"], p["secondary"], p["gold"]
        is_compact = (h <= 1400)
        s = w / 1080.0
        
        vig = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        vdraw = ImageDraw.Draw(vig)
        lw = int(480 * s)
        rw = int(540 * s)
        for x in range(lw):
            a = int(235 * (1.0 - (x/float(lw))**2.5))
            vdraw.line([(x, 0), (x, h)], fill=(8, 10, 16, a))
        for x in range(w - rw, w):
            ratio = (x - (w - rw)) / float(rw)
            a = int(240 * (ratio**2.5))
            vdraw.line([(x, 0), (x, h)], fill=(8, 10, 16, a))
        poster = Image.alpha_composite(base, vig)
        draw = ImageDraw.Draw(poster)
        
        f_badge = get_font("Rajdhani-Bold.ttf", int((22 if is_compact else 25) * s), "arialbd.ttf")
        f_tag = get_font("Rajdhani-Bold.ttf", int(23 * s), "arialbd.ttf")
        f_body = get_font("Rajdhani-SemiBold.ttf", int((19 if is_compact else 22) * s), "arial.ttf")
        f_wm = get_font("Rajdhani-Bold.ttf", int(22 * s), "arialbd.ttf")
        
        # Left Wing
        lx = int(50 * s)
        ly = int(50 * s)
        max_left_w = int(390 * s)
        
        draw.text((lx, ly), meta["protocol"], fill=secondary, font=f_badge)
        ty = ly + int(32 * s)
        title_bottom, f_title, _ = draw_adaptive_title(draw, meta["title"], "BebasNeue-Regular.ttf", lx, ty, max_w=max_left_w, target_size=int((96 if is_compact else 108)*s), min_size=int(38*s), max_lines=2)
        
        bar_y = title_bottom + int(10 * s)
        draw.line([(lx, bar_y), (lx + int(280*s), bar_y)], fill=primary, width=int(5*s))
        
        tagline_y = bar_y + int(10 * s)
        f_sub, _ = fit_single_line_font(draw, meta["tagline"], "Rajdhani-Bold.ttf", max_left_w, int((24 if is_compact else 28)*s), min_size=int(16*s))
        draw.text((lx, tagline_y), meta["tagline"], fill=gold, font=f_sub)
        tag_bottom = tagline_y + int((f_sub.size if hasattr(f_sub, 'size') else 22) * 1.25)
        
        t_y = tag_bottom + int((20 if is_compact else 35) * s)
        draw.rounded_rectangle([lx, t_y, lx + int(370*s), t_y + int(125*s)], radius=int(8*s), fill=(12, 16, 26, 215), outline=p["border"], width=1)
        draw.text((lx + int(20*s), t_y + int(16*s)), "TARGET ANATOMY:", fill=primary, font=f_badge)
        draw.text((lx + int(20*s), t_y + int(44*s)), meta["target"], fill=(255,255,255,255), font=f_body)
        draw.text((lx + int(20*s), t_y + int(78*s)), f"RANGE: {meta.get('range', 'INFIGHTING [0.5M]')}", fill=gold, font=f_badge)
        
        draw.line([(lx, t_y - 12), (lx + int(30*s), t_y - 12)], fill=primary, width=2)
        draw.line([(lx, t_y - 12), (lx, t_y + int(18*s))], fill=primary, width=2)
        
        # Right Wing
        rx1 = w - int(510 * s)
        rx2 = w - int(45 * s)
        rw_box = rx2 - rx1
        
        if is_compact:
            ry = int(140 * s)
            r_card_h = int(220 * s)
            r_gap = int(16 * s)
        else:
            ry = int(220 * s)
            r_card_h = int(290 * s)
            r_gap = int(32 * s)
            
        r_max_text_h = r_card_h - int(54 * s)
        for num, tag, desc in tips:
            draw.polygon([
                (rx1 + int(25*s), ry),
                (rx2, ry),
                (rx2, ry + r_card_h),
                (rx1, ry + r_card_h),
                (rx1, ry + int(25*s))
            ], fill=(12, 16, 24, 225), outline=primary)
            draw.text((rx1 + int(20*s), ry + int(12*s)), f"{num} // {tag}", fill=gold, font=f_tag)
            draw_wrapped_text(draw, desc, f_body, (215, 225, 240, 255), rx1 + int(20*s), ry + int(46*s), rw_box - int(38*s), 1.25, max_height=r_max_text_h)
            ry += r_card_h + r_gap
            
        flaw_h = int(58 * s)
        draw.rounded_rectangle([rx1, ry, rx2, ry + flaw_h], radius=int(6*s), fill=(28, 8, 12, 235), outline=(255, 45, 65, 200), width=1)
        f_flaw_lbl = get_font("Rajdhani-Bold.ttf", int((17 if is_compact else 20) * s), "arialbd.ttf")
        draw.text((rx1 + int(16*s), ry + int(8*s)), "[ ! ] CRITICAL FLAW:", fill=(255, 80, 95, 255), font=f_flaw_lbl)
        
        caution_text = meta.get('caution', 'DROPPING REAR GUARD ON ROTATION')
        f_flaw_body, _ = fit_single_line_font(draw, caution_text, "Rajdhani-Bold.ttf", rw_box - int(32*s), int((17 if is_compact else 20) * s), min_size=int(12*s))
        draw.text((rx1 + int(16*s), ry + int(30*s)), caution_text, fill=(255, 200, 205, 255), font=f_flaw_body)
        
        bbox_f = draw.textbbox((0, 0), meta["watermark"], font=f_wm)
        fw = bbox_f[2] - bbox_f[0]
        fx = (w - fw) // 2
        wy = h - int(55*s)
        draw.rounded_rectangle([fx-int(22*s), wy-int(10*s), fx+fw+int(22*s), wy+int(35*s)], radius=int(6*s), fill=(10, 14, 20, 210), outline=primary, width=1)
        draw.text((fx, wy), meta["watermark"], fill=(235, 245, 255, 255), font=f_wm)
        return poster

    # ----------------- 6. DIAGONAL KINETIC SLASH (NEW) -----------------
    def _render_diagonal_slash(self, base, w, h, p, tips, meta):
        primary, secondary, gold = p["primary"], p["secondary"], p["gold"]
        is_compact = (h <= 1400)
        s = w / 1080.0
        
        vig = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        vdraw = ImageDraw.Draw(vig)
        top_h = int(320 if is_compact else 400)
        for y in range(top_h):
            a = int(225 * (1.0 - (y/float(top_h))**0.75))
            vdraw.line([(0, y), (w, y)], fill=(8, 10, 16, a))
        bot_h = int(580 if is_compact else 720)
        for y in range(h - bot_h, h):
            ratio = (y - (h - bot_h)) / float(bot_h)
            a = int(245 * (ratio**0.8))
            vdraw.line([(0, y), (w, y)], fill=(6, 8, 14, a))
        poster = Image.alpha_composite(base, vig)
        draw = ImageDraw.Draw(poster)
        
        max_title_w = int(960 * s)
        f_title, _ = fit_single_line_font(draw, meta["title"], "BebasNeue-Regular.ttf", max_title_w, int((118 if is_compact else 138) * s), min_size=int(55*s))
        f_badge = get_font("Rajdhani-Bold.ttf", int((22 if is_compact else 25) * s), "arialbd.ttf")
        f_tag = get_font("Rajdhani-Bold.ttf", int(24 * s), "arialbd.ttf")
        f_body = get_font("Rajdhani-SemiBold.ttf", int((20 if is_compact else 23) * s), "arial.ttf")
        f_wm = get_font("Rajdhani-Bold.ttf", int(22 * s), "arialbd.ttf")
        
        hy = int((38 if is_compact else 50) * s)
        draw.text((int(60*s), hy), f"{meta['protocol']}  >>>  {meta.get('range', 'INFIGHTING [0.5M]')}", fill=secondary, font=f_badge)
        
        ty = int((70 if is_compact else 88) * s)
        tx = int(60 * s)
        for dx, dy in [(-3,0),(3,0),(0,-3),(0,3),(4,4)]:
            draw.text((tx+dx, ty+dy), meta["title"], fill=(0,0,0,230), font=f_title)
        draw.text((tx, ty), meta["title"], fill=(255,255,255,255), font=f_title)
        
        t_box = draw.textbbox((tx, ty), meta["title"], font=f_title)
        title_bottom = t_box[3]
        
        tagline_y = title_bottom + int(14 * s)
        f_sub, _ = fit_single_line_font(draw, meta["tagline"], "Rajdhani-Bold.ttf", max_title_w, int((26 if is_compact else 32) * s), min_size=int(18*s))
        draw.text((tx, tagline_y), meta["tagline"], fill=gold, font=f_sub)
        
        slash_y = tagline_y + int((f_sub.size if hasattr(f_sub, 'size') else 26) * 1.25) + int(24 * s)
        draw.line([(0, slash_y + int(45*s)), (w, slash_y - int(35*s))], fill=(primary[0], primary[1], primary[2], 90), width=int(4*s))
        draw.line([(0, slash_y + int(60*s)), (w, slash_y - int(20*s))], fill=(gold[0], gold[1], gold[2], 70), width=int(2*s))
        
        if is_compact:
            curr_y = int(580 * s)
            card_h = int(145 * s)
            gap = int(18 * s)
            skew = int(24 * s)
        else:
            curr_y = int(980 * s)
            card_h = int(185 * s)
            gap = int(30 * s)
            skew = int(36 * s)
            
        x_start = int(54 * s)
        card_w = w - int(108 * s)
        card_max_text_h = card_h - int(52 * s)
        
        for num, tag, desc in tips:
            poly = [
                (x_start + skew, curr_y),
                (x_start + card_w, curr_y),
                (x_start + card_w - skew, curr_y + card_h),
                (x_start, curr_y + card_h)
            ]
            draw.polygon(poly, fill=(10, 14, 22, 225), outline=p["border"])
            draw.polygon([
                (x_start + skew, curr_y),
                (x_start + skew + int(12*s), curr_y),
                (x_start + int(12*s), curr_y + card_h),
                (x_start, curr_y + card_h)
            ], fill=primary)
            
            draw.text((x_start + skew + int(24*s), curr_y + int(12*s)), f"/// {num} : {tag}", fill=gold, font=f_tag)
            draw_wrapped_text(draw, desc, f_body, (215, 225, 240, 255), x_start + skew + int(24*s), curr_y + int(46*s), card_w - skew*2 - int(40*s), 1.25, max_height=card_max_text_h)
            curr_y += card_h + gap
            
        flaw_y = curr_y + int(5*s)
        flaw_poly = [
            (x_start + skew, flaw_y),
            (x_start + card_w, flaw_y),
            (x_start + card_w - skew, flaw_y + int(48*s)),
            (x_start, flaw_y + int(48*s))
        ]
        draw.polygon(flaw_poly, fill=(28, 8, 12, 235), outline=(255, 45, 65, 200))
        flaw_str = f"[ ! ] CRITICAL FLAW // {meta.get('caution', 'DROPPING REAR GUARD')}"
        f_flaw, _ = fit_single_line_font(draw, flaw_str, "Rajdhani-Bold.ttf", card_w - skew*2 - int(48*s), int((20 if is_compact else 23) * s), min_size=int(14*s))
        draw.text((x_start + skew + int(24*s), flaw_y + int(12*s)), flaw_str, fill=(255, 95, 110, 255), font=f_flaw)
        
        bbox_f = draw.textbbox((0, 0), meta["watermark"], font=f_wm)
        fw = bbox_f[2] - bbox_f[0]
        fx = (w - fw) // 2
        wy = h - int(50*s)
        draw.rounded_rectangle([fx-int(22*s), wy-int(10*s), fx+fw+int(22*s), wy+int(35*s)], radius=int(6*s), fill=(10, 14, 20, 210), outline=primary, width=1)
        draw.text((fx, wy), meta["watermark"], fill=(235, 245, 255, 255), font=f_wm)
        return poster

    # ----------------- 7. TACTICAL BLUEPRINT DOSSIER (NEW) -----------------
    def _render_blueprint_dossier(self, base, w, h, p, tips, meta):
        primary, secondary, gold = p["primary"], p["secondary"], p["gold"]
        is_compact = (h <= 1400)
        s = w / 1080.0
        
        vig = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        vdraw = ImageDraw.Draw(vig)
        top_h = int(240 if is_compact else 320)
        for y in range(top_h):
            a = int(230 * (1.0 - (y/float(top_h))**0.6))
            vdraw.line([(0, y), (w, y)], fill=(6, 10, 18, a))
        bot_h = int(580 if is_compact else 720)
        for y in range(h - bot_h, h):
            ratio = (y - (h - bot_h)) / float(bot_h)
            a = int(245 * (ratio**0.7))
            vdraw.line([(0, y), (w, y)], fill=(5, 8, 14, a))
        poster = Image.alpha_composite(base, vig)
        draw = ImageDraw.Draw(poster)
        
        max_title_w = int(960 * s)
        f_title, _ = fit_single_line_font(draw, meta["title"], "BebasNeue-Regular.ttf", max_title_w, int((105 if is_compact else 125) * s), min_size=int(52*s))
        f_badge = get_font("Rajdhani-Bold.ttf", int((20 if is_compact else 24) * s), "arialbd.ttf")
        f_tag = get_font("Rajdhani-Bold.ttf", int(22 * s), "arialbd.ttf")
        f_body = get_font("Rajdhani-SemiBold.ttf", int((19 if is_compact else 22) * s), "arial.ttf")
        f_ruler = get_font("Rajdhani-Bold.ttf", int(14 * s), "arial.ttf")
        f_wm = get_font("Rajdhani-Bold.ttf", int(22 * s), "arialbd.ttf")
        
        draw.line([(int(40*s), int(35*s)), (w - int(40*s), int(35*s))], fill=(primary[0], primary[1], primary[2], 120), width=1)
        
        zone_text = f"ZONE: {meta['target']}"
        f_zone, _ = fit_single_line_font(draw, zone_text, "Rajdhani-Bold.ttf", int(360*s), int((18 if is_compact else 22)*s), min_size=int(12*s))
        zb = draw.textbbox((0, 0), zone_text, font=f_zone)
        zw = zb[2] - zb[0]
        zone_x = w - int(45*s) - zw
        draw.text((zone_x, int(15*s)), zone_text, fill=gold, font=f_zone)
        
        dossier_text = f"COMBAT DOSSIER // SYS_ANALYSIS // {meta['protocol']}"
        max_dossier_w = zone_x - int(65*s)
        f_badge, _ = fit_single_line_font(draw, dossier_text, "Rajdhani-Bold.ttf", max_dossier_w, int((20 if is_compact else 24)*s), min_size=int(13*s))
        draw.text((int(45*s), int(15*s)), dossier_text, fill=secondary, font=f_badge)
        
        for i in range(12):
            ry = int((120 + i * 80) * s)
            draw.line([(int(25*s), ry), (int(38*s), ry)], fill=(255, 255, 255, 120), width=1)
            if i % 2 == 0:
                draw.text((int(10*s), ry - int(8*s)), f"{i:02d}", fill=(200, 220, 250, 140), font=f_ruler)
                
        ty = int((55 if is_compact else 75) * s)
        tx = int(50 * s)
        for dx, dy in [(-3,0),(3,0),(0,-3),(0,3),(4,4)]:
            draw.text((tx+dx, ty+dy), meta["title"], fill=(0,0,0,230), font=f_title)
        draw.text((tx, ty), meta["title"], fill=(255,255,255,255), font=f_title)
        
        t_box = draw.textbbox((tx, ty), meta["title"], font=f_title)
        title_bottom = t_box[3]
        
        tagline_y = title_bottom + int(12 * s)
        tag_full = f"{meta['tagline']}  //  RANGE: {meta.get('range', 'INFIGHTING [0.5M]')}"
        f_sub, _ = fit_single_line_font(draw, tag_full, "Rajdhani-Bold.ttf", max_title_w, int((26 if is_compact else 30) * s), min_size=int(16*s))
        draw.text((tx, tagline_y), tag_full, fill=gold, font=f_sub)
        
        if is_compact:
            curr_y = int(580 * s)
            card_h = int(140 * s)
            gap = int(16 * s)
        else:
            curr_y = int(980 * s)
            card_h = int(185 * s)
            gap = int(28 * s)
            
        card_x1 = int(50 * s)
        card_x2 = w - int(50 * s)
        card_w = card_x2 - card_x1
        card_max_text_h = card_h - int(48 * s)
        
        for num, tag, desc in tips:
            draw.rectangle([card_x1, curr_y, card_x2, curr_y + card_h], fill=(8, 12, 20, 225), outline=p["border"], width=1)
            draw.line([(card_x1, curr_y), (card_x1 + int(15*s), curr_y)], fill=primary, width=2)
            draw.line([(card_x1, curr_y), (card_x1, curr_y + int(15*s))], fill=primary, width=2)
            draw.line([(card_x2, curr_y), (card_x2 - int(15*s), curr_y)], fill=primary, width=2)
            draw.line([(card_x2, curr_y), (card_x2, curr_y + int(15*s))], fill=primary, width=2)
            
            draw.text((card_x1 + int(24*s), curr_y + int(10*s)), f"[ MODULE_{num} // {tag} ]", fill=gold, font=f_tag)
            draw_wrapped_text(draw, desc, f_body, (215, 225, 240, 255), card_x1 + int(24*s), curr_y + int(42*s), card_w - int(48*s), 1.25, max_height=card_max_text_h)
            curr_y += card_h + gap
            
        flaw_y = curr_y + int(4*s)
        draw.rectangle([card_x1, flaw_y, card_x2, flaw_y + int(48*s)], fill=(24, 8, 12, 235), outline=(255, 45, 65, 200), width=1)
        flaw_str = f"[ ! ] SYSTEM VULNERABILITY / FLAW: {meta.get('caution', 'DROPPING REAR GUARD ON ROTATION')}"
        f_flaw, _ = fit_single_line_font(draw, flaw_str, "Rajdhani-Bold.ttf", card_w - int(48*s), int((19 if is_compact else 22) * s), min_size=int(13*s))
        draw.text((card_x1 + int(24*s), flaw_y + int(12*s)), flaw_str, fill=(255, 95, 110, 255), font=f_flaw)
        
        bbox_f = draw.textbbox((0, 0), meta["watermark"], font=f_wm)
        fw = bbox_f[2] - bbox_f[0]
        fx = (w - fw) // 2
        wy = h - int(50*s)
        draw.rounded_rectangle([fx-int(22*s), wy-int(10*s), fx+fw+int(22*s), wy+int(35*s)], radius=int(6*s), fill=(10, 14, 20, 210), outline=primary, width=1)
        draw.text((fx, wy), meta["watermark"], fill=(235, 245, 255, 255), font=f_wm)
        return poster

    # ----------------- 8. MINIMALIST BRUTALIST COMBAT (NEW) -----------------
    def _render_brutalist_combat(self, base, w, h, p, tips, meta):
        primary, secondary, gold = p["primary"], p["secondary"], p["gold"]
        is_compact = (h <= 1400)
        s = w / 1080.0
        
        vig = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        vdraw = ImageDraw.Draw(vig)
        top_h = int(260 if is_compact else 340)
        for y in range(top_h):
            a = int(235 * (1.0 - (y/float(top_h))**0.65))
            vdraw.line([(0, y), (w, y)], fill=(5, 5, 8, a))
        bot_h = int(580 if is_compact else 720)
        for y in range(h - bot_h, h):
            ratio = (y - (h - bot_h)) / float(bot_h)
            a = int(245 * (ratio**0.75))
            vdraw.line([(0, y), (w, y)], fill=(4, 5, 8, a))
        poster = Image.alpha_composite(base, vig)
        draw = ImageDraw.Draw(poster)
        
        max_title_w = int(960 * s)
        f_title, _ = fit_single_line_font(draw, meta["title"], "BebasNeue-Regular.ttf", max_title_w, int((125 if is_compact else 145) * s), min_size=int(55*s))
        f_badge = get_font("Rajdhani-Bold.ttf", int((22 if is_compact else 26) * s), "arialbd.ttf")
        f_tag = get_font("Rajdhani-Bold.ttf", int(24 * s), "arialbd.ttf")
        f_body = get_font("Rajdhani-SemiBold.ttf", int((20 if is_compact else 23) * s), "arial.ttf")
        f_num = get_font("BebasNeue-Regular.ttf", int((60 if is_compact else 72) * s), "impact.ttf")
        f_wm = get_font("Rajdhani-Bold.ttf", int(22 * s), "arialbd.ttf")
        
        hy = int((35 if is_compact else 45) * s)
        f_badge, _ = fit_single_line_font(draw, meta["protocol"], "Rajdhani-Bold.ttf", int(380*s), int((22 if is_compact else 26) * s), min_size=int(14*s))
        p_bbox = draw.textbbox((0, 0), meta["protocol"], font=f_badge)
        p_w = p_bbox[2] - p_bbox[0]
        badge_w = p_w + int(26 * s)
        draw.rectangle([int(45*s), hy, int(45*s) + badge_w, hy + int(38*s)], fill=primary)
        draw.text((int(58*s), hy + int(7*s)), meta["protocol"], fill=(0, 0, 0, 255), font=f_badge)
        
        range_str = f"RANGE: {meta.get('range', 'INFIGHTING [0.5M]')}"
        range_x = int(45*s) + badge_w + int(20*s)
        max_range_w = w - int(170*s) - range_x
        f_range, _ = fit_single_line_font(draw, range_str, "Rajdhani-Bold.ttf", max_range_w, int((20 if is_compact else 24)*s), min_size=int(13*s))
        draw.text((range_x, hy + int(7*s)), range_str, fill=gold, font=f_range)
        
        ty = int((80 if is_compact else 98) * s)
        tx = int(45 * s)
        draw.text((tx, ty), meta["title"], fill=(255,255,255,255), font=f_title)
        
        dm_x = w - int(160*s)
        dm_y = int(45*s)
        for row in range(5):
            for col in range(5):
                draw.ellipse([dm_x + col*int(18*s), dm_y + row*int(18*s), dm_x + col*int(18*s) + int(5*s), dm_y + row*int(18*s) + int(5*s)], fill=(primary[0], primary[1], primary[2], 180))
                
        t_box = draw.textbbox((tx, ty), meta["title"], font=f_title)
        title_bottom = t_box[3]
        
        tagline_y = title_bottom + int(14 * s)
        f_sub, _ = fit_single_line_font(draw, meta["tagline"], "Rajdhani-Bold.ttf", max_title_w, int((28 if is_compact else 34) * s), min_size=int(18*s))
        draw.text((tx, tagline_y), meta["tagline"], fill=gold, font=f_sub)
        
        if is_compact:
            curr_y = int(580 * s)
            card_h = int(140 * s)
            gap = int(16 * s)
        else:
            curr_y = int(980 * s)
            card_h = int(185 * s)
            gap = int(28 * s)
            
        bx1 = int(45 * s)
        bx2 = w - int(45 * s)
        bw = bx2 - bx1
        card_max_text_h = card_h - int(52 * s)
        
        for num, tag, desc in tips:
            draw.rectangle([bx1, curr_y, bx2, curr_y + card_h], fill=(8, 10, 14, 235), outline=(255, 255, 255, 200), width=2)
            draw.rectangle([bx1, curr_y, bx1 + int(75*s), curr_y + card_h], fill=primary)
            draw.text((bx1 + int(16*s), curr_y + int((15 if is_compact else 25)*s)), num, fill=(0, 0, 0, 255), font=f_num)
            
            draw.text((bx1 + int(95*s), curr_y + int(12*s)), tag.upper(), fill=gold, font=f_tag)
            draw_wrapped_text(draw, desc, f_body, (225, 235, 248, 255), bx1 + int(95*s), curr_y + int(46*s), bw - int(115*s), 1.25, max_height=card_max_text_h)
            curr_y += card_h + gap
            
        flaw_y = curr_y + int(4*s)
        draw.rectangle([bx1, flaw_y, bx2, flaw_y + int(48*s)], fill=(28, 6, 10, 240), outline=(255, 40, 60, 255), width=2)
        flaw_str = f"[ ! ] CRITICAL FLAW: {meta.get('caution', 'DROPPING REAR GUARD')}"
        f_flaw, _ = fit_single_line_font(draw, flaw_str, "Rajdhani-Bold.ttf", bw - int(40*s), int((20 if is_compact else 23) * s), min_size=int(14*s))
        draw.text((bx1 + int(20*s), flaw_y + int(12*s)), flaw_str, fill=(255, 95, 110, 255), font=f_flaw)
        
        bbox_f = draw.textbbox((0, 0), meta["watermark"], font=f_wm)
        fw = bbox_f[2] - bbox_f[0]
        fx = (w - fw) // 2
        wy = h - int(50*s)
        draw.rounded_rectangle([fx-int(22*s), wy-int(10*s), fx+fw+int(22*s), wy+int(35*s)], radius=int(6*s), fill=(10, 14, 20, 210), outline=primary, width=1)
        draw.text((fx, wy), meta["watermark"], fill=(235, 245, 255, 255), font=f_wm)
        return poster

    # ----------------- 9. CLEAN ART WATERMARK (CREATOR SIGNATURE) -----------------
    def _render_clean_watermark(self, poster, w, h, p, meta):
        primary = p["primary"]
        is_compact = (h <= 1400)
        s = w / 1080.0
        draw = ImageDraw.Draw(poster)
        
        f_wm = get_font("Rajdhani-Bold.ttf", int((20 if is_compact else 22) * s), "arialbd.ttf")
        wm_text = meta["watermark"]
        bbox_f = draw.textbbox((0, 0), wm_text, font=f_wm)
        fw = bbox_f[2] - bbox_f[0]
        fh = bbox_f[3] - bbox_f[1]
        fx = (w - fw) // 2
        wy = h - int(45 * s)
        
        pad_x = int(22 * s)
        pad_y = int(8 * s)
        draw.rounded_rectangle(
            [fx - pad_x, wy - pad_y, fx + fw + pad_x, wy + int(32 * s)],
            radius=int(6 * s),
            fill=(10, 14, 20, 215),
            outline=(primary[0], primary[1], primary[2], 160),
            width=1
        )
        draw.text((fx, wy), wm_text, fill=(235, 245, 255, 255), font=f_wm)
        return poster

    # ----------------- 10. DYNAMIC SOCIAL CTA (LIKE • FOLLOW • SHARE) -----------------
    def _render_social_cta(self, poster, w, h, p, meta, layout, is_clean_art=False):
        primary, secondary, gold = p["primary"], p["secondary"], p["gold"]
        s = w / 1080.0
        is_compact = (h <= 1400)
        draw = ImageDraw.Draw(poster)

        cta_phrases = [
            "// LIKE • FOLLOW • SHARE FOR MORE TIPS",
            "[ SAVE • SHARE • FOLLOW @RINGPULSEOFFICIAL ]",
            "DOUBLE TAP IF USEFUL • SHARE WITH YOUR CORNER",
            "// SUPPORT THE LAB: LIKE • SHARE • FOLLOW FOR MORE",
            "SAVE TO REINFORCE YOUR FIGHT IQ • FOLLOW @RINGPULSEOFFICIAL",
            "FIGHT IQ BREAKDOWN // LIKE • FOLLOW • REPOST",
            "[ LIKE • COMMENT • SHARE • FOLLOW ]",
            "DRILL THIS COMBO // DOUBLE TAP • SHARE WITH YOUR TEAM",
            "SAVE & SHARE WITH YOUR SPARRING PARTNER // @RINGPULSEOFFICIAL",
            "SHARE WITH YOUR COACH // FOLLOW FOR MORE COMBAT BREAKDOWNS"
        ]
        cta_text = random.choice(cta_phrases)

        # Diverse font selection
        font_options = [
            ("Rajdhani-Bold.ttf", "arialbd.ttf"),
            ("BebasNeue-Regular.ttf", "arialbd.ttf"),
            ("Rajdhani-SemiBold.ttf", "arial.ttf")
        ]
        font_file, font_fallback = random.choice(font_options)
        
        # Diverse color accents
        accent = random.choice([
            primary,
            secondary,
            gold,
            (255, 255, 255, 255)
        ])
        
        if is_clean_art:
            # On clean artwork, place CTA strictly at top_right to guarantee zero overlap with bottom watermark
            mode = "top_right"
        else:
            # Layout-aware safe placement:
            if layout in ["Classic Bottom Card", "Cyberpunk Target Lock HUD", "Floating Tactical Callouts (Left/Right)"]:
                mode = "top_right"
            elif layout in ["Side Editorial Column (Magazine)", "Diagonal Kinetic Slash"]:
                mode = random.choice(["top_right", "bottom_corner"])
            elif layout == "Dual-Wing Symmetrical Frame":
                mode = "bottom_center"
            else:
                mode = "top_right"

        # Font size: subtle, clean, highly legible
        target_font_size = int((15 if is_compact else 18) * s)
        max_cta_w = int(500 * s)
        f_cta, _ = fit_single_line_font(draw, cta_text, font_file, max_cta_w, target_font_size, min_size=int(12*s), fallback=font_fallback)
        c_box = draw.textbbox((0, 0), cta_text, font=f_cta)
        cw = c_box[2] - c_box[0]
        ch = c_box[3] - c_box[1]

        pad_x = int(12 * s)
        pad_y = int(5 * s)
        pill_w = cw + pad_x * 2
        pill_h = ch + pad_y * 2

        if is_clean_art:
            if mode == "top_right":
                px = w - pill_w - int(40 * s)
                py = int((36 if is_compact else 44) * s)
            elif mode == "bottom_corner":
                px = w - pill_w - int(40 * s)
                py = h - pill_h - int((40 if is_compact else 48) * s)
            else:  # bottom_center
                px = (w - pill_w) // 2
                py = h - pill_h - int((92 if is_compact else 102) * s)
        else:
            if mode == "top_right":
                # Placed near top right corner (opposite protocol badge or title)
                px = w - pill_w - int(40 * s)
                py = int((36 if is_compact else 44) * s)
            elif mode == "bottom_corner":
                # Placed in bottom right corner slightly above watermark level
                px = w - pill_w - int(40 * s)
                py = h - pill_h - int((65 if is_compact else 75) * s)
            else:  # bottom_center
                # Placed right above the watermark pill with generous clearance
                px = (w - pill_w) // 2
                py = h - pill_h - int((92 if is_compact else 102) * s)

        # Draw sleek high-tech pill background
        draw.rounded_rectangle(
            [px, py, px + pill_w, py + pill_h],
            radius=int(6 * s),
            fill=(10, 14, 22, 225),
            outline=(accent[0], accent[1], accent[2], 180),
            width=1
        )
        # Draw micro glowing pip / dot
        dot_r = int(3 * s)
        draw.ellipse(
            [px + int(6*s), py + (pill_h - dot_r*2)//2, px + int(6*s) + dot_r*2, py + (pill_h - dot_r*2)//2 + dot_r*2],
            fill=accent
        )
        # Draw text
        draw.text((px + int(14*s), py + pad_y - 1), cta_text, fill=(240, 245, 255, 255), font=f_cta)
        return poster

NODE_CLASS_MAPPINGS = {
    "FighterPosterDesigner": FighterPosterDesigner
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FighterPosterDesigner": "Fighter Poster Designer (1080x1350 / 1080x1920 Clean)"
}
