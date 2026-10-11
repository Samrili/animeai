import os
import sys
import time
import requests

MODELS = [
    {
        "name": "SD VAE (Colors & Latent Decode)",
        "url": "https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors",
        "dest": "ComfyUI/models/vae/vae-ft-mse-840000-ema-pruned.safetensors"
    },
    {
        "name": "4x-UltraSharp AI Upscaler",
        "url": "https://huggingface.co/lokCX/4x-Ultrasharp/resolve/main/4x-UltraSharp.pth",
        "dest": "ComfyUI/models/upscale_models/4x-UltraSharp.pth"
    },
    {
        "name": "IP-Adapter Plus SD1.5 (Style Transfer)",
        "url": "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-plus_sd15.safetensors",
        "dest": "ComfyUI/models/ipadapter/ip-adapter-plus_sd15.safetensors"
    },
    {
        "name": "ControlNet Lineart fp16 (Outlines)",
        "url": "https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11p_sd15_lineart_fp16.safetensors",
        "dest": "ComfyUI/models/controlnet/control_v11p_sd15_lineart_fp16.safetensors"
    },
    {
        "name": "ControlNet Depth fp16 (Depth Map)",
        "url": "https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11f1p_sd15_depth_fp16.safetensors",
        "dest": "ComfyUI/models/controlnet/control_v11f1p_sd15_depth_fp16.safetensors"
    },
    {
        "name": "AnimateDiff Motion Module v1.5 v2",
        "url": "https://huggingface.co/guoyww/animatediff/resolve/main/mm_sd_v15_v2.ckpt",
        "dest": "ComfyUI/models/animatediff_models/mm_sd_v15_v2.ckpt"
    },
    {
        "name": "CLIP Vision Model (Visual Encoder)",
        "url": "https://huggingface.co/h94/IP-Adapter/resolve/main/models/image_encoder/model.safetensors",
        "dest": "ComfyUI/models/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors"
    },
    {
        "name": "Anime Checkpoint (ToonYou Beta6)",
        "url": "https://huggingface.co/frankjoshua/toonyou_beta6/resolve/main/toonyou_beta6.safetensors",
        "dest": "ComfyUI/models/checkpoints/toonyou_beta6.safetensors"
    }
]

def download_model(item):
    name = item["name"]
    url = item["url"]
    dest = os.path.abspath(item["dest"])
    tmp_dest = dest + ".tmp"
    os.makedirs(os.path.dirname(dest), exist_ok=True)

    if os.path.exists(dest) and os.path.getsize(dest) > 1000000:
        sz_mb = os.path.getsize(dest) / (1024 * 1024)
        print(f"[MEVCUT] {name} ({sz_mb:.1f} MB) zaten tam olarak indirilmis.")
        sys.stdout.flush()
        return

    print(f"\n=======================================================")
    print(f"Indiriliyor: {name}")
    print(f"URL: {url}")
    print(f"Hedef: {dest}")
    print(f"=======================================================")
    sys.stdout.flush()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    # Check existing partial size
    resume_header = {}
    downloaded_bytes = 0
    if os.path.exists(tmp_dest):
        downloaded_bytes = os.path.getsize(tmp_dest)
        resume_header = {"Range": f"bytes={downloaded_bytes}-"}
        print(f"Kaldigi yerden devam ediliyor: {downloaded_bytes / (1024*1024):.1f} MB")
        sys.stdout.flush()

    headers.update(resume_header)

    response = requests.get(url, headers=headers, stream=True, timeout=30)
    
    if response.status_code == 416: # Range not satisfiable, file might be complete
        response = requests.get(url, headers={"User-Agent": headers["User-Agent"]}, stream=True, timeout=30)
        downloaded_bytes = 0

    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0)) + downloaded_bytes
    mode = 'ab' if downloaded_bytes > 0 else 'wb'

    chunk_size = 2 * 1024 * 1024 # 2MB
    last_print = time.time()
    start_time = time.time()
    current_bytes = downloaded_bytes

    with open(tmp_dest, mode) as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                current_bytes += len(chunk)
                now = time.time()
                if now - last_print >= 2.0 or current_bytes >= total_size:
                    speed = (current_bytes - downloaded_bytes) / (now - start_time + 0.001) / (1024 * 1024)
                    pct = (current_bytes / total_size * 100) if total_size > 0 else 0
                    print(f"  --> {current_bytes/(1024*1024):.1f} / {total_size/(1024*1024):.1f} MB ({pct:.1f}%) | Hiz: {speed:.2f} MB/s")
                    sys.stdout.flush()
                    last_print = now

    if os.path.exists(dest):
        os.remove(dest)
    os.rename(tmp_dest, dest)
    print(f"[TAMAMLANDI] {name} basariyla kaydedildi!\n")
    sys.stdout.flush()

def main():
    print(f"Model indirme baslatildi. Toplam {len(MODELS)} model.")
    sys.stdout.flush()
    for item in MODELS:
        try:
            download_model(item)
        except Exception as e:
            print(f"[HATA] {item['name']} indirilemedi: {e}")
            sys.stdout.flush()
    print("\nTum modeller hazir!")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
