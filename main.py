"""Generate different editions of the book, as determined by profiles.yml."""


def main():
    return 1


def mask_parts(parts, whitelist):
    """Strip files that don't match whitelist from parts."""
    new_parts = []

    # This could be done better (recursively or otherwise) since parts,
    # chapters and sections have similar structures but this is simpler
    # if the nesting structure is relatively stable.
    for part in parts:
        new_chapters = []

        for chapter in part["chapters"]:
            new_chapter = dict()

            if chapter["file"] in whitelist:
                new_chapter["file"] = chapter["file"]

            if chapter.get("sections"):
                new_sections = []
                for section in chapter["sections"]:
                    new_section = dict()

                    if section.get("sections"):
                        new_sub_sections = []

                        for sub_section in section["sections"]:
                            if sub_section["file"] in whitelist:
                                new_sub_sections.append(sub_section)

                        if new_sub_sections:
                            new_section["sections"] = new_sub_sections

                    if section["file"] in whitelist:
                        new_section["file"] = section["file"]

                    if new_section:
                        if section.get("title"):
                            new_section["title"] = section["title"]
                        new_sections.append(new_section)

                if new_sections:
                    new_chapter["sections"] = new_sections

            if new_chapter:
                if chapter.get("title"):
                    new_chapter["title"] = chapter["title"]
                new_chapters.append(new_chapter)

        if new_chapters:
            new_parts.append({"chapters": new_chapters})

    return new_parts


def mask_toc(toc, whitelist):
    """Strip files from toc if not in whitelist."""

    # Otherwise we would have to mutate toc, even as we iterated
    # over it.
    new_toc = dict()

    for key, value in toc.items():
        if key == "parts":
            new_toc[key] = mask_parts(value, whitelist)

        else:
            # Copy anything else from the toc root level
            new_toc[key] = value

    return new_toc


if __name__ == "__main__":
    main()  # pragma: no cover
