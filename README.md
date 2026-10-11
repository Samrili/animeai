# AnimeAI Studio 🥋⚡
### Dual-Tab Video-to-Video Anime Engine & Combat Poster Atelier
*Bilingual AI Studio (Türkçe & English) Powered by ComfyUI, AnimateDiff, and ControlNet*

---

## 📌 Genel Bakış // Overview

**AnimeAI Studio**, gerçek videoları yüksek kaliteli anime sahnelerine dönüştüren ve dövüş sporları temalı tipografik afişler üreten, uçtan uca yerel bir yapay zeka stüdyosudur.

The system is engineered as a complete turnkey creative suite featuring a dual-workspace architecture:
1. **ComfyUI Backend (Tab 1):** Video-to-Video anime transformation engine powered by AnimateDiff, ControlNet (Lineart/Depth), and ToonYou Beta6 diffusion.
2. **RingPulse AI Studio (Tab 2):** Ultra-modern visual masking suite and automated combat infographic poster designer with dual high-resolution outputs.

---

## ✨ Temel Özellikler // Key Features

- 🎬 **Video 2 Video Anime Dönüşümü:**
  - Gerçek spor ve dövüş videolarını akıcı anime animasyonlarına dönüştürür.
  - Düğüm içi anlık canlı önizleme (Live Preview) oynatıcısı.
  - Ayarlanabilir kare limiti (`frame_load_cap`) ve kare hızı (`force_rate`).

- 🛡️ **Bölge Koruma & Maskeleme Atölyesi (Region Protection Mask):**
  - Videodaki marka logolarını, sponsor yazılarını, yüzleri veya sporcu figürünü anime etkisinden korur.
  - Fırça ve dikdörtgen araçlarıyla tuval üzerinde boyama; tek tıkla ComfyUI akışına otomatik aktarım.

- 🥊 **Dövüş Posteri Tasarım Atölyesi (Fighter Poster Atelier):**
  - Boks, Muay Thai, BJJ, MMA, Güreş, Judo, Sambo ve Karate dahil 120+ teknik kütüphanesi.
  - 8 farklı düzen mimarisi (*Floating Tactical*, *Side Column*, *Cyberpunk HUD*, vb.).
  - Hem yazılı tipografik afiş hem de saf temiz çizim (*Clean Art*) çıktıları.

- 🌐 **İki Dilli Kullanım (Bilingual TR / EN):**
  - Türkçe ve İngilizce arasında tek tıkla anında geçiş ve `localStorage` hafızası.
  - Eksiksiz kullanıcı rehberi ve hata/durum bildirimleri.

- ⚙️ **Akıllı Donanım Motoru (Smart Hardware Launcher):**
  - Sistemin GPU ve VRAM miktarını (4GB, 6GB, 8GB, 12GB+, 24GB) otomatik tespit eder.
  - `--lowvram`, `--normalvram` veya `--highvram` bellek bayraklarını dinamik olarak ayarlar.
  - VRAM yetersizliği (*CUDA Out-Of-Memory*) ve Windows masaüstü çökmesini önler.

---

## 💻 Sistem Gereksinimleri // System Requirements

| Donanım / Hardware | Minimum | Önerilen / Recommended |
|---|---|---|
| **İşletim Sistemi / OS** | Windows 10/11 (64-bit) / Linux | Windows 11 (64-bit) |
| **İşlemci / CPU** | 4 Çekirdek (Intel i5 / Ryzen 5) | 8 Çekirdek (Intel i7 / Ryzen 7) |
| **Ekran Kartı / GPU** | NVIDIA GTX 1660 / RTX 3050 (4-6 GB) | NVIDIA RTX 3060 / 4060+ (8-12 GB) |
| **RAM** | 16 GB DDR4 | 32 GB DDR4/DDR5 |
| **Depolama / Storage** | 15 GB boş alan (SSD önerilir) | 25 GB NVMe SSD |
| **Python** | Python 3.10, 3.11 veya 3.12 | Python 3.11 (64-bit) |

---

## 🚀 Hızlı Başlangıç // Quick Start Guide

### 1. Depoyu İndirin // Clone Repository
```bash
git clone https://github.com/KULLANICI_ADINIZ/animeai.git
cd animeai
```

### 2. Tek Tıkla Kurulum // 1-Click Automated Setup
Klasör içerisindeki **`kurulum.bat`** dosyasına çift tıklayın (veya terminalden çalıştırın):
```cmd
kurulum.bat
```
Bu komut sırasıyla:
- Python ve donanım mimarinizi test eder.
- CUDA destekli PyTorch kütüphanelerini kurar.
- Gerekli tüm yapay zeka modellerini (`toonyou_beta6`, `animatediff`, `controlnet`, `4x-ultrasharp`, vb.) Hugging Face üzerinden otomatik ve kesintisiz olarak indirir.

### 3. Başlatma // Launch Studio
Kurulum bittikten sonra **`baslat.bat`** dosyasına çift tıklayın:
```cmd
baslat.bat
```
- Donanımınıza en uygun VRAM parametreleri ayarlanır.
- ComfyUI sunucusu arka planda başlar (`127.0.0.1:8188`).
- RingPulse AI Studio tarayıcınızda otomatik olarak açılır.

---

## 📁 Proje Dizin Yapısı // Project Structure

```
animeai/
├── ComfyUI/                       # ComfyUI Çekirdek Motoru
│   ├── custom_nodes/              # Entegre Eklentiler & Custom Nodes
│   │   ├── ComfyUI-AutoTextCleaner/   # FighterPosterDesigner & Maske Entegrasyonu
│   │   ├── ComfyUI-VideoHelperSuite/  # VHS Video Oynatıcı & Render Motoru
│   │   ├── ComfyUI-AnimateDiff-Evolved/
│   │   ├── ComfyUI-Advanced-ControlNet/
│   │   └── ...
│   └── models/                    # Model Klasörleri (.gitkeep ile korunur)
├── fonts/                         # Tipografi Yazı Tipleri (Rajdhani, BebasNeue)
├── samples/                       # Örnek Video Kareleri
├── scripts/                       # Yardımcı Araçlar & İndiriciler
│   ├── download_models.py         # Otomatik Model İndirme Aracı
│   ├── smart_launcher.py          # Donanım & VRAM Optimize Başlatıcı
│   └── open_browser_tabs.py       # Akıllı Tarayıcı Sekme Yöneticisi
├── studio.html                    # RingPulse AI Studio Arayüzü
├── index.html                     # Web Giriş Sayfası (studio.html ikizi)
├── baslat.bat                     # Akıllı Başlatıcı Dosyası
├── kurulum.bat                    # Tek Tıkla Otomatik Kurulum Dosyası
├── requirements.txt               # Python Bağımlılıkları
└── README.md                      # Proje Dokümantasyonu
```

---

## ❓ Sıkça Sorulan Sorular // FAQ

**1. "CUDA Out of Memory" hatası alıyorum, ne yapmalıyım?**
- `baslat.bat` dosyasını çalıştırdığınızda sistem VRAM miktarınızı otomatik tespit eder. 6GB altındaki kartlarda sistem otomatik olarak `--lowvram` moduna geçer. Manuel müdahale gerekmez.

**2. Video üretimi çok uzun sürüyor mu?**
- Hızlı denemeler için ComfyUI ekranındaki **"1. VIDEO YUKLE"** düğümünden `frame_load_cap` değerini 30 veya 45 yapın. Bu sayede 1-2 dakikada tam sonucu test edebilirsiniz.

**3. Maskeleme ne işe yarıyor?**
- Videodaki yazıların, logoların veya dövüşçünün animeye dönüşüp bozulmasını engeller. Beyaz alanlar orijinal video kalitesinde korunur, siyah alanlar anime stiline aktarılır.

---

## 📜 Lisans // License
Bu proje açık kaynak topluluğuna sunulmuştur. Kullanılan temel modellerin (SD 1.5, AnimateDiff, ToonYou) kendi açık kaynak kullanım koşulları geçerlidir.
