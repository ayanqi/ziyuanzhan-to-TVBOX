#!/usr/bin/env python3
import json
from pathlib import Path

SOURCE = Path('docs/data/online.json')
OUTPUT = Path('docs/data/tvbox.json')

def infer_type(api: str) -> int:
    url = api.lower()
    # TVBox: 0=XML CMS, 1=JSON CMS
    if '/inc/api.php' in url and 'json' not in url:
        return 0
    return 1

def main():
    raw = json.loads(SOURCE.read_text(encoding='utf-8-sig'))
    rows = raw if isinstance(raw, list) else raw.get('data', [])
    sites, seen = [], set()
    for row in rows:
        api = str(row.get('api', '')).strip()
        if not api or api in seen:
            continue
        seen.add(api)
        sites.append({
            'key': f'zyz_{len(sites)+1:03d}',
            'name': row.get('name') or f'资源站{len(sites)+1}',
            'type': infer_type(api),
            'api': api,
            'searchable': 1,
            'quickSearch': 1,
            'filterable': 1
        })
    OUTPUT.write_text(json.dumps({'sites': sites}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Generated {OUTPUT}: {len(sites)} sites')

if __name__ == '__main__':
    main()
