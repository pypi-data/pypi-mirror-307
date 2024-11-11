from setuptools import setup, find_packages

setup(
    name="runtexts",
    version="1.0",
    packages=find_packages(),
    install_requires=["pyautogui"],
    entry_points={
        "console_scripts": [
            "runtexts=runtexts.cli:main",
        ],
    },
    author="Maruf Ovi",
    description="A CLI tool to send automated messages.",
    url="https://github.com/iamovi/project_runtexts",  # Optional, for hosting on GitHub
)
