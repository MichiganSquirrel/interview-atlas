#!/usr/bin/env python3
"""Validate, export, and push only explicitly managed interview files."""
import argparse, fcntl, json, os, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = Path(os.environ.get('INTERVIEW_SITE', str(Path.home() / 'personal_site'))).resolve()
MODULES = [m['id'] for m in json.loads((ROOT / 'modules.json').read_text())]
NOTE_PATHS = MODULES + ['.translations', 'assets', 'downloads', 'scripts', '.github',
    'catalog.json', 'modules.json', 'README.md', 'SYNC.md', 'ATTRIBUTION.md',
    'AGENTS.md', '.gitignore', 'package.json', 'package-lock.json']
SITE_PATHS = ['src/data/interview-catalog.json', 'src/components/InterviewHub.astro',
    'src/components/InterviewNote.astro', 'src/pages/interview', 'src/pages/cn/interview',
    'src/layouts/BaseLayout.astro', 'public/_headers', 'public/interview-notes']

def run(args, cwd=ROOT, env=None):
    print('+', ' '.join(map(str,args)), flush=True)
    return subprocess.run(list(map(str,args)),cwd=cwd,env=env,check=True)

def publish(repo, paths, message):
    # A branch divergence is reported, never resolved by rewriting user history.
    run(['git','fetch','origin','main'],repo)
    if subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD'],cwd=repo).returncode:
        raise RuntimeError(f'{repo}: remote main has new commits; reconcile before publishing')
    existing = [p for p in paths if (repo / p).exists() or subprocess.run(
        ['git','ls-files','--error-unmatch',p],cwd=repo,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0]
    run(['git','add','-A','--',*existing],repo)
    changed = subprocess.run(['git','diff','--cached','--quiet','--',*existing],cwd=repo).returncode
    if changed:
        run(['git','commit','--only','-m',message,'--',*existing],repo)
    run(['git','push','origin','HEAD:main'],repo)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--push',action='store_true')
    parser.add_argument('--allow-stale',action='store_true')
    args=parser.parse_args()
    (ROOT/'.local').mkdir(exist_ok=True)
    with (ROOT/'.local/sync.lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        env={**os.environ,'INTERVIEW_SITE':str(SITE)}
        run(['node','scripts/build.mjs',*(['--allow-stale'] if args.allow_stale else [])],env=env)
        run(['python3','scripts/pack.py'])
        # Copy the archive created after the HTML export.
        shutil.copy2(ROOT/'downloads/interview-atlas.zip',SITE/'public/interview-notes/downloads/interview-atlas.zip')
        run(['npm','run','build'],SITE)
        if args.push:
            publish(ROOT,NOTE_PATHS,'notes: sync interview sources and visual exports')
            publish(SITE,SITE_PATHS,'site: sync bilingual interview atlas')
        print('Interview notes, offline bundle, and website are synchronized.',flush=True)
if __name__=='__main__': main()
