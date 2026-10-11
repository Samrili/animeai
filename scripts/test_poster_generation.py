import urllib.request
import json
import time

COMFY_URL = "http://127.0.0.1:8188"

prompt_workflow = {
    "1": {
        "class_type": "CheckpointLoaderSimple",
        "inputs": { "ckpt_name": "toonyou_beta6.safetensors" }
    },
    "2": {
        "class_type": "LoraLoader",
        "inputs": {
            "model": ["1", 0],
            "clip": ["1", 1],
            "lora_name": "more_details.safetensors",
            "strength_model": 0.6,
            "strength_clip": 0.6
        }
    },
    "3": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "clip": ["2", 1],
            "text": "masterpiece, best quality, 1man, flexible Muay Thai champion, executing question mark kick, foot whipping over opponent guard, glowing energy aura, gym arena background, dynamic action anime, 8k"
        }
    },
    "4": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "clip": ["2", 1],
            "text": "low quality, bad anatomy, deformed limbs, bad hands, extra fingers, missing fingers, blurry, text, watermark, signature"
        }
    },
    "5": {
        "class_type": "EmptyLatentImage",
        "inputs": { "width": 576, "height": 1024, "batch_size": 1 }
    },
    "6": {
        "class_type": "KSampler",
        "inputs": {
            "model": ["2", 0],
            "positive": ["3", 0],
            "negative": ["4", 0],
            "latent_image": ["5", 0],
            "seed": 448811,
            "steps": 20,
            "cfg": 7.0,
            "sampler_name": "dpmpp_2m",
            "scheduler": "karras",
            "denoise": 1.0
        }
    },
    "7": {
        "class_type": "VAEDecode",
        "inputs": { "samples": ["6", 0], "vae": ["1", 2] }
    },
    "8": {
        "class_type": "UpscaleModelLoader",
        "inputs": { "model_name": "4x-UltraSharp.pth" }
    },
    "9": {
        "class_type": "ImageUpscaleWithModel",
        "inputs": { "upscale_model": ["8", 0], "image": ["7", 0] }
    },
    "10": {
        "class_type": "FighterPosterDesigner",
        "inputs": {
            "image": ["9", 0],
            "title": "QUESTION MARK KICK",
            "tagline": "BODY TEEP FEINT TO HIGH HEAD KNOCKOUT",
            "protocol_badge": "[ TACTICAL PROTOCOL // MT-02 ]",
            "watermark": "@ringpulseofficial",
            "card_title": "/// EXECUTION KEYPOINTS",
            "target_zone": "V_TARGET: TEMPLE // MASTOID PROCESS",
            "tip_1_tag": "TEEP BAIT",
            "tip_1_desc": "Chamber knee high straight up down the center. Deceive opponent into dropping their guard to catch a front push kick.",
            "tip_2_tag": "HIP ROLL TURNOVER",
            "tip_2_desc": "At the peak apex, violently snap hip over. Convert vertical chamber into a descending roundhouse arc.",
            "tip_3_tag": "INSTEP WHIP",
            "tip_3_desc": "Slap top of instep across the back of the neck or temple as their hands are trapped low protecting body.",
            "theme_color": "Cyber Cyan",
            "layout_archetype": "Floating Tactical Callouts (Left/Right)",
            "resolution_mode": "1080x1920 (9:16 Story/Reel)"
        }
    },
    "11": {
        "class_type": "SaveImage",
        "inputs": {
            "filename_prefix": "fighter_posters/ringpulse_poster_clean",
            "images": ["10", 0]
        }
    }
}

req = urllib.request.Request(
    f"{COMFY_URL}/prompt",
    data=json.dumps({"prompt": prompt_workflow}).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)
res = urllib.request.urlopen(req)
prompt_id = json.loads(res.read())["prompt_id"]
print("Queued prompt:", prompt_id)

start_time = time.time()
while time.time() - start_time < 90:
    time.sleep(2)
    h_res = urllib.request.urlopen(f"{COMFY_URL}/history/{prompt_id}")
    history = json.loads(h_res.read())
    if prompt_id in history:
        outputs = history[prompt_id].get("outputs", {})
        if "11" in outputs and "images" in outputs["11"]:
            img_info = outputs["11"]["images"][0]
            print("Generated successfully!")
            print(f"File: {img_info['subfolder']}/{img_info['filename']}")
            break
else:
    print("Timed out waiting for generation.")
