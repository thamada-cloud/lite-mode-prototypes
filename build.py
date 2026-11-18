"""Builds the Lite Mode prototype pages from src/template.html. Run: python3 build.py"""
import os
t = open('src/template.html').read()
cut = t.index('<div class="stage">')
head_part, body_part = t[:cut], t[cut:]
# folder (the public link) -> (template variant, page title, label, hint)
V = {
 'version-a': ('live', 'Lite Mode Version A', 'Version A · Live today', 'Tap the Lite switch in the header'),
 'version-b': ('e2',   'Lite Mode Version B', 'Version B · Segmented control', 'Tap Discover or Lite to switch'),
 'version-c': ('f3',   'Lite Mode Version C', 'Version C · Discover | switch | Lite', 'Tap the switch or either half'),
 'fix2':      ('fix2', 'Lite Mode Fix 2', 'Fix 2 · Segmented · Recessed track', 'Tap Discover or Lite to switch'),
 'f':         ('f',    'Lite Mode Option F', 'Option F · Discover | switch | Lite', 'Tap the switch or a label'),
}
# Earlier links that were already shared keep working and forward to the new ones
REDIRECTS = {'live': 'version-a', 'e2': 'version-b', 'f3': 'version-c'}
META = '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="robots" content="noindex, nofollow">\n<meta name="theme-color" content="#f6f8f9" media="(prefers-color-scheme: light)">\n<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'
for folder, (variant, title, name, hint) in V.items():
    sub = lambda s: s.replace('__TITLE__', title).replace('__NAME__', name).replace('__HINT__', hint).replace('__VARIANT__', variant)
    os.makedirs(folder, exist_ok=True)
    html = f'<!doctype html>\n<html lang="en">\n<head>\n{META}<base href="../">\n{sub(head_part)}</head>\n<body>\n{sub(body_part)}</body>\n</html>\n'
    open(f'{folder}/index.html', 'w').write(html)
for old, new in REDIRECTS.items():
    os.makedirs(old, exist_ok=True)
    open(f'{old}/index.html', 'w').write(f'''<!doctype html>
<html lang="en"><head>{META}<title>{V[new][1]}</title>
<meta http-equiv="refresh" content="0; url=../{new}/">
<link rel="canonical" href="../{new}/">
<script>location.replace('../{new}/' + location.hash);</script>
</head><body><p>This prototype moved to <a href="../{new}/">{V[new][2]}</a>.</p></body></html>
''')
QUICK = [('version-b','Lite','b'),('version-b','Simple','d'),('version-b','Focus','g'),('version-b','Focus','r'),('version-c','Lite','b'),('version-c','Simple','d'),('version-c','Focus','g'),('version-c','Focus','r')]
quick = ''.join(f'<a href="{v}/?name={n}&amp;icon={i}"><b>{V[v][1].replace("Lite Mode ","")} · {n} + {i.upper()}</b></a>' for v, n, i in QUICK)
cards = ''.join(f'<a href="{f}/"><b>{n}</b><span>{h}</span></a>' for f, (_, _, n, h) in V.items())
open('index.html', 'w').write(f'''<!doctype html>
<html lang="en"><head>{META}<title>Lite Mode Prototypes</title>
<style>
:root {{ --bg:#f6f8f9; --ink:#27292d; --ink2:#3f4447; --brand:#c6002b; --card:#fff; color-scheme: light; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#000; --ink:#fff; --ink2:#e6eaed; --brand:#f4747c; --card:#27292d; color-scheme: dark; }} }}
body {{ margin:0; background:var(--bg); color:var(--ink); font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text",system-ui,sans-serif; padding:48px max(16px, env(safe-area-inset-left,0px)); }}
main {{ max-width:560px; margin:0 auto; display:flex; flex-direction:column; gap:12px; }}
h1 {{ font-size:28px; margin:0; }} p {{ margin:0 0 12px; color:var(--ink2); line-height:1.5; }}
a {{ display:flex; flex-direction:column; gap:4px; padding:16px 18px; background:var(--card); border-radius:12px; text-decoration:none; color:inherit; box-shadow:0 1px 2px rgba(39,41,45,.08); }}
a:hover, a:focus-visible {{ outline:2px solid var(--brand); }}
a span {{ font-size:14px; color:var(--ink2); }}
h2 {{ font-size:20px; margin:24px 0 0; }}
form {{ display:flex; flex-wrap:wrap; gap:10px 14px; align-items:end; padding:16px 18px; background:var(--card); border-radius:12px; }}
label {{ display:flex; flex-direction:column; gap:4px; font-size:13px; color:var(--ink2); }}
select, form button {{ font:inherit; font-size:15px; padding:8px 10px; border-radius:8px; border:1px solid rgba(128,128,128,.4); background:var(--bg); color:var(--ink); }}
form button {{ background:var(--brand); color:#fff; border:0; font-weight:600; padding:9px 18px; }}
.quick {{ display:grid; grid-template-columns:1fr 1fr; gap:8px; }}
.quick a {{ padding:12px 14px; }}
.quick b {{ font-size:14px; font-weight:600; }}
</style></head>
<body><main><h1>Lite Mode prototypes</h1>
<p>Home screen with Discover and Lite. Each prototype has the same content; only the control that switches between the two views changes. Scroll each view and tap the control to switch.</p>
{cards}
<h2>Names and icons</h2>
<p>Try the shortlisted entry icons and names inside a prototype. Letters match the Custom icons board in Figma. The icon is outlined when off and filled when Lite is on.</p>
<form id="pick">
<label>Prototype <select name="v"><option value="version-b">Version B</option><option value="version-c">Version C</option><option value="version-a">Version A</option></select></label>
<label>Name <select name="name"><option>Lite</option><option>Simple</option><option>Focus</option><option>Essentials</option><option>Favorites</option><option>Quick Play</option></select></label>
<label>Icon <select name="icon"><option value="b">B Player</option><option value="d">D Simple screen</option><option value="o">O D minimal</option><option value="g">G Focus frame</option><option value="r">R Tile in focus</option><option value="">No icon</option></select></label>
<button type="submit">Open</button>
</form>
<div class="quick">{quick}</div>
<script>
document.getElementById('pick').addEventListener('submit', e => {{
  e.preventDefault(); const f = new FormData(e.target);
  const q = new URLSearchParams({{ name: f.get('name') }}); if (f.get('icon')) q.set('icon', f.get('icon'));
  location.href = f.get('v') + '/?' + q.toString();
}});
</script>
</main></body></html>
''')
print('built')
