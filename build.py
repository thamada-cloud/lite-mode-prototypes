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
META = '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="robots" content="noindex, nofollow">\n'
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
</style></head>
<body><main><h1>Lite Mode prototypes</h1>
<p>Home screen with Discover and Lite. Each prototype has the same content; only the control that switches between the two views changes. Scroll each view and tap the control to switch.</p>
{cards}</main></body></html>
''')
print('built')
