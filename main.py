"""Generate different editions of the book, as determined by profiles.yml."""
from typing import Any, Dict, List

# from copy import deepcopy


def main():
    return 1


def mask_rec(
    parts_chapters_sections: List[Dict[str, Any]], whitelist: List[str]
) -> None:
    result = []

    # Each item is a dict
    for item in parts_chapters_sections:

        if "file" in item:
            if item["file"] in whitelist:
                result.append(item)

    return result


def mask_toc(toc, whitelist):
    """Strip files from toc if not in whitelist."""

    # Otherwise we would have to mutate toc, even as we iterated
    # over it.
    new_toc = dict()

    for key, value in toc.items():
        if key == "parts":
            new_parts = []

            # This could be done better (recursively or otherwise) since parts,
            # chapters and sections have similar structure but this is simpler
            # if the nesting structure is relatively stable.
            for part in value:
                new_chapters = []

                for chapter in part["chapters"]:

                    if chapter["file"] in whitelist:
                        new_chapters.append({"file": chapter["file"]})

                new_parts.append({"chapters": new_chapters})

            new_toc["parts"] = new_parts
        else:
            # Copy anything else from the toc root level
            new_toc[key] = value

    return new_toc


if __name__ == "__main__":
    main()
