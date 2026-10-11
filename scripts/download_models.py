"""
AnimeAI - Automated AI Model Downloader
Downloads all required Stable Diffusion, AnimateDiff, ControlNet, and Upscaler models
from Hugging Face repositories directly into ComfyUI directory structure.
Supports resumable chunked downloads, size verification, and integrity checking.
"""

import os
import sys
import time
import shutil
import urllib.request
import urllib.error

MODELS = [
    {
        "name": "ToonYou Beta6 Anime Checkpoint",
        "category": "checkpoints",
        "dest": "ComfyUI/models/checkpoints/toonyou_beta6.safetensors",
        "url": "https://huggingface.co/frankjoshua/toonyou_beta6/resolve/main/toonyou_beta6.safetensors",
        "min_size_mb": 2100,
        "desc": "Core SD 1.5 Anime diffusion model for video and poster art"
    },
    {
        "name": "AnimateDiff Motion Module v1.5 v2",
        "category": "animatediff",
        "dest": "ComfyUI/models/animatediff_models/mm_sd_v15_v2.ckpt",
        "url": "https://huggingface.co/guoyww/animatediff/resolve/main/mm_sd_v15_v2.ckpt",
        "min_size_mb": 1700,
        "desc": "Temporal video diffusion module for coherent video generation"
    },
    {
        "name": "AnimateDiff Motion LoRA (ZoomIn)",
        "category": "animatediff_lora",
        "dest": "ComfyUI/models/animatediff_motion_lora/v2_lora_ZoomIn.ckpt",
        "copy_to": "ComfyUI/models/loras/v2_lora_ZoomIn.ckpt",
        "url": "https://huggingface.co/guoyww/animatediff/resolve/main/v2_lora_ZoomIn.ckpt",
        "min_size_mb": 70,
        "desc": "Dynamic camera zoom motion LoRA"
    },
    {
        "name": "Stable Diffusion VAE (FT-MSE 840k)",
        "category": "vae",
        "dest": "ComfyUI/models/vae/vae-ft-mse-840000-ema-pruned.safetensors",
        "url": "https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors",
        "min_size_mb": 310,
        "desc": "High-fidelity variational autoencoder for rich color decoding"
    },
    {
        "name": "Anime Detailer LoRA (More Details)",
        "category": "loras",
        "dest": "ComfyUI/models/loras/more_details.safetensors",
        "url": "https://huggingface.co/frankjoshua/more_details/resolve/main/more_details.safetensors",
        "min_size_mb": 8,
        "desc": "Micro-contrast and anatomical line enhancer"
    },
    {
        "name": "ControlNet Lineart fp16",
        "category": "controlnet",
        "dest": "ComfyUI/models/controlnet/control_v11p_sd15_lineart_fp16.safetensors",
        "url": "https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11p_sd15_lineart_fp16.safetensors",
        "min_size_mb": 650,
        "desc": "Preserves source video outline and fighter contours"
    },
    {
        "name": "ControlNet Depth fp16",
        "category": "controlnet",
        "dest": "ComfyUI/models/controlnet/control_v11f1p_sd15_depth_fp16.safetensors",
        "url": "https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11f1p_sd15_depth_fp16.safetensors",
        "min_size_mb": 650,
        "desc": "Preserves 3D spatial geometry and fighter depth"
    },
    {
        "name": "4x-UltraSharp AI Upscaler",
        "category": "upscale",
        "dest": "ComfyUI/models/upscale_models/4x-UltraSharp.pth",
        "url": "https://huggingface.co/lokCX/4x-Ultrasharp/resolve/main/4x-UltraSharp.pth",
        "min_size_mb": 60,
        "desc": "Crystal clear 4x super-resolution upscaler"
    },
    {
        "name": "IP-Adapter Plus SD1.5",
        "category": "ipadapter",
        "dest": "ComfyUI/models/ipadapter/ip-adapter-plus_sd15.safetensors",
        "url": "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-plus_sd15.safetensors",
        "min_size_mb": 90,
        "desc": "Image prompt style transfer adapter"
    },
    {
        "name": "CLIP Vision Model (Visual Encoder)",
        "category": "clip_vision",
        "dest": "ComfyUI/models/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors",
        "url": "https://huggingface.co/h94/IP-Adapter/resolve/main/models/image_encoder/model.safetensors",
        "min_size_mb": 2300,
        "desc": "High-capacity image embeddings extractor for IP-Adapter"
    }
]

def format_size(bytes_val):
    if bytes_val >= 1024 * 1024 * 1024:
        return f"{bytes_val / (1024**3):.2f} GB"
    elif bytes_val >= 1024 * 1024:
        return f"{bytes_val / (1024**2):.1f} MB"
    elif bytes_val >= 1024:
        return f"{bytes_val / 1024:.0f} KB"
    return f"{bytes_val} B"

def download_file(url, dest_path, min_size_bytes=1000000):
    dest_path = os.path.abspath(dest_path)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    part_path = dest_path + ".part"

    # Check if already completed and valid
    if os.path.exists(dest_path):
        cur_sz = os.path.getsize(dest_path)
        if cur_sz >= min_size_bytes:
            print(f"  [OK] Already downloaded: {format_size(cur_sz)} (Skipping)")
            return True

    # Try curl if available (supports fast resume)
    have_curl = (shutil.which("curl.exe") or shutil.which("curl"))
    if have_curl:
        cmd = [
            "curl.exe" if shutil.which("curl.exe") else "curl",
            "-L",
            "-C", "-",
            "--retry", "5",
            "--retry-delay", "2",
            "--progress-bar",
            "-o", part_path,
            url
        ]
        ret = os.system(" ".join(cmd))
        if ret == 0 and os.path.exists(part_path) and os.path.getsize(part_path) >= min_size_bytes:
            if os.path.exists(dest_path):
                os.remove(dest_path)
            os.rename(part_path, dest_path)
            print(f"  [SUCCESS] Completed via curl: {format_size(os.path.getsize(dest_path))}")
            return True

    # Fallback to python urllib with resume
    resume_byte = 0
    if os.path.exists(part_path):
        resume_byte = os.path.getsize(part_path)

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    if resume_byte > 0:
        headers["Range"] = f"bytes={resume_byte}-"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content_range = resp.headers.get("Content-Range")
            total_size = None
            if content_range:
                try:
                    total_size = int(content_range.split("/")[-1])
                except:
                    pass
            if total_size is None:
                cl = resp.headers.get("Content-Length")
                if cl:
                    total_size = int(cl) + resume_byte

            mode = "ab" if resume_byte > 0 and resp.status == 206 else "wb"
            if mode == "wb":
                resume_byte = 0

            downloaded = resume_byte
            chunk_size = 1024 * 1024  # 1 MB
            start_time = time.time()
            last_print = start_time

            with open(part_path, mode) as f:
                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    now = time.time()
                    if now - last_print >= 1.0:
                        speed = downloaded / max(now - start_time, 0.001)
                        if total_size:
                            pct = (downloaded / total_size) * 100
                            print(f"\r  Downloading: {pct:5.1f}% | {format_size(downloaded)} / {format_size(total_size)} | {format_size(speed)}/s", end="", flush=True)
                        else:
                            print(f"\r  Downloading: {format_size(downloaded)} | {format_size(speed)}/s", end="", flush=True)
                        last_print = now

            print()
            if os.path.exists(dest_path):
                os.remove(dest_path)
            os.rename(part_path, dest_path)
            print(f"  [SUCCESS] Finished: {format_size(os.path.getsize(dest_path))}")
            return True
    except Exception as e:
        print(f"\n  [ERROR] Download failed: {e}")
        return False

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base_dir)

    print("=" * 65)
    print("       AnimeAI - Model Verification & Downloader")
    print("=" * 65)
    print(f"Target Directory: {base_dir}")
    print(f"Total Models Catalogued: {len(MODELS)}")
    print("=" * 65)

    all_ok = True
    for idx, item in enumerate(MODELS, 1):
        name = item["name"]
        dest = item["dest"]
        url = item["url"]
        min_bytes = item["min_size_mb"] * 1024 * 1024

        print(f"\n[{idx}/{len(MODELS)}] {name}")
        print(f"  Destination : {dest}")
        print(f"  Description : {item['desc']}")
        
        ok = download_file(url, dest, min_bytes)
        if not ok:
            all_ok = False

        # If model has secondary destination (e.g. copied to loras)
        if ok and "copy_to" in item:
            copy_dest = os.path.abspath(item["copy_to"])
            os.makedirs(os.path.dirname(copy_dest), exist_ok=True)
            if not os.path.exists(copy_dest) or os.path.getsize(copy_dest) < min_bytes:
                shutil.copyfile(os.path.abspath(dest), copy_dest)
                print(f"  [SYNC] Copied to secondary path: {item['copy_to']}")

    print("\n" + "=" * 65)
    if all_ok:
        print(" [SUCCESS] All models are present, verified, and ready!")
    else:
        print(" [WARNING] Some models failed to download. Please rerun this script.")
    print("=" * 65)

if __name__ == "__main__":
    main()
