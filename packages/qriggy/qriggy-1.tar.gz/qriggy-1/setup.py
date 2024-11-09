from setuptools import setup, find_packages

setup(
    name="qriggy",
    version="1",
    packages=find_packages(),
    install_requires=[
        "qrcode[pil]",
    ],
    description="A simple QR code generator package.",
    author="ZIGGY",
    author_email="xx@gmail.com",
    license="MIT",
)
