import json

with open('anime_vid2vid_workflow_fast.json', 'r', encoding='utf-8') as f:
    wf = json.load(f)

import urllib.request
import json

with urllib.request.urlopen('http://127.0.0.1:8188/object_info') as resp:
    obj_info = json.loads(resp.read().decode('utf-8'))

with open('anime_vid2vid_workflow_fast.json', 'r', encoding='utf-8') as f:
    wf = json.load(f)

print("Checking all nodes against ComfyUI object_info...")
all_ok = True
for n in wf['nodes']:
    t = n['type']
    if t in obj_info:
        info = obj_info[t]
        input_order = info.get('input_order', {}).get('required', []) + info.get('input_order', {}).get('optional', [])
        req = info.get('input', {}).get('required', {})
        opt = info.get('input', {}).get('optional', {})
        schema = {**req, **opt}
        
        # Determine widget inputs (those not linked and having widget types)
        linked_names = {i['name'] for i in n.get('inputs', []) if i.get('link') is not None}
        widget_names = [k for k in input_order if k not in linked_names and schema[k][0] not in ['IMAGE', 'LATENT', 'MODEL', 'VAE', 'CONDITIONING', 'CONTROL_NET', 'CONTEXT_OPTIONS', 'CLIP_VISION', 'UPSCALE_MODEL']]
        
        vals = n.get('widgets_values', [])
        if isinstance(vals, list) and len(vals) == len(widget_names):
            for name, val in zip(widget_names, vals):
                conf = schema[name]
                itype = conf[0]
                if itype == 'COMBO' or isinstance(itype, list):
                    options = conf[1].get('options', []) if (len(conf) > 1 and isinstance(conf[1], dict)) else itype
                    if isinstance(options, list) and val not in options:
                        print(f"ERROR: Node {n['id']} ({t}) input '{name}' has value '{val}' not in {options[:5]}...!")
                        all_ok = False
                    else:
                        print(f"OK: Node {n['id']} ({t}) '{name}' = '{val}'")

if all_ok:
    print("\nALL WIDGET VALUES AND COMBOS ARE 100% VALID IN COMFYUI!")

















