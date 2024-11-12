from setuptools import setup, find_packages

setup(
    name="runtexts",
    version="1.1",
    packages=find_packages(),
    install_requires=[
        "pyautogui",
        "colorama" 
    ],
    entry_points={
        "console_scripts": [
            "runtexts=runtexts.cli:main",
        ],
    },
    author="Maruf Ovi",
    description="A CLI tool to send automated messages.",
    url="https://github.com/iamovi/project_runtexts",
)
