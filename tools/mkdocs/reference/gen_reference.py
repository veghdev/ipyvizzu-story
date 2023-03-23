"""A module for generating the code reference."""

from pathlib import Path
import sys
from types import ModuleType

import mkdocs_gen_files  # type: ignore

import ipyvizzustory


REPO_PATH = Path(__file__).parent / ".." / ".." / ".."
MKDOCS_PATH = REPO_PATH / "tools" / "mkdocs"


sys.path.insert(0, str(MKDOCS_PATH / "modules"))

from context import (  # pylint: disable=import-error, wrong-import-position, wrong-import-order
    chdir,
)


class Reference:
    """A class for generating the code reference."""

    # pylint: disable=too-few-public-methods

    @staticmethod
    def generate(package: ModuleType, folder: str) -> None:
        """
        A method for generating the code reference.

        Args:
            package: The src package.
            folder: The destination folder of the code reference.
        """

        for path in sorted(Path("src").rglob("*.py")):
            module_path = path.relative_to("src").with_suffix("")

            doc_path = path.relative_to("src").with_suffix(".md")
            full_doc_path = Path(folder, doc_path)

            parts = tuple(module_path.parts)

            if parts[-1] == "__main__":
                continue
            if parts[-1] == "__init__":
                parts = parts[:-1]
                doc_path = doc_path.with_name("index.md")
                full_doc_path = full_doc_path.with_name("index.md")

            item = ".".join(parts)
            if item == package.__name__:
                mkdocs_gen_files.set_edit_path(full_doc_path, ".." / path)
                with mkdocs_gen_files.open(full_doc_path, "w") as f_md:
                    f_md.write(f"{package.__doc__}\n")
                    f_md.write(f"::: {package.__name__}.get_story\n")
                    f_md.write("    options:\n")
                    f_md.write("      show_root_members_full_path: false\n")
                    f_md.write(f"::: {package.__name__}.Story\n")
                    f_md.write("    options:\n")
                    f_md.write("      show_root_members_full_path: false\n")
                    f_md.write(f"::: {package.__name__}.Slide\n")
                    f_md.write("    options:\n")
                    f_md.write("      show_root_members_full_path: false\n")
                    f_md.write(f"::: {package.__name__}.Step\n")
                    f_md.write("    options:\n")
                    f_md.write("      show_root_members_full_path: false\n")
            else:
                mkdocs_gen_files.set_edit_path(full_doc_path, ".." / path)
                with mkdocs_gen_files.open(full_doc_path, "w") as f_md:
                    f_md.write(f"::: {item}")


def main() -> None:
    """
    The main method.
    It generates the code reference.
    """

    with chdir(REPO_PATH):
        Reference.generate(ipyvizzustory, "reference")


main()
