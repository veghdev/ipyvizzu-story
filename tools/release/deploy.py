"""A module for deploying site."""

from pathlib import Path
from subprocess import Popen
import sys


REPO_PATH = Path(__file__).parent / ".." / ".."
MKDOCS_PATH = REPO_PATH / "tools" / "mkdocs"


sys.path.insert(0, str(MKDOCS_PATH / "modules"))

from context import (  # pylint: disable=import-error, wrong-import-position, wrong-import-order
    chdir,
)
from vizzu import (  # pylint: disable=import-error, wrong-import-position, wrong-import-order
    Vizzu,
    IPYVIZZU_SITE_URL,
)


class Deploy:
    """A class for deploying site."""

    latest: bool = True

    @staticmethod
    def mike() -> None:
        """A method for deploying site."""

        version = Vizzu.get_ipyvizzustory_version()

        params = [
            "mike",
            "deploy",
        ]
        if Deploy.latest:
            params.append("-u")
        params.append(version)
        if Deploy.latest:
            params.append("latest")
        params.append("-F")
        params.append("tools/mkdocs/mkdocs.yml")

        with Popen(
            params,
        ) as process:
            process.communicate()

        if process.returncode:
            raise RuntimeError("failed to run mike")

    @staticmethod
    def set_config(restore: bool) -> None:
        """
        A method for setting config.

        Args:
            restore: A flag to restore the config.
        """

        ipyvizzu_version = Vizzu.get_ipyvizzu_version()

        with open(MKDOCS_PATH / "mkdocs.yml", "r", encoding="utf8") as fh_readme:
            content = fh_readme.read()

        if not restore:
            content = content.replace("  #  - mike:", "  - mike:")
            content = content.replace(
                "  #      version_selector: true", "      version_selector: true"
            )
            content = content.replace(
                "  #      alias_type: symlink", "      alias_type: symlink"
            )
            content = content.replace(
                "  #      canonical_version: latest", "      canonical_version: latest"
            )
            content = content.replace(
                "  #      redirect_template: ./tools/mkdocs/overrides/mike/redirect.html",
                "      redirect_template: ./tools/mkdocs/overrides/mike/redirect.html",
            )
            content = content.replace(
                f"{IPYVIZZU_SITE_URL}/latest/objects.inv",
                f"{IPYVIZZU_SITE_URL}/{ipyvizzu_version}/objects.inv",
            )

            if not Deploy.latest:
                content = content.replace(
                    "- content.action.edit",
                    "# - content.action.edit",
                )
        else:
            content = content.replace("  - mike:", "  #  - mike:")
            content = content.replace(
                "      version_selector: true", "  #      version_selector: true"
            )
            content = content.replace(
                "      alias_type: symlink", "  #      alias_type: symlink"
            )
            content = content.replace(
                "      canonical_version: latest", "  #      canonical_version: latest"
            )
            content = content.replace(
                "      redirect_template: ./tools/mkdocs/overrides/mike/redirect.html",
                "  #      redirect_template: ./tools/mkdocs/overrides/mike/redirect.html",
            )
            content = content.replace(
                f"{IPYVIZZU_SITE_URL}/{ipyvizzu_version}/objects.inv",
                f"{IPYVIZZU_SITE_URL}/latest/objects.inv",
            )

            if not Deploy.latest:
                content = content.replace(
                    "# - content.action.edit",
                    "- content.action.edit",
                )

        with open(MKDOCS_PATH / "mkdocs.yml", "w", encoding="utf8") as fh_readme:
            fh_readme.write(content)


def main() -> None:
    """
    The main method.
    It set deploys site.
    """

    with chdir(REPO_PATH):
        Deploy.set_config(restore=False)
        Deploy.mike()
        Deploy.set_config(restore=True)


main()
