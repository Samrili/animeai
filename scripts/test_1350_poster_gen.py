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
            "text": "masterpiece, best quality, 1man, athletic muscular boxer, throwing explosive lead hook punch, dynamic combat pose, boxing gloves, sweat flying, intense fierce expression, dark boxing gym ring background, dramatic volumetric rim lighting, cinematic anime combat, 8k wallpaper"
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
        "inputs": { "width": 640, "height": 800, "batch_size": 1 }
    },
    "6": {
        "class_type": "KSampler",
        "inputs": {
            "model": ["2", 0],
            "positive": ["3", 0],
            "negative": ["4", 0],
            "latent_image": ["5", 0],
            "seed": 918273,
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
            "title": "THE LEAD HOOK",
            "tagline": "EXPLOSIVE ROTATIONAL POWER & ANGLE CUTTING",
            "protocol_badge": "[ COMBAT LAB // PROTOCOL 01 ]",
            "watermark": "@ringpulseofficial",
            "card_title": "/// EXECUTION KEYPOINTS",
            "target_zone": "V_TARGET: CHIN // TEMPLE",
            "tip_1_tag": "KINETIC TORQUE",
            "tip_1_desc": "Pivot lead foot 90° on the ball. Whip hips and core synchronously to generate maximum centrifugal force.",
            "tip_2_tag": "HORIZONTAL LOCK",
            "tip_2_desc": "Keep elbow horizontally locked level with the fist. Never drop the elbow below shoulder line at impact.",
            "tip_3_tag": "IRON COUNTER GUARD",
            "tip_3_desc": "Keep rear glove glued to the cheekbone. Slip head slightly off the center line to evade return fire.",
            "theme_color": "Random Palette",
            "layout_archetype": "Random Layout Archetype",
            "resolution_mode": "1080x1350 (4:5 Feed Post)",
            "caution_flaw": "DROPPING REAR GUARD ON ROTATION",
            "range_class": "INFIGHTING / POCKET [0.5M]"
        }
    },
    "11": {
        "class_type": "SaveImage",
        "inputs": {
            "filename_prefix": "fighter_posters/ringpulse_1350_poster",
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
print("Queued 1080x1350 prompt successfully:", prompt_id)

start_time = time.time()
while time.time() - start_time < 90:
    time.sleep(2)
    h_res = urllib.request.urlopen(f"{COMFY_URL}/history/{prompt_id}")
    history = json.loads(h_res.read())
    if prompt_id in history:
        outputs = history[prompt_id].get("outputs", {})
        if "11" in outputs and "images" in outputs["11"]:
            img_info = outputs["11"]["images"][0]
            print("Generated 1080x1350 poster successfully!")
            print(f"File: {img_info['subfolder']}/{img_info['filename']}")
            break
else:
    print("Timed out waiting for generation.")
