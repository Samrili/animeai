import os
import time
import urllib.request
import webbrowser


def open_tabs():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    for _ in range(60):
        time.sleep(1)
        try:
            with urllib.request.urlopen("http://127.0.0.1:8188/system_stats", timeout=1) as resp:
                if resp.status == 200:
                    break
        except Exception:
            continue

    time.sleep(1.5)

    studio_url = "http://127.0.0.1:8188/studio.html"
    try:
        webbrowser.open(studio_url)
    except Exception:
        studio_html = os.path.join(base_dir, "studio.html")
        if os.path.exists(studio_html):
            try:
                webbrowser.open(os.path.abspath(studio_html))
            except Exception:
                os.system(f'start "" "{studio_html}"')


if __name__ == "__main__":
    open_tabs()
