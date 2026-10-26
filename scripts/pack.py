#!/usr/bin/env python3
"""Build a portable Obsidian vault and offline reading bundle."""
import json
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / 'catalog.json').read_text())
paths = {ROOT / n['path'] for n in catalog['notes'] if n['lang'] == 'zh'}
paths |= {ROOT / '.translations/en' / n['path'] for n in catalog['notes'] if n['lang'] == 'en'}
paths |= set((ROOT / 'assets').rglob('*'))
paths |= {ROOT / p for p in catalog.get('assets',[])}
paths |= {ROOT / 'README.md', ROOT / 'SYNC.md', ROOT / 'ATTRIBUTION.md'}
paths |= set((ROOT / 'downloads').glob('*.html'))
archive = ROOT / 'downloads/interview-atlas.zip'
with ZipFile(archive, 'w', ZIP_DEFLATED) as z:
    for p in sorted(paths):
        if p.is_file():
            info=ZipInfo('interview-atlas/' + str(p.relative_to(ROOT)), date_time=(2026,10,25,0,0,0))
            info.compress_type=ZIP_DEFLATED
            z.writestr(info,p.read_bytes())
    z.writestr(ZipInfo('interview-atlas/.obsidian/app.json',date_time=(2026,10,25,0,0,0)), json.dumps({
        'useMarkdownLinks': True, 'attachmentFolderPath': 'assets'
    }))
print(f'Portable vault and HTML bundle: {archive.name} ({archive.stat().st_size:,} bytes)')
