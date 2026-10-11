import json

with open('animeai_workflow.json', encoding='utf-8') as f:
    wf = json.load(f)

print("Nodes count:", len(wf['nodes']))
for n in wf['nodes']:
    inps = [(i['name'], i.get('link')) for i in n.get('inputs', [])]
    outs = [(o['name'], o.get('links')) for o in n.get('outputs', [])]
    print(f"ID {n['id']} ({n['type']}) - Title: '{n.get('title', '')}'")
    print(f"   Inputs: {inps}")
    print(f"   Outputs: {outs}")
