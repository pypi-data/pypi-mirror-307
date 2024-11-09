from setuptools import setup, find_packages

setup(
    name="github-folder-downloader",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        'console_scripts': [
            'github-download=github_downloader.cli:main',
        ],
    },
    author="Md.Soykot",
    author_email="md.soykot2910@gmail.com",
    description="A tool to download files and folders from GitHub repositories",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/soykot2910/github-folder-downloader",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 