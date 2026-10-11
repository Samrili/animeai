import json
import os

def update_workflow_file(file_path):
    print(f"Updating workflow: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        wf = json.load(f)

    nodes = wf['nodes']
    links = wf['links']

    # 1. Update Node 205 (AutoTextCleaner)
    n205 = next((n for n in nodes if n['id'] == 205), None)
    if n205:
        # Set mask_mode to Box and shape_padding to 8
        n205['widgets_values'] = [
            True,
            "Box (Tum Kutu ve Sekil Koruma)",
            0.40,
            4,
            5,
            "Telea",
            8,
            "Inpaint Background (Arka Plani Temizle - Onerilen)"
        ]
        # Ensure output 1 (text_mask) links has 326
        if n205['outputs'][1]['links'] is None:
            n205['outputs'][1]['links'] = [326]
        elif 326 not in n205['outputs'][1]['links']:
            n205['outputs'][1]['links'].append(326)

    # 2. Update Node 135 (VHS_LoadVideo)
    n135 = next((n for n in nodes if n['id'] == 135), None)
    if n135:
        if 327 not in n135['outputs'][0]['links']:
            n135['outputs'][0]['links'].append(327)

    # 3. Update Node 200 (ImageScale)
    n200 = next((n for n in nodes if n['id'] == 200), None)
    if n200:
        n200['order'] = 35

    # 4. Check / Update Link 314
    # Link 314 was [314, 200, 0, 201, 0, 'IMAGE'] -> now connects 200 slot 0 to 206 slot 0
    link314 = next((l for l in links if l[0] == 314), None)
    if link314:
        link314[3] = 206
        link314[4] = 0

    # 5. Add / Update Node 206 (AutoTextShapeOverlay)
    n206 = next((n for n in nodes if n['id'] == 206), None)
    if not n206:
        n206 = {
            "id": 206,
            "type": "AutoTextShapeOverlay",
            "pos": [1800, 400],
            "size": [320, 220],
            "flags": {},
            "order": 36,
            "mode": 0,
            "inputs": [
                {
                    "name": "anime_images",
                    "type": "IMAGE",
                    "link": 314
                },
                {
                    "name": "original_images",
                    "type": "IMAGE",
                    "link": 327
                },
                {
                    "name": "text_mask",
                    "type": "MASK",
                    "link": 326
                },
                {
                    "name": "blend_feather",
                    "type": "INT",
                    "widget": {
                        "name": "blend_feather"
                    }
                },
                {
                    "name": "opacity",
                    "type": "FLOAT",
                    "widget": {
                        "name": "opacity"
                    }
                },
                {
                    "name": "user_mask",
                    "type": "MASK",
                    "link": 329
                },
                {
                    "name": "cleaned_images",
                    "type": "IMAGE",
                    "link": 330
                }
            ],
            "outputs": [
                {
                    "name": "images",
                    "type": "IMAGE",
                    "links": [328],
                    "shape": 3,
                    "slot_index": 0
                }
            ],
            "properties": {
                "Node name for S&R": "AutoTextShapeOverlay"
            },
            "widgets_values": [
                2,
                1.0
            ],
            "title": "Auto Text & Shape Preserver (Overlay)"
        }
        nodes.append(n206)
    else:
        n206['pos'] = [1800, 400]
        n206['order'] = 36
        user_mask_inp = next((i for i in n206['inputs'] if i['name'] == 'user_mask'), None)
        if not user_mask_inp:
            n206['inputs'].append({
                "name": "user_mask",
                "type": "MASK",
                "link": 329
            })
        else:
            user_mask_inp['link'] = 329

        cleaned_inp = next((i for i in n206['inputs'] if i['name'] == 'cleaned_images'), None)
        if not cleaned_inp:
            n206['inputs'].append({
                "name": "cleaned_images",
                "type": "IMAGE",
                "link": 330
            })
        else:
            cleaned_inp['link'] = 330

    # Ensure Node 205 output 0 (cleaned images) has link 330
    if n205:
        if n205['outputs'][0]['links'] is None:
            n205['outputs'][0]['links'] = [320, 330]
        elif 330 not in n205['outputs'][0]['links']:
            n205['outputs'][0]['links'].append(330)

    # 5.1 Add / Update Node 207 (LoadImage for protection_mask.png)
    n207 = next((n for n in nodes if n['id'] == 207), None)
    if not n207:
        n207 = {
            "id": 207,
            "type": "LoadImage",
            "pos": [1450, 600],
            "size": [315, 314],
            "flags": {},
            "order": 35,
            "mode": 0,
            "inputs": [],
            "outputs": [
                {
                    "name": "IMAGE",
                    "type": "IMAGE",
                    "links": [],
                    "slot_index": 0
                },
                {
                    "name": "MASK",
                    "type": "MASK",
                    "links": [329],
                    "slot_index": 1
                }
            ],
            "properties": {
                "Node name for S&R": "LoadImage"
            },
            "widgets_values": [
                "protection_mask.png",
                "image"
            ],
            "title": "Koruma Maskesi (Beyaz=Koru, Siyah=Anime)"
        }
        nodes.append(n207)
    else:
        n207['widgets_values'] = ["protection_mask.png", "image"]
        if 329 not in n207['outputs'][1]['links']:
            n207['outputs'][1]['links'].append(329)

    # 6. Update Node 201 (VHS_VideoCombine)
    n201 = next((n for n in nodes if n['id'] == 201), None)
    if n201:
        n201['pos'] = [2180, 400]
        n201['order'] = 37
        # input 0 'images' now connected to link 328
        n201['inputs'][0]['link'] = 328

    # 7. Add new links if not present
    existing_link_ids = {l[0] for l in links}
    if 326 not in existing_link_ids:
        links.append([326, 205, 1, 206, 2, "MASK"])
    if 327 not in existing_link_ids:
        links.append([327, 135, 0, 206, 1, "IMAGE"])
    if 328 not in existing_link_ids:
        links.append([328, 206, 0, 201, 0, "IMAGE"])
    if 329 not in existing_link_ids:
        links.append([329, 207, 1, 206, 5, "MASK"])
    if 330 not in existing_link_ids:
        # slot index 6 is cleaned_images
        cleaned_slot_idx = next(i for i, inp in enumerate(n206['inputs']) if inp['name'] == 'cleaned_images')
        links.append([330, 205, 0, 206, cleaned_slot_idx, "IMAGE"])

    wf['last_node_id'] = max(n['id'] for n in nodes)
    wf['last_link_id'] = max(l[0] for l in links)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(wf, f, indent=2)

    print(f"Successfully updated {file_path}! Total nodes: {len(nodes)}, Total links: {len(links)}")

if __name__ == '__main__':
    update_workflow_file('animeai_workflow.json')
    fast_wf = 'ComfyUI/user/default/workflows/anime_vid2vid_workflow_fast.json'
    if os.path.exists(fast_wf):
        update_workflow_file(fast_wf)
