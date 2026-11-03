# AnimeAI Studio
**Dual-Tab Video-to-Video Anime Engine & Combat Poster Atelier**  
*Bilingual local production suite (TR / EN) built on ComfyUI, AnimateDiff, and ControlNet*

---

## Genel Bakış / Overview

**AnimeAI Studio**, gerçek spor ve dövüş videolarını zamansal tutarlılığa sahip anime animasyonlarına dönüştüren ve dövüş sporları temalı yüksek çözünürlüklü tipografik afişler üreten yerel bir yapay zeka üretim hattıdır.

The workspace runs locally across two synchronized tabs:
1. **ComfyUI Backend (Tab 1):** Video-to-Video diffusion pipeline combining AnimateDiff v2 motion modules, ControlNet (Lineart & Depth), IP-Adapter Plus, and ToonYou Beta6 checkpoints.
2. **RingPulse Studio UI (Tab 2):** Browser-based interactive canvas for region protection masking (`mask_tool`) and automated combat technique poster layout generation (`studio.html`).

---

## Temel Özellikler / Core Capabilities

- **Video-to-Video Anime Pipeline**
  - Converts live-action footage into stylized anime sequences while preserving subject geometry and motion via ControlNet Lineart and Depth conditioning.
  - Configurable frame cap (`frame_load_cap`) and target frame rate (`force_rate`) for rapid iteration or full-sequence rendering.

- **Region Protection Masking**
  - Interactive HTML5 canvas (`#bg-canvas` / `#draw-canvas`) with brush and rectangular selection tools to isolate sponsor logos, HUD overlays, or fighter silhouettes from diffusion stylization.
  - Exports binary alpha masks directly into the active ComfyUI workflow.

- **Fighter Poster Atelier**
  - Catalog of 120+ combat techniques across Boxing, Muay Thai, Brazilian Jiu-Jitsu, MMA, Wrestling, Judo, Sambo, and Karate (`scripts/techniques_data.json`).
  - 8 typographic layout presets (*Floating Tactical*, *Side Column*, *Cyberpunk HUD*, etc.) producing both clean artwork and composite infographic posters.

- **Hardware-Aware Launcher (`scripts/smart_launcher.py`)**
  - Queries PyTorch CUDA device properties at startup to measure available VRAM (`< 5.5 GB`, `5.5–9.5 GB`, `> 9.5 GB`) and injects the corresponding memory flags (`--lowvram`, `--reserve-vram`, `--highvram`).
  - Cleans stale port listeners (`8188`) and leftover SQLite lock files (`comfyui.db.lock`) before launching the server.

---

## Sistem Gereksinimleri / System Requirements

| Bileşen / Component | Minimum | Önerilen / Recommended |
|---|---|---|
| **OS** | Windows 10/11 (64-bit) or Linux | Windows 11 (64-bit) |
| **CPU** | 4 Cores (Intel i5 / Ryzen 5) | 8 Cores (Intel i7 / Ryzen 7) |
| **GPU** | NVIDIA GTX 1660 / RTX 3050 (4–6 GB VRAM) | NVIDIA RTX 3060 / 4060+ (8–12 GB VRAM) |
| **RAM** | 16 GB DDR4 | 32 GB DDR4 / DDR5 |
| **Storage** | 15 GB free space (SSD) | 25 GB NVMe SSD |
| **Python** | Python 3.10 – 3.12 | Python 3.11 (64-bit) |

---

## Kurulum ve Çalıştırma / Setup & Usage

### 1. Depoyu Klonlayın / Clone the Repository
```bash
git clone https://github.com/Samrili/animeai.git
cd animeai
```

### 2. Kurulum ve Model İndirme / Environment & Model Provisioning
`kurulum.bat` betiğini çalıştırın:
```cmd
kurulum.bat
```
Bu adım CUDA destekli PyTorch paketlerini kurar ve `scripts/download_models.py` aracılığıyla gerekli tüm ağırlıkları (`toonyou_beta6`, `mm_sd_v15_v2`, `control_v11p_sd15_lineart_fp16`, `control_v11f1p_sd15_depth_fp16`, `4x-UltraSharp`, `ip-adapter-plus_sd15`) Hugging Face üzerinden `curl` / `HTTP Range` devam ettirme desteğiyle indirir.

### 3. Stüdyoyu Başlatma / Launch
```cmd
baslat.bat
```
- `scripts/smart_launcher.py` GPU VRAM kapasitesini algılar ve uygun bellek bayraklarıyla ComfyUI sunucusunu `127.0.0.1:8188` üzerinde başlatır.
- Sunucu hazır olduğunda `scripts/open_browser_tabs.py` otomatik olarak `studio.html` arayüzünü tarayıcıda açar.

---

## Dizin Yapısı / Directory Layout

```text
animeai/
├── baslat.bat                     # Hardware-aware studio launcher
├── kurulum.bat                    # Automated environment & model setup script
├── studio.html                    # Unified RingPulse Studio web interface
├── index.html                     # Static web entry mirror of studio.html
├── workflows/
│   ├── animeai_workflow.json              # Video-to-Video ComfyUI graph
│   └── anime_fighter_poster_workflow.json # Combat poster ComfyUI graph
├── scripts/
│   ├── smart_launcher.py          # VRAM profiler & ComfyUI process runner
│   ├── download_models.py         # Resumable Hugging Face model provisioner
│   ├── open_browser_tabs.py       # Readiness poller & browser launcher
│   ├── build_unified_studio.py    # Static studio HTML bundler
│   └── techniques_data.json       # Combat sports technique metadata
├── tools/                         # Standalone masking & poster utilities
├── assets/                        # Typography and reference frame samples
├── ComfyUI/                       # Local ComfyUI runtime and custom nodes
└── requirements.txt               # Python package dependencies
```

---

## Sorun Giderme / Troubleshooting

- **CUDA Out of Memory:** `baslat.bat` üzerinden başlatıldığında `smart_launcher.py` 6 GB altı kartlarda otomatik olarak `--lowvram --reserve-vram 0.3` parametrelerini uygular.
- **Hızlı Test / Fast Preview:** Uzun videoları test ederken ComfyUI içerisindeki video yükleme düğümünde `frame_load_cap` değerini `30` veya `45` olarak sınırlayarak çıktıyı kısa sürede doğrulayabilirsiniz.
- **Bölge Koruma Maskesi:** Beyaz boyanan alanlar orijinal video karesini korur, siyah alanlar anime difüzyon katmanından geçer.

---

## Lisans / License
Açık kaynak olarak paylaşılmıştır. İndirilen difüzyon ve ControlNet ağırlıkları kendi model lisanslarına (SD 1.5, AnimateDiff, ToonYou) tabidir.
