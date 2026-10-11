import json

with open('animeai_workflow.json', 'r', encoding='utf-8') as f:
    wf = json.load(f)

link_map = {l[0]: l for l in wf['links']}

for n in sorted(wf['nodes'], key=lambda x: x['id']):
    nid = n['id']
    ntype = n.get('type')
    title = n.get('title', ntype)
    pos = n.get('pos')
    size = n.get('size')
    if isinstance(pos, dict): pos = [pos.get('0', 0), pos.get('1', 0)]
    if isinstance(size, dict): size = [size.get('0', 0), size.get('1', 0)]
    
    in_s = []
    for inp in n.get('inputs', []):
        lid = inp.get('link')
        if lid and lid in link_map:
            src = link_map[lid][1]
            in_s.append(f"{inp.get('name')} <- #{src}")
            
    print(f"Node {nid:3d} | pos=({pos[0]:5.0f}, {pos[1]:5.0f}) size=({size[0]:4.0f}, {size[1]:4.0f}) | {title} [{ntype}]")
    if in_s:
        print("   IN: " + ", ".join(in_s))
