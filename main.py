"""Generate different editions of the book, as determined by profiles.yml."""


def main():
    return 1


def mask_parts(components, whitelist):
    """something recursive"""

    new_components = []

    for component in components:
        # We could be in a part, a chapter or a section
        new_component = dict()

        for key, value in component.items():
            if key == "file":
                if value in whitelist:
                    new_component["file"] = value

            elif key in ("parts", "chapters", "sections"):
                sub_components = mask_parts(value, whitelist)
                if sub_components:
                    new_component[key] = sub_components

        if new_component:

            # Add other entries, like "title": "my title"
            for key, value in component.items():
                if key not in ("file", "parts", "chapters", "sections"):
                    new_component[key] = value

            new_components.append(new_component)

    return new_components


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
