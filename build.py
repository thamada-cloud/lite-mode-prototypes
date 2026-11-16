"""Builds the four Lite Mode prototype pages from src/template.html. Run: python3 build.py"""
import os
t = open('src/template.html').read()
cut = t.index('<div class="stage">')
head_part, body_part = t[:cut], t[cut:]
V = {
 'live': ('Lite Mode Live Today', 'Live today', 'Tap the Lite switch in the header'),
 'e2':   ('Lite Mode Option E2', 'Option E2 · Segmented · Inset 4', 'Tap Discover or Lite to switch'),
 'fix2': ('Lite Mode Fix 2', 'Fix 2 · Segmented · Recessed track', 'Tap Discover or Lite to switch'),
 'f':    ('Lite Mode Option F', 'Option F · Discover | switch | Lite', 'Tap the switch or a label'),
}
META = '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="robots" content="noindex, nofollow">\n'
for k, (title, name, hint) in V.items():
    sub = lambda s: s.replace('__TITLE__', title).replace('__NAME__', name).replace('__HINT__', hint).replace('__VARIANT__', k)
    os.makedirs(k, exist_ok=True)
    html = f'<!doctype html>\n<html lang="en">\n<head>\n{META}<base href="../">\n{sub(head_part)}</head>\n<body>\n{sub(body_part)}</body>\n</html>\n'
    open(f'{k}/index.html', 'w').write(html)
cards = ''.join(f'<a href="{k}/"><b>{n}</b><span>{h}</span></a>' for k, (_, n, h) in V.items())
open('index.html', 'w').write(f'''<!doctype html>
<html lang="en"><head>{META}<title>Lite Mode Prototypes</title>
<style>
:root {{ --bg:#f6f8f9; --ink:#27292d; --ink2:#3f4447; --brand:#c6002b; --card:#fff; color-scheme: light; }}
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
