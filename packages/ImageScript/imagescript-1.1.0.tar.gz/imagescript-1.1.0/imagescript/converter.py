import sys
from pathlib import Path

from PIL import Image

from imagescript._utils import (
    bytes_to_image_data,
    decrypt,
    encrypt,
    image_data_to_bytes,
    pack_steganography,
    prevent_overwrite,
    unpack_steganography,
)


class Converter:
    @classmethod
    def file_to_image(
        cls,
        file: Path,
        size: tuple[int, int],
        output: Path,
        overwrite: bool,
        password: str | None = None
    ) -> None:
        """Takes an arbitrary file, reads the contained data and transforms it into an image.

        Args:
            file (Path): The target file to read and work with.
            size (tuple[int, int]): The aspect ratios of the final image.
            output (Path): The output path for the finished image.
            password (str | None, optional): A password needed for encryption if any. Defaults to None.
        """
        bsuffix = f"{file.suffix}\n".encode()
        with open(file, "rb") as f:
            raw = f.read()
        if password:
            raw = encrypt(raw, password)
        raw = bsuffix + raw
        data = bytes_to_image_data(raw, size[0], size[1])

        save_location = output.with_suffix(".webp")
        if not overwrite:
            save_location = prevent_overwrite(save_location)
        Image.fromarray(data, mode="RGB").save(save_location, format="webp", lossless=True)

    @classmethod
    def image_to_file(
        cls,
        file: Path,
        output: Path,
        overwrite: bool,
        password: str | None = None
    ):
        """Reads an image file created by this tools and extracts the contained data.
        Saves the data into a file of the original file-type.

        Args:
            file (Path): The image file to read in.
            output (Path): The output path and optionally filename.
            password (str | None, optional): A password needed for decryption if any. Defaults to None.
        """
        filesuffix, data = cls._read_image(file, password)
        output = output.with_suffix(filesuffix)
        if not overwrite:
            output = prevent_overwrite(output)
        with open(output, "wb") as f:
            f.write(data)

    @classmethod
    def execute_image(
        cls,
        file: Path,
        args: list[str],
        password: str | None = None
    ):
        """Directly executes a python script transformed into an image by this tool.

        Args:
            file (Path): The image file to execute
            password (str | None, optional): A password needed for encryption if any. Defaults to None.

        Raises:
            TypeError: In case the original content was not a python script.
        """
        filesuffix, data = cls._read_image(file, password)
        if filesuffix[:3] != ".py":
            raise TypeError("Image does not contain a python file")
        sys.argv = ["null", *args]
        exec(data.decode(), globals() | {"__name__": "__main__"})

    @classmethod
    def pack(
        cls,
        file: Path,
        image: Path,
        output: Path,
        overwrite: bool,
        password: str | None = None
    ):
        """Hides data from a file in a cover image

        Args:
            file (Path): The file to get the data from
            image (Path): The image to hide the data in
            output (Path): The output file path
            overwrite (bool): Whether to overwrite the output file if it exists
            password (str | None, optional): A password needed for encryption if any. Defaults to None.
        """
        img = Image.open(image)
        imgdata: list[tuple[int, int, int]] = list(img.getdata())
        with open(file, "rb") as f:
            raw = f.read()
        if password:
            raw = encrypt(raw, password)
        raw = f"{file.suffix}\n".encode() + raw
        imgdata = pack_steganography(raw, imgdata)
        img.putdata(imgdata)

        save_location = output.with_suffix(".webp")
        if not overwrite:
            save_location = prevent_overwrite(save_location)
        img.save(save_location, format="WEBP", lossless=True)


    @classmethod
    def unpack(
        cls,
        file: Path,
        output: Path,
        overwrite: bool,
        password: str | None = None
    ):
        """Extracts data from a image that contains data hidden by this tool

        Args:
            file (Path): The image to extract the data from
            output (Path): The output file path
            overwrite (bool): Whether to overwrite the output file if it exists
            password (str | None, optional): A password needed for encryption if any. Defaults to None.
        """
        img = Image.open(file)
        imgdata: list[tuple[int, int, int]] = list(img.getdata())
        data = unpack_steganography(imgdata)
        filesuffix, data = data.split(b"\n", 1)
        if password:
            data = decrypt(data, password)

        output = output.with_suffix(filesuffix.decode())
        if not overwrite:
            output = prevent_overwrite(output)
        output.write_bytes(data)


    @staticmethod
    def _read_image(file: Path, password: str | None) -> tuple[str, bytes]:
        """Reads and parses an image and returns the original file suffix and data contained in image

        Args:
            file (Path): Image to read and parse
            password (str | None): The password to use for decryption if any

        Returns:
            tuple[str, bytes]: original file suffix, image data
        """
        img = Image.open(file)
        data = image_data_to_bytes(img.getdata())
        filesuffix, data = data.split(b"\n", 1)
        data = data.rstrip(b"\x00")
        if password:
            data = decrypt(data, password)
        return filesuffix.decode(), data
