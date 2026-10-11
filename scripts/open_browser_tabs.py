import os
import sys
import time
import urllib.request
import webbrowser

def open_tabs():
    """
    ComfyUI sunucusu tamamen aktif hale gelip 8188 portunda yanit verene kadar
    arka planda sessizce bekler. Yapay zeka hazir oldugu an:
      1. Sekme: ComfyUI (Otomatik acilir)
      2. Sekme: 10 saniye sonra mask_tool.html acilir
      3. Sekme: 3 saniye sonra poster_tool.html acilir
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mask_tool = os.path.join(base_dir, "mask_tool.html")
    poster_tool = os.path.join(base_dir, "poster_tool.html")

    # ComfyUI sunucusunun hazir olmasini bekle (maksimum 60 saniye)
    for _ in range(60):
        time.sleep(1)
        try:
            with urllib.request.urlopen("http://127.0.0.1:8188/system_stats", timeout=1) as resp:
                if resp.status == 200:
                    break
        except Exception:
            continue

    # ComfyUI acildiktan hemen sonra 1.5 saniye bekle ve Studio'yu ac
    time.sleep(1.5)

    # 2. Sekme: Birlesik RingPulse AI Studio (Maske + Poster Tek Catida)
    studio_html = os.path.join(base_dir, "studio.html")
    target_page = studio_html if os.path.exists(studio_html) else mask_tool

    if os.path.exists(target_page):
        try:
            webbrowser.open(os.path.abspath(target_page))
        except Exception:
            os.system(f'start "" "{target_page}"')

if __name__ == "__main__":
    open_tabs()
