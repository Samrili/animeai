import json
import copy

with open('ref_workflow.json', encoding='utf-8') as f:
    wf = json.load(f)

# Helper to find node by id or type
def find_node_by_id(nodes, nid):
    for n in nodes:
        if n['id'] == nid:
            return n
    return None

def find_nodes_by_type(nodes, ntype):
    return [n for n in nodes if n['type'] == ntype]

nodes = wf['nodes']
links = wf['links']

# 1. Update CheckpointLoaderSimple (ID 34)
ckpt_node = find_node_by_id(nodes, 34)
if ckpt_node:
    ckpt_node['widgets_values'] = ["toonyou_beta6.safetensors"]

# 2. Update VAELoader (ID 94)
vae_node = find_node_by_id(nodes, 94)
if vae_node:
    vae_node['widgets_values'] = ["vae-ft-mse-840000-ema-pruned.safetensors"]

# 3. Update ControlNet loaders (127: depth, 128: lineart)
cnet_depth = find_node_by_id(nodes, 127)
if cnet_depth:
    cnet_depth['widgets_values'] = ["control_v11f1p_sd15_depth_fp16.safetensors"]

cnet_lineart = find_node_by_id(nodes, 128)
if cnet_lineart:
    cnet_lineart['widgets_values'] = ["control_v11p_sd15_lineart_fp16.safetensors"]

# 4. Update IP-Adapter loader (140) & CLIP Vision (139)
ipa_model = find_node_by_id(nodes, 140)
if ipa_model:
    ipa_model['widgets_values'] = ["ip-adapter-plus_sd15.safetensors"]

clip_vision = find_node_by_id(nodes, 139)
if clip_vision:
    clip_vision['widgets_values'] = ["CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors"]

# 5. Update UpscaleModelLoader (123)
upscale_loader = find_node_by_id(nodes, 123)
if upscale_loader:
    upscale_loader['widgets_values'] = ["4x-UltraSharp.pth"]

# 6. Update Prompts: Positive (24) and Negative (7)
pos_node = find_node_by_id(nodes, 24)
if pos_node:
    pos_node['widgets_values'] = [
        "masterpiece, best quality, beautiful anime style, anime aesthetics, highly detailed eyes and face, Makoto Shinkai style, vivid cinematic colors, 8k resolution"
    ]

neg_node = find_node_by_id(nodes, 7)
if neg_node:
    neg_node['widgets_values'] = [
        "worst quality, low quality, normal quality, lowres, bad anatomy, bad hands, blurry, signature, watermark, jpeg artifacts, deformed"
    ]

# 7. Update Resolution: 9:16 aspect ratio (432x768)
scale_node = find_node_by_id(nodes, 136)
if scale_node:
    scale_node['widgets_values'] = [
        "nearest-exact",
        432,
        768,
        "disabled"
    ]
    scale_node['title'] = "Downscale to 9:16 (432x768)"

# 8. Bypass Circular Padding:
# Circular Padding Model (ID 150): connects 159 (or 142) -> 106 (AnimateDiff)
# In ref_workflow: link 288 went from 142 (IPAdapter) to 150 (CircularModel), and 289 went from 150 to 106 (AnimateDiff).
# We redirect link 288 directly to 106 input 0 (model)!
for l in links:
    if l[0] == 288:  # IPAdapter output
        l[3] = 106    # AnimateDiff loader
        l[4] = 0      # model input

# Remove 150 and 151 and 148 circular nodes from active graph
# For VAE: link 287 was VAE from 151 (Circular VAE) to 148. Link 254 was VAE from 94 to 151.
# We redirect link 254 to VAEEncode (154) and VAEDecode (148)!
# Change node 148 type from 'CircularVAEDecode' to 'VAEDecode'
dec_node = find_node_by_id(nodes, 148)
if dec_node:
    dec_node['type'] = 'VAEDecode'
    dec_node['title'] = 'VAE Decode (Frames)'
    # remove tiling widget
    dec_node['widgets_values'] = []
    # update input vae link to point directly from 94 (VAELoader)
    # Link 254 originates from 94 slot 0. Let's make link 287 also originate from 94 slot 0!
    for l in links:
        if l[0] == 287:
            l[1] = 94
            l[2] = 0

# Remove Circular padding nodes
wf['nodes'] = [n for n in nodes if n['id'] not in [150, 151]]

# 9. Add Full HD (1080x1920) Rescale and Video Output
# Upscaler 124 (ImageUpscaleWithModelBatched) upscales 432x768 by 4x -> 1728x3072
# We add ImageScale node (ID 200) to downscale 1728x3072 to exactly 1080x1920 (9:16 Full HD)
# and VHS_VideoCombine (ID 201) to save MP4!

max_link = max(l[0] for l in wf['links'])
link_upscale_to_scale = max_link + 1
link_scale_to_vhs = max_link + 2

node_hd_scale = {
    "id": 200,
    "type": "ImageScale",
    "pos": [1450, 400],
    "size": {"0": 315, "1": 130},
    "flags": {},
    "order": 35,
    "mode": 0,
    "inputs": [
        {"name": "image", "type": "IMAGE", "link": link_upscale_to_scale}
    ],
    "outputs": [
        {"name": "IMAGE", "type": "IMAGE", "links": [link_scale_to_vhs], "slot_index": 0}
    ],
    "properties": {"Node name for S&R": "ImageScale"},
    "widgets_values": ["lanczos", 1080, 1920, "disabled"],
    "title": "HD Resize to 1080x1920 (9:16 Full HD)"
}

node_vhs_combine = {
    "id": 201,
    "type": "VHS_VideoCombine",
    "pos": [1800, 400],
    "size": {"0": 315, "1": 490},
    "flags": {},
    "order": 36,
    "mode": 0,
    "inputs": [
        {"name": "images", "type": "IMAGE", "link": link_scale_to_vhs},
        {"name": "audio", "type": "AUDIO", "link": None, "shape": 7},
        {"name": "meta_batch", "type": "VHS_BatchManager", "link": None, "shape": 7},
        {"name": "vae", "type": "VAE", "link": None, "shape": 7}
    ],
    "outputs": [
        {"name": "Filenames", "type": "VHS_FILENAMES", "links": None}
    ],
    "properties": {"Node name for S&R": "VHS_VideoCombine"},
    "widgets_values": {
        "frame_rate": 30,
        "loop_count": 0,
        "filename_prefix": "AnimeAI_Instagram_9x16",
        "format": "video/h264-mp4",
        "pingpong": False,
        "save_output": True
    },
    "title": "Instagram 9:16 Full HD Video Output (MP4)"
}

# Connect 124 (ImageUpscaleWithModelBatched) output to 200
up_node = find_node_by_id(wf['nodes'], 124)
if up_node:
    # Add link to outputs
    up_node['outputs'][0]['links'].append(link_upscale_to_scale)

# Append links
wf['links'].append([link_upscale_to_scale, 124, 0, 200, 0, "IMAGE"])
wf['links'].append([link_scale_to_vhs, 200, 0, 201, 0, "IMAGE"])

# Append new nodes
wf['nodes'].append(node_hd_scale)
wf['nodes'].append(node_vhs_combine)

# Update KSampler for 30fps + hizli hareket kalitesi
ksampler = find_node_by_id(wf['nodes'], 3)
if ksampler:
    # Widgets: [seed, 'fixed', steps, cfg, sampler_name, scheduler, denoise]
    ksampler['widgets_values'][2] = 25              # steps (hizli hareket icin)
    ksampler['widgets_values'][3] = 7.5             # cfg
    ksampler['widgets_values'][4] = 'dpmpp_2m_sde'  # sampler: motion blur azaltir
    ksampler['widgets_values'][6] = 0.70            # denoise (guclu anime donusumu)

# ADE_LoopedUniformContextOptions (ID 122): context_overlap 6 -> 8
# [context_length, context_stride, context_overlap, closed_loop, fuse_method, ...]
ctx_node = find_node_by_id(wf['nodes'], 122)
if ctx_node:
    ctx_node['widgets_values'][2] = 8  # context_overlap: daha puzursuz hareket gecisi

# ADE_AnimateDiffLoaderWithContext (ID 106): motion_scale 0.8 -> 1.0
# [model_name, beta_schedule, motion_scale, apply_v2_models_properly, ...]
ade_node = find_node_by_id(wf['nodes'], 106)
if ade_node:
    ade_node['widgets_values'][2] = 1.0  # motion_scale: tam hareket gucu

# VHS_LoadVideo (ID 135): 30fps giris + 48 frame (~1.6 sn @ 30fps)
vhs_load = find_node_by_id(wf['nodes'], 135)
if vhs_load:
    wv = vhs_load['widgets_values']
    if isinstance(wv, dict):
        wv['force_rate'] = 30
        wv['frame_load_cap'] = 48

# Save updated workflow
out_path = 'anime_vid2vid_workflow.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(wf, f, indent=2)

print(f"Workflow successfully created: {out_path} with {len(wf['nodes'])} nodes!")

