from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='flickpy',
    version='3.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'flickpy=Flickpy.cli:main',
        ],
    },
    install_requires=[],
    description="A Python package for displaying various loading animations in the terminal.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="MrFidal",
    author_email="mrfidal@proton.me",
    url="https://github.com/bytebreach/flickpy",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
