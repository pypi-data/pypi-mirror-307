from setuptools import setup, find_packages

VERSION = '1.0.a2'
DESCRIPTION = 'Python image program'
with open("README.md", "r", encoding="utf8") as file:
    LONG_DESCRIPTION = file.read()

setup(
        name="python-imager",
        version=VERSION,
        author="T-Sana",
        author_email="tsana.code@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=["numpy", "opencv-python", "screeninfo"],
        keywords=['python', 'image'],
        classifiers= [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
        ],
        license="LICENCE",
)