import json

wf = json.load(open('animeai_workflow.json', encoding='utf-8'))
for nid in [3, 126, 128, 130, 131, 106, 122, 152, 24, 7]:
    n = [x for x in wf['nodes'] if x['id'] == nid][0]
    print(f"Node {nid} ({n['type']}) - Title: '{n.get('title', '')}'")
    print("   widgets:", n.get('widgets_values'))
