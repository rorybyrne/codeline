"""Writer

Author: Rory Byrne <rory@rory.bio>
"""
from codeline.sdk.context.file import File


class Writer:

    def __init__(self, file_path: str):
        self._file_path = file_path

    def write(self, file: File):
        """Writes the buffer to a file"""
        with open(self._file_path, 'w') as f:
            for line in file:
                f.write(str(line))
                f.write('\n')
