"""Builds dist/index.html: one self-contained file with fonts and logos embedded."""
import base64, pathlib

root = pathlib.Path(__file__).parent
tpl = (root / "src" / "template.html").read_text(encoding="utf-8")

def uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode((root / path).read_bytes()).decode()

faces = [
    ("Cinzel", "fonts/cinzel.woff", "normal", "400 900"),
    ("Great Vibes", "fonts/great-vibes.woff", "normal", "400"),
    ("Cormorant Garamond", "fonts/cormorant.woff", "normal", "300 700"),
    ("Cormorant Garamond", "fonts/cormorant-italic.woff", "italic", "300 700"),
    ("Montserrat", "fonts/montserrat.woff", "normal", "100 900"),
]
css = "\n".join(
    f"@font-face{{font-family:'{fam}';src:url({uri(p, 'font/woff')}) format('woff');"
    f"font-style:{style};font-weight:{wt};font-display:swap;}}"
    for fam, p, style, wt in faces
)

out = (tpl.replace("/*__FONTFACES__*/", css)
          .replace("__LOGO_SI__", uri("assets/savvy-indians.png", "image/png"))
          .replace("__LOGO_HI__", uri("assets/hackindia.png", "image/png"))
          .replace("__LOGO_ABES__", uri("assets/abes.png", "image/png"))
          .replace("__SIGNATURE__", uri("assets/signature.png", "image/png")))

(root / "dist").mkdir(exist_ok=True)
(root / "dist" / "index.html").write_text(out, encoding="utf-8")
print("dist/index.html", round(len(out.encode()) / 1024), "KB")
