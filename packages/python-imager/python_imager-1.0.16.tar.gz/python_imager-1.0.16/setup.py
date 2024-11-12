from setuptools import setup, find_packages

VERSION = '1.0.16'
DESCRIPTION = 'Python image program'

setup(
        name="python-imager",
        version=VERSION,
        author="T-Sana",
        author_email="tsana.code@gmail.com",
        description=DESCRIPTION,
        long_description="README.md",
        packages=find_packages(),
        install_requires=["numpy", "opencv-python", "screeninfo"],
        keywords=['python', 'image'],
        classifiers= [
            "Programming Language :: Python :: 3",
        ],
        license="LICENCE"
)