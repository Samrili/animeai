import json
import os

def build_studio():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    techniques_path = os.path.join(base_dir, "scripts", "techniques_data.json")
    samples_path = os.path.join(base_dir, "scripts", "samples_data.json")
    
    with open(techniques_path, "r", encoding="utf-8") as f:
        techniques = json.load(f)
    
    techniques_js = json.dumps(techniques, ensure_ascii=False, indent=2)

    if os.path.exists(samples_path):
        with open(samples_path, "r", encoding="utf-8") as f:
            samples_data = json.load(f)
    else:
        samples_data = {}
    samples_js = json.dumps(samples_data)
    
    html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RingPulse // AI Combat & Mask Studio</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Rajdhani:wght@500;600;700&family=Outfit:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-dark: #07090e;
      --bg-panel: rgba(13, 17, 27, 0.85);
      --bg-card: rgba(20, 26, 42, 0.65);
      --border: rgba(255, 38, 70, 0.35);
      --border-subtle: rgba(255, 255, 255, 0.08);
      --crimson: #ff2646;
      --crimson-glow: rgba(255, 38, 70, 0.45);
      --cyan: #00ebff;
      --cyan-glow: rgba(0, 235, 255, 0.4);
      --purple: #8b5cf6;
      --purple-glow: rgba(139, 92, 246, 0.4);
      --gold: #f59e0b;
      --gold-glow: rgba(245, 158, 11, 0.35);
      --green: #10b981;
      --text: #f0f4fc;
      --text-muted: #94a3b8;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      background: var(--bg-dark);
      background-image: 
        radial-gradient(circle at 12% 15%, rgba(255, 38, 70, 0.07) 0%, transparent 45%),
        radial-gradient(circle at 88% 85%, rgba(0, 235, 255, 0.06) 0%, transparent 45%),
        radial-gradient(circle at 50% 50%, rgba(139, 92, 246, 0.04) 0%, transparent 50%);
      color: var(--text);
      font-family: 'Outfit', sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }}

    /* HEADER */
    header {{
      padding: 12px 32px;
      background: rgba(9, 12, 20, 0.95);
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
      backdrop-filter: blur(16px);
      gap: 20px;
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      user-select: none;
    }}

    .brand-logo {{
      width: 36px;
      height: 36px;
      background: linear-gradient(135deg, var(--crimson), #99001e);
      clip-path: polygon(25% 0%, 100% 0%, 75% 100%, 0% 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Rajdhani', sans-serif;
      font-weight: 700;
      font-size: 20px;
      color: #fff;
      box-shadow: 0 0 16px var(--crimson-glow);
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .brand:hover .brand-logo {{
      transform: scale(1.05);
      box-shadow: 0 0 22px var(--crimson-glow);
    }}

    .brand-text {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .brand-title {{
      font-family: 'Rajdhani', sans-serif;
      font-weight: 700;
      font-size: 20px;
      letter-spacing: 2px;
      text-transform: uppercase;
      line-height: 1;
      color: #fff;
    }}

    .brand-badge {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 11px;
      font-weight: 700;
      background: rgba(255, 38, 70, 0.15);
      border: 1px solid rgba(255, 38, 70, 0.35);
      color: var(--crimson);
      padding: 2px 7px;
      border-radius: 6px;
      letter-spacing: 1px;
    }}

    /* ULTRA-MODERN MAGNETIC SEGMENTED SWITCHER */
    .nav-switcher {{
      position: relative;
      display: flex;
      align-items: center;
      background: rgba(14, 18, 30, 0.92);
      padding: 4px;
      border-radius: 30px;
      border: 1px solid rgba(255, 255, 255, 0.09);
      box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.6), 0 4px 20px rgba(0, 0, 0, 0.35);
      overflow: hidden;
    }}

    /* LIQUID SLIDING PILL */
    .nav-slider-pill {{
      position: absolute;
      top: 4px;
      bottom: 4px;
      left: 0;
      border-radius: 24px;
      pointer-events: none;
      z-index: 1;
      transition: transform 0.42s cubic-bezier(0.16, 1, 0.3, 1),
                  width 0.42s cubic-bezier(0.16, 1, 0.3, 1),
                  background 0.42s ease,
                  box-shadow 0.42s ease,
                  border-color 0.42s ease;
      border: 1px solid transparent;
      opacity: 0;
    }}
    .nav-slider-pill.pill-active {{
      opacity: 1;
    }}
    .nav-slider-pill.pill-poster {{
      background: linear-gradient(135deg, rgba(255, 38, 70, 0.28), rgba(185, 75, 251, 0.22));
      border-color: rgba(255, 38, 70, 0.5);
      box-shadow: 0 0 22px rgba(255, 38, 70, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.25);
    }}
    .nav-slider-pill.pill-mask {{
      background: linear-gradient(135deg, rgba(139, 92, 246, 0.32), rgba(0, 235, 255, 0.25));
      border-color: rgba(139, 92, 246, 0.55);
      box-shadow: 0 0 22px rgba(139, 92, 246, 0.45), inset 0 1px 1px rgba(255, 255, 255, 0.25);
    }}

    .nav-tab {{
      position: relative;
      z-index: 2;
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 20px;
      border-radius: 24px;
      border: none;
      background: transparent;
      color: var(--text-muted);
      font-family: 'Rajdhani', sans-serif;
      font-size: 13.5px;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
      cursor: pointer;
      user-select: none;
      transition: color 0.25s ease, transform 0.15s ease, text-shadow 0.25s ease;
    }}
    .nav-tab:hover {{
      color: #fff;
    }}
    .nav-tab:active {{
      transform: scale(0.95);
    }}
    .nav-tab.active {{
      color: #ffffff;
      text-shadow: 0 0 12px rgba(255, 255, 255, 0.4);
    }}

    .nav-icon {{
      font-size: 14px;
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .nav-tab:hover .nav-icon {{
      transform: scale(1.15) rotate(4deg);
    }}

    /* SERVER STATUS */
    .server-status {{
      display: flex;
      align-items: center;
      gap: 9px;
      font-family: 'Rajdhani', sans-serif;
      font-size: 12px;
      font-weight: 600;
      letter-spacing: 1px;
      padding: 6px 14px;
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .server-status:hover {{ border-color: rgba(255, 255, 255, 0.2); }}

    .status-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #888;
      box-shadow: 0 0 8px #888;
      transition: all 0.3s;
    }}
    .status-dot.online {{
      background: #00ff66;
      box-shadow: 0 0 10px #00ff66;
    }}
    .status-dot.offline {{
      background: #ff3344;
      box-shadow: 0 0 10px #ff3344;
    }}

    /* HARDWARE-ACCELERATED DIRECTIONAL SPRING VIEW TRANSITIONS */
    .view-container {{
      display: none;
      width: 100%;
      opacity: 0;
      will-change: transform, opacity, filter;
    }}
    .view-container.active-view {{
      display: block;
      opacity: 1;
    }}

    /* Slide in from Right (Poster -> Mask) */
    .view-container.anim-slide-in-right {{
      animation: slideInFromRight 0.42s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}
    /* Slide in from Left (Mask -> Poster) */
    .view-container.anim-slide-in-left {{
      animation: slideInFromLeft 0.42s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}

    @keyframes slideInFromRight {{
      0% {{
        opacity: 0;
        transform: translateX(36px) scale(0.985);
        filter: blur(10px);
      }}
      50% {{
        filter: blur(3px);
      }}
      100% {{
        opacity: 1;
        transform: translateX(0) scale(1);
        filter: blur(0);
      }}
    }}

    @keyframes slideInFromLeft {{
      0% {{
        opacity: 0;
        transform: translateX(-36px) scale(0.985);
        filter: blur(10px);
      }}
      50% {{
        filter: blur(3px);
      }}
      100% {{
        opacity: 1;
        transform: translateX(0) scale(1);
        filter: blur(0);
      }}
    }}

    /* ========================================================= */
    /* POSTER TOOL STYLES                                       */
    /* ========================================================= */
    .poster-grid {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px 24px 60px 24px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 32px;
      align-items: start;
    }}

    @media (max-width: 1024px) {{
      .poster-grid {{ grid-template-columns: 1fr; }}
    }}

    .hero-card {{
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 18px;
      padding: 26px;
      box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
      backdrop-filter: blur(12px);
      display: flex;
      flex-direction: column;
      gap: 18px;
      position: relative;
      overflow: hidden;
    }}

    .hero-card::before {{
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--crimson), var(--gold), var(--cyan));
    }}

    .section-title {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 1.8px;
      text-transform: uppercase;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .pill-group {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }}

    .format-pill {{
      padding: 10px 14px;
      background: var(--bg-card);
      border: 1.5px solid var(--border-subtle);
      border-radius: 10px;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      gap: 2px;
      transition: all 0.2s ease;
      color: var(--text);
    }}
    .format-pill:hover {{
      border-color: rgba(255, 38, 70, 0.5);
      transform: translateY(-1px);
    }}
    .format-pill.active {{
      background: rgba(255, 38, 70, 0.12);
      border-color: var(--crimson);
      box-shadow: 0 0 16px rgba(255, 38, 70, 0.25);
    }}

    .pill-label {{
      font-family: 'Rajdhani', sans-serif;
      font-weight: 700;
      font-size: 14px;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .pill-desc {{ font-size: 11px; color: var(--text-muted); }}

    .sport-filter {{ display: flex; flex-wrap: wrap; gap: 6px; }}

    .sport-btn, .option-pill {{
      padding: 5px 11px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
      color: var(--text-muted);
      font-family: 'Rajdhani', sans-serif;
      font-size: 12px;
      font-weight: 600;
      letter-spacing: 0.5px;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .sport-btn:hover, .option-pill:hover {{
      color: #fff;
      border-color: rgba(255, 255, 255, 0.25);
    }}
    .sport-btn.active, .option-pill.active {{
      background: var(--cyan);
      color: #000;
      font-weight: 700;
      border-color: var(--cyan);
      box-shadow: 0 0 12px var(--cyan-glow);
    }}

    .batch-selector {{
      display: flex;
      gap: 8px;
    }}
    .batch-pill {{
      flex: 1;
      padding: 8px 10px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      cursor: pointer;
      text-align: center;
      transition: all 0.2s;
    }}
    .batch-pill:hover {{ border-color: rgba(255, 255, 255, 0.2); }}
    .batch-pill.active {{
      border-color: var(--gold);
      background: rgba(245, 158, 11, 0.12);
      box-shadow: 0 0 12px var(--gold-glow);
    }}
    .batch-label {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 13px;
      font-weight: 700;
      color: var(--gold);
    }}
    .batch-sub {{ font-size: 10.5px; color: var(--text-muted); margin-top: 1px; }}

    .hero-btn {{
      padding: 16px 24px;
      background: linear-gradient(135deg, var(--crimson), #c40026);
      border: none;
      border-radius: 12px;
      color: #fff;
      cursor: pointer;
      box-shadow: 0 10px 30px var(--crimson-glow);
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
      transition: all 0.25s ease;
      position: relative;
      overflow: hidden;
    }}
    .hero-btn:hover:not(:disabled) {{
      transform: translateY(-2px);
      box-shadow: 0 15px 40px rgba(255, 38, 70, 0.6);
      background: linear-gradient(135deg, #ff3d5a, #d6002b);
    }}
    .hero-btn:disabled {{ opacity: 0.6; cursor: not-allowed; }}
    .hero-btn-title {{
      font-family: 'Bebas Neue', sans-serif;
      font-size: 26px;
      letter-spacing: 2px;
    }}
    .hero-btn-sub {{
      font-size: 12px;
      color: rgba(255, 255, 255, 0.85);
      font-weight: 500;
    }}

    .selection-badge {{
      display: none;
      padding: 8px 12px;
      background: rgba(0, 235, 255, 0.08);
      border: 1px solid rgba(0, 235, 255, 0.3);
      border-radius: 8px;
      font-size: 12px;
      color: var(--cyan);
      align-items: center;
      gap: 8px;
    }}

    /* DRAWER */
    .drawer-toggle {{
      background: rgba(0, 0, 0, 0.3);
      border: 1px dashed var(--border-subtle);
      border-radius: 10px;
      padding: 10px 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      color: var(--text-muted);
      font-family: 'Rajdhani', sans-serif;
      font-size: 12px;
      font-weight: 600;
      letter-spacing: 1px;
      transition: all 0.2s;
    }}
    .drawer-toggle:hover {{
      color: #fff;
      border-color: rgba(255, 255, 255, 0.2);
    }}
    .drawer-rnd-btn {{
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #cbd5e1;
      padding: 3px 9px;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.8px;
      border-radius: 4px;
      cursor: pointer;
      font-family: 'Rajdhani', sans-serif;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .drawer-rnd-btn:hover {{
      background: rgba(255, 38, 70, 0.25);
      border-color: var(--crimson);
      color: #ffffff;
      transform: scale(1.04);
    }}
    .drawer-rnd-btn:active {{
      transform: scale(0.96);
    }}
    .drawer-content {{
      display: none;
      flex-direction: column;
      gap: 12px;
      padding: 14px;
      background: rgba(0, 0, 0, 0.3);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
    }}
    .drawer-content.open {{ display: flex; }}

    .form-group {{ display: flex; flex-direction: column; gap: 5px; }}
    .form-label {{ font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); }}
    .form-input, .form-select, .form-textarea {{
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 8px 12px;
      color: #fff;
      font-family: 'Outfit', sans-serif;
      font-size: 12.5px;
      transition: all 0.2s;
    }}
    .form-input:focus, .form-select:focus, .form-textarea:focus {{
      outline: none;
      border-color: var(--cyan);
      box-shadow: 0 0 10px var(--cyan-glow);
    }}

    .secondary-btn {{
      padding: 10px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      color: var(--text);
      font-family: 'Rajdhani', sans-serif;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 1px;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .secondary-btn:hover {{ border-color: var(--cyan); color: #fff; }}

    /* VIEWPORT CARD */
    .viewport-card {{
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 18px;
      padding: 22px;
      box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
      backdrop-filter: blur(12px);
      display: flex;
      flex-direction: column;
      gap: 14px;
      align-items: center;
    }}

    .viewport-tabs {{
      display: flex;
      background: rgba(0, 0, 0, 0.5);
      border: 1px solid var(--border-subtle);
      border-radius: 24px;
      padding: 3px;
      gap: 4px;
      width: 100%;
      max-width: 420px;
    }}
    .view-tab {{
      flex: 1;
      padding: 7px 12px;
      background: transparent;
      border: none;
      border-radius: 20px;
      color: var(--text-muted);
      font-family: 'Rajdhani', sans-serif;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 1px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s;
    }}
    .view-tab.active {{
      background: var(--crimson);
      color: #fff;
      box-shadow: 0 0 14px var(--crimson-glow);
    }}
    .view-tab.tab-clean.active {{
      background: var(--cyan);
      color: #000;
      box-shadow: 0 0 14px var(--cyan-glow);
    }}

    .image-viewport {{
      width: 100%;
      max-width: 480px;
      aspect-ratio: 4 / 5;
      background: #000;
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      overflow: hidden;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
      transition: aspect-ratio 0.3s ease;
      transform: translateZ(0);
      backface-visibility: hidden;
    }}
    .image-viewport.ratio-story {{ aspect-ratio: 9 / 16; max-width: 380px; }}

    .preview-img {{
      width: 100%;
      height: 100%;
      object-fit: contain;
      display: none;
      content-visibility: auto;
    }}

    .empty-state {{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 30px;
      text-align: center;
      gap: 12px;
      color: var(--text-muted);
    }}
    .empty-icon {{ font-size: 40px; opacity: 0.6; }}
    .empty-title {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 18px;
      font-weight: 700;
      color: #fff;
      letter-spacing: 1px;
    }}
    .empty-desc {{ font-size: 12px; line-height: 1.5; max-width: 280px; }}

    .progress-overlay {{
      display: none;
      position: absolute;
      inset: 0;
      background: rgba(7, 9, 14, 0.92);
      backdrop-filter: blur(8px);
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 16px;
      z-index: 10;
    }}
    .spinner-ring {{
      width: 50px;
      height: 50px;
      border: 3px solid rgba(255, 38, 70, 0.2);
      border-top-color: var(--crimson);
      border-radius: 50%;
      animation: spin 0.9s linear infinite;
      box-shadow: 0 0 20px var(--crimson-glow);
    }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}

    .progress-bar-container {{
      width: 200px;
      height: 4px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 2px;
      overflow: hidden;
    }}
    .progress-bar-glow {{
      width: 50%;
      height: 100%;
      background: linear-gradient(90deg, var(--crimson), var(--cyan));
      animation: progressPulse 1.4s ease-in-out infinite alternate;
    }}
    @keyframes progressPulse {{
      from {{ width: 20%; transform: translateX(-20%); }}
      to {{ width: 85%; transform: translateX(20%); }}
    }}

    .action-bar {{
      display: none;
      width: 100%;
      max-width: 480px;
      gap: 10px;
    }}
    .dl-btn {{
      flex: 1;
      padding: 11px 14px;
      border-radius: 10px;
      border: 1px solid var(--border-subtle);
      font-family: 'Rajdhani', sans-serif;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 1px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s;
    }}
    .dl-btn-poster {{
      background: rgba(255, 38, 70, 0.15);
      border-color: var(--crimson);
      color: #fff;
    }}
    .dl-btn-poster:hover {{
      background: var(--crimson);
      box-shadow: 0 0 16px var(--crimson-glow);
    }}
    .dl-btn-clean {{
      background: rgba(0, 235, 255, 0.15);
      border-color: var(--cyan);
      color: #fff;
    }}
    .dl-btn-clean:hover {{
      background: var(--cyan);
      color: #000;
      box-shadow: 0 0 16px var(--cyan-glow);
    }}

    /* GALLERY CARD CONTAINER */
    .gallery-container {{
      max-width: 1440px;
      margin: 0 auto 50px auto;
      padding: 0 24px;
      width: 100%;
    }}

    .gallery-box {{
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 18px;
      padding: 20px 24px 18px 24px;
      box-shadow: 0 15px 40px rgba(0, 0, 0, 0.45);
      backdrop-filter: blur(14px);
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}

    .gallery-box::before {{
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 2px;
      background: linear-gradient(90deg, transparent, rgba(0, 235, 255, 0.45), rgba(255, 38, 70, 0.4), transparent);
    }}

    .gallery-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 8px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }}
    .gallery-title {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 2px;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 9px;
      text-transform: uppercase;
    }}
    .gallery-count {{
      background: rgba(0, 235, 255, 0.12);
      border: 1px solid rgba(0, 235, 255, 0.3);
      padding: 2px 8px;
      border-radius: 12px;
      font-size: 11px;
      color: var(--cyan);
      font-weight: 700;
      letter-spacing: 0.5px;
    }}
    .gallery-strip {{
      display: flex;
      gap: 14px;
      overflow-x: auto;
      padding: 6px 2px 12px 2px;
      min-height: 175px;
      align-items: center;
    }}
    .gallery-strip::-webkit-scrollbar {{
      height: 6px;
    }}
    .gallery-strip::-webkit-scrollbar-track {{
      background: rgba(0, 0, 0, 0.25);
      border-radius: 4px;
    }}
    .gallery-strip::-webkit-scrollbar-thumb {{
      background: rgba(255, 255, 255, 0.18);
      border-radius: 4px;
      transition: background 0.2s;
    }}
    .gallery-strip::-webkit-scrollbar-thumb:hover {{
      background: var(--cyan);
    }}

    .gallery-card {{
      flex: 0 0 122px;
      aspect-ratio: 4 / 5;
      background: #000;
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      overflow: hidden;
      cursor: pointer;
      position: relative;
      transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.5);
      transform: translateZ(0);
      backface-visibility: hidden;
      contain: content;
    }}
    .gallery-card:hover {{
      border-color: var(--crimson);
      transform: translateY(-3px) scale(1.02);
      box-shadow: 0 10px 24px rgba(255, 38, 70, 0.3);
    }}
    .gallery-card.active {{
      border-color: var(--cyan);
      box-shadow: 0 0 18px var(--cyan-glow);
      transform: translateY(-2px);
    }}
    .gallery-thumb {{ width: 100%; height: 100%; object-fit: cover; }}
    .gallery-clean-pill {{
      position: absolute;
      top: 6px; right: 6px;
      background: rgba(0, 235, 255, 0.85);
      color: #000;
      font-size: 9px;
      font-weight: 700;
      padding: 1px 4px;
      border-radius: 4px;
    }}
    .gallery-card-label {{
      position: absolute;
      bottom: 0; left: 0; right: 0;
      padding: 4px 6px;
      font-size: 9.5px;
      font-weight: 600;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      color: #fff;
      background: rgba(10, 14, 22, 0.88);
    }}
    .gallery-empty {{
      color: var(--text-muted);
      font-size: 13px;
      padding: 36px 20px;
      text-align: center;
      width: 100%;
      border: 1px dashed rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      background: rgba(0, 0, 0, 0.25);
    }}

    /* ========================================================= */
    /* MASK TOOL STYLES                                         */
    /* ========================================================= */
    .mask-grid {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px;
      display: grid;
      grid-template-columns: 1fr 320px;
      gap: 28px;
      align-items: start;
      min-height: calc(100vh - 120px);
    }}

    @media (max-width: 1024px) {{
      .mask-grid {{ grid-template-columns: 1fr; }}
    }}

    .mask-canvas-box {{
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 18px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 580px;
      position: relative;
      box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
      backdrop-filter: blur(12px);
    }}

    #drop-zone {{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 14px;
      width: 100%;
      height: 100%;
      min-height: 480px;
      border: 2px dashed rgba(139, 92, 246, 0.35);
      border-radius: 14px;
      cursor: pointer;
      transition: all 0.25s ease;
      color: var(--text-muted);
      background: rgba(20, 26, 42, 0.3);
    }}
    #drop-zone:hover {{
      border-color: var(--cyan);
      color: #fff;
      background: rgba(0, 235, 255, 0.04);
      box-shadow: 0 0 30px rgba(0, 235, 255, 0.1);
    }}
    #drop-zone.hidden {{ display: none; }}

    #canvas-wrapper {{
      display: none;
      flex-direction: column;
      align-items: center;
      gap: 12px;
      width: 100%;
    }}
    #canvas-wrapper.visible {{ display: flex; }}

    #canvas-container {{
      position: relative;
      border-radius: 10px;
      overflow: hidden;
      box-shadow: 0 0 0 1px var(--border-subtle), 0 20px 50px rgba(0, 0, 0, 0.8);
      background: #000;
    }}
    #bg-canvas, #draw-canvas {{
      display: block;
      position: absolute;
      top: 0; left: 0;
    }}
    #bg-canvas {{ z-index: 1; }}
    #draw-canvas {{ z-index: 2; cursor: crosshair; }}

    .mask-legend {{
      display: flex;
      align-items: center;
      gap: 14px;
      font-size: 12px;
      color: var(--text-muted);
      background: rgba(0, 0, 0, 0.4);
      padding: 6px 16px;
      border-radius: 20px;
      border: 1px solid var(--border-subtle);
    }}
    .legend-tag {{ display: flex; align-items: center; gap: 6px; }}
    .legend-color {{ width: 10px; height: 10px; border-radius: 2px; }}

    /* MASK CONTROL PANEL */
    .mask-controls {{
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 18px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 20px;
      box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
      position: sticky;
      top: 80px;
    }}

    .mask-controls::before {{
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--purple), var(--cyan));
    }}

    .mask-tool-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }}

    .tool-btn {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      padding: 12px 8px;
      border-radius: 10px;
      border: 1px solid var(--border-subtle);
      background: var(--bg-card);
      color: var(--text-muted);
      cursor: pointer;
      font-family: 'Rajdhani', sans-serif;
      font-size: 13px;
      font-weight: 600;
      transition: all 0.15s ease;
    }}
    .tool-btn svg {{ width: 20px; height: 20px; }}
    .tool-btn:hover {{
      border-color: var(--purple);
      color: #fff;
      background: rgba(139, 92, 246, 0.1);
    }}
    .tool-btn.active {{
      border-color: var(--purple);
      background: rgba(139, 92, 246, 0.25);
      color: #fff;
      box-shadow: 0 0 14px var(--purple-glow);
    }}

    .brush-slider-wrap {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .slider-header {{
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      color: var(--text-muted);
    }}
    .slider-header span:last-child {{
      color: var(--cyan);
      font-weight: 700;
    }}
    input[type=range] {{
      -webkit-appearance: none;
      width: 100%;
      height: 5px;
      border-radius: 3px;
      background: rgba(255, 255, 255, 0.15);
      outline: none;
    }}
    input[type=range]::-webkit-slider-thumb {{
      -webkit-appearance: none;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: var(--cyan);
      cursor: pointer;
      box-shadow: 0 0 10px var(--cyan-glow);
    }}

    .undo-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }}

    .action-stack {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-top: 6px;
    }}

    .btn-comfy-save {{
      width: 100%;
      padding: 13px 16px;
      border-radius: 10px;
      border: none;
      background: linear-gradient(135deg, var(--purple), #6366f1);
      color: #fff;
      font-family: 'Rajdhani', sans-serif;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 1px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 4px 18px var(--purple-glow);
      transition: all 0.2s ease;
    }}
    .btn-comfy-save:hover:not(:disabled) {{
      background: linear-gradient(135deg, #9d6df8, #7477f7);
      transform: translateY(-1px);
      box-shadow: 0 6px 24px rgba(139, 92, 246, 0.6);
    }}
    .btn-comfy-save:disabled {{ opacity: 0.6; cursor: not-allowed; }}
    .btn-comfy-save.btn-success {{
      background: linear-gradient(135deg, #059669, #10b981) !important;
      box-shadow: 0 4px 16px rgba(16, 185, 129, 0.4) !important;
    }}

    .btn-mask-clear {{
      width: 100%;
      padding: 12px 16px;
      border-radius: 10px;
      border: 1px solid rgba(255, 38, 70, 0.3);
      background: rgba(255, 38, 70, 0.12);
      color: #ff6b81;
      font-family: 'Rajdhani', sans-serif;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 1px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all 0.2s ease;
    }}
    .btn-mask-clear:hover:not(:disabled) {{
      background: rgba(255, 38, 70, 0.25);
      color: #fff;
      border-color: var(--crimson);
    }}
    .btn-mask-clear:disabled {{ opacity: 0.6; cursor: not-allowed; }}
    .btn-mask-clear.btn-success {{
      background: rgba(16, 185, 129, 0.25) !important;
      border-color: #10b981 !important;
      color: #34d399 !important;
    }}

    .mask-status-bar {{
      padding: 8px 12px;
      background: rgba(0, 0, 0, 0.35);
      border-radius: 8px;
      font-size: 11px;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .mask-status-bar .pos {{ color: var(--cyan); font-family: monospace; }}

    /* SAMPLE BUTTONS (MASK TOOL) */
    .sample-actions {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin-top: 14px;
      padding: 6px 12px;
      background: rgba(13, 17, 27, 0.75);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      backdrop-filter: blur(8px);
      z-index: 5;
    }}
    .sample-label {{
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      font-family: 'Rajdhani', sans-serif;
    }}
    .sample-btn {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 6px 12px;
      background: rgba(20, 26, 42, 0.9);
      border: 1px solid rgba(139, 92, 246, 0.4);
      border-radius: 8px;
      color: #f0f4fc;
      font-family: 'Rajdhani', sans-serif;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.5px;
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .sample-btn:hover {{
      background: rgba(139, 92, 246, 0.3);
      border-color: var(--cyan);
      color: #fff;
      transform: translateY(-1.5px);
      box-shadow: 0 0 14px var(--cyan-glow);
    }}
    .sample-btn:active {{
      transform: scale(0.97);
    }}

    .mask-sample-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      padding: 8px 12px;
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      margin-bottom: 12px;
    }}
    .sample-bar-title {{
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.8px;
      color: var(--text-muted);
      font-family: 'Rajdhani', sans-serif;
    }}
    .sample-bar-btns {{
      display: flex;
      gap: 6px;
    }}
    .sample-bar-btns .sample-btn {{
      padding: 5px 10px;
      font-size: 12px;
    }}

    /* FLOATING TOAST */
    #toast {{
      position: fixed;
      top: 24px;
      right: 24px;
      max-width: 420px;
      background: #101424;
      border-left: 4px solid var(--cyan);
      box-shadow: 0 12px 35px rgba(0, 0, 0, 0.7), 0 0 1px 1px var(--border-subtle);
      border-radius: 10px;
      padding: 14px 18px;
      color: #f1f5f9;
      font-size: 13px;
      line-height: 1.5;
      z-index: 9999;
      opacity: 0;
      transform: translateY(-10px);
      pointer-events: none;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    #toast.visible {{
      opacity: 1;
      transform: translateY(0);
      pointer-events: auto;
    }}
    #toast.toast-success {{ border-left-color: var(--green); }}
    #toast.toast-warning {{ border-left-color: var(--gold); }}
    #toast.toast-error   {{ border-left-color: var(--crimson); }}
    #toast.toast-info    {{ border-left-color: var(--cyan); }}

    .btn-spinner {{
      display: inline-block;
      width: 14px;
      height: 14px;
      border: 2px solid rgba(255,255,255,0.3);
      border-radius: 50%;
      border-top-color: #fff;
      animation: spin 0.8s linear infinite;
    }}
    input[type=file] {{ display: none; }}
  </style>
</head>
<body>

  <!-- HEADER -->
  <header>
    <div class="brand" onclick="switchStudioView('poster')">
      <div class="brand-logo">RP</div>
      <div class="brand-text">
        <div class="brand-title">RINGPULSE</div>
        <span class="brand-badge">STUDIO</span>
      </div>
    </div>

    <!-- ULTRA-MODERN MAGNETIC VIEW SWITCHER -->
    <div class="nav-switcher" id="navSwitcher">
      <div class="nav-slider-pill" id="navSliderPill"></div>
      <button class="nav-tab active" id="tabNavPoster" onclick="switchStudioView('poster')">
        POSTER
      </button>
      <button class="nav-tab tab-mask" id="tabNavMask" onclick="switchStudioView('mask')">
        MASKE
      </button>
    </div>

    <div class="server-status" id="serverStatusBox" onclick="checkServer(true)" title="Durumu yenilemek için tıklayın">
      <div class="status-dot" id="statusDot"></div>
      <span id="statusText">COMFYUI KONTROL EDILIYOR...</span>
    </div>
  </header>

  <!-- ======================================================== -->
  <!-- 1. POSTER VIEW                                           -->
  <!-- ======================================================== -->
  <div id="posterView" class="view-container active-view">
    <div class="poster-grid">

      <!-- LEFT: CONTROLS -->
      <div class="hero-card">
        <!-- 1. FORMAT -->
        <div>
          <div class="section-title">FORMAT</div>
          <div class="pill-group" style="margin-top: 8px;">
            <div class="format-pill active" id="format45" onclick="setFormat('4:5')">
              <div class="pill-label">4:5</div>
              <div class="pill-desc">1080 × 1350</div>
            </div>
            <div class="format-pill" id="format916" onclick="setFormat('9:16')">
              <div class="pill-label">9:16</div>
              <div class="pill-desc">1080 × 1920</div>
            </div>
          </div>
        </div>

        <!-- 2. SPORT -->
        <div>
          <div class="section-title">2. DÖVÜŞ BRANŞI</div>
          <div class="sport-filter" style="margin-top: 8px;">
            <button class="sport-btn active" id="sportBtnAll" onclick="setSport('all', this)">TÜMÜ ({len(techniques)})</button>
            <button class="sport-btn" onclick="setSport('boxing', this)">BOKS</button>
            <button class="sport-btn" onclick="setSport('muay_thai', this)">MUAY THAI</button>
            <button class="sport-btn" onclick="setSport('kickboxing', this)">KICKBOKS</button>
            <button class="sport-btn" onclick="setSport('mma', this)">MMA</button>
            <button class="sport-btn" onclick="setSport('sambo', this)">SAMBO</button>
            <button class="sport-btn" onclick="setSport('bjj', this)">BJJ</button>
            <button class="sport-btn" onclick="setSport('wrestling', this)">GÜREŞ</button>
            <button class="sport-btn" onclick="setSport('judo', this)">JUDO</button>
            <button class="sport-btn" onclick="setSport('karate', this)">KARATE</button>
            <button class="sport-btn" onclick="setSport('lethwei', this)">LETHWEI</button>
          </div>
        </div>

        <!-- 3. GENDER & STYLE -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <div>
            <div class="section-title">3. CİNSİYET</div>
            <div style="display: flex; gap: 6px; margin-top: 6px;">
              <button class="option-pill active" onclick="setGender('random', this)">KARIŞIK</button>
              <button class="option-pill" onclick="setGender('male', this)">ERKEK</button>
              <button class="option-pill" onclick="setGender('female', this)">KADIN</button>
            </div>
          </div>
          <div>
            <div class="section-title">4. ÇİZİM STİLİ</div>
            <div style="display: flex; gap: 6px; margin-top: 6px;">
              <button class="option-pill active" onclick="setStyle('random', this)">KARIŞIK</button>
              <button class="option-pill" onclick="setStyle('modern', this)">MODERN</button>
              <button class="option-pill" onclick="setStyle('baki', this)">BAKI</button>
              <button class="option-pill" onclick="setStyle('ippo', this)">IPPO</button>
            </div>
          </div>
        </div>

        <!-- 4. BATCH -->
        <div>
          <div class="section-title">5. ÜRETİM ADEDİ</div>
          <div class="batch-selector" style="margin-top: 8px;">
            <div class="batch-pill active" onclick="setBatchCount(1, this)">
              <div class="batch-label">1×</div>
            </div>
            <div class="batch-pill" onclick="setBatchCount(3, this)">
              <div class="batch-label">3×</div>
            </div>
            <div class="batch-pill" onclick="setBatchCount(5, this)">
              <div class="batch-label">5×</div>
            </div>
          </div>
        </div>

        <!-- SELECTION BADGE -->
        <div class="selection-badge" id="selectionBadge">
          
          <span id="selectionText">Teknik seçildi</span>
        </div>

        <!-- HERO BUTTON -->
        <button class="hero-btn" id="generateHeroBtn" onclick="handleHeroGenerate()">
          <span class="hero-btn-title" id="heroBtnText">OLUŞTUR</span>
        </button>

        <!-- ADVANCED DRAWER -->
        <div>
          <div class="drawer-toggle" onclick="toggleDrawer()">
            <div style="display: flex; align-items: center; gap: 8px;">
              <span>GELİŞMİŞ</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <button type="button" class="drawer-rnd-btn" onclick="event.stopPropagation(); randomizeAdvancedSettings(true);" title="Teknik, başlık ve düzeni rastgele karıştır">
                KARIŞTIR
              </button>
              <span id="drawerArrow">▼</span>
            </div>
          </div>
          <div class="drawer-content" id="advancedDrawer">
            <div class="form-group">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <label class="form-label">Teknik (Opsiyonel)</label>
                <button type="button" class="drawer-rnd-btn" onclick="randomizeAdvancedSettings(true)" style="padding: 2px 7px; font-size: 9px;" title="Rastgele teknik ve ayar seç">
                  RASTGELE SEÇ
                </button>
              </div>
              <select class="form-select" id="manualTechniqueSelect" onchange="onManualSelectTechnique(this.value)">
                <option value="">Rastgele</option>
              </select>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
              <div class="form-group">
                <label class="form-label">Başlık</label>
                <input class="form-input" id="posterTitle" value="">
              </div>
              <div class="form-group">
                <label class="form-label">Alt Başlık</label>
                <input class="form-input" id="posterTagline" value="">
              </div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
              <div class="form-group">
                <label class="form-label">Layout</label>
                <select class="form-select" id="layoutStyle">
                  <option value="Floating Tactical Callouts (Left/Right)">Floating Tactical (Varsayılan)</option>
                  <option value="Side Editorial Column (Magazine)">Side Editorial Column</option>
                  <option value="Cyberpunk Target Lock HUD">Cyberpunk Target Lock HUD</option>
                  <option value="Classic Bottom Card">Classic Bottom Card</option>
                  <option value="Dual-Wing Symmetrical Frame">Dual-Wing Symmetrical Frame</option>
                  <option value="Diagonal Kinetic Slash">Diagonal Kinetic Slash</option>
                  <option value="Tactical Blueprint Dossier">Tactical Blueprint Dossier</option>
                  <option value="Minimalist Brutalist Combat">Minimalist Brutalist Combat</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Renk Paleti</label>
                <select class="form-select" id="themeColor">
                  <option value="Crimson Red">Crimson Red (Kırmızı)</option>
                  <option value="Cyber Cyan">Cyber Cyan (Turkuaz)</option>
                  <option value="Golden Bronze">Golden Bronze (Altın)</option>
                  <option value="Toxic Emerald">Toxic Emerald (Yeşil)</option>
                  <option value="Electric Violet">Electric Violet (Mor)</option>
                  <option value="Solar Amber">Solar Amber (Turuncu)</option>
                  <option value="Ice Cobalt">Ice Cobalt (Mavi)</option>
                  <option value="Bloodline Ruby">Bloodline Ruby (Bordo)</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">Fighter Anime Prompt</label>
              <textarea class="form-textarea" id="fighterPrompt" rows="2"></textarea>
            </div>
            <div style="display: flex; gap: 8px;">
              <button class="secondary-btn" style="flex: 1;" onclick="generateWithCustomSettings()">
                ÖZEL AYARLARLA ÜRET
              </button>
              <button class="secondary-btn" type="button" style="flex: 0 0 auto; background: rgba(255,255,255,0.06); border-color: rgba(255,255,255,0.18);" onclick="randomizeAdvancedSettings(true)" title="Teknik, başlık, düzen ve paleti rastgele karıştır">
                KARIŞTIR
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- RIGHT: VIEWPORT -->
      <div class="viewport-card">
        <div class="viewport-tabs">
          <button class="view-tab active" id="tabPoster" onclick="switchPreviewTab('poster')">
            YAZILI POSTER
          </button>
          <button class="view-tab tab-clean" id="tabClean" onclick="switchPreviewTab('clean')">
            TEMİZ ÇİZİM
          </button>
          <button class="view-tab" onclick="openFullscreen()" title="Tam Ekran Aç" style="flex: 0 0 42px;">
            <span>↗</span>
          </button>
        </div>

        <div class="image-viewport" id="imageViewport">
          <div class="empty-state" id="placeholderState">
            <div class="empty-icon"></div>
            <div class="empty-title">...</div>
            <div class="empty-desc"></div>
          </div>

          <div class="progress-overlay" id="progressOverlay">
            <div class="spinner-ring"></div>
            <div style="font-family:'Rajdhani',sans-serif;font-size:18px;font-weight:700;letter-spacing:1px;" id="progressText">ÇİZİLİYOR...</div>
            <div style="font-size:12px;color:var(--text-muted);" id="progressSubtext">ToonYou Beta6 + 4x-UltraSharp HD</div>
            <div class="progress-bar-container">
              <div class="progress-bar-glow"></div>
            </div>
          </div>

          <img id="posterImg" class="preview-img" alt="Combat Poster" decoding="async">
          <img id="cleanImg" class="preview-img" alt="Clean Art" decoding="async">
        </div>

        <div class="action-bar" id="actionBar">
          <button class="dl-btn dl-btn-poster" onclick="downloadImage('poster')">
            POSTER İNDİR
          </button>
          <button class="dl-btn dl-btn-clean" id="downloadCleanBtn" onclick="downloadImage('clean')">
            TEMİZ ÇİZİM İNDİR
          </button>
        </div>
      </div>
    </div>

    <!-- GALLERY -->
    <div class="gallery-container">
      <div class="gallery-box">
        <div class="gallery-header">
          <div class="gallery-title">
            <span>GALERİ</span>
            <span class="gallery-count" id="galleryCount">0</span>
          </div>
          <button class="option-pill" onclick="fetchRecentGallery()" title="ComfyUI çıktı klasörünü tara" style="display:flex;align-items:center;gap:6px;padding:6px 14px;">
            <span>Yenile</span>
          </button>
        </div>
        <div class="gallery-strip" id="galleryStrip">
          <div class="gallery-empty">Henüz bu oturumda poster üretilmedi. "Rastgele Poster Oluştur"a basarak başlayın.</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ======================================================== -->
  <!-- 2. MASK VIEW                                             -->
  <!-- ======================================================== -->
  <div id="maskView" class="view-container">
    <div class="mask-grid">

      <!-- MAIN CANVAS AREA -->
      <div class="mask-canvas-box" id="canvas-area">
        <div id="drop-zone" onclick="document.getElementById('file-input').click()">
          <svg viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="currentColor" stroke-width="1.5" style="opacity:0.6;stroke:var(--purple);">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5"/>
          </svg>
          <div class="sample-actions" onclick="event.stopPropagation()">
            <span class="sample-label">ÖRNEK:</span>
            <button type="button" class="sample-btn" onclick="loadSampleMask('1080x1920')" title="1080×1920 Dikey Kare">1080×1920</button>
            <button type="button" class="sample-btn" onclick="loadSampleMask('1080x1350')" title="1080×1350 Feed Post Karesi">1080×1350</button>
          </div>
        </div>

        <div id="canvas-wrapper">
          <div id="canvas-container">
            <canvas id="bg-canvas"></canvas>
            <canvas id="draw-canvas"></canvas>
          </div>
          <div class="mask-legend">
            <div class="legend-tag">
              <span class="legend-color" style="background:rgba(255,38,70,0.85);box-shadow:0 0 8px rgba(255,38,70,0.6);"></span>
              <span><strong>Korumalı Alan:</strong> Animeye dönüşmez (orijinal video kalır)</span>
            </div>
            <span>•</span>
            <div class="legend-tag">
              <span class="legend-color" style="background:#111;border:1px solid #444;"></span>
              <span><strong>Boş Alan:</strong> Anime stiline dönüştürülür</span>
            </div>
          </div>
        </div>

        <input type="file" id="file-input" accept="image/*">
      </div>

      <!-- RIGHT MASK CONTROLS -->
      <div class="mask-controls">
        <div class="mask-sample-bar">
          <span class="sample-bar-title">ÖRNEK</span>
          <div class="sample-bar-btns">
            <button type="button" class="sample-btn" onclick="loadSampleMask('1080x1920')" title="1080×1920 Dikey Kare">1080×1920</button>
            <button type="button" class="sample-btn" onclick="loadSampleMask('1080x1350')" title="1080×1350 Feed Post Karesi">1080×1350</button>
          </div>
        </div>

        <div class="section-title">ÇİZİM ARAÇLARI</div>
        <div class="mask-tool-grid">
          <button class="tool-btn active" id="btn-rect" onclick="setMaskTool('rect')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="18" height="18" rx="2"/>
            </svg>
            Dikdörtgen
          </button>
          <button class="tool-btn" id="btn-brush" onclick="setMaskTool('brush')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M9.53 16.122a3 3 0 0 0-5.78 1.128 2.25 2.25 0 0 1-2.4 2.245 4.5 4.5 0 0 0 8.4-2.245c0-.399-.078-.78-.22-1.128Z"/>
            </svg>
            Fırça
          </button>
          <button class="tool-btn" id="btn-eraser" onclick="setMaskTool('eraser')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M15.75 9.75 3 22.5m13.5 0H3m15.75-15L9.375 16.875M20.25 6l-2.25-2.25M18 3.75l2.25 2.25"/>
            </svg>
            Silgi
          </button>
          <button class="tool-btn" id="btn-fill" onclick="setMaskTool('fill')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
            </svg>
            Tümünü Koru
          </button>
        </div>

        <div class="brush-slider-wrap">
          <div class="slider-header">
            <span>Fırça / Silgi Çapı</span>
            <span id="brush-label">30px</span>
          </div>
          <input type="range" id="brush-size" min="5" max="250" value="30"
            oninput="document.getElementById('brush-label').textContent = this.value + 'px'">
        </div>

        <div class="undo-row">
          <button class="secondary-btn" onclick="maskUndo()">↶ Geri Al</button>
          <button class="secondary-btn" onclick="maskRedo()">↷ İleri Al</button>
        </div>

        <div class="action-stack">
          <button class="btn-comfy-save" id="btn-save-comfy" onclick="saveMaskToComfyUI()">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
              <polyline points="17 21 17 13 7 13 7 21"></polyline>
              <polyline points="7 3 7 8 15 8"></polyline>
            </svg>
            ComfyUI'a Otomatik Kaydet
          </button>

          <button class="btn-mask-clear" id="btn-clear-mask" onclick="clearMask()" title="Tuvali temizler ve ComfyUI'a otomatik boş maske kaydeder">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            </svg>
            Maskeyi Temizle
          </button>
        </div>

        <div class="mask-status-bar">
          <span id="mask-status-text">Kare yükleyerek başlayın</span>
          <span class="pos" id="mask-cursor-pos"></span>
        </div>
      </div>
    </div>
  </div>

  <!-- FLOATING TOAST -->
  <div id="toast"></div>

  <!-- ======================================================== -->
  <!-- JAVASCRIPT LOGIC                                         -->
  <!-- ======================================================== -->
  <script>
    const COMFY_URL = "http://127.0.0.1:8188";
    const TECHNIQUES = {techniques_js};
    const SAMPLES = {samples_js};

    // SHARED TOAST NOTIFICATION
    const toastEl = document.getElementById('toast');
    function showToast(htmlMsg, type = 'success', duration = 4500) {{
      toastEl.className = 'toast-' + type + ' visible';
      toastEl.innerHTML = htmlMsg;
      clearTimeout(toastEl._timer);
      toastEl._timer = setTimeout(() => {{
        toastEl.classList.remove('visible');
      }}, duration);
    }}

    // ========================================================
    // ULTRA-MODERN VIEW SWITCHER & MAGNETIC SLIDER PILL
    // ========================================================
    let currentView = null;

    function updateNavIndicator() {{
      const activeTabEl = document.querySelector('.nav-tab.active');
      const pill = document.getElementById('navSliderPill');
      const switcher = document.getElementById('navSwitcher');
      if (!activeTabEl || !pill || !switcher) return;

      const tabRect = activeTabEl.getBoundingClientRect();
      const switcherRect = switcher.getBoundingClientRect();

      const left = tabRect.left - switcherRect.left;
      const width = tabRect.width;

      pill.style.transform = `translateX(${{left}}px)`;
      pill.style.width = `${{width}}px`;
      pill.classList.add('pill-active');

      if (activeTabEl.id === 'tabNavMask') {{
        pill.className = 'nav-slider-pill pill-active pill-mask';
      }} else {{
        pill.className = 'nav-slider-pill pill-active pill-poster';
      }}
    }}

    function switchStudioView(newView, isInitial = false) {{
      if (!isInitial && newView === currentView && document.querySelector('.view-container.active-view')) {{
        updateNavIndicator();
        return;
      }}

      const posterView = document.getElementById('posterView');
      const maskView = document.getElementById('maskView');
      const tabNavPoster = document.getElementById('tabNavPoster');
      const tabNavMask = document.getElementById('tabNavMask');

      const isGoingToMask = (newView === 'mask');
      const enterAnim = isGoingToMask ? 'anim-slide-in-right' : 'anim-slide-in-left';

      // Reset existing animation classes
      posterView.classList.remove('anim-slide-in-right', 'anim-slide-in-left');
      maskView.classList.remove('anim-slide-in-right', 'anim-slide-in-left');

      if (isGoingToMask) {{
        posterView.classList.remove('active-view');
        maskView.classList.add('active-view');
        if (!isInitial) maskView.classList.add(enterAnim);
        tabNavPoster.classList.remove('active');
        tabNavMask.classList.add('active');
        window.location.hash = '#mask';
        currentView = 'mask';
      }} else {{
        maskView.classList.remove('active-view');
        posterView.classList.add('active-view');
        if (!isInitial) posterView.classList.add(enterAnim);
        tabNavMask.classList.remove('active');
        tabNavPoster.classList.add('active');
        window.location.hash = '#poster';
        currentView = 'poster';
      }}

      updateNavIndicator();
    }}

    window.addEventListener('resize', updateNavIndicator);

    // SERVER HEALTH CHECK
    async function checkServer(showFeedback = false) {{
      if (document.hidden && !showFeedback) return;
      const dot = document.getElementById('statusDot');
      const text = document.getElementById('statusText');
      try {{
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 2000);
        const res = await fetch(`${{COMFY_URL}}/system_stats`, {{ method: 'GET', signal: controller.signal }});
        clearTimeout(timeoutId);
        if (res.ok) {{
          dot.className = "status-dot online";
          text.textContent = "COMFYUI AKTİF (8188)";
          if (showFeedback) showToast("ComfyUI sunucusu aktif ve hazır!", "success", 2500);
          return true;
        }}
      }} catch (e) {{}}
      dot.className = "status-dot offline";
      text.textContent = "COMFYUI BAĞLANTISI YOK";
      if (showFeedback) showToast("ComfyUI sunucusuna erişilemedi (127.0.0.1:8188).", "warning", 3000);
      return false;
    }}
    setInterval(checkServer, 10000);
    document.addEventListener('visibilitychange', () => {{
      if (!document.hidden) checkServer();
    }});
    checkServer();

    // ========================================================
    // POSTER STUDIO LOGIC
    // ========================================================
    let selectedFormat = '4:5';
    let selectedSport = 'all';
    let selectedGender = 'random';
    let selectedStyle = 'random';
    let selectedBatch = 1;
    let currentPosterUrl = null;
    let currentCleanUrl = null;
    let currentTitleName = "FIGHTER";
    let activePosterTab = 'poster';
    let galleryItems = [];

    const AVAILABLE_LAYOUTS = [
      "Floating Tactical Callouts (Left/Right)",
      "Side Editorial Column (Magazine)",
      "Cyberpunk Target Lock HUD",
      "Classic Bottom Card",
      "Dual-Wing Symmetrical Frame",
      "Diagonal Kinetic Slash",
      "Tactical Blueprint Dossier",
      "Minimalist Brutalist Combat"
    ];

    const AVAILABLE_PALETTES = [
      "Crimson Red",
      "Cyber Cyan",
      "Golden Bronze",
      "Toxic Emerald",
      "Electric Violet",
      "Solar Amber",
      "Ice Cobalt",
      "Bloodline Ruby"
    ];

    function updateAdvancedFields(tech, layout, palette, promptOverride = null) {{
      if (!tech) return;
      const titleEl = document.getElementById('posterTitle');
      const taglineEl = document.getElementById('posterTagline');
      const promptEl = document.getElementById('fighterPrompt');
      const layoutEl = document.getElementById('layoutStyle');
      const themeEl = document.getElementById('themeColor');
      const selectEl = document.getElementById('manualTechniqueSelect');

      if (titleEl) titleEl.value = tech.title || "";
      if (taglineEl) taglineEl.value = tech.tagline || "";
      if (promptEl) {{
        promptEl.value = promptOverride || buildEnrichedPrompt(tech.prompt);
      }}
      if (layoutEl && layout) layoutEl.value = layout;
      if (themeEl && palette) themeEl.value = palette;
      if (selectEl) {{
        const idx = TECHNIQUES.indexOf(tech);
        if (idx !== -1) selectEl.value = idx;
      }}
    }}

    function randomizeAdvancedSettings(notify = false) {{
      if (!TECHNIQUES || TECHNIQUES.length === 0) return;
      
      let pool = TECHNIQUES;
      if (selectedSport && selectedSport !== 'all') {{
        const filtered = TECHNIQUES.filter(t => t.sport === selectedSport);
        if (filtered.length > 0) pool = filtered;
      }}
      
      const randomTech = pool[Math.floor(Math.random() * pool.length)];
      const randomLayout = AVAILABLE_LAYOUTS[Math.floor(Math.random() * AVAILABLE_LAYOUTS.length)];
      const randomPalette = AVAILABLE_PALETTES[Math.floor(Math.random() * AVAILABLE_PALETTES.length)];
      
      updateAdvancedFields(randomTech, randomLayout, randomPalette);

      if (notify) {{
        showToast(`Gelişmiş ayarlar rastgele güncellendi: ${{randomTech.name}}`);
      }}
      return {{ tech: randomTech, layout: randomLayout, palette: randomPalette }};
    }}

    function setFormat(fmt) {{
      selectedFormat = fmt;
      document.getElementById('format45').classList.toggle('active', fmt === '4:5');
      document.getElementById('format916').classList.toggle('active', fmt === '9:16');
      const vp = document.getElementById('imageViewport');
      vp.classList.toggle('ratio-story', fmt === '9:16');
    }}

    function setSport(sport, btn) {{
      selectedSport = sport;
      document.querySelectorAll('.sport-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      randomizeAdvancedSettings();
    }}

    function setGender(gender, btn) {{
      selectedGender = gender;
      btn.parentElement.querySelectorAll('.option-pill').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const promptEl = document.getElementById('fighterPrompt');
      if (promptEl && promptEl.value) {{
        promptEl.value = applyGenderToPrompt(promptEl.value, gender);
      }}
    }}

    function setStyle(style, btn) {{
      selectedStyle = style;
      btn.parentElement.querySelectorAll('.option-pill').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    }}

    function setBatchCount(count, pill) {{
      selectedBatch = count;
      document.querySelectorAll('.batch-pill').forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      const btnTitle = document.getElementById('heroBtnText');
      const btnSub = document.getElementById('heroBtnSubtext');
      if (count === 1) {{
        btnTitle.textContent = "RASTGELE POSTER OLUŞTUR";
        btnSub.textContent = `${{TECHNIQUES.length}} dövüş tekniği ve 8 tasarım düzeni arasından otomatik çizer`;
      }} else if (count === 3) {{
        btnTitle.textContent = "3'LÜ SERİ OLUŞTUR";
        btnSub.textContent = "3 farklı tekniği ve düzeni sırayla otomatik üretip galeriye ekler";
      }} else {{
        btnTitle.textContent = "5'Lİ TOPLU OLUŞTUR";
        btnSub.textContent = "5 farklı tekniği ve düzeni sırayla otomatik üretip galeriye ekler";
      }}
    }}

    function toggleDrawer() {{
      const drawer = document.getElementById('advancedDrawer');
      const arrow = document.getElementById('drawerArrow');
      drawer.classList.toggle('open');
      arrow.textContent = drawer.classList.contains('open') ? '▲' : '▼';
    }}

    function switchPreviewTab(tab) {{
      activePosterTab = tab;
      document.getElementById('tabPoster').classList.toggle('active', tab === 'poster');
      document.getElementById('tabClean').classList.toggle('active', tab === 'clean');
      updatePreviewDisplay();
    }}

    function updatePreviewDisplay() {{
      const posterImg = document.getElementById('posterImg');
      const cleanImg = document.getElementById('cleanImg');
      const placeholder = document.getElementById('placeholderState');
      const actionBar = document.getElementById('actionBar');
      const tabClean = document.getElementById('tabClean');
      const downloadCleanBtn = document.getElementById('downloadCleanBtn');

      if (!currentPosterUrl && !currentCleanUrl) {{
        placeholder.style.display = 'flex';
        actionBar.style.display = 'none';
        posterImg.style.display = 'none';
        cleanImg.style.display = 'none';
        return;
      }}

      placeholder.style.display = 'none';
      actionBar.style.display = 'flex';

      const hasClean = Boolean(currentCleanUrl);
      tabClean.style.opacity = hasClean ? '1' : '0.45';
      downloadCleanBtn.disabled = !hasClean;
      downloadCleanBtn.style.opacity = hasClean ? '1' : '0.45';

      if (activePosterTab === 'clean' && !hasClean) {{
        activePosterTab = 'poster';
        document.getElementById('tabPoster').classList.add('active');
        document.getElementById('tabClean').classList.remove('active');
      }}

      if (activePosterTab === 'poster') {{
        posterImg.style.display = 'block';
        cleanImg.style.display = 'none';
      }} else {{
        posterImg.style.display = 'none';
        cleanImg.style.display = 'block';
      }}
    }}

    function openFullscreen() {{
      const targetUrl = (activePosterTab === 'poster') ? currentPosterUrl : currentCleanUrl;
      if (targetUrl) window.open(targetUrl, '_blank');
    }}

    async function downloadImage(type) {{
      const url = (type === 'poster') ? currentPosterUrl : currentCleanUrl;
      if (!url) return;
      const safeTitle = (currentTitleName || "fighter").toLowerCase().replace(/[^a-z0-9]/g, '_');
      const filename = (type === 'poster') ? `ringpulse_poster_${{safeTitle}}.png` : `ringpulse_clean_art_${{safeTitle}}.png`;
      try {{
        const res = await fetch(url);
        const blob = await res.blob();
        const blobUrl = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = blobUrl;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(() => URL.revokeObjectURL(blobUrl), 1000);
      }} catch (err) {{
        window.open(url, '_blank');
      }}
    }}

    function applyGenderToPrompt(text, genderChoice) {{
      if (!text) return "";
      let targetGender = genderChoice;
      if (targetGender === 'random') {{
        targetGender = (Math.random() < 0.5) ? 'female' : 'male';
      }}

      if (targetGender === 'female') {{
        let res = text
          .replace(/\\b1man\\b/gi, '1woman')
          .replace(/\\b1boy\\b/gi, '1girl')
          .replace(/\\bman\\b/gi, 'woman')
          .replace(/\\bboy\\b/gi, 'girl')
          .replace(/\\bmale fighter\\b/gi, 'female fighter')
          .replace(/\\bmale boxer\\b/gi, 'female boxer')
          .replace(/\\bmale\\b/gi, 'female')
          .replace(/muscular boxer/gi, 'athletic toned female boxer')
          .replace(/muscular fighter/gi, 'athletic toned female fighter')
          .replace(/athletic muscular/gi, 'athletic toned muscular female')
          .replace(/heavyweight boxer/gi, 'fierce female champion boxer')
          .replace(/handsome/gi, 'beautiful fierce');
        if (!res.includes('1woman') && !res.includes('female')) {{
          res = res.replace(/masterpiece, best quality, /i, 'masterpiece, best quality, 1woman, ');
        }}
        return res;
      }} else {{
        let res = text
          .replace(/\\b1woman\\b/gi, '1man')
          .replace(/\\b1girl\\b/gi, '1boy')
          .replace(/\\bwoman\\b/gi, 'man')
          .replace(/\\bgirl\\b/gi, 'boy')
          .replace(/\\bfemale fighter\\b/gi, 'male fighter')
          .replace(/\\bfemale boxer\\b/gi, 'male boxer')
          .replace(/\\bfemale\\b/gi, 'male')
          .replace(/beautiful fierce/gi, 'handsome sharp');
        if (!res.includes('1man') && !res.includes('male')) {{
          res = res.replace(/masterpiece, best quality, /i, 'masterpiece, best quality, 1man, ');
        }}
        return res;
      }}
    }}

    function buildEnrichedPrompt(basePrompt, gender = null, style = null) {{
      let prompt = basePrompt || "";
      let genderChoice = gender || selectedGender;

      if (genderChoice === 'random') {{
        genderChoice = (Math.random() < 0.5) ? 'female' : 'male';
      }}

      prompt = applyGenderToPrompt(prompt, genderChoice);

      // Advanced anatomical perfection & muscle striation boosters
      if (!prompt.includes('anatomically correct')) {{
        if (genderChoice === 'female') {{
          prompt += ", athletic toned female fighter, defined feminine abs, fierce battle-ready expression, (perfect female athletic anatomy, anatomically correct:1.2), (detailed hands, 5 fingers:1.15), (correct muscle anatomy, well-defined muscle striations, natural dynamic fighting pose:1.15)";
        }} else {{
          prompt += ", athletic muscular male fighter, sharp jawline, ripped chiseled physique, (perfect male athletic anatomy, anatomically correct:1.2), (detailed hands, 5 fingers:1.15), (correct muscle anatomy, well-defined muscle striations, natural dynamic fighting pose:1.15)";
        }}
      }}

      let styleChoice = style || selectedStyle;
      if (styleChoice === 'random') {{
        const styles = ['modern', 'baki', 'ippo', 'cyber'];
        styleChoice = styles[Math.floor(Math.random() * styles.length)];
      }}

      if (!prompt.includes('baki manga') && !prompt.includes('ippo') && !prompt.includes('cyberpunk anime') && !prompt.includes('cinematic anime combat')) {{
        if (styleChoice === 'baki') {{
          prompt += ", baki manga style, kengan ashura, extreme muscular vascularity, heavy impact lines, brutal combat anatomy, veins popping, high contrast grit";
        }} else if (styleChoice === 'ippo') {{
          prompt += ", classic 90s boxing shonen anime style, hajime no ippo style, heavy ink outlines, sweat bursts, dynamic speed lines, retro anime grit";
        }} else if (styleChoice === 'cyber') {{
          prompt += ", cyberpunk anime fighter, glowing neon combat tattoos, dark gym, rain reflections, neon lens flares, futuristic combat gear";
        }} else {{
          prompt += ", cinematic anime combat, vibrant volumetric lighting, sharp cel-shaded, dramatic rim lighting, masterwork anime illustration";
        }}
      }}
      return prompt;
    }}

    async function handleHeroGenerate() {{
      const count = selectedBatch;
      const btn = document.getElementById('generateHeroBtn');
      btn.disabled = true;

      try {{
        let pool = TECHNIQUES;
        if (selectedSport !== 'all') {{
          pool = TECHNIQUES.filter(t => t.sport === selectedSport);
          if (pool.length === 0) pool = TECHNIQUES;
        }}

        const shuffled = [...pool].sort(() => 0.5 - Math.random());
        const selectedTechs = shuffled.slice(0, count);

        for (let i = 0; i < selectedTechs.length; i++) {{
          const tech = selectedTechs[i];
          const randomLayout = AVAILABLE_LAYOUTS[Math.floor(Math.random() * AVAILABLE_LAYOUTS.length)];
          const randomPalette = AVAILABLE_PALETTES[Math.floor(Math.random() * AVAILABLE_PALETTES.length)];
          
          const itemGender = (selectedGender === 'random') ? ((Math.random() < 0.5) ? 'female' : 'male') : selectedGender;
          const finalPrompt = buildEnrichedPrompt(tech.prompt, itemGender);

          // Dynamically synchronize advanced drawer inputs with each random generation
          updateAdvancedFields(tech, randomLayout, randomPalette, finalPrompt);

          const badge = document.getElementById('selectionBadge');
          const badgeText = document.getElementById('selectionText');
          badge.style.display = 'flex';
          badgeText.textContent = `[${{i + 1}}/${{count}}] ${{tech.name}} • ${{tech.sport.toUpperCase()}} • ${{randomLayout.split('(')[0].trim()}} • ${{randomPalette}}`;

          await triggerWorkflowExecution({{
            prompt: finalPrompt,
            title: tech.title,
            tagline: tech.tagline,
            protocol: tech.protocol,
            cardTitle: "/// EXECUTION KEYPOINTS",
            target: tech.target,
            caution: tech.caution,
            range: tech.range,
            tip1Tag: tech.tip1Tag,
            tip1Desc: tech.tip1Desc,
            tip2Tag: tech.tip2Tag,
            tip2Desc: tech.tip2Desc,
            tip3Tag: tech.tip3Tag,
            tip3Desc: tech.tip3Desc,
            theme: randomPalette,
            layout: randomLayout,
            sport: tech.sport,
            batchIndex: i + 1,
            batchTotal: count
          }});
        }}
      }} finally {{
        btn.disabled = false;
      }}
    }}

    function generateWithCustomSettings() {{
      const title = document.getElementById('posterTitle').value.trim();
      const tagline = document.getElementById('posterTagline').value.trim();
      const rawPrompt = document.getElementById('fighterPrompt').value.trim();
      const layout = document.getElementById('layoutStyle').value;
      const theme = document.getElementById('themeColor').value;
      const finalPrompt = buildEnrichedPrompt(rawPrompt);

      const badge = document.getElementById('selectionBadge');
      const badgeText = document.getElementById('selectionText');
      badge.style.display = 'flex';
      badgeText.textContent = `Özel: "${{title}}" • ${{layout.split('(')[0].trim()}} • ${{theme}}`;

      triggerWorkflowExecution({{
        prompt: finalPrompt,
        title: title,
        tagline: tagline,
        protocol: "[ COMBAT LAB // CUSTOM ]",
        cardTitle: "/// EXECUTION KEYPOINTS",
        target: "V_TARGET: MULTI-ZONE",
        caution: "AVOID OVER-EXTENSION",
        range: "FIGHT DISTANCE [1.0M]",
        tip1Tag: "KINETIC CHAIN",
        tip1Desc: "Engage lower kinetic chain through hips and core for maximum leverage.",
        tip2Tag: "GUARD STABILITY",
        tip2Desc: "Maintain structural guard integrity throughout the execution phase.",
        tip3Tag: "COUNTER DRILL",
        tip3Desc: "Immediately angle step off the opponent centerline upon completion.",
        theme: theme,
        layout: layout,
        sport: "custom",
        batchIndex: 1,
        batchTotal: 1
      }});
    }}

    async function triggerWorkflowExecution(params) {{
      const overlay = document.getElementById('progressOverlay');
      const progressText = document.getElementById('progressText');
      const progressSubtext = document.getElementById('progressSubtext');

      overlay.style.display = 'flex';
      const batchPrefix = params.batchTotal > 1 ? `[${{params.batchIndex}}/${{params.batchTotal}}] ` : "";
      progressText.textContent = `${{batchPrefix}}KUYRUĞA ALINIYOR...`;
      progressSubtext.textContent = `"${{params.title}}"`;

      const seedVal = Math.floor(Math.random() * 999999999);
      const isFeed = (selectedFormat === '4:5');
      const latentW = isFeed ? 640 : 540;
      const latentH = isFeed ? 800 : 960;
      const resMode = isFeed ? "1080x1350 (4:5 Feed Post)" : "1080x1920 (9:16 Story/Reel)";

      let themeColorVal = params.theme || "Crimson Red";
      if (themeColorVal === "Golden Bronze") themeColorVal = "UFC Gold";
      else if (themeColorVal === "Toxic Emerald") themeColorVal = "Emerald Green";

      const promptWorkflow = {{
        "1": {{
          "class_type": "CheckpointLoaderSimple",
          "inputs": {{ "ckpt_name": "toonyou_beta6.safetensors" }}
        }},
        "2": {{
          "class_type": "LoraLoader",
          "inputs": {{
            "model": ["1", 0],
            "clip": ["1", 1],
            "lora_name": "more_details.safetensors",
            "strength_model": 0.6,
            "strength_clip": 0.6
          }}
        }},
        "3": {{
          "class_type": "CLIPTextEncode",
          "inputs": {{
            "clip": ["2", 1],
            "text": params.prompt
          }}
        }},
        "4": {{
          "class_type": "CLIPTextEncode",
          "inputs": {{
            "clip": ["2", 1],
            "text": "worst quality, low quality, (bad anatomy, bad hands, mutated hands, missing fingers, extra fingers, malformed limbs, deformed limbs, deformed feet, floating limbs, disconnected limbs, mutation, gross proportions, poorly drawn face, disfigured:1.3), (flat shading, undefined flabby muscles, distorted body, extra arms, extra legs:1.2), blurry, out of focus, motion blur, text, watermark, signature, jpeg artifacts"
          }}
        }},
        "5": {{
          "class_type": "EmptyLatentImage",
          "inputs": {{ "width": latentW, "height": latentH, "batch_size": 1 }}
        }},
        "6": {{
          "class_type": "KSampler",
          "inputs": {{
            "model": ["2", 0],
            "positive": ["3", 0],
            "negative": ["4", 0],
            "latent_image": ["5", 0],
            "seed": seedVal,
            "steps": 24,
            "cfg": 7.2,
            "sampler_name": "dpmpp_2m",
            "scheduler": "karras",
            "denoise": 1.0
          }}
        }},
        "7": {{
          "class_type": "VAEDecode",
          "inputs": {{ "samples": ["6", 0], "vae": ["1", 2] }}
        }},
        "8": {{
          "class_type": "UpscaleModelLoader",
          "inputs": {{ "model_name": "4x-UltraSharp.pth" }}
        }},
        "9": {{
          "class_type": "ImageUpscaleWithModel",
          "inputs": {{ "upscale_model": ["8", 0], "image": ["7", 0] }}
        }},
        "10": {{
          "class_type": "FighterPosterDesigner",
          "inputs": {{
            "image": ["9", 0],
            "title": params.title,
            "tagline": params.tagline,
            "protocol_badge": params.protocol,
            "watermark": "@ringpulseofficial",
            "card_title": params.cardTitle,
            "target_zone": params.target,
            "tip_1_tag": params.tip1Tag,
            "tip_1_desc": params.tip1Desc,
            "tip_2_tag": params.tip2Tag,
            "tip_2_desc": params.tip2Desc,
            "tip_3_tag": params.tip3Tag,
            "tip_3_desc": params.tip3Desc,
            "theme_color": themeColorVal,
            "layout_archetype": params.layout,
            "resolution_mode": resMode,
            "caution_flaw": params.caution,
            "range_class": params.range
          }}
        }},
        "11": {{
          "class_type": "SaveImage",
          "inputs": {{
            "filename_prefix": "fighter_posters/ringpulse_poster",
            "images": ["10", 0]
          }}
        }},
        "12": {{
          "class_type": "SaveImage",
          "inputs": {{
            "filename_prefix": "fighter_posters/ringpulse_clean",
            "images": ["10", 1]
          }}
        }}
      }};

      try {{
        progressText.textContent = `${{batchPrefix}}COMFYUI'A GÖNDERİLDİ`;
        const queueRes = await fetch(`${{COMFY_URL}}/prompt`, {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{ prompt: promptWorkflow }})
        }});

        if (!queueRes.ok) {{
          let errDetail = `Sunucu hatası (${{queueRes.status}})`;
          try {{
            const errData = await queueRes.json();
            if (errData.node_errors) {{
              const nodeKeys = Object.keys(errData.node_errors);
              if (nodeKeys.length > 0) {{
                const firstErr = errData.node_errors[nodeKeys[0]].errors[0];
                errDetail = `${{firstErr.message}}: ${{firstErr.details || ""}}`;
              }}
            }} else if (errData.error) {{
              errDetail = typeof errData.error === 'string' ? errData.error : (errData.error.message || JSON.stringify(errData.error));
            }}
          }} catch(e) {{}}
          throw new Error("ComfyUI kuyruk hatası: " + errDetail);
        }}

        const queueData = await queueRes.json();
        const promptId = queueData.prompt_id;
        if (!promptId) {{
          throw new Error("ComfyUI prompt ID döndürmedi.");
        }}

        progressText.textContent = `${{batchPrefix}}ÇİZİLİYOR...`;
        progressSubtext.textContent = "ToonYou Beta6 + 4x-UltraSharp HD";

        let completed = false;
        const maxPolls = 60;
        for (let i = 0; i < maxPolls; i++) {{
          await new Promise(r => setTimeout(r, 1500));
          progressSubtext.textContent = `ToonYou Beta6 + 4x-UltraSharp HD (${{Math.round((i + 1) * 1.5)}}s)`;

          try {{
            const histRes = await fetch(`${{COMFY_URL}}/history/${{promptId}}`);
            if (!histRes.ok) continue;
            const histData = await histRes.json();

            if (promptId in histData) {{
              const histItem = histData[promptId];
              if (histItem.status && histItem.status.status_str === "error") {{
                let errReason = "Model üretim hatası";
                if (histItem.status.messages) {{
                  for (const msg of histItem.status.messages) {{
                    if (msg[0] === "execution_error" && msg[1]) {{
                      errReason = msg[1].exception_message || msg[1].exception_type || errReason;
                    }}
                  }}
                }}
                throw new Error("ComfyUI üretim hatası: " + errReason);
              }}

              const outputs = histItem.outputs || {{}};
              let posterUrl = null;
              let cleanUrl = null;

              if ("11" in outputs && outputs["11"].images && outputs["11"].images.length > 0) {{
                const imgObj = outputs["11"].images[0];
                posterUrl = `${{COMFY_URL}}/view?filename=${{encodeURIComponent(imgObj.filename)}}&subfolder=${{encodeURIComponent(imgObj.subfolder || "")}}&type=${{encodeURIComponent(imgObj.type || "output")}}`;
              }}
              if ("12" in outputs && outputs["12"].images && outputs["12"].images.length > 0) {{
                const imgObj = outputs["12"].images[0];
                cleanUrl = `${{COMFY_URL}}/view?filename=${{encodeURIComponent(imgObj.filename)}}&subfolder=${{encodeURIComponent(imgObj.subfolder || "")}}&type=${{encodeURIComponent(imgObj.type || "output")}}`;
              }}

              if (posterUrl) {{
                displayResult(posterUrl, cleanUrl, params.title);
                addToGallery({{
                  title: params.title,
                  sport: params.sport || "COMBAT",
                  posterUrl: posterUrl,
                  cleanUrl: cleanUrl
                }});
                completed = true;
                break;
              }}
            }}
          }} catch (pollErr) {{
            if (pollErr.message && pollErr.message.includes("ComfyUI üretim hatası")) {{
              throw pollErr;
            }}
          }}
        }}

        if (!completed) {{
          showToast("Oluşturma zaman aşımına uğradı (90s).", "warning");
        }}
      }} catch (err) {{
        console.error(err);
        showToast("Poster oluşturulurken hata: " + err.message, "error");
      }} finally {{
        overlay.style.display = 'none';
        checkServer();
      }}
    }}

    function displayResult(posterUrl, cleanUrl, titleName) {{
      currentPosterUrl = posterUrl || null;
      currentCleanUrl = cleanUrl || null;
      currentTitleName = titleName || "FIGHTER";
      const posterImg = document.getElementById('posterImg');
      const cleanImg = document.getElementById('cleanImg');

      if (posterUrl) posterImg.src = posterUrl;
      if (cleanUrl) cleanImg.src = cleanUrl;
      else cleanImg.removeAttribute('src');

      if (activePosterTab === 'clean' && !cleanUrl) {{
        activePosterTab = 'poster';
        document.getElementById('tabPoster').classList.add('active');
        document.getElementById('tabClean').classList.remove('active');
      }}
      updatePreviewDisplay();
    }}

    function addToGallery(item) {{
      galleryItems.unshift(item);
      renderGallery();
    }}

    function renderGallery() {{
      const strip = document.getElementById('galleryStrip');
      const countBadge = document.getElementById('galleryCount');
      countBadge.textContent = galleryItems.length;

      if (galleryItems.length === 0) {{
        strip.innerHTML = '<div class="gallery-empty">Henüz bu oturumda poster üretilmedi. "Rastgele Poster Oluştur"a basarak başlayın.</div>';
        return;
      }}

      strip.innerHTML = '';
      galleryItems.forEach((item, idx) => {{
        const card = document.createElement('div');
        card.className = `gallery-card ${{idx === 0 ? 'active' : ''}}`;
        card.onclick = () => {{
          document.querySelectorAll('.gallery-card').forEach(c => c.classList.remove('active'));
          card.classList.add('active');
          displayResult(item.posterUrl, item.cleanUrl, item.title);
        }};

        const img = document.createElement('img');
        img.className = 'gallery-thumb';
        img.src = item.posterUrl;
        img.loading = 'lazy';
        img.decoding = 'async';

        const label = document.createElement('div');
        label.className = 'gallery-card-label';
        label.textContent = item.title;

        card.appendChild(img);
        if (item.cleanUrl) {{
          const cleanBadge = document.createElement('span');
          cleanBadge.className = 'gallery-clean-pill';
          cleanBadge.textContent = 'ART';
          card.appendChild(cleanBadge);
        }}
        card.appendChild(label);
        strip.appendChild(card);
      }});
    }}

    async function fetchRecentGallery() {{
      try {{
        const res = await fetch(`${{COMFY_URL}}/history`);
        const data = await res.json();
        const recentEntries = [];

        Object.keys(data).forEach(id => {{
          const entry = data[id];
          const outputs = entry.outputs || {{}};
          let pObj = null, cObj = null;

          for (const nid of Object.keys(outputs)) {{
            const nOut = outputs[nid];
            if (nOut && nOut.images && nOut.images.length > 0) {{
              for (const img of nOut.images) {{
                const fn = (img.filename || "").toLowerCase();
                if (fn.includes('clean')) cObj = img;
                else if (fn.includes('poster')) pObj = img;
              }}
            }}
          }}

          if (!pObj && outputs["11"] && outputs["11"].images && outputs["11"].images.length > 0) {{
            pObj = outputs["11"].images[0];
          }}
          if (!cObj && outputs["12"] && outputs["12"].images && outputs["12"].images.length > 0) {{
            cObj = outputs["12"].images[0];
          }}

          if (pObj || cObj) {{
            const posterImgObj = pObj || cObj;
            const pUrl = `${{COMFY_URL}}/view?filename=${{encodeURIComponent(posterImgObj.filename)}}&subfolder=${{encodeURIComponent(posterImgObj.subfolder || "")}}&type=${{encodeURIComponent(posterImgObj.type || "output")}}`;
            const cUrl = cObj ? `${{COMFY_URL}}/view?filename=${{encodeURIComponent(cObj.filename)}}&subfolder=${{encodeURIComponent(cObj.subfolder || "")}}&type=${{encodeURIComponent(cObj.type || "output")}}` : null;

            let title = posterImgObj.filename.replace('.png', '').replace('ringpulse_poster_', '').replace('ringpulse_clean_', '').replace(/_/g, ' ').toUpperCase();
            try {{
              if (entry.prompt && entry.prompt.length > 2) {{
                const pNodes = entry.prompt[2];
                for (const k of Object.keys(pNodes)) {{
                  if (pNodes[k].class_type === "FighterPosterDesigner" && pNodes[k].inputs && pNodes[k].inputs.title) {{
                    title = pNodes[k].inputs.title;
                    break;
                  }}
                }}
              }}
            }} catch (e) {{}}

            recentEntries.push({{
              title: title,
              sport: "COMBAT",
              posterUrl: pUrl,
              cleanUrl: cUrl
            }});
          }}
        }});

        if (recentEntries.length > 0) {{
          galleryItems = recentEntries.reverse().slice(0, 24);
          renderGallery();
        }}
      }} catch (e) {{
        console.warn("Could not fetch ComfyUI history for gallery:", e);
      }}
    }}

    function populateDropdown() {{
      const select = document.getElementById('manualTechniqueSelect');
      if (!select) return;
      select.innerHTML = '<option value="">Rastgele</option>';
      TECHNIQUES.forEach((t, idx) => {{
        const opt = document.createElement('option');
        opt.value = idx;
        opt.textContent = `${{t.name}} [${{t.sport.toUpperCase()}}]`;
        select.appendChild(opt);
      }});
    }}

    function onManualSelectTechnique(idx) {{
      if (idx === "" || idx === undefined) {{
        randomizeAdvancedSettings(false);
        return;
      }}
      const t = TECHNIQUES[parseInt(idx)];
      if (!t) return;
      document.getElementById('posterTitle').value = t.title || "";
      document.getElementById('posterTagline').value = t.tagline || "";
      document.getElementById('fighterPrompt').value = t.prompt || "";
    }}

    // ========================================================
    // MASK TOOL LOGIC
    // ========================================================
    let maskTool = 'rect';
    let maskDrawing = false;
    let maskStartX = 0, maskStartY = 0;
    let maskBrushSize = 30;
    let maskImgW = 0, maskImgH = 0;
    let maskOrigImgW = 0, maskOrigImgH = 0;
    let maskHistory = [];
    let maskHistIdx = -1;
    let maskRectSnapshot = null;

    const bgCanvas       = document.getElementById('bg-canvas');
    const drawCanvas     = document.getElementById('draw-canvas');
    const bgCtx          = bgCanvas.getContext('2d');
    const drawCtx        = drawCanvas.getContext('2d');
    const maskContainer  = document.getElementById('canvas-container');
    const maskDropZone   = document.getElementById('drop-zone');
    const maskWrapper    = document.getElementById('canvas-wrapper');
    const maskFileInput  = document.getElementById('file-input');
    const maskStatusText = document.getElementById('mask-status-text');
    const maskCursorEl   = document.getElementById('mask-cursor-pos');

    drawCanvas.style.opacity = '0.65';
    drawCanvas.style.filter  = 'invert(30%) sepia(100%) saturate(700%) hue-rotate(300deg) brightness(1.1)';

    maskFileInput.addEventListener('change', e => loadMaskFile(e.target.files[0]));
    document.addEventListener('dragover', e => e.preventDefault());
    document.addEventListener('drop', e => {{
      e.preventDefault();
      if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {{
        loadMaskFile(e.dataTransfer.files[0]);
      }}
    }});

    function loadMaskFile(file) {{
      if (!file || !file.type.startsWith('image/')) return;
      const objectUrl = URL.createObjectURL(file);
      const img = new Image();
      img.onload = () => {{
        initMaskCanvas(img);
        URL.revokeObjectURL(objectUrl);
      }};
      img.onerror = () => {{
        URL.revokeObjectURL(objectUrl);
        showToast('Görsel yüklenemedi', 'error');
      }};
      img.src = objectUrl;
    }}

    function initMaskCanvas(img) {{
      maskOrigImgW = img.naturalWidth || img.width;
      maskOrigImgH = img.naturalHeight || img.height;

      const area = document.getElementById('canvas-area');
      const MAX_H = Math.max(window.innerHeight - 200, 500);
      const MAX_W = area ? (area.clientWidth - 40) : 800;
      let scale = Math.min(MAX_H / maskOrigImgH, MAX_W / maskOrigImgW, 1);
      maskImgW = Math.round(maskOrigImgW * scale);
      maskImgH = Math.round(maskOrigImgH * scale);

      [bgCanvas, drawCanvas].forEach(c => {{
        c.width  = maskImgW;
        c.height = maskImgH;
        c.style.width  = maskImgW + 'px';
        c.style.height = maskImgH + 'px';
        c.style.position = 'absolute';
      }});
      maskContainer.style.width  = maskImgW + 'px';
      maskContainer.style.height = maskImgH + 'px';

      bgCtx.drawImage(img, 0, 0, maskImgW, maskImgH);
      drawCtx.clearRect(0, 0, maskImgW, maskImgH);

      maskHistory = [];
      maskHistIdx = -1;
      saveMaskHistory();

      maskDropZone.classList.add('hidden');
      maskWrapper.classList.add('visible');
      maskStatusText.textContent = `${{maskOrigImgW}}x${{maskOrigImgH}}`;
    }}

    function loadSampleMask(type) {{
      const key = 'sample_' + type;
      const src = SAMPLES[key];
      if (!src) {{
        showToast('Örnek fotoğraf bulunamadı', 'warning');
        return;
      }}
      const img = new Image();
      img.onload = () => {{
        initMaskCanvas(img);
        showToast(`${{type}} hazır!`, 'info', 1800);
      }};
      img.onerror = () => {{
        showToast('Örnek fotoğraf yüklenemedi', 'error');
      }};
      img.src = src;
    }}

    function setMaskTool(t) {{
      maskTool = t;
      ['rect','brush','eraser','fill'].forEach(id => {{
        document.getElementById('btn-' + id)?.classList.toggle('active', id === t);
      }});
    }}

    function maskPos(e) {{
      const r = drawCanvas.getBoundingClientRect();
      const scaleX = maskImgW / r.width;
      const scaleY = maskImgH / r.height;
      return {{
        x: Math.round((e.clientX - r.left) * scaleX),
        y: Math.round((e.clientY - r.top) * scaleY)
      }};
    }}

    drawCanvas.addEventListener('mousedown', e => {{
      maskDrawing = true;
      const p = maskPos(e);
      maskStartX = p.x; maskStartY = p.y;

      if (maskTool === 'fill') {{
        drawCtx.fillStyle = 'rgba(255, 50, 50, 0.9)';
        drawCtx.fillRect(0, 0, maskImgW, maskImgH);
        maskDrawing = false;
        saveMaskHistory();
        return;
      }}
      if (maskTool === 'rect') {{
        maskRectSnapshot = drawCtx.getImageData(0, 0, maskImgW, maskImgH);
      }} else {{
        drawCtx.beginPath();
        drawCtx.moveTo(p.x, p.y);
      }}
    }});

    drawCanvas.addEventListener('mousemove', e => {{
      const p = maskPos(e);
      maskCursorEl.textContent = `${{p.x}}, ${{p.y}}`;
      if (!maskDrawing) return;

      maskBrushSize = parseInt(document.getElementById('brush-size').value) || 30;

      if (maskTool === 'rect') {{
        drawCtx.putImageData(maskRectSnapshot, 0, 0);
        drawCtx.fillStyle = 'rgba(255, 50, 50, 0.85)';
        drawCtx.fillRect(maskStartX, maskStartY, p.x - maskStartX, p.y - maskStartY);
      }} else if (maskTool === 'brush') {{
        drawCtx.globalCompositeOperation = 'source-over';
        drawCtx.strokeStyle = 'rgba(255, 50, 50, 0.9)';
        drawCtx.lineWidth = maskBrushSize;
        drawCtx.lineCap = 'round';
        drawCtx.lineJoin = 'round';
        drawCtx.lineTo(p.x, p.y);
        drawCtx.stroke();
      }} else if (maskTool === 'eraser') {{
        drawCtx.globalCompositeOperation = 'destination-out';
        drawCtx.lineWidth = maskBrushSize;
        drawCtx.lineCap = 'round';
        drawCtx.lineJoin = 'round';
        drawCtx.lineTo(p.x, p.y);
        drawCtx.stroke();
        drawCtx.globalCompositeOperation = 'source-over';
      }}
    }});

    window.addEventListener('mouseup', () => {{
      if (maskDrawing) {{
        maskDrawing = false;
        drawCtx.closePath();
        saveMaskHistory();
      }}
    }});

    function saveMaskHistory() {{
      maskHistIdx++;
      maskHistory = maskHistory.slice(0, maskHistIdx);
      maskHistory.push(drawCtx.getImageData(0, 0, maskImgW, maskImgH));
      if (maskHistory.length > 25) {{
        maskHistory.shift();
        maskHistIdx--;
      }}
    }}

    function maskUndo() {{
      if (maskHistIdx <= 0) return;
      maskHistIdx--;
      drawCtx.putImageData(maskHistory[maskHistIdx], 0, 0);
      maskStatusText.textContent = 'Geri alındı';
    }}

    function maskRedo() {{
      if (maskHistIdx >= maskHistory.length - 1) return;
      maskHistIdx++;
      drawCtx.putImageData(maskHistory[maskHistIdx], 0, 0);
      maskStatusText.textContent = 'İleri alındı';
    }}

    async function uploadMaskBlob(blob) {{
      const formData = new FormData();
      formData.append('image', blob, 'protection_mask.png');
      formData.append('overwrite', 'true');
      formData.append('type', 'input');

      // 1. Standart ComfyUI endpoint
      try {{
        const resp = await fetch(`${{COMFY_URL}}/upload/image`, {{ method: 'POST', body: formData }});
        if (resp.ok) {{
          const data = await resp.json();
          if (data.name) return true;
        }}
      }} catch (e) {{}}

      // 2. Yedek AnimeAI endpoint
      try {{
        const resp2 = await fetch(`${{COMFY_URL}}/animeai/save_mask`, {{ method: 'POST', body: formData }});
        if (resp2.ok) return true;
      }} catch (e2) {{}}

      return false;
    }}

    // MASKEYİ TEMİZLE & BOŞ GÜNCELLE
    async function clearMask() {{
      if (maskImgW > 0) {{
        drawCtx.clearRect(0, 0, maskImgW, maskImgH);
        saveMaskHistory();
      }}

      const btn = document.getElementById('btn-clear-mask');
      const originalHtml = btn ? btn.innerHTML : '';
      if (btn) {{
        btn.innerHTML = `<span class="btn-spinner"></span> Boş Maske Kaydediliyor...`;
        btn.disabled = true;
      }}

      maskStatusText.textContent = 'Maske temizlendi, ComfyUI güncelleniyor...';

      const w = maskOrigImgW || maskImgW || 1080;
      const h = maskOrigImgH || maskImgH || 1350;
      const emptyCanvas = document.createElement('canvas');
      emptyCanvas.width = w;
      emptyCanvas.height = h;
      const ectx = emptyCanvas.getContext('2d');
      ectx.fillStyle = '#000000';
      ectx.fillRect(0, 0, w, h);

      try {{
        const blob = await new Promise(resolve => emptyCanvas.toBlob(resolve, 'image/png'));
        const isSuccess = await uploadMaskBlob(blob);

        if (isSuccess) {{
          if (btn) {{
            btn.innerHTML = `Boş Maske Güncellendi!`;
            btn.classList.add('btn-success');
          }}
          showToast(
            '<b>Maske temizlendi ve ComfyUI güncellendi!</b><br>' +
            `<small>Çözünürlük: ${{w}}x${{h}} | Korunan Alan: %0</small><br>` +
            '<code>protection_mask.png</code> boş olarak kaydedildi. Tüm video (%100) anime stiline dönüştürülecektir.',
            'success',
            4000
          );
          maskStatusText.textContent = `Boş maske ComfyUI/input/ klasörüne yazıldı (${{w}}x${{h}})`;

          setTimeout(() => {{
            if (btn) {{
              btn.innerHTML = originalHtml;
              btn.classList.remove('btn-success');
              btn.disabled = false;
            }}
          }}, 2500);
        }} else {{
          if (btn) {{
            btn.innerHTML = originalHtml;
            btn.disabled = false;
          }}
          showToast('Maske tuvalde temizlendi fakat ComfyUI sunucusuna ulaşılamadı.', 'warning', 3500);
          maskStatusText.textContent = 'Maske temizlendi (ComfyUI çevrimdışı)';
        }}
      }} catch (err) {{
        if (btn) {{
          btn.innerHTML = originalHtml;
          btn.disabled = false;
        }}
        showToast('Hata: ' + err.message, 'error');
      }}
    }}

    function generateExportCanvas() {{
      const drawData = drawCtx.getImageData(0, 0, maskImgW, maskImgH);
      const tempCanvas = document.createElement('canvas');
      tempCanvas.width = maskImgW;
      tempCanvas.height = maskImgH;
      const tctx = tempCanvas.getContext('2d');
      const outImgData = tctx.createImageData(maskImgW, maskImgH);

      let drawnCount = 0;
      for (let i = 0; i < drawData.data.length; i += 4) {{
        const alpha = drawData.data[i + 3];
        if (alpha > 10) {{
          outImgData.data[i]     = 255;
          outImgData.data[i + 1] = 255;
          outImgData.data[i + 2] = 255;
          outImgData.data[i + 3] = 0;
          drawnCount++;
        }} else {{
          outImgData.data[i]     = 0;
          outImgData.data[i + 1] = 0;
          outImgData.data[i + 2] = 0;
          outImgData.data[i + 3] = 255;
        }}
      }}
      tctx.putImageData(outImgData, 0, 0);

      const exportCanvas = document.createElement('canvas');
      exportCanvas.width = maskOrigImgW || maskImgW;
      exportCanvas.height = maskOrigImgH || maskImgH;
      const ectx = exportCanvas.getContext('2d');
      ectx.imageSmoothingEnabled = false;
      ectx.drawImage(tempCanvas, 0, 0, exportCanvas.width, exportCanvas.height);
      exportCanvas._drawnCount = drawnCount;
      return exportCanvas;
    }}

    // MASKEYİ COMFYUI'A KAYDET
    async function saveMaskToComfyUI() {{
      if (!maskImgW) {{
        showToast('Lütfen önce bir video karesi yükleyin!', 'warning');
        return;
      }}

      const btn = document.getElementById('btn-save-comfy');
      const originalHtml = btn.innerHTML;
      btn.innerHTML = `<span class="btn-spinner"></span> ComfyUI'a Yazılıyor...`;
      btn.disabled = true;

      try {{
        const exportCanvas = generateExportCanvas();
        const blob = await new Promise(resolve => exportCanvas.toBlob(resolve, 'image/png'));
        const isSuccess = await uploadMaskBlob(blob);

        if (isSuccess) {{
          btn.innerHTML = `ComfyUI'a Kaydedildi!`;
          btn.classList.add('btn-success');
          showToast(
            '<b>protection_mask.png ComfyUI/input/ klasörüne kaydedildi!</b><br>' +
            `<small>Çözünürlük: ${{exportCanvas.width}}x${{exportCanvas.height}} | Korunan Piksel: ${{exportCanvas._drawnCount}}</small><br>` +
            'ComfyUI akışınızda <b>Queue Prompt</b> diyerek videoyu işleyebilirsiniz.',
            'success',
            5000
          );
          maskStatusText.textContent = `protection_mask.png yazıldı (${{exportCanvas.width}}x${{exportCanvas.height}})`;

          setTimeout(() => {{
            btn.innerHTML = originalHtml;
            btn.classList.remove('btn-success');
            btn.disabled = false;
          }}, 3000);
        }} else {{
          btn.innerHTML = originalHtml;
          btn.disabled = false;
          const link = document.createElement('a');
          link.download = 'protection_mask.png';
          link.href = exportCanvas.toDataURL('image/png');
          link.click();
          showToast('Otomatik aktarılamadı — maske indirildi (ComfyUI/input/ klasörüne taşıyın).', 'warning', 6000);
        }}
      }} catch (err) {{
        btn.innerHTML = originalHtml;
        btn.disabled = false;
        showToast('Beklenmeyen hata: ' + err.message, 'error');
      }}
    }}

    // INITIALIZATION
    window.addEventListener('DOMContentLoaded', () => {{
      populateDropdown();
      randomizeAdvancedSettings();
      fetchRecentGallery();

      // Check URL Hash for initial view
      const initialView = (window.location.hash === '#mask') ? 'mask' : 'poster';
      switchStudioView(initialView, true);
      setTimeout(updateNavIndicator, 60);
    }});

    window.addEventListener('hashchange', () => {{
      const targetView = (window.location.hash === '#mask') ? 'mask' : 'poster';
      if (targetView !== currentView) {{
        switchStudioView(targetView);
      }}
    }});
  </script>
</body>
</html>
'''

    out_file = os.path.join(base_dir, "studio.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated studio.html: {len(html)} bytes")

    # Also write index.html as mirror
    index_file = os.path.join(base_dir, "index.html")
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated index.html: {len(html)} bytes")

if __name__ == "__main__":
    build_studio()
