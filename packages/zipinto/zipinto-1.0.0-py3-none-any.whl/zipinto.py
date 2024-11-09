from pathlib import Path
import zipfile
import sys
import os


class ZipIntoException(Exception):
    def __init__(self, msg):
        super().__init__(
            "There have been some issues in the decompress, as shown below\n" + msg)


def decompress(zip_path: str, new_path: str, encoding: str = "utf-8") -> None:
    try:
        if not os.path.exists(new_path):
            os.makedirs(new_path)

        else:
            new_path += "\\" + os.path.splitext(os.path.basename(zip_path))[0]
            if os.path.exists(new_path):
                return

            os.makedirs(new_path)

        with zipfile.ZipFile(zip_path, "r") as z:
            for file in z.infolist():
                if file.is_dir():
                    os.makedirs(new_path + "\\" + file.filename)

                else:
                    with z.open(file.filename, "r") as zr:
                        with Path(new_path + "\\" + file.filename).open("w", encoding=encoding) as wr:
                            wr.write(zr.read().decode(encoding))

    except Exception as e:
        raise ZipIntoException(str(e))
