from setuptools import setup, find_packages

setup(
    name="runtexts",
    version="1.3",
    packages=find_packages(),
    install_requires=[
        "pyautogui",
        "colorama",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "runtexts=runtexts.cli:main",
        ],
    },
    author="Maruf Ovi",
    author_email="fornet.ovi@gmail.com",
    description="A CLI tool to send automated messages.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/iamovi/project_runtexts",
    license="MIT",
    keywords="automation, messaging, CLI, pyautogui",
    python_requires=">=3.6",
)
