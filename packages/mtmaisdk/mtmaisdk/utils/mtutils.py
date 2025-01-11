import gzip
import importlib
import os
import random
import re
import shutil
import subprocess
import sys
import urllib
from io import BytesIO
from pathlib import Path

import httpx
from nanoid import generate


def gen_orm_id_key():
    return generate("1234567890abcdef", 16)


def ranstr(num):
    H = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    ret = []
    for i in range(num):
        ret.append(random.choice(H))
    return "".join(ret)


async def write_to_file(filename: str, text: str) -> None:
    """Asynchronously write text to a file in UTF-8 encoding.

    Args:
        filename (str): The filename to write to.
        text (str): The text to write.
    """
    import aiofiles

    # Ensure text is a string
    if not isinstance(text, str):
        text = str(text)

    # Convert text to UTF-8, replacing any problematic characters
    text_utf8 = text.encode("utf-8", errors="replace").decode("utf-8")

    async with aiofiles.open(filename, "w", encoding="utf-8") as file:
        await file.write(text_utf8)


async def write_text_to_md(text: str, filename: str = "") -> str:
    """Writes text to a Markdown file and returns the file path.

    Args:
        text (str): Text to write to the Markdown file.

    Returns
    -------
        str: The file path of the generated Markdown file.
    """
    file_path = f"outputs/{filename[:60]}.md"
    await write_to_file(file_path, text)
    return urllib.parse.quote(file_path)


async def write_md_to_pdf(text: str, filename: str = "") -> str:
    """Converts Markdown text to a PDF file and returns the file path.

    Args:
        text (str): Markdown text to convert.

    Returns
    -------
        str: The encoded file path of the generated PDF.
    """
    file_path = f"outputs/{filename[:60]}.pdf"

    try:
        from md2pdf.core import md2pdf

        md2pdf(
            file_path,
            md_content=text,
            # md_file_path=f"{file_path}.md",
            css_file_path="./frontend/pdf_styles.css",
            base_url=None,
        )
        print(f"Report written to {file_path}.pdf")
    except Exception as e:
        print(f"Error in converting Markdown to PDF: {e}")
        return ""

    encoded_file_path = urllib.parse.quote(file_path)
    return encoded_file_path


async def write_md_to_word(text: str, filename: str = "") -> str:
    """Converts Markdown text to a DOCX file and returns the file path.

    Args:
        text (str): Markdown text to convert.

    Returns
    -------
        str: The encoded file path of the generated DOCX.
    """
    import mistune

    file_path = f"outputs/{filename[:60]}.docx"

    try:
        from docx import Document
        from htmldocx import HtmlToDocx

        # Convert report markdown to HTML
        html = mistune.html(text)
        # Create a document object
        doc = Document()
        # Convert the html generated from the report to document format
        HtmlToDocx().add_html_to_document(html, doc)

        # Saving the docx document to file_path
        doc.save(file_path)

        print(f"Report written to {file_path}")

        encoded_file_path = urllib.parse.quote(file_path)
        return encoded_file_path

    except Exception as e:
        print(f"Error in converting Markdown to DOCX: {e}")
        return ""


# Regular expression for a valid filename
VALID_FILENAME_RE = r"^[\w,\s-]+\.[A-Za-z]{2,}$"


def is_valid_filename(filename: str) -> bool:
    return re.match(VALID_FILENAME_RE, filename) is not None


def ensure_directory_exists(directory: str):
    p = Path(directory)
    if not p.exists():
        Path.mkdir(directory, parents=True)


async def write_file(path: str, content: str):
    ensure_directory_exists(Path(path).parent)
    with Path.open(path, "w") as r:
        r.write(content)


async def pipe(reader, writer):
    """流转发"""
    while True:
        if reader.at_eof():
            return
        data = await reader.read(4096)
        if len(data) > 0:
            print(">:", len(data))
            writer.write(data)


def is_in_gitpod():
    """是否在gitpod中运行"""
    return bool(os.environ.get("GITPOD_REPO_ROOT"))


def in_colab():
    return bool(os.environ.get("COLAB_RELEASE_TAG"))


def get_pyproject_version():
    # content = Path("./pyproject.toml").read_text()
    content = Path("./mtmai/core/__version__.py").read_text()
    match = re.search(r'version\s*=\s*"(\d+\.\d+\.\d+)"', content)
    if not match:
        msg = "版本号未在 pyproject.toml 中找到"
        raise ValueError(msg)
    return match.group(1)


def increment_patch_version(version):
    major, minor, patch = map(int, version.split("."))
    patch += 1
    return f"{major}.{minor}.{patch}"


def pyproject_patch_version(project_dir: str = "."):
    pyproject_path = Path(f"{project_dir}/pyproject.toml")
    content = pyproject_path.read_text(encoding="utf-8")

    old_version = get_pyproject_version(project_dir)
    new_version = increment_patch_version(old_version)

    # 使用正则表达式替换旧版本号为新版本号
    new_content = re.sub(
        r'version\s*=\s*"\d+\.\d+\.\d+"', f'version = "{new_version}"', content
    )
    pyproject_path.write_text(new_content, encoding="utf-8")

    content2 = f'version = "{new_version}"\n'
    Path("./mtmai/core/__version__.py").write_text(content2)


def download_and_extract_gz(url, output_file_path):
    """
    下载并直接解压 .gz 文件到指定文件路径

    :param url: 文件下载链接
    :param output_file_path: 输出文件的完整路径
    """
    dest_folder = Path(output_file_path)

    if not Path.exists(dest_folder):
        Path.mkdir(dest_folder, parents=True)

    response = httpx.get(url, stream=True)
    response.raise_for_status()
    with gzip.open(BytesIO(response.content), "rb") as f_in:  # noqa: SIM117
        with open(output_file_path, "wb") as f_out:  # noqa: PTH123
            shutil.copyfileobj(f_in, f_out)


def install_and_import(package):
    try:
        __import__(package)
    except ModuleNotFoundError:
        print(f"Module '{package}' not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        # Re-import the package after installation
        globals()[package] = __import__(package)


def command_exists(cmd_name: str) -> bool:
    try:
        # Run the command with 'which' to check if it exists
        result = subprocess.run(
            ["which", cmd_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return result.returncode == 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    # 方式2:
    # from distutils.spawn import find_executable
    # return find_executable(cmd_name) is not None


def bash(bash_script: str):
    process = subprocess.Popen(  # noqa: S602
        bash_script,
        shell=True,
        stdout=sys.stdout,
        stderr=sys.stderr,
        text=True,
    )

    process.wait()

    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, bash_script)

    return process.returncode


def install_packages_if_missing(package_names: list[str]):
    for pkg in package_names:
        try:
            importlib.import_module(pkg)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])  # noqa: S603
