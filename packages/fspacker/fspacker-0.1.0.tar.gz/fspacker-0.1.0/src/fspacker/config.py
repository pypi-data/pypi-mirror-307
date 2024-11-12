import hashlib
import json
import logging
import pathlib
import platform
import subprocess
import sys
import time
import typing

import requests

logging.basicConfig(level=logging.INFO, format="[*] %(message)s")

# python embed config
PYTHON_VER = platform.python_version()
PLAT_ARCH = platform.machine().lower()

# python 镜像
EMBED_URL_PREFIX: typing.Dict[str, str] = dict(
    official="https://www.python.org/ftp/python/",
    huawei="https://mirrors.huaweicloud.com/python/",
)

# archive file name
EMBED_ARCHIVE_NAME = f"python-{PYTHON_VER}-embed-{PLAT_ARCH}.zip"
PATH_CWD = pathlib.Path(__file__).parent
PATH_CONFIG = PATH_CWD / "config.json"
PATH_EMBED_REPO = PATH_CWD / "embed-repo"
PATH_WHEEL_REPO = PATH_CWD / "wheel-repo"


def calc_checksum(
        filepath: pathlib.Path, algorithm="md5", block_size=4096
) -> str:
    """计算文件校验和.

    Args:
        filepath (pathlib.Path): 输入文件路径.
        algorithm (str, optional): 校验算法, 默认为 "md5".
        block_size (int, optional): 读取块长度, 默认为 4096.
    """
    if algorithm == "md5":
        hasher = hashlib.md5()
    elif algorithm == "sha1":
        hasher = hashlib.sha1()
    elif algorithm == "sha256":
        hasher = hashlib.sha256()
    else:
        raise ValueError(f"不支持的校验和算法: [{algorithm}]")

    logging.info(f"计算文件[{filepath}]校验和")
    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(block_size), b""):
            hasher.update(chunk)
    logging.info(f"计算值[{hasher.hexdigest()}]")
    return hasher.hexdigest()


def get_json_value(filepath: pathlib.Path, key: str) -> typing.Any:
    with open(filepath, "r") as f:
        data = json.load(f)
        return data.setdefault(key, None)


def update_json_values(
        filepath: pathlib.Path, updates: typing.Dict[str, typing.Any]
):
    """Update [key, value] in json file

    Args:
        filepath (pathlib.Path): Input file
        updates (typing.Dict[str, typing.Any]): update values
    """
    if filepath.exists():
        with open(filepath, "r") as fr:
            data = json.load(fr)
    else:
        data = {}

    for key, value in updates.items():
        data[key] = value

    with open(filepath, "w") as fw:
        json.dump(data, fw, indent=4, ensure_ascii=False)


def check_url_access_time(url: str) -> float:
    """检查 url 访问是否超时"""
    start = time.perf_counter()
    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()
        time_used = time.perf_counter() - start
        logging.info(f"{url} 访问用时: {time_used:.2f}s")
        return time_used
    except requests.exceptions.RequestException:
        logging.info(f"{url} 访问超时")
        return -1


def check_embed_urls() -> str:
    """检查可用镜像"""
    min_time, fastest_url = 10.0, ""
    for name, embed_url in EMBED_URL_PREFIX.items():
        time_used = check_url_access_time(embed_url)
        if time_used > 0:
            if time_used < min_time:
                fastest_url = embed_url
                min_time = time_used

    logging.info(f"找到最快镜像地址: {fastest_url}")
    return fastest_url


def fetch_lib_wheel(libname: str):
    # wheel_files = list(_.name for _ in PATH_WHEEL_REPO.iterdir() if _.is_file())
    if not PATH_WHEEL_REPO.exists():
        logging.info(f"创建 wheel-repo 文件夹[{PATH_WHEEL_REPO}]")
        PATH_WHEEL_REPO.mkdir(parents=True)

    with subprocess.Popen(
            [
                sys.executable,
                "-m",
                "pip",
                "download",
                libname,
                "-d",
                str(PATH_WHEEL_REPO),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
    ) as process:
        if process.stdout:
            for line in process.stdout:
                logging.info(line.decode("utf8"))
