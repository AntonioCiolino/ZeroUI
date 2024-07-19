from setuptools import setup, find_packages

setup(
    name="ZeroUI",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "Pillow",
        "evdev"
    ],
    author="Antonio Ciolino",
    author_email="antonio.ciolino@icloud.com",
    description="ZeroUI: A package for UI components",
    license="",
    keywords="Pi Zero, UI, touchscreen, PiTFT",
    url="https://github.com/AntonioCiolin/ZeroUI",  # Update with your URL
)
