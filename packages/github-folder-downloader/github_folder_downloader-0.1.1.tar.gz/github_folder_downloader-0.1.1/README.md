# GitHub Folder Downloader

A command-line tool to easily download files and folders from GitHub repositories. This tool allows you to download single files or entire directories from any public GitHub repository without needing to clone the entire repository.

## Features

- Download single files from GitHub repositories
- Download entire folders recursively
- Simple command-line interface
- Support for both file URLs (blob) and folder URLs (tree)
- Customizable download location

## Installation

### Option 1: Install from PyPI

```bash
pip install github-folder-downloader
```

### Option 2: Install from source

```bash
# Clone the repository
git clone https://github.com/soykot2910/github-folder-downloader.git

# Navigate to the project directory
cd github-folder-downloader

# Install the package
pip install .
```

## Usage

### Command Line Interface

1. Basic usage:
```bash
github-download <github-url>
```

2. Download a single file:
```bash
github-download https://github.com/user/repo/blob/master/path/to/file.pdf
```

3. Download an entire folder:
```bash
github-download https://github.com/user/repo/tree/master/docs
```

4. Specify custom output directory:
```bash
github-download -o ./my-downloads https://github.com/user/repo/tree/master/docs
```

5. Interactive mode (if no URL provided):
```bash
github-download
```

### Command Line Options

```bash
github-download --help
```

Available options:
- `-o, --output`: Specify output directory (default: ./downloaded_files)
- `-h, --help`: Show help message

### Python Package Usage

You can also use it as a Python package in your code:

```python
from github_downloader import download_from_github

# Download a single file
download_from_github(
    "https://github.com/user/repo/blob/master/file.pdf"
)

# Download a folder to custom location
download_from_github(
    "https://github.com/user/repo/tree/master/docs",
    dest_folder="./my-downloads"
)
```

## URL Format Examples

### For Files
```
https://github.com/username/repository/blob/branch/path/to/file.ext
```
Example:
```
https://github.com/tensorflow/tensorflow/blob/master/README.md
```

### For Folders
```
https://github.com/username/repository/tree/branch/path/to/folder
```
Example:
```
https://github.com/tensorflow/tensorflow/tree/master/tensorflow/python
```

## Common Issues and Solutions

1. **Permission Error**: If you get a permission error while downloading, make sure you have write permissions in the output directory.

2. **Invalid URL Format**: Make sure your GitHub URL follows the correct format. It should contain either 'blob' (for files) or 'tree' (for folders).

3. **Download Failed**: If downloads fail, check your internet connection and verify that the GitHub repository is public and accessible.

## Requirements

- Python 3.6 or higher
- `requests` library (automatically installed with the package)

## Development

Want to contribute? Great! Here's how:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies:
```bash
pip install -e .
```
4. Make your changes
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- Md.Soykot
- Email: md.soykot2910@gmail.com
- GitHub: [@soykot2910](https://github.com/soykot2910)

## Support

If you encounter any issues or have questions, please:
1. Check the [Common Issues](#common-issues-and-solutions) section
2. Open an issue on GitHub
3. Contact the author via email

## Acknowledgments

- Thanks to GitHub for providing their API
- Inspired by the need to download specific parts of repositories without cloning