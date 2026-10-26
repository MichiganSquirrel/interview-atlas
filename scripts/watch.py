#!/usr/bin/env python3
"""A launchd-triggered, debounced watcher; no model runs or token use here."""
import fcntl, hashlib, json, os, subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LOCAL=ROOT/'.local'
LOCAL.mkdir(exist_ok=True)
STATE=LOCAL/'watch-state.json'

def fingerprint():
    modules=json.loads((ROOT/'modules.json').read_text())
    files=[]
    for directory in [*[m['id'] for m in modules],'.translations/en','assets']:
        files += [p for p in (ROOT/directory).rglob('*') if p.is_file()]
    h=hashlib.sha256()
    for p in sorted(files):
        h.update(str(p.relative_to(ROOT)).encode()); h.update(p.read_bytes())
    return h.hexdigest()

def save(state):
    temp=STATE.with_suffix('.tmp');temp.write_text(json.dumps(state,indent=2));temp.replace(STATE)

with (LOCAL/'watch.lock').open('w') as lock:
    try: fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError: sys.exit(0)
    current=fingerprint()
    state=json.loads(STATE.read_text()) if STATE.exists() else {}
    if '--initialize' in sys.argv:
        save({'published':current,'observed':current,'observed_at':time.time()});sys.exit(0)
    if current==state.get('published') and not state.get('error'): sys.exit(0)
    if current!=state.get('observed'):
        state.update(observed=current,observed_at=time.time());save(state);sys.exit(0)
    if time.time()-state.get('observed_at',0)<40: sys.exit(0)
    if time.time()-state.get('last_attempt',0)<300: sys.exit(0)
    state['last_attempt']=time.time()
    try:
        subprocess.run([sys.executable,str(ROOT/'scripts/sync.py'),'--push','--allow-stale'],cwd=ROOT,check=True)
        # If a user edits during a build, leave that newer version pending for the next pass.
        state.update(published=current,observed=fingerprint())
        state.pop('error',None)
    except Exception as e:
        state['error']=str(e);print(str(e),file=sys.stderr)
    save(state)
