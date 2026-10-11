import os
import subprocess
import sys

REMAINING_MODELS = [
    {
        "name": "SD VAE (Colors & Latent Decode)",
        "url": "https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors",
        "dest": "ComfyUI/models/vae/vae-ft-mse-840000-ema-pruned.safetensors"
    },
    {
        "name": "IP-Adapter Plus SD1.5",
        "url": "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-plus_sd15.safetensors",
        "dest": "ComfyUI/models/ipadapter/ip-adapter-plus_sd15.safetensors"
    },
    {
        "name": "ControlNet Lineart fp16",
        "url": "https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11p_sd15_lineart_fp16.safetensors",
        "dest": "ComfyUI/models/controlnet/control_v11p_sd15_lineart_fp16.safetensors"
    },
    {
        "name": "ControlNet Depth fp16",
        "url": "https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11f1p_sd15_depth_fp16.safetensors",
        "dest": "ComfyUI/models/controlnet/control_v11f1p_sd15_depth_fp16.safetensors"
    },
    {
        "name": "AnimateDiff Motion Module (v1.5 v2)",
        "url": "https://huggingface.co/guoyww/animatediff/resolve/main/mm_sd_v15_v2.ckpt",
        "dest": "ComfyUI/models/animatediff_models/mm_sd_v15_v2.ckpt"
    },
    {
        "name": "CLIP Vision (Image Encoder)",
        "url": "https://huggingface.co/h94/IP-Adapter/resolve/main/models/image_encoder/model.safetensors",
        "dest": "ComfyUI/models/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors"
    }
]

def main():
    print(f"Kalan modeller indiriliyor... (Toplam: {len(REMAINING_MODELS)})")
    sys.stdout.flush()

    for idx, item in enumerate(REMAINING_MODELS, 1):
        name = item["name"]
        url = item["url"]
        dest = os.path.abspath(item["dest"])
        os.makedirs(os.path.dirname(dest), exist_ok=True)

        if os.path.exists(dest) and os.path.getsize(dest) > 10 * 1024 * 1024:
            sz_mb = os.path.getsize(dest) / (1024 * 1024)
            print(f"[{idx}/{len(REMAINING_MODELS)}] [MEVCUT] {name} ({sz_mb:.1f} MB)")
            sys.stdout.flush()
            continue

        print(f"\n[{idx}/{len(REMAINING_MODELS)}] >>> Indiriliyor: {name}")
        print(f"Hedef: {dest}")
        sys.stdout.flush()

        # Run curl with resume support
        cmd = [
            "curl.exe",
            "-L",
            "-C", "-",
            "--retry", "5",
            "--retry-delay", "2",
            "-o", dest,
            url
        ]

        ret = subprocess.run(cmd)
        if ret.returncode == 0:
            print(f"[BASARILI] {name} indirildi.")
        else:
            print(f"[UYARI] {name} icin curl kodu: {ret.returncode}")
        sys.stdout.flush()

    print("\nTum modellerin indirme islemi tamamlandi!")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
