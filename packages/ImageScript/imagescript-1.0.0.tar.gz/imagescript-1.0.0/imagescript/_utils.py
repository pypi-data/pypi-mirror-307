import math
from hashlib import sha3_256
from pathlib import Path

import numpy as np
from Crypto.Cipher import AES


def _bytes_to_vector3(raw: bytes) -> list[tuple[int, int, int]]:
    """Converts raw bytes to an array of 3D vectors."""
    blockcount = math.ceil(len(raw) / 3)
    raw = raw.ljust(blockcount*3, b"\x00")
    return [(raw[3*i], raw[3*i + 1], raw[3*i + 2]) for i in range(blockcount)]


def bytes_to_image_data(raw: bytes, ratio_x: int, ratio_y: int) -> np.ndarray:
    """Converts raw bytes to an 2D array of 3D vectors for usage as pixels in an image.

    Args:
        raw (bytes): The raw bytes to convert.
        ratio_x (int): The ratio of the width of the image.
        ratio_y (int): The ratio of the height of the image.

    Returns:
        np.ndarray: The converted 2D array of 3D vectors.
    """
    # Transform data into 3D vectors
    data = _bytes_to_vector3(raw)
    # Calculate the aspect ratios
    rx = ratio_y / ratio_x
    ry = ratio_x / ratio_y

    # Calculate the dimensions of the image
    width = math.ceil(math.sqrt(len(data) / rx))
    width = width + (ratio_x - width % ratio_x) % ratio_x
    height = math.ceil(math.sqrt(len(data) / ry))
    height = height + (ratio_y - height % ratio_y) % ratio_y

    # Pad data with NULLS to fit the width and height
    data = data + [(0, 0, 0)] * (width * height - len(data))

    # Reshape data to a 2D Pixel Array
    return np.array(data).reshape((width, height, 3)).astype(np.uint8)


def image_data_to_bytes(data: list[tuple[int, int, int]]) -> bytes:
    """Converts a 1D array of 3D vectors to raw bytes."""
    return np.array(data, dtype=np.uint8).flatten().tobytes()


def pack_steganography(
        data: bytes,
        cover: list[tuple[int, int, int]]
    ) -> list[tuple[int, int, int]]:
    """Takes input data and hides it in the cover image data

    Args:
        data (bytes): The data to hide
        cover (list[tuple[int, int, int]]): The pixel data of the cover image

    Returns:
        list[tuple[int, int, int]]: The new cover image with data hidden within
    """
    cover[0] = (math.floor(len(data) / (256**2)), math.floor(len(data) / 256), len(data)%256)
    dpos = 0
    for i in range(1, len(cover), 6):
        davg = math.floor(16 * data[dpos] / 256)
        for j in range(6):
            cover[i+j] = (
                cover[i+j][0] - cover[i+j][0] % 16 + davg,
                cover[i+j][1] - cover[i+j][1] % 16 + (davg if j != 5 else math.ceil((data[dpos] - davg * 16)/2)),
                cover[i+j][2] - cover[i+j][2] % 16 + (davg if j != 5 else math.floor((data[dpos] - davg * 16)/2)),
            )
        dpos += 1
        if dpos >= len(data):
            break
    if dpos < len(data):
        raise EOFError("Ran out of space for the data. You have to use a larger image.")

    return cover


def unpack_steganography(
        data: list[tuple[int, int, int]],
    ) -> bytes:
    """Takes image data and extracts hidden data

    Args:
        data (list[tuple[int, int, int]]): The image data to analyze

    Returns:
        bytes: The extracted data
    """
    result = bytes()
    datasize = data[0][0] * (256**2) + data[0][1] * 256 + data[0][2]
    dpos = 0
    for i in range(1, len(data), 6):
        val = 0
        for j in range(6):
            val += data[i+j][0] % 16
            val += data[i+j][1] % 16
            val += data[i+j][2] % 16
        result += val.to_bytes()
        dpos += 1  # noqa: SIM113
        if dpos >= datasize:
            break

    return result


def encrypt(data: bytes, password: str) -> bytes:
    """Encrypts the given data with the given password using AES."""
    cypher = AES.new(sha3_256(password.encode()).digest(), AES.MODE_GCM)
    return cypher.encrypt(data) + b"\n\n\n" + cypher.nonce


def decrypt(data: bytes, password: str) -> bytes:
    """Decrypts the given data with the given password using AES."""
    data, nonce = data.rsplit(b"\n\n\n", 1)
    cypher = AES.new(sha3_256(password.encode()).digest(), AES.MODE_GCM, nonce=nonce)
    return cypher.decrypt(data)


def prevent_overwrite(file: Path) -> Path:
    """Prevents an exiting file from being overwritten by adding a arbitrary ".out" suffix if the target path exists.

    Args:
        file (Path): The target output path

    Returns:
        Path: The new output path in case of an overwrite.
    """
    if file.exists():
        return file.with_suffix(".out" + file.suffix)
    return file
