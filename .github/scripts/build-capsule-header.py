import base64
import pathlib
import sys

repo = pathlib.Path(".").resolve()
dist = repo / "dist"
logo_path = dist / "ana.svg"
base_path = dist / "capsule-base.svg"
out_path = dist / "capsule-header.svg"

color1 = sys.argv[1] if len(sys.argv) > 1 else "FF6B6B"
color2 = sys.argv[2] if len(sys.argv) > 2 else "4ECDC4"

if not logo_path.exists() or not base_path.exists():
    raise SystemExit("Missing dist/ana.svg or dist/capsule-base.svg")

logo = logo_path.read_text(encoding="utf-8")
base = base_path.read_text(encoding="utf-8")

base = base.replace('<svg ', '<svg preserveAspectRatio="xMidYMid slice" ')

escaped_logo_xml = logo
img_data_uri = "data:image/svg+xml;base64," + base64.b64encode(logo.encode("utf-8")).decode("ascii")

overlay = f"""<g id="ana-logo-overlay">
  <rect width="800" height="280" fill="url(#bg)" opacity="0"/>
  <image href="{img_data_uri}" x="261" y="0" width="278" height="280" preserveAspectRatio="xMidYMid meet"/>
</g>"""

gradient = f"""<linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#{color1}"/>
    <stop offset="100%" stop-color="#{color2}"/>
  </linearGradient>"""

if '<defs>' in base:
    base = base.replace('<defs>', f"<defs>\n  {gradient}")
else:
    base = base.replace('<svg ', f'<svg><defs>\n  {gradient}\n</defs>')

base = base.replace('</svg>', overlay + '\n</svg>')

out_path.write_text(base, encoding="utf-8")
print(f"Wrote composite header to {out_path}")
