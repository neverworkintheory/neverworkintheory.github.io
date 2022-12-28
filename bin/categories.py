"""Extract information from posts."""

import argparse
import frontmatter
import sys
import yaml


def main():
    config = _parse_args()
    categories = _get_categories(config)
    yaml.dump(categories, sys.stdout)


def _get_categories(config):
    """Extract post categories."""
    accum = {}

    for filename in config.posts:
        info = frontmatter.load(filename)
        if "categories" not in info:
            print(f"{filename} has no categories", file=sys.stderr)
        else:
            stripped = filename.replace(".md", ".html").split("/")[-1]
            fields = stripped.split("-", maxsplit=3)
            url = "/" + "/".join(fields)
            date = info["date"].strftime("%Y-%m-%d")
            for cat in info["categories"]:
                accum.setdefault(cat, set()).add((date, url, info["title"]))

    result = []
    for name in sorted(accum.keys()):
        entries = list(sorted(accum[name]))
        entries = [{"date": i[0], "reviewed": i[1], "title": i[2]} for i in entries]
        result.append({"name": name, "entries": entries})

    return result


def _parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", help="Path prefix to remove from filenames")
    parser.add_argument("posts", nargs="+", help="Paths to blog posts")
    return parser.parse_args()


if __name__ == '__main__':
    main()
