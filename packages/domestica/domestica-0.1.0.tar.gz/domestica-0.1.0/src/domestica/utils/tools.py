import asyncio
import os
import shutil
import sys
import tarfile
import zipfile

import aiohttp

from ..models import Quality
from . import appdirs


async def download_m3u8_video(
    url: str,
    save_dir: str,
    quality: Quality = Quality.P1080,
    subtitle_lang: str = "en",
    output_name: str = "output",
) -> None:
    """
    Downloads a video using N_m3u8DL-RE with specific options.

    Parameters:
    - url (str): The URL of the video to be downloaded.
    - save_dir (str): The directory where the downloaded video will be saved.
    - quality (Quality): The desired video quality, e.g., Quality.P1080. Default is Quality.P1080.
    - subtitle_lang (str): The language of the subtitles desired, e.g., "en".
    - output_name (str): The name of the output file without the extension.
    """
    os.makedirs(save_dir, exist_ok=True)

    print(f"[DOWNLOADING] {output_name}", flush=True, end="")

    download_command = [
        "N_m3u8DL-RE",
        "--select-video",
        f"res='{quality.value}*':codec=hvc1:for=best",
        "--sub-format",
        "SRT",
        "--select-subtitle",
        f'lang="{subtitle_lang}":for=all',
        "--auto-subtitle-fix",
        url,
        "--save-dir",
        save_dir,
        "--save-name",
        output_name,
        "--concurrent-download",
    ]

    process = await asyncio.create_subprocess_exec(
        *download_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    await process.wait()

    if process.returncode == 0:
        print(f"\r[COMPLETED] {output_name}")
    else:
        print(f"\r[ERROR] {output_name}")


async def download_file(url: str, save_dir: str, output: str) -> None:
    """
    Downloads a file from a URL and saves it to the specified path.

    Args:
        url (str): The URL of the file to be downloaded.
        save_dir (str): The path where the file should be saved.
        output (str): The name of the output file.
    """
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, output)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(path, "wb") as file:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        file.write(chunk)
            else:
                raise Exception(f"Failed to download file: {url}")


async def upload_from_path(path: str) -> str:
    """
    Uploads a file to the catbox.moe service.

    Args:
        path (str): The path to the file to be uploaded.

    Returns:
        str: The response from the catbox.moe service.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} does not exist.")

    ENDPOINT = "https://catbox.moe/user/api.php"
    user_hash = "4b6585b7d61940d8b98d8e0a4"
    payload = aiohttp.FormData()
    payload.add_field("reqtype", "fileupload")
    payload.add_field("userhash", user_hash)

    with open(path, "rb") as file:
        payload.add_field(
            "fileToUpload",
            file,
            filename=os.path.basename(path),
        )
        async with aiohttp.ClientSession() as session:
            async with session.post(ENDPOINT, data=payload) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    raise Exception(f"Failed to upload file: {path}")


async def upload_from_bytes(file_data: bytes, filename: str) -> str:
    """
    Uploads a file to the catbox.moe service from bytes.

    Args:
        file_data (bytes): The file data in bytes to be uploaded.
        filename (str): The name of the file to be uploaded.

    Returns:
        str: The response from the catbox.moe service.
    """
    ENDPOINT = "https://catbox.moe/user/api.php"
    user_hash = "4b6585b7d61940d8b98d8e0a4"

    payload = aiohttp.FormData()
    payload.add_field("reqtype", "fileupload")
    payload.add_field("userhash", user_hash)
    payload.add_field(
        "fileToUpload",
        file_data,
        filename=filename,
        content_type="application/octet-stream",
    )

    async with aiohttp.ClientSession() as session:
        async with session.post(ENDPOINT, data=payload) as response:
            if response.status == 200:
                return await response.text()
            else:
                raise Exception(f"Failed to upload file: {filename}")


async def download_dependencies() -> None:
    """
    Downloads the required dependencies for the application.
    """
    app_dir = appdirs.get_app_dir()
    bin_dir = os.path.join(app_dir, "bin")
    dependencies_dir = os.path.join(app_dir, "dependencies")

    os.makedirs(app_dir, exist_ok=True)
    os.makedirs(bin_dir, exist_ok=True)
    os.makedirs(dependencies_dir, exist_ok=True)

    version = "v0.2.1-beta"
    name = "N_m3u8DL-RE_Beta"
    build = "20240828"
    format = "tar.gz"
    platform = "osx-arm64"

    m3u8dl_bin_path = os.path.join(bin_dir, "N_m3u8DL-RE")
    # TODO: add support for arm architecture
    if sys.platform.startswith("darwin"):
        pass

    elif sys.platform.startswith("linux"):
        platform = "linux-x64"

    elif sys.platform.startswith("win"):
        platform = "win-x64"
        format = "zip"
        m3u8dl_bin_path = os.path.join(bin_dir, "N_m3u8DL-RE.exe")

    else:
        raise RuntimeError("Unsupported platform")

    m3u8dl_url = f"https://github.com/nilaoda/N_m3u8DL-RE/releases/download/{version}/{name}_{platform}_{build}.{format}"

    # Download m3u8dl binary
    if not os.path.exists(m3u8dl_bin_path):
        zip_name = f"{name}_{version}.{format}"
        await download_file(m3u8dl_url, dependencies_dir, zip_name)

        zip_path = os.path.join(dependencies_dir, zip_name)

        if format == "zip":
            with zipfile.ZipFile(zip_path, "r") as zip:
                zip.extractall(dependencies_dir)

        if format == "tar.gz":
            with tarfile.open(zip_path, "r") as tar:
                tar.extractall(dependencies_dir)

        os.remove(zip_path)

        # Move binary to bin directory
        for dir, subdirs, files in os.walk(dependencies_dir):
            for file in files:
                if file in ["N_m3u8DL-RE", "N_m3u8DL-RE.exe"]:
                    bin_src = os.path.join(dir, file)
                    shutil.move(bin_src, bin_dir)

        # Set executable permission
        if not os.access(m3u8dl_bin_path, os.X_OK):
            os.chmod(m3u8dl_bin_path, 0o744)

    # Add bin directory to PATH
    if "PATH" not in os.environ:
        os.environ["PATH"] = bin_dir
    elif bin_dir not in os.environ["PATH"]:
        os.environ["PATH"] = bin_dir + os.pathsep + os.environ["PATH"]
