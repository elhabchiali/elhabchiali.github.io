"""Check local links, assets, metadata and document landmarks. No dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json

ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=set();self.links=[];self.h1=0;self.main=0;self.description=False;self.canonical=False;self.missing_alt=[];self.duplicates=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids:self.duplicates.append(a['id'])
            self.ids.add(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='main':self.main+=1
        if tag=='meta' and a.get('name')=='description':self.description=bool(a.get('content'))
        if tag=='link' and a.get('rel')=='canonical':self.canonical=True
        if tag=='img' and 'alt' not in a:self.missing_alt.append(a.get('src'))
        for key in ('href','src'):
            if a.get(key):self.links.append(a[key])

def check():
    pages={}
    for path in ROOT.glob('*.html'):
        page=Page();page.feed(path.read_text());pages[path]=page
    errors=[]
    for path,page in pages.items():
        if page.h1!=1:errors.append(f'{path.name}: expected one H1, got {page.h1}')
        if page.main!=1:errors.append(f'{path.name}: expected one main')
        if not page.description or not page.canonical:errors.append(f'{path.name}: missing metadata')
        if page.missing_alt or page.duplicates:errors.append(f'{path.name}: alt/ID issue')
        for link in page.links:
            u=urlsplit(link)
            if u.scheme or u.netloc:continue
            target=ROOT/unquote(u.path.lstrip('/')) if u.path.startswith('/') else path.parent/unquote(u.path)
            if not u.path:target=path
            if target.is_dir():target=target/'index.html'
            if not target.is_file():errors.append(f'{path.name}: missing {link}');continue
            if u.fragment and target.suffix=='.html' and target in pages and u.fragment not in pages[target].ids:errors.append(f'{path.name}: missing fragment {link}')
    if errors:raise SystemExit('\n'.join(errors))
    print(f'PASS: {len(pages)} pages; local links, fragments, assets, metadata, landmarks and image alt attributes.')

if __name__=='__main__':check()
