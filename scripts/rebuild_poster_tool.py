import json

with open("scripts/techniques_data.json", "r", encoding="utf-8") as f:
    techniques = json.load(f)

techniques_js = json.dumps(techniques, indent=2)

html_content = f'''<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RingPulse // AI Combat Poster Studio</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Rajdhani:wght@500;600;700&family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-dark: #07090e;
      --bg-panel: rgba(14, 18, 28, 0.82);
      --bg-card: rgba(22, 28, 44, 0.65);
      --border: rgba(255, 38, 70, 0.35);
      --border-subtle: rgba(255, 255, 255, 0.08);
      --crimson: #ff2646;
      --crimson-glow: rgba(255, 38, 70, 0.45);
      --cyan: #00ebff;
      --cyan-glow: rgba(0, 235, 255, 0.4);
      --gold: #ffc300;
      --gold-glow: rgba(255, 195, 0, 0.35);
      --purple: #b94bfb;
      --text: #f0f4fc;
      --text-muted: #94a3b8;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      background: var(--bg-dark);
      background-image: 
        radial-gradient(circle at 15% 15%, rgba(255, 38, 70, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 85% 85%, rgba(0, 235, 255, 0.07) 0%, transparent 40%),
        radial-gradient(circle at 50% 50%, rgba(185, 75, 251, 0.04) 0%, transparent 50%);
      color: var(--text);
      font-family: 'Outfit', sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }}

    /* HEADER */
    header {{
      padding: 16px 36px;
      background: rgba(10, 14, 22, 0.95);
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
      backdrop-filter: blur(14px);
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    .brand-logo {{
      width: 40px;
      height: 40px;
      background: linear-gradient(135deg, var(--crimson), #b80024);
      clip-path: polygon(25% 0%, 100% 0%, 75% 100%, 0% 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Rajdhani', sans-serif;
      font-weight: 700;
      font-size: 22px;
      color: #fff;
      box-shadow: 0 0 20px var(--crimson-glow);
    }}

    .brand-text {{
      display: flex;
      flex-direction: column;
    }}

    .brand-title {{
      font-family: 'Rajdhani', sans-serif;
      font-weight: 700;
      font-size: 22px;
      letter-spacing: 2px;
      text-transform: uppercase;
      line-height: 1.1;
    }}

    .brand-title span {{
      color: var(--crimson);
    }}

    .brand-subtitle {{
      font-size: 12px;
      color: var(--text-muted);
      letter-spacing: 0.5px;
    }}

    .server-status {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-family: 'Rajdhani', sans-serif;
      font-size: 13px;
      font-weight: 600;
      letter-spacing: 1px;
      padding: 6px 14px;
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
    }}

    .status-dot {{
      width: 9px;
      height: 9px;
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

    /* MAIN CONTAINER */
    .container {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 28px 24px 60px 24px;
      width: 100%;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 36px;
      align-items: start;
    }}

    @media (max-width: 1024px) {{
      .container {{
        grid-template-columns: 1fr;
      }}
    }}

    /* HERO CONTROL CARD */
    .hero-card {{
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
      padding: 30px;
      box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
      backdrop-filter: blur(12px);
      display: flex;
      flex-direction: column;
      gap: 22px;
      position: relative;
      overflow: hidden;
    }}

    .hero-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--crimson), var(--gold), var(--cyan));
    }}

    .section-title {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 1.8px;
      text-transform: uppercase;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    /* FORMAT PILLS */
    .pill-group {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }}

    .format-pill {{
      padding: 12px 16px;
      background: var(--bg-card);
      border: 1.5px solid var(--border-subtle);
      border-radius: 12px;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      gap: 3px;
      transition: all 0.25s ease;
      color: var(--text);
    }}

    .format-pill:hover {{
      border-color: rgba(255, 38, 70, 0.5);
      transform: translateY(-2px);
    }}

    .format-pill.active {{
      background: rgba(255, 38, 70, 0.12);
      border-color: var(--crimson);
      box-shadow: 0 0 20px rgba(255, 38, 70, 0.25);
    }}

    .pill-label {{
      font-family: 'Rajdhani', sans-serif;
      font-weight: 700;
      font-size: 15px;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .pill-desc {{
      font-size: 11px;
      color: var(--text-muted);
    }}

    /* SPORT PILLS */
    .sport-filter {{
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
    }}

    .sport-btn, .option-pill {{
      padding: 6px 13px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
      color: var(--text-muted);
      font-family: 'Rajdhani', sans-serif;
      font-size: 13px;
      font-weight: 600;
      letter-spacing: 0.5px;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .sport-btn:hover, .option-pill:hover {{
      color: #fff;
      border-color: rgba(255, 255, 255, 0.25);
    }}

    .sport-btn.active {{
      background: rgba(0, 235, 255, 0.12);
      border-color: var(--cyan);
      color: var(--cyan);
      box-shadow: 0 0 12px var(--cyan-glow);
    }}

    .option-pill.active {{
      background: rgba(255, 195, 0, 0.14);
      border-color: var(--gold);
      color: var(--gold);
      box-shadow: 0 0 12px var(--gold-glow);
    }}

    /* BATCH SELECTOR */
    .batch-selector {{
      display: flex;
      gap: 10px;
    }}

    .batch-pill {{
      flex: 1;
      padding: 10px 14px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      color: var(--text-muted);
      font-family: 'Rajdhani', sans-serif;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .batch-pill:hover {{
      color: #fff;
      border-color: rgba(255, 255, 255, 0.3);
    }}

    .batch-pill.active {{
      background: rgba(185, 75, 251, 0.15);
      border-color: var(--purple);
      color: #fff;
      box-shadow: 0 0 14px rgba(185, 75, 251, 0.35);
    }}

    /* THE GIANT HERO BUTTON */
    .hero-btn-container {{
      padding-top: 4px;
    }}

    .hero-generate-btn {{
      width: 100%;
      padding: 22px 28px;
      background: linear-gradient(135deg, #ff2646 0%, #b80024 50%, #750017 100%);
      border: 1.5px solid #ff6680;
      border-radius: 16px;
      color: #fff;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 6px;
      position: relative;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(255, 38, 70, 0.4), 0 0 20px rgba(255, 38, 70, 0.2);
      transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}

    .hero-generate-btn::before {{
      content: '';
      position: absolute;
      top: -50%;
      left: -50%;
      width: 200%;
      height: 200%;
      background: linear-gradient(45deg, transparent 40%, rgba(255, 255, 255, 0.2) 50%, transparent 60%);
      transform: rotate(25deg);
      transition: all 0.75s;
    }}

    .hero-generate-btn:hover:not(:disabled)::before {{
      left: 100%;
    }}

    .hero-generate-btn:hover:not(:disabled) {{
      transform: translateY(-3px) scale(1.01);
      box-shadow: 0 16px 40px rgba(255, 38, 70, 0.55), 0 0 30px rgba(255, 38, 70, 0.4);
      border-color: #ffffff;
    }}

    .hero-generate-btn:active:not(:disabled) {{
      transform: translateY(1px) scale(0.99);
    }}

    .hero-generate-btn:disabled {{
      opacity: 0.6;
      cursor: not-allowed;
      filter: grayscale(0.5);
    }}

    .hero-btn-title {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 25px;
      font-weight: 700;
      letter-spacing: 2px;
      text-transform: uppercase;
      display: flex;
      align-items: center;
      gap: 12px;
      text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
    }}

    .hero-btn-subtitle {{
      font-size: 12px;
      color: rgba(255, 255, 255, 0.85);
      font-weight: 400;
      letter-spacing: 0.5px;
    }}

    /* LIVE SELECTION BADGE */
    .selection-badge {{
      display: none;
      padding: 12px 16px;
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid rgba(0, 235, 255, 0.3);
      border-radius: 12px;
      font-family: 'Rajdhani', sans-serif;
      font-size: 13px;
      letter-spacing: 1px;
      color: var(--cyan);
      display: flex;
      align-items: center;
      gap: 10px;
      animation: fadeIn 0.3s ease;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(-5px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* COLLAPSIBLE ADVANCED DRAWER */
    details.advanced-drawer {{
      background: rgba(10, 14, 22, 0.6);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 14px 18px;
      transition: all 0.3s;
    }}

    details.advanced-drawer[open] {{
      border-color: rgba(255, 255, 255, 0.2);
      padding-bottom: 22px;
    }}

    summary.drawer-header {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      color: var(--text-muted);
      cursor: pointer;
      user-select: none;
      display: flex;
      align-items: center;
      justify-content: space-between;
      list-style: none;
    }}

    summary.drawer-header::-webkit-details-marker {{
      display: none;
    }}

    summary.drawer-header:hover {{
      color: #fff;
    }}

    .drawer-content {{
      margin-top: 18px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    .form-group {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .form-label {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
      color: var(--text-muted);
    }}

    .form-input, .form-select, .form-textarea {{
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 10px 14px;
      color: #fff;
      font-family: 'Outfit', sans-serif;
      font-size: 13px;
      transition: all 0.2s;
    }}

    .form-input:focus, .form-select:focus, .form-textarea:focus {{
      outline: none;
      border-color: var(--cyan);
      box-shadow: 0 0 10px var(--cyan-glow);
    }}

    .secondary-btn {{
      padding: 12px;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 8px;
      color: #fff;
      font-family: 'Rajdhani', sans-serif;
      font-weight: 700;
      font-size: 14px;
      letter-spacing: 1px;
      text-transform: uppercase;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .secondary-btn:hover {{
      background: rgba(255, 255, 255, 0.15);
      border-color: #fff;
    }}

    /* RIGHT COLUMN: PREVIEW & DUAL DOWNLOAD */
    .preview-card {{
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
      padding: 24px;
      box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
      backdrop-filter: blur(12px);
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    /* PREVIEW TABS */
    .preview-tabs {{
      display: flex;
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 4px;
      gap: 4px;
    }}

    .preview-tab {{
      flex: 1;
      padding: 10px 16px;
      background: transparent;
      border: none;
      border-radius: 8px;
      color: var(--text-muted);
      font-family: 'Rajdhani', sans-serif;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all 0.2s;
    }}

    .preview-tab.active {{
      background: var(--bg-card);
      color: #fff;
      border: 1px solid rgba(255, 255, 255, 0.15);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }}

    /* IMAGE FRAME */
    .image-viewport {{
      width: 100%;
      background: #020305;
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      overflow: hidden;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      aspect-ratio: 4 / 5;
      transition: aspect-ratio 0.3s ease;
    }}

    .image-viewport.ratio-story {{
      aspect-ratio: 9 / 16;
      max-height: 70vh;
      margin: 0 auto;
    }}

    .display-img {{
      width: 100%;
      height: 100%;
      object-fit: contain;
      display: none;
    }}

    /* PLACEHOLDER */
    .empty-state {{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 14px;
      color: var(--text-muted);
      text-align: center;
      padding: 40px 20px;
    }}

    .empty-icon {{
      font-size: 50px;
      opacity: 0.4;
      animation: float 3s ease-in-out infinite;
    }}

    @keyframes float {{
      0%, 100% {{ transform: translateY(0); }}
      50% {{ transform: translateY(-8px); }}
    }}

    .empty-title {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 17px;
      font-weight: 700;
      letter-spacing: 1px;
      color: #fff;
    }}

    .empty-desc {{
      font-size: 13px;
      max-width: 320px;
      line-height: 1.5;
    }}

    /* PROGRESS OVERLAY */
    .progress-overlay {{
      display: none;
      position: absolute;
      inset: 0;
      background: rgba(7, 9, 14, 0.94);
      backdrop-filter: blur(8px);
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 18px;
      padding: 30px;
      z-index: 10;
    }}

    .spinner {{
      width: 52px;
      height: 52px;
      border: 3px solid rgba(255, 38, 70, 0.2);
      border-top-color: var(--crimson);
      border-right-color: var(--cyan);
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }}

    @keyframes spin {{
      to {{ transform: rotate(360deg); }}
    }}

    .progress-text {{
      font-family: 'Rajdhani', sans-serif;
      font-weight: 700;
      font-size: 18px;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: #fff;
      text-align: center;
    }}

    .progress-subtext {{
      font-size: 13px;
      color: var(--text-muted);
      text-align: center;
    }}

    .progress-bar-wrap {{
      width: 80%;
      height: 6px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 4px;
      overflow: hidden;
    }}

    .progress-bar-fill {{
      width: 30%;
      height: 100%;
      background: linear-gradient(90deg, var(--crimson), var(--cyan));
      border-radius: 4px;
      animation: progressPulse 1.5s ease-in-out infinite alternate;
    }}

    @keyframes progressPulse {{
      from {{ width: 25%; transform: translateX(-10%); }}
      to {{ width: 85%; transform: translateX(20%); }}
    }}

    /* DUAL DOWNLOAD ACTION BAR */
    .action-bar {{
      display: none;
      flex-direction: column;
      gap: 10px;
    }}

    .download-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }}

    .download-btn {{
      padding: 13px;
      border-radius: 12px;
      border: none;
      cursor: pointer;
      font-family: 'Rajdhani', sans-serif;
      font-weight: 700;
      font-size: 14px;
      letter-spacing: 1px;
      text-transform: uppercase;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all 0.2s;
    }}

    .btn-poster {{
      background: linear-gradient(135deg, var(--crimson), #c40026);
      color: #fff;
      box-shadow: 0 4px 15px var(--crimson-glow);
    }}

    .btn-poster:hover {{
      transform: translateY(-2px);
      box-shadow: 0 8px 25px var(--crimson-glow);
    }}

    .btn-clean {{
      background: linear-gradient(135deg, #0088cc, #005588);
      color: #fff;
      border: 1px solid rgba(0, 235, 255, 0.4);
      box-shadow: 0 4px 15px rgba(0, 136, 204, 0.35);
    }}

    .btn-clean:hover {{
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(0, 235, 255, 0.45);
    }}

    .btn-fullscreen {{
      padding: 9px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      color: var(--text-muted);
      font-family: 'Rajdhani', sans-serif;
      font-size: 13px;
      font-weight: 600;
      letter-spacing: 1px;
      text-transform: uppercase;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s;
    }}

    .btn-fullscreen:hover {{
      color: #fff;
      border-color: rgba(255, 255, 255, 0.3);
      background: rgba(255, 255, 255, 0.1);
    }}

    /* GALLERY STRIP SECTION */
    .gallery-section {{
      grid-column: 1 / -1;
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      backdrop-filter: blur(12px);
    }}

    .gallery-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .gallery-title {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 16px;
      font-weight: 700;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      display: flex;
      align-items: center;
      gap: 10px;
      color: #fff;
    }}

    .gallery-count {{
      font-size: 12px;
      padding: 2px 8px;
      background: rgba(255, 38, 70, 0.2);
      border: 1px solid rgba(255, 38, 70, 0.4);
      color: var(--crimson);
      border-radius: 12px;
    }}

    .gallery-refresh-btn {{
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      color: var(--text-muted);
      font-family: 'Rajdhani', sans-serif;
      font-size: 12px;
      font-weight: 600;
      letter-spacing: 1px;
      text-transform: uppercase;
      padding: 6px 12px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }}

    .gallery-refresh-btn:hover {{
      color: #fff;
      border-color: rgba(255, 255, 255, 0.25);
    }}

    .gallery-strip {{
      display: flex;
      gap: 14px;
      overflow-x: auto;
      padding: 8px 4px 14px 4px;
    }}

    .gallery-strip::-webkit-scrollbar {{
      height: 6px;
    }}
    .gallery-strip::-webkit-scrollbar-track {{
      background: rgba(0, 0, 0, 0.2);
      border-radius: 4px;
    }}
    .gallery-strip::-webkit-scrollbar-thumb {{
      background: rgba(255, 255, 255, 0.2);
      border-radius: 4px;
    }}
    .gallery-strip::-webkit-scrollbar-thumb:hover {{
      background: var(--crimson);
    }}

    .gallery-card {{
      flex: 0 0 140px;
      height: 175px;
      background: var(--bg-card);
      border: 1.5px solid var(--border-subtle);
      border-radius: 12px;
      overflow: hidden;
      cursor: pointer;
      position: relative;
      display: flex;
      flex-direction: column;
      transition: all 0.25s ease;
    }}

    .gallery-card:hover {{
      transform: translateY(-4px);
      border-color: var(--cyan);
      box-shadow: 0 8px 20px rgba(0, 235, 255, 0.25);
    }}

    .gallery-card.active {{
      border-color: var(--crimson);
      box-shadow: 0 0 16px var(--crimson-glow);
    }}

    .gallery-clean-pill {{
      position: absolute;
      top: 6px;
      right: 6px;
      background: rgba(10, 14, 22, 0.88);
      border: 1px solid rgba(0, 235, 255, 0.5);
      border-radius: 6px;
      font-size: 11px;
      padding: 1px 5px;
      line-height: 1.2;
      pointer-events: none;
      backdrop-filter: blur(4px);
    }}

    .gallery-thumb {{
      width: 100%;
      height: 130px;
      object-fit: cover;
      background: #020305;
    }}

    .gallery-card-label {{
      padding: 6px 8px;
      font-family: 'Rajdhani', sans-serif;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      color: #fff;
      background: rgba(10, 14, 22, 0.9);
      border-top: 1px solid var(--border-subtle);
    }}

    .gallery-empty {{
      color: var(--text-muted);
      font-size: 13px;
      padding: 20px;
      text-align: center;
      width: 100%;
    }}
  </style>
</head>
<body>

  <!-- HEADER -->
  <header>
    <div class="brand">
      <div class="brand-logo"></div>
      <div class="brand-text">
        <div class="brand-title">RINGPULSE <span>AI STUDIO</span></div>
        <div class="brand-subtitle">Tek Tıkla Anime Dövüş Posteri, Temiz Çizim ve Galeri</div>
      </div>
    </div>
    <div class="server-status">
      <div class="status-dot" id="statusDot"></div>
      <span id="statusText">COMFYUI KONTROL EDILIYOR...</span>
    </div>
  </header>

  <!-- MAIN VIEW -->
  <div class="container">

    <!-- LEFT: CONTROLS -->
    <div class="hero-card">

      <!-- 1. FORMAT SELECTION -->
      <div>
        <div class="section-title">1. POSTER FORMATI</div>
        <div class="pill-group" style="margin-top: 10px;">
          <div class="format-pill active" id="format45" onclick="setFormat('4:5')">
            <div class="pill-label"> 4:5 FEED POST</div>
            <div class="pill-desc">1080 × 1350 px (Instagram Gönderisi)</div>
          </div>
          <div class="format-pill" id="format916" onclick="setFormat('9:16')">
            <div class="pill-label"> 9:16 STORY / REEL</div>
            <div class="pill-desc">1080 × 1920 px (Dikey Hikaye)</div>
          </div>
        </div>
      </div>

      <!-- 2. SPORT FILTER -->
      <div>
        <div class="section-title">2. SPOR BRANŞI FİLTRESİ (İSTEĞE BAĞLI)</div>
        <div class="sport-filter" style="margin-top: 8px;">
          <button class="sport-btn active" onclick="setSport('all', this)">Tümü (61 Teknik)</button>
          <button class="sport-btn" onclick="setSport('boxing', this)"> Boks</button>
          <button class="sport-btn" onclick="setSport('muay_thai', this)"> Muay Thai</button>
          <button class="sport-btn" onclick="setSport('mma', this)"> MMA</button>
          <button class="sport-btn" onclick="setSport('bjj', this)"> BJJ / Jiu-Jitsu</button>
          <button class="sport-btn" onclick="setSport('kickboxing', this)"> Kickboks</button>
          <button class="sport-btn" onclick="setSport('sambo', this)"> Sambo</button>
          <button class="sport-btn" onclick="setSport('wrestling', this)"> Güreş</button>
          <button class="sport-btn" onclick="setSport('judo', this)"> Judo</button>
          <button class="sport-btn" onclick="setSport('karate', this)"> Karate</button>
          <button class="sport-btn" onclick="setSport('lethwei', this)"> Lethwei</button>
        </div>
      </div>

      <!-- 3. FIGHTER VARIETY (GENDER & ANIME STYLE) -->
      <div>
        <div class="section-title">3. DÖVÜŞÇÜ CİNSİYETİ & ANİME STİLİ</div>
        <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 8px;">
          <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <button class="option-pill active" onclick="setGender('random', this)"> Rastgele Cinsiyet</button>
            <button class="option-pill" onclick="setGender('male', this)"> Erkek Dövüşçü</button>
            <button class="option-pill" onclick="setGender('female', this)"> Kadın Dövüşçü</button>
          </div>
          <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <button class="option-pill active" onclick="setStyle('random', this)"> Rastgele Stil</button>
            <button class="option-pill" onclick="setStyle('modern', this)"> Modern Anime</button>
            <button class="option-pill" onclick="setStyle('baki', this)"> Baki (Kaslı)</button>
            <button class="option-pill" onclick="setStyle('ippo', this)"> Hajime no Ippo</button>
            <button class="option-pill" onclick="setStyle('cyber', this)"> Cyber Strike</button>
          </div>
        </div>
      </div>

      <!-- 4. BATCH PRODUCTION SELECTOR -->
      <div>
        <div class="section-title">4. ÜRETİM ADEDİ (TEKİL / SERİ)</div>
        <div class="batch-selector" style="margin-top: 8px;">
          <div class="batch-pill active" onclick="setBatchCount(1, this)"> 1x Tekil</div>
          <div class="batch-pill" onclick="setBatchCount(3, this)"> 3x Seri Üretim</div>
          <div class="batch-pill" onclick="setBatchCount(5, this)"> 5x Toplu Üretim</div>
        </div>
      </div>

      <!-- 5. THE GIANT HERO BUTTON -->
      <div class="hero-btn-container">
        <button class="hero-generate-btn" id="generateHeroBtn" onclick="handleHeroGenerate()">
          <div class="hero-btn-title">
            <span></span>
            <span id="heroBtnText">RASTGELE POSTER OLUŞTUR</span>
          </div>
          <div class="hero-btn-subtitle" id="heroBtnSubtext">
            61 dövüş tekniği ve 8 tasarım düzeni arasından otomatik seçip anında çizer
          </div>
        </button>
      </div>

      <!-- SELECTION STATUS BADGE -->
      <div class="selection-badge" id="selectionBadge">
        <span></span>
        <span id="selectionText">Seçilen teknik bilgisi burada görünecek...</span>
      </div>

      <!-- 6. COLLAPSIBLE ADVANCED DRAWER -->
      <details class="advanced-drawer" id="advancedDrawer">
        <summary class="drawer-header">
          <span> Manuel Ayarlar & Özel Metin Düzenleme (İsteğe Bağlı)</span>
          <span>▼</span>
        </summary>
        <div class="drawer-content">
          <div class="form-group">
            <label class="form-label">Teknik Listesinden Doğrudan Seç</label>
            <select class="form-select" id="manualTechniqueSelect" onchange="onManualSelectTechnique(this.value)">
              <option value="">-- Rastgele yerine belirli bir teknik seç --</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Tasarım Düzeni (Layout Archetype)</label>
            <select class="form-select" id="layoutStyle">
              <option value="Random Layout Archetype"> Rastgele Layout (8 Farklı Tip)</option>
              <option value="Floating Tactical Callouts (Left/Right)">1. Floating Tactical Callouts</option>
              <option value="Side Editorial Column (Magazine)">2. Side Editorial Column</option>
              <option value="Cyberpunk Target Lock HUD">3. Cyberpunk Target Lock HUD</option>
              <option value="Classic Bottom Card">4. Classic Bottom Card (Apex Cyber Console)</option>
              <option value="Dual-Wing Symmetrical Frame">5. Dual-Wing Symmetrical Frame</option>
              <option value="Diagonal Kinetic Slash">6. Diagonal Kinetic Slash</option>
              <option value="Tactical Blueprint Dossier">7. Tactical Blueprint Dossier</option>
              <option value="Minimalist Brutalist Combat">8. Minimalist Brutalist Combat</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Renk Paleti</label>
            <select class="form-select" id="themeColor">
              <option value="Random Palette"> Rastgele Palet</option>
              <option value="Crimson Red">Crimson Red (Neon Kırmızı + Cyan)</option>
              <option value="Cyber Cyan">Cyber Cyan (Turkuaz + Amber)</option>
              <option value="Golden Bronze">Golden Bronze (Altın Sarısı + Cyan)</option>
              <option value="Toxic Emerald">Toxic Emerald (Zümrüt Yeşili + Mor)</option>
              <option value="Electric Violet">Electric Violet (Elektrik Mor + Cyan)</option>
              <option value="Solar Amber">Solar Amber (Güneş Turuncusu + Sarı)</option>
              <option value="Ice Cobalt">Ice Cobalt (Buz Mavisi + Neon Mavi)</option>
              <option value="Bloodline Ruby">Bloodline Ruby (Koyu Yakut + Pembe)</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Özel Başlık (Title)</label>
            <input type="text" class="form-input" id="posterTitle" value="THE LEAD HOOK">
          </div>

          <div class="form-group">
            <label class="form-label">Alt Başlık (Tagline)</label>
            <input type="text" class="form-input" id="posterTagline" value="EXPLOSIVE ROTATIONAL POWER & ANGLE CUTTING">
          </div>

          <div class="form-group">
            <label class="form-label">Fighter Anime Prompt</label>
            <textarea class="form-textarea" id="fighterPrompt" rows="3">masterpiece, best quality, 1man, athletic muscular boxer, throwing explosive lead hook punch, dynamic combat pose, boxing gloves, sweat flying, intense fierce expression, dark boxing gym ring background, dramatic volumetric rim lighting, cinematic anime combat, 8k wallpaper</textarea>
          </div>

          <button class="secondary-btn" onclick="generateWithCustomSettings()">
             Bu Özel Ayarlarla Oluştur
          </button>
        </div>
      </details>

    </div>

    <!-- RIGHT: PREVIEW & DUAL DOWNLOAD SHOWCASE -->
    <div class="preview-card">

      <!-- PREVIEW TABS: POSTER vs CLEAN -->
      <div class="preview-tabs">
        <button class="preview-tab active" id="tabPoster" onclick="switchPreviewTab('poster')">
          <span></span>
          <span>Yazılı Poster</span>
        </button>
        <button class="preview-tab" id="tabClean" onclick="switchPreviewTab('clean')">
          <span></span>
          <span>Yazısız Çizim</span>
        </button>
      </div>

      <!-- VIEWPORT -->
      <div class="image-viewport" id="imageViewport">
        
        <!-- PLACEHOLDER -->
        <div class="empty-state" id="placeholderState">
          <div class="empty-icon"></div>
          <div class="empty-title">POSTER VE ÇİZİM BURADA GÖRÜNECEK</div>
          <div class="empty-desc">
            Soldaki <strong>"RASTGELE POSTER OLUŞTUR"</strong> butonuna basın. Sistem hem yazılı infografiği hem de temiz yazısız çizimi saniyeler içinde üretecektir.
          </div>
        </div>

        <!-- PROGRESS OVERLAY -->
        <div class="progress-overlay" id="progressOverlay">
          <div class="spinner"></div>
          <div class="progress-text" id="progressText">ÇİZİM BAŞLATIYOR...</div>
          <div class="progress-subtext" id="progressSubtext">ToonYou Beta6 + 4x-UltraSharp</div>
          <div class="progress-bar-wrap">
            <div class="progress-bar-fill"></div>
          </div>
        </div>

        <!-- IMAGES -->
        <img id="posterImg" class="display-img" alt="Yazılı Poster">
        <img id="cleanImg" class="display-img" alt="Yazısız Temiz Çizim">
      </div>

      <!-- DUAL DOWNLOAD ACTION BAR -->
      <div class="action-bar" id="actionBar">
        <div class="download-grid">
          <button class="download-btn btn-poster" id="downloadPosterBtn" onclick="downloadImage('poster')">
            <span></span>
            <span>Yazılı Posteri İndir (PNG)</span>
          </button>
          <button class="download-btn btn-clean" id="downloadCleanBtn" onclick="downloadImage('clean')">
            <span></span>
            <span>Yazısız Çizimi İndir (PNG)</span>
          </button>
        </div>
        <button class="btn-fullscreen" onclick="openFullscreen()">
          <span></span>
          <span>Aktif Görseli Tam Boyut Aç</span>
        </button>
      </div>

    </div>

    <!-- BOTTOM: RECENT GALLERY STRIP -->
    <div class="gallery-section">
      <div class="gallery-header">
        <div class="gallery-title">
          <span></span>
          <span>SON ÜRETİLENLER / GALERİ</span>
          <span class="gallery-count" id="galleryCount">0</span>
        </div>
        <button class="gallery-refresh-btn" onclick="fetchRecentGallery()">
          <span></span>
          <span>Yenile</span>
        </button>
      </div>
      <div class="gallery-strip" id="galleryStrip">
        <div class="gallery-empty" id="galleryEmpty">Henüz bu oturumda poster üretilmedi. "Rastgele Poster Oluştur"a basarak başlayın.</div>
      </div>
    </div>

  </div>

  <script>
    const COMFY_URL = "http://127.0.0.1:8188";
    const TECHNIQUES = {techniques_js};

    let selectedFormat = '4:5'; // '4:5' or '9:16'
    let selectedSport = 'all';
    let selectedGender = 'random'; // 'random', 'male', 'female'
    let selectedStyle = 'random'; // 'random', 'modern', 'baki', 'ippo', 'cyber'
    let selectedBatch = 1; // 1, 3, 5

    let currentPosterUrl = null;
    let currentCleanUrl = null;
    let currentTitleName = "FIGHTER";
    let activeTab = 'poster'; // 'poster' or 'clean'

    let galleryItems = []; // Array of {{ id, title, sport, posterUrl, cleanUrl }}

    // Server Health Check
    async function checkServer() {{
      const dot = document.getElementById('statusDot');
      const text = document.getElementById('statusText');
      try {{
        const res = await fetch(`${{COMFY_URL}}/system_stats`, {{ method: 'GET' }});
        if (res.ok) {{
          dot.className = "status-dot online";
          text.textContent = "COMFYUI AKTİF (8188)";
        }} else {{
          dot.className = "status-dot offline";
          text.textContent = "COMFYUI YANIT VERMİYOR";
        }}
      }} catch (e) {{
        dot.className = "status-dot offline";
        text.textContent = "COMFYUI BAĞLANTISI YOK";
      }}
    }}
    setInterval(checkServer, 5000);
    checkServer();

    // Format Selector
    function setFormat(fmt) {{
      selectedFormat = fmt;
      document.getElementById('format45').classList.toggle('active', fmt === '4:5');
      document.getElementById('format916').classList.toggle('active', fmt === '9:16');

      const vp = document.getElementById('imageViewport');
      if (fmt === '9:16') {{
        vp.classList.add('ratio-story');
      }} else {{
        vp.classList.remove('ratio-story');
      }}
    }}

    // Sport Filter
    function setSport(sport, btn) {{
      selectedSport = sport;
      document.querySelectorAll('.sport-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    }}

    // Gender Filter
    function setGender(gender, btn) {{
      selectedGender = gender;
      btn.parentElement.querySelectorAll('.option-pill').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    }}

    // Anime Style Filter
    function setStyle(style, btn) {{
      selectedStyle = style;
      btn.parentElement.querySelectorAll('.option-pill').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    }}

    // Batch Selector
    function setBatchCount(count, pill) {{
      selectedBatch = count;
      document.querySelectorAll('.batch-pill').forEach(p => p.classList.remove('active'));
      pill.classList.add('active');

      const btnTitle = document.getElementById('heroBtnText');
      const btnSub = document.getElementById('heroBtnSubtext');
      if (count === 1) {{
        btnTitle.textContent = "RASTGELE POSTER OLUŞTUR";
        btnSub.textContent = "61 dövüş tekniği ve 8 tasarım düzeni arasından otomatik seçip anında çizer";
      }} else if (count === 3) {{
        btnTitle.textContent = " 3'LÜ SERİ POSTER OLUŞTUR";
        btnSub.textContent = "3 farklı tekniği ve layout'u sırayla otomatik üretip galeriye ekler";
      }} else {{
        btnTitle.textContent = " 5'Lİ TOPLU POSTER OLUŞTUR";
        btnSub.textContent = "5 farklı tekniği ve layout'u sırayla otomatik üretip galeriye ekler";
      }}
    }}

    // Preview Tab Switcher
    function switchPreviewTab(tab) {{
      activeTab = tab;
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
      if (hasClean) {{
        tabClean.style.opacity = '1';
        tabClean.style.pointerEvents = 'auto';
        tabClean.title = 'Yazısız Çizim';
        downloadCleanBtn.disabled = false;
        downloadCleanBtn.style.opacity = '1';
      }} else {{
        tabClean.style.opacity = '0.45';
        tabClean.title = 'Bu üretim için yazısız kopya mevcut değil';
        downloadCleanBtn.disabled = true;
        downloadCleanBtn.style.opacity = '0.45';
        if (activeTab === 'clean') {{
          activeTab = 'poster';
          document.getElementById('tabPoster').classList.add('active');
          document.getElementById('tabClean').classList.remove('active');
        }}
      }}

      if (activeTab === 'poster') {{
        posterImg.style.display = 'block';
        cleanImg.style.display = 'none';
      }} else {{
        posterImg.style.display = 'none';
        cleanImg.style.display = 'block';
      }}
    }}

    function openFullscreen() {{
      const targetUrl = (activeTab === 'poster') ? currentPosterUrl : currentCleanUrl;
      if (targetUrl) {{
        window.open(targetUrl, '_blank');
      }}
    }}

    // Direct Blob Downloader
    async function downloadImage(type) {{
      const url = (type === 'poster') ? currentPosterUrl : currentCleanUrl;
      if (!url) {{
        if (type === 'clean') {{
          alert("Bu görsel için yazısız versiyon bulunamadı.");
        }}
        return;
      }}
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
        console.error("Direct download fallback:", err);
        window.open(url, '_blank');
      }}
    }}

    // Build Prompt with Gender & Style Modifiers
    function buildEnrichedPrompt(basePrompt) {{
      let prompt = basePrompt;

      // Gender modifier
      let genderChoice = selectedGender;
      if (genderChoice === 'random') {{
        genderChoice = (Math.random() < 0.25) ? 'female' : 'male';
      }}

      if (genderChoice === 'female') {{
        prompt = prompt.replace(/\b1man\b/g, '1woman')
                       .replace(/muscular boxer/g, 'athletic toned female boxer')
                       .replace(/muscular fighter/g, 'athletic toned female fighter')
                       .replace(/athletic muscular/g, 'athletic toned muscular female')
                       .replace(/handsome/g, 'beautiful fierce');
        prompt += ", athletic toned female fighter, muscular abs, fierce expression, battle-ready stance";
      }} else {{
        prompt += ", athletic muscular male fighter, sharp jawline, ripped physique";
      }}

      // Style modifier
      let styleChoice = selectedStyle;
      if (styleChoice === 'random') {{
        const styles = ['modern', 'baki', 'ippo', 'cyber'];
        styleChoice = styles[Math.floor(Math.random() * styles.length)];
      }}

      if (styleChoice === 'baki') {{
        prompt += ", baki manga style, kengan ashura, extreme muscular vascularity, heavy impact lines, brutal combat anatomy, veins popping, high contrast grit";
      }} else if (styleChoice === 'ippo') {{
        prompt += ", classic 90s boxing shonen anime style, hajime no ippo style, heavy ink outlines, sweat bursts, dynamic speed lines, retro anime grit";
      }} else if (styleChoice === 'cyber') {{
        prompt += ", cyberpunk anime fighter, glowing neon combat tattoos, dark gym, rain reflections, neon lens flares, futuristic combat gear";
      }} else {{
        prompt += ", cinematic anime combat, vibrant volumetric lighting, sharp cel-shaded, dramatic rim lighting";
      }}

      return prompt;
    }}

    // Hero Generate Handler (Single or Batch)
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

        // Shuffle pool
        const shuffled = [...pool].sort(() => 0.5 - Math.random());
        const selectedTechs = shuffled.slice(0, count);

        for (let i = 0; i < selectedTechs.length; i++) {{
          const tech = selectedTechs[i];
          const layouts = [
            "Floating Tactical Callouts (Left/Right)",
            "Side Editorial Column (Magazine)",
            "Cyberpunk Target Lock HUD",
            "Classic Bottom Card",
            "Dual-Wing Symmetrical Frame",
            "Diagonal Kinetic Slash",
            "Tactical Blueprint Dossier",
            "Minimalist Brutalist Combat"
          ];
          const randomLayout = layouts[Math.floor(Math.random() * layouts.length)];

          const palettes = [
            "Crimson Red", "Cyber Cyan", "Golden Bronze",
            "Toxic Emerald", "Electric Violet", "Solar Amber",
            "Ice Cobalt", "Bloodline Ruby"
          ];
          const randomPalette = palettes[Math.floor(Math.random() * palettes.length)];

          const finalPrompt = buildEnrichedPrompt(tech.prompt);

          // Show badge
          const badge = document.getElementById('selectionBadge');
          const badgeText = document.getElementById('selectionText');
          badge.style.display = 'flex';
          badgeText.textContent = `[${{i+1}}/${{count}}] ${{tech.icon}} ${{tech.name}} • ${{tech.sport.toUpperCase()}} • ${{randomLayout.split('(')[0].trim()}} • ${{randomPalette}}`;

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
      badgeText.textContent = ` Özel: "${{title}}" • ${{layout.split('(')[0].trim()}} • ${{theme}}`;

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
            "text": "low quality, bad anatomy, deformed limbs, bad hands, extra fingers, missing fingers, blurry, text, watermark, signature"
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
            "steps": 22,
            "cfg": 7.0,
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
            "theme_color": params.theme,
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
        const queueData = await queueRes.json();
        const promptId = queueData.prompt_id;

        progressText.textContent = `${{batchPrefix}}ÇİZİLİYOR...`;
        progressSubtext.textContent = "ToonYou Beta6 + 4x-UltraSharp HD";

        // Poll history
        let completed = false;
        for (let i = 0; i < 45; i++) {{
          await new Promise(r => setTimeout(r, 1500));
          const histRes = await fetch(`${{COMFY_URL}}/history/${{promptId}}`);
          const histData = await histRes.json();

          if (promptId in histData) {{
            const outputs = histData[promptId].outputs || {{}};
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
        }}

        if (!completed) {{
          alert("Oluşturma zaman aşımına uğradı. ComfyUI terminalini kontrol edin.");
        }}
      }} catch (err) {{
        console.error(err);
        alert("Poster oluşturulurken hata: " + err.message);
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

      if (posterUrl) {{
        posterImg.src = posterUrl;
      }}
      if (cleanUrl) {{
        cleanImg.src = cleanUrl;
      }} else {{
        cleanImg.removeAttribute('src');
      }}

      // If activeTab is 'clean' but this item has no cleanUrl, fallback to 'poster'
      if (activeTab === 'clean' && !cleanUrl) {{
        activeTab = 'poster';
        document.getElementById('tabPoster').classList.add('active');
        document.getElementById('tabClean').classList.remove('active');
      }}

      updatePreviewDisplay();
    }}

    // GALLERY LOGIC
    function addToGallery(item) {{
      // Prepend
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

        const label = document.createElement('div');
        label.className = 'gallery-card-label';
        label.textContent = item.title;

        card.appendChild(img);
        if (item.cleanUrl) {{
          const cleanBadge = document.createElement('span');
          cleanBadge.className = 'gallery-clean-pill';
          cleanBadge.innerHTML = '';
          cleanBadge.title = 'Yazısız Çizim Mevcut';
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
          let pObj = null;
          let cObj = null;

          // Search across all node outputs in this run
          for (const nid of Object.keys(outputs)) {{
            const nOut = outputs[nid];
            if (nOut && nOut.images && nOut.images.length > 0) {{
              for (const img of nOut.images) {{
                const fn = (img.filename || "").toLowerCase();
                if (fn.includes('clean')) {{
                  cObj = img;
                }} else if (fn.includes('poster')) {{
                  pObj = img;
                }}
              }}
            }}
          }}

          // Fallbacks by node IDs 11 (poster) and 12 (clean)
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

    // Populate manual select dropdown
    function populateDropdown() {{
      const select = document.getElementById('manualTechniqueSelect');
      TECHNIQUES.forEach((t, idx) => {{
        const opt = document.createElement('option');
        opt.value = idx;
        opt.textContent = `${{t.icon}} ${{t.name}} [${{t.sport.toUpperCase()}}]`;
        select.appendChild(opt);
      }});
    }}

    function onManualSelectTechnique(idx) {{
      if (idx === "") return;
      const t = TECHNIQUES[parseInt(idx)];
      document.getElementById('posterTitle').value = t.title;
      document.getElementById('posterTagline').value = t.tagline;
      document.getElementById('fighterPrompt').value = t.prompt;
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      populateDropdown();
      fetchRecentGallery();
    }});
  </script>
</body>
</html>
'''

with open("poster_tool.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("rebuild_poster_tool.py updated and poster_tool.html successfully regenerated!")
