#!/usr/bin/env python3
"""Show the annotation paragraphs of item descriptions properly in the
landscape2 output.

scripts/build_data.py appends each annotation to the item description as
a separate "Label: value" paragraph. landscape2 inserts descriptions as
plain text, so in the item detail views (modal and detail page) this
script:
- adds `white-space: pre-line` to the description styles, so the blank
  lines between paragraphs are kept;
- renders the description through __ddiDesc (appended to the bundle),
  which shows the "Label:" of every paragraph after the first in bold.
  It builds DOM nodes with textContent, so no data is parsed as HTML.
Card previews (2-line clamp) are left as they are.

Run after every `landscape2 build`, since the build overwrites build/:
    python3 scripts/patch_build.py [build-dir]

The script fails if a snippet is no longer found (e.g. when run twice on
the same build, or after a landscape2 upgrade), so a patch is never
skipped silently.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (old snippet, new snippet) in the main bundle.
PATCHES = (
    # CSS-in-JS description styles of the detail modal and detail page.
    (
        "aH=ue`\n  font-size: 0.9rem !important;\n`",
        "aH=ue`\n  font-size: 0.9rem !important;\n  white-space: pre-line;\n`",
    ),
    (
        "SH=ue`\n  font-size: 0.9rem;\n`",
        "SH=ue`\n  font-size: 0.9rem;\n  white-space: pre-line;\n`",
    ),
    # Description inserts of the same two views.
    (
        "E(T,`mt-4 text-muted ${aH}`),y(T,r)",
        "E(T,`mt-4 text-muted ${aH}`),y(T,()=>__ddiDesc(r()))",
    ),
    (
        "E(m,`mt-4 mb-3 text-muted ${SH}`),y(m,r)",
        "E(m,`mt-4 mb-3 text-muted ${SH}`),y(m,()=>__ddiDesc(r()))",
    ),
)

# Appended to the bundle; function declarations are hoisted, so the
# patched inserts above can call it. Returns the text unchanged unless it
# has annotation paragraphs, otherwise an array of strings and <strong>
# nodes, which Solid's insert renders as is.
HELPER = r"""
function __ddiDesc(t){if(typeof t!=="string"||!t.includes("\n\n"))return t;return t.split("\n\n").flatMap((p,i)=>{const o=i>0?["\n\n"]:[];const m=i>0&&p.match(/^([^:\n]{1,80}):\s/);if(m){const b=document.createElement("strong");b.textContent=m[1]+":";o.push(b,p.slice(m[1].length+1))}else o.push(p);return o})}
"""

# The bundle name carries a per-build hash.
GLOB = "assets/index-*.js"


def main():
    build = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "build"
    files = sorted(build.glob(GLOB))
    if not files:
        sys.exit(f"no landscape2 output found in {build}")

    counts = {old: 0 for old, _ in PATCHES}
    for path in files:
        text = path.read_text(encoding="utf-8")
        new_text = text
        for old, new in PATCHES:
            n = new_text.count(old)
            if n:
                counts[old] += n
                new_text = new_text.replace(old, new)
        if new_text != text:
            if "__ddiDesc(r())" in new_text:
                new_text = new_text.rstrip("\n") + "\n" + HELPER.lstrip("\n")
            path.write_text(new_text, encoding="utf-8")
            print(f"patched {path.relative_to(build)}")

    missing = [old for old, n in counts.items() if n == 0]
    for old, n in counts.items():
        print(f"{n:3d}x {old.splitlines()[0]}")
    if missing:
        sys.exit("not found (already patched, or landscape2 changed): "
                 + "; ".join(m.splitlines()[0] for m in missing))


if __name__ == "__main__":
    main()
