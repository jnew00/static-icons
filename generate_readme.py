import os

# Your GitHub username and repo name
USERNAME = "jnew00"
REPO = "static-icons"
BRANCH = "main"

# Base URL for raw images
BASE_URL = f"https://raw.githubusercontent.com/{USERNAME}/{REPO}/{BRANCH}/"

# Thumbnail width (in pixels) - configurable
THUMBNAIL_WIDTH = 64

# Output README filename
OUTPUT = "README.md"

# Markdown header
HEADER = """# 📂 Static Icons / Images

These are my images hosted for Unraid or other purposes to hotlink.

---
"""

# Markdown footer with instructions
INSTRUCTIONS = f"""
---

## 💡 How to Use

✅ **Right-click any icon** and copy the link to use it in Unraid Docker container templates or elsewhere.

✅ **Example Direct URL:**
```
https://raw.githubusercontent.com/{USERNAME}/{REPO}/{BRANCH}/folder/icon.png
```
"""

def generate_table(filepaths):
    """Generate a Markdown table with thumbnails and filenames."""
    lines = []
    lines.append("| Icon | Filename |")
    lines.append("|:-:|:-:|")
    for f in filepaths:
        img = f'<a href="{BASE_URL}{f}"><img src="{BASE_URL}{f}" width="{THUMBNAIL_WIDTH}"></a>'
        name = f"`{os.path.basename(f)}`"
        lines.append(f"| {img} | {name} |")
    return "\n".join(lines)

def main():
    # Get a list of all top-level subfolders
    subfolders = [f.name for f in os.scandir(".") if f.is_dir() and not f.name.startswith(".")]
    subfolders.sort()

    markdown = HEADER

    if not subfolders:
        markdown += "_No folders found._"
    else:
        for folder in subfolders:
            # Collect images in this folder
            icons = []
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith((".png", ".jpg", ".jpeg", ".svg", ".gif")):
                        relpath = os.path.relpath(os.path.join(root, file), ".")
                        icons.append(relpath)
            icons.sort()

            if icons:
                # Add heading for this folder
                markdown += f"\n## 📁 {folder.capitalize()}\n\n"
                markdown += generate_table(icons)
                markdown += "\n"
            else:
                pass

    markdown += INSTRUCTIONS

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"\n✅ README.md generated with icons grouped by folder, one per row.\n")

if __name__ == "__main__":
    main()