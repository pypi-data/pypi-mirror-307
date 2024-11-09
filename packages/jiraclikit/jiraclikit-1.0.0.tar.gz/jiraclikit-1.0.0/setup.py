from pathlib import Path

import setuptools


def read_multiline_as_list(file_path: Path | str) -> list[str]:
    with open(file_path) as fh:
        contents = fh.read().split("\n")
        if contents[-1] == "":
            contents.pop()
        return contents


requirements = read_multiline_as_list("requirements.txt")
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jiraclikit",
    version="1.0.0",
    author="hashtagcyber",
    author_email="domko@rabbit.tech",
    description="Kit (as in baby bunny) for Jira CLI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/q-os/security",
    packages=setuptools.find_packages(),
    python_requires=">=3.12",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "jc=jiraclikit.jc:main",
        ],
    },
)
