import json

def build_poster_workflow():
    workflow = {
        "id": "anime_fighter_poster_1080x1920",
        "revision": 0,
        "last_node_id": 11,
        "last_link_id": 15,
        "nodes": [
            {
                "id": 1,
                "type": "CheckpointLoaderSimple",
                "pos": [-1200, -200],
                "size": [315, 98],
                "flags": {},
                "order": 0,
                "mode": 0,
                "inputs": [],
                "outputs": [
                    {"name": "MODEL", "type": "MODEL", "links": [1], "slot_index": 0},
                    {"name": "CLIP", "type": "CLIP", "links": [2], "slot_index": 1},
                    {"name": "VAE", "type": "VAE", "links": [10], "slot_index": 2}
                ],
                "properties": {"Node name for S&R": "CheckpointLoaderSimple"},
                "widgets_values": ["toonyou_beta6.safetensors"]
            },
            {
                "id": 2,
                "type": "LoraLoader",
                "pos": [-840, -200],
                "size": [315, 126],
                "flags": {},
                "order": 1,
                "mode": 0,
                "inputs": [
                    {"name": "model", "type": "MODEL", "link": 1},
                    {"name": "clip", "type": "CLIP", "link": 2}
                ],
                "outputs": [
                    {"name": "MODEL", "type": "MODEL", "links": [3], "slot_index": 0},
                    {"name": "CLIP", "type": "CLIP", "links": [4, 5], "slot_index": 1}
                ],
                "properties": {"Node name for S&R": "LoraLoader"},
                "widgets_values": ["more_details.safetensors", 0.6, 0.6]
            },
            {
                "id": 3,
                "type": "CLIPTextEncode",
                "pos": [-480, -250],
                "size": [400, 180],
                "flags": {},
                "order": 2,
                "mode": 0,
                "inputs": [
                    {"name": "clip", "type": "CLIP", "link": 4}
                ],
                "outputs": [
                    {"name": "CONDITIONING", "type": "CONDITIONING", "links": [6], "slot_index": 0}
                ],
                "title": "Positive Prompt (Fighter Style)",
                "properties": {"Node name for S&R": "CLIPTextEncode"},
                "widgets_values": ["masterpiece, best quality, 1man, athletic muscular boxer, throwing explosive lead hook punch, dynamic combat pose, boxing gloves, sweat flying, intense fierce expression, dark boxing gym ring background, dramatic volumetric rim lighting, cinematic anime combat, 8k wallpaper"]
            },
            {
                "id": 4,
                "type": "CLIPTextEncode",
                "pos": [-480, -30],
                "size": [400, 140],
                "flags": {},
                "order": 3,
                "mode": 0,
                "inputs": [
                    {"name": "clip", "type": "CLIP", "link": 5}
                ],
                "outputs": [
                    {"name": "CONDITIONING", "type": "CONDITIONING", "links": [7], "slot_index": 0}
                ],
                "title": "Negative Prompt",
                "properties": {"Node name for S&R": "CLIPTextEncode"},
                "widgets_values": ["low quality, bad anatomy, deformed limbs, bad hands, extra fingers, missing fingers, blurry, text, watermark, signature"]
            },
            {
                "id": 5,
                "type": "EmptyLatentImage",
                "pos": [-480, 150],
                "size": [315, 106],
                "flags": {},
                "order": 4,
                "mode": 0,
                "inputs": [],
                "outputs": [
                    {"name": "LATENT", "type": "LATENT", "links": [8], "slot_index": 0}
                ],
                "title": "4:5 Base Latent (640x800)",
                "properties": {"Node name for S&R": "EmptyLatentImage"},
                "widgets_values": [640, 800, 1]
            },
            {
                "id": 6,
                "type": "KSampler",
                "pos": [-40, -150],
                "size": [315, 474],
                "flags": {},
                "order": 5,
                "mode": 0,
                "inputs": [
                    {"name": "model", "type": "MODEL", "link": 3},
                    {"name": "positive", "type": "CONDITIONING", "link": 6},
                    {"name": "negative", "type": "CONDITIONING", "link": 7},
                    {"name": "latent_image", "type": "LATENT", "link": 8}
                ],
                "outputs": [
                    {"name": "LATENT", "type": "LATENT", "links": [9], "slot_index": 0}
                ],
                "properties": {"Node name for S&R": "KSampler"},
                "widgets_values": [999123, "randomize", 22, 7.0, "dpmpp_2m", "karras", 1.0]
            },
            {
                "id": 7,
                "type": "VAEDecode",
                "pos": [315, -150],
                "size": [210, 80],
                "flags": {},
                "order": 6,
                "mode": 0,
                "inputs": [
                    {"name": "samples", "type": "LATENT", "link": 9},
                    {"name": "vae", "type": "VAE", "link": 10}
                ],
                "outputs": [
                    {"name": "IMAGE", "type": "IMAGE", "links": [11], "slot_index": 0}
                ],
                "properties": {"Node name for S&R": "VAEDecode"},
                "widgets_values": []
            },
            {
                "id": 8,
                "type": "UpscaleModelLoader",
                "pos": [315, -20],
                "size": [300, 70],
                "flags": {},
                "order": 7,
                "mode": 0,
                "inputs": [],
                "outputs": [
                    {"name": "UPSCALE_MODEL", "type": "UPSCALE_MODEL", "links": [12], "slot_index": 0}
                ],
                "properties": {"Node name for S&R": "UpscaleModelLoader"},
                "widgets_values": ["4x-UltraSharp.pth"]
            },
            {
                "id": 9,
                "type": "ImageUpscaleWithModel",
                "pos": [560, -100],
                "size": [240, 100],
                "flags": {},
                "order": 8,
                "mode": 0,
                "inputs": [
                    {"name": "upscale_model", "type": "UPSCALE_MODEL", "link": 12},
                    {"name": "image", "type": "IMAGE", "link": 11}
                ],
                "outputs": [
                    {"name": "IMAGE", "type": "IMAGE", "links": [13], "slot_index": 0}
                ],
                "title": "4x-UltraSharp HD Upscaler",
                "properties": {"Node name for S&R": "ImageUpscaleWithModel"},
                "widgets_values": []
            },
            {
                "id": 10,
                "type": "FighterPosterDesigner",
                "pos": [840, -250],
                "size": [480, 820],
                "flags": {},
                "order": 9,
                "mode": 0,
                "inputs": [
                    {"name": "image", "type": "IMAGE", "link": 13}
                ],
                "outputs": [
                    {"name": "poster_image", "type": "IMAGE", "links": [14], "slot_index": 0},
                    {"name": "clean_image", "type": "IMAGE", "links": [15], "slot_index": 1}
                ],
                "title": "Fighter Poster Designer (1080x1350 + Watermark)",
                "properties": {"Node name for S&R": "FighterPosterDesigner"},
                "widgets_values": [
                    "THE LEAD HOOK",
                    "EXPLOSIVE ROTATIONAL POWER & ANGLE CUTTING",
                    "[ COMBAT LAB // PROTOCOL 01 ]",
                    "@ringpulseofficial",
                    "/// EXECUTION KEYPOINTS",
                    "V_TARGET: CHIN // TEMPLE",
                    "KINETIC TORQUE",
                    "Pivot lead foot 90° on the ball. Whip hips and core synchronously to generate maximum centrifugal force.",
                    "HORIZONTAL LOCK",
                    "Keep elbow horizontally locked level with the fist. Never drop the elbow below shoulder line at impact.",
                    "IRON COUNTER GUARD",
                    "Keep rear glove glued to the cheekbone. Slip head slightly off the center line to evade return fire.",
                    "Crimson Red",
                    "Random Layout Archetype",
                    "1080x1350 (4:5 Feed Post)",
                    "DROPPING REAR GUARD ON ROTATION",
                    "INFIGHTING / POCKET [0.5M]"
                ]
            },
            {
                "id": 11,
                "type": "SaveImage",
                "pos": [1360, -150],
                "size": [500, 680],
                "flags": {},
                "order": 10,
                "mode": 0,
                "inputs": [
                    {"name": "images", "type": "IMAGE", "link": 14}
                ],
                "title": "Save Infographic Combat Poster",
                "properties": {"Node name for S&R": "SaveImage"},
                "widgets_values": ["fighter_posters/ringpulse_poster"]
            },
            {
                "id": 12,
                "type": "SaveImage",
                "pos": [1360, 560],
                "size": [500, 680],
                "flags": {},
                "order": 11,
                "mode": 0,
                "inputs": [
                    {"name": "images", "type": "IMAGE", "link": 15}
                ],
                "title": "Save Clean Raw Artwork",
                "properties": {"Node name for S&R": "SaveImage"},
                "widgets_values": ["fighter_posters/ringpulse_clean"]
            }
        ],
        "links": [
            [1, 1, 0, 2, 0, "MODEL"],
            [2, 1, 1, 2, 1, "CLIP"],
            [3, 2, 0, 6, 0, "MODEL"],
            [4, 2, 1, 3, 0, "CLIP"],
            [5, 2, 1, 4, 0, "CLIP"],
            [6, 3, 0, 6, 1, "CONDITIONING"],
            [7, 4, 0, 6, 2, "CONDITIONING"],
            [8, 5, 0, 6, 3, "LATENT"],
            [9, 6, 0, 7, 0, "LATENT"],
            [10, 1, 2, 7, 1, "VAE"],
            [11, 7, 0, 9, 1, "IMAGE"],
            [12, 8, 0, 9, 0, "UPSCALE_MODEL"],
            [13, 9, 0, 10, 0, "IMAGE"],
            [14, 10, 0, 11, 0, "IMAGE"],
            [15, 10, 1, 12, 0, "IMAGE"]
        ],
        "groups": [
            {
                "title": "1. Model & LoRA Pipeline (Fast)",
                "bounding": [-1230, -280, 730, 250],
                "color": "#3f789e",
                "font_size": 24
            },
            {
                "title": "2. High-Impact Anime Prompts & 9:16 Latent",
                "bounding": [-500, -320, 440, 600],
                "color": "#a1503c",
                "font_size": 24
            },
            {
                "title": "3. KSampler & 4x-UltraSharp HD Upscaling",
                "bounding": [-60, -220, 880, 560],
                "color": "#4a7545",
                "font_size": 24
            },
            {
                "title": "4. Poster Designer (1080x1920 + RingPulse Watermark)",
                "bounding": [820, -320, 1060, 920],
                "color": "#784b8a",
                "font_size": 24
            }
        ],
        "config": {},
        "extra": {
            "ds": {
                "scale": 0.8,
                "offset": [1250, 350]
            }
        },
        "version": 0.4
    }
    return workflow

if __name__ == "__main__":
    wf = build_poster_workflow()
    with open("anime_fighter_poster_workflow.json", "w", encoding="utf-8") as f:
        json.dump(wf, f, indent=2)
    print("Created anime_fighter_poster_workflow.json successfully!")
