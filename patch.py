import re
import sys
import shutil
from pathlib import Path

_, content, *dirs = sys.argv
patched = Path(content, "_patched")

re_colon_fence = re.compile(
    r"""
        ^::(:+)  # 1. colon fence
        \s*      # whitespace
        ([a-z]+) # 2. directive
    """,
    flags=re.X | re.M
)

# https://myst-parser.readthedocs.io/en/latest/syntax/cross-referencing.html#creating-explicit-targets
re_heading_target = re.compile(
    r"""
        ^(\#+)      # 1. heading
        \s*         # whitespace
        ([a-zA-z\s\-]+) # 2. text
        \{\#(.*)\}    # 3. target
    """,
    flags=re.X | re.M
)

re_image_attrs_inline = re.compile(
    r"""
        (!\[.*?\])            # 1. optional inline alt text
        \((.+)\)              # 2. path
        (
            \{((.|\n)*?)\}
        )?                    # 3. attrs
    """,
    flags=re.X
)
re_attrs_alt = re.compile(r"alt='(\S+)'")
re_attrs_width = re.compile(r"width='(\S+)'")

def replace_attrs(m: re.Match):
    if m.group(1):
        path_text = m.group(2)
        if attrs := m.group(3):
            alt_text = alt.group(1) if (alt := re_attrs_alt.search(attrs)) else ""
            width_text = width.group(1) if (width := re_attrs_width.search(attrs)) else "680px"

            # NOTE: workaround since myst attrs_inline extension
            # does not handle widths in % due to a bug
            if "%" in width_text:
                value = int(width_text.removesuffix("%")) * 680 // 100
                width_text = f"{value}px"

            attrs_text = f"{{ width={width_text} }}"
        else:
            alt_text = ""
            attrs_text = ""
        
        return f"![{alt_text}]({path_text}){attrs_text}"

re_figures_with_ref = re.compile(
    r"""
        ^!\[.*\]      # optional inline alt text
        \[(.*)\]      # 1. reference
    """,
    flags=re.X | re.M
)

def replace_ref(m: re.Match):
    if (ref := m.group(1)):
        ref = ref.replace("-", "_")
        return " ".join(["{{", ref, " }}"])

def patch(file: Path) -> str:
    text = file.read_text()
    # convert to MyST style colon fence with curly braces
    text = re_colon_fence.sub(r"::\1{\2}", text)
    # add heading target using the syntax: (target)=
    text = re_heading_target.sub(r"(\3)=\n\1 \2", text)
    # convert it to {{ }} for Jinja2 substitutions
    text = re_image_attrs_inline.sub(replace_attrs, text)
    text = re_figures_with_ref.sub(replace_ref, text)
    return text


print(f"Patching {dirs=} into {patched}")
for dir in dirs:
    patched_dir = patched / dir
    patched_dir.mkdir(parents=True, exist_ok=True)
    for item in Path(dir).iterdir():
        item_patched = patched_dir / item.name
        if item.is_file():
            item_patched.write_text(patch(item))
        else:
            shutil.copytree(item, item_patched, dirs_exist_ok=True)

print("Creating symlinks...")
