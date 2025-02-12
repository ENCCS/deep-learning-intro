import re
import sys
import shutil
from pathlib import Path

_, content, *dirs = sys.argv
patched = Path(content, "_patched")

pattern_colon_fence = re.compile(
    r"""
        ^::(:+)  # 1. colon fence
        \s*      # whitespace
        ([a-z]+) # 2. directive
    """,
    flags=re.X | re.M,
)
# convert to MyST style colon fence with curly braces
replace_with_myst_directives = r"::\1{\2}"

# https://myst-parser.readthedocs.io/en/latest/syntax/cross-referencing.html#creating-explicit-targets
pattern_heading_target = re.compile(
    r"""
        ^(\#+)      # 1. heading
        \s*         # whitespace
        ([a-zA-z\s\-]+) # 2. text
        \{\#(.*)\}    # 3. target
    """,
    flags=re.X | re.M,
)
# add heading target using the syntax: (target)=
replace_with_myst_heading_target = r"(\3)=\n\1 \2"

# Note: this expression below (?:.|\n)*? is a non-capturing group containing
# any character or new lines https://stackoverflow.com/a/34958489
pattern_image_attrs_inline = re.compile(
    r"""
        (!\[(?:.|\n)*?\])     # 1. optional inline alt text
        \((.+)\)              # 2. path
        (
            \{(?:.|\n)*?\}
        )?                    # 3. attrs
    """,
    flags=re.X,
)
pattern_attrs_alt = re.compile(r"alt='(\S+)'")
pattern_attrs_width = re.compile(r"width='(\S+)'")


def replace_with_myst_attrs_line(m: re.Match[str]) -> str:
    if inline_alt_text := m.group(1):
        path_text = m.group(2)
        if attrs := m.group(3):
            alt_text = alt.group(1) if (alt := pattern_attrs_alt.search(attrs)) else ""
            width_text = (
                width.group(1) if (width := pattern_attrs_width.search(attrs)) else ""
            )
            inline_alt_text = (
                inline_alt_text.removeprefix("![").removesuffix("]").strip()
            )

            # NOTE: workaround since myst attrs_inline extension
            # does not handle widths in % due to a bug
            if "%" in width_text:
                value = int(width_text.removesuffix("%")) * 680 // 100
                width_text = f"{value}px"

            # attrs_text = f"{{ width={width_text} align=center }}"

            attrs_text = "align=center"
            if width_text:
                attrs_text += f" width={width_text}"

            attrs_text = f"{{ {attrs_text} }}"
        else:
            alt_text = ""
            attrs_text = "{ align=center }"

        return f"![{alt_text}]({path_text}){attrs_text}"
    else:
        return ""


pattern_figures_with_ref = re.compile(
    r"""
        ^!\[.*\]      # optional inline alt text
        \[(.*)\]      # 1. reference
    """,
    flags=re.X | re.M,
)


def replace_with_jinja_var(m: re.Match[str]) -> str:
    """Convert it to {{ }} for Jinja2 substitutions"""
    if ref := m.group(1):
        ref = ref.replace("-", "_")
        return " ".join(["{{", ref, " }}"])
    else:
        return ""


def patch(file: Path) -> str:
    """The main workhorse"""
    text = file.read_text()
    text = pattern_colon_fence.sub(replace_with_myst_directives, text)
    text = pattern_heading_target.sub(replace_with_myst_heading_target, text)
    text = pattern_figures_with_ref.sub(replace_with_jinja_var, text)
    text = pattern_image_attrs_inline.sub(replace_with_myst_attrs_line, text)
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
