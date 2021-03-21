import tempfile
from pathlib import Path

from codeline.service.file import FileService

SOURCE_CODE = b"""def my_function(input: str):
    # ~$ echo "hello"
    do_something(input)
    with open(str) as f:
        f.write(input)
"""


def test_read_lines_success():
    """Reading lines into a File instance"""
    service = FileService()
    with tempfile.NamedTemporaryFile() as fp:
        fp.write(SOURCE_CODE)
        fp.seek(0)

        file_path = Path(fp.name)
        file = service.read(file_path)
        assert len(file) == 5
