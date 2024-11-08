
from io import StringIO
import sys


class CaptureOutput():
    def __enter__(self):
        self.stdout = list[str]()
        self._stdout = sys.stdout
        sys.stdout = self._str_stdout = StringIO()
        self.stderr = list[str]()
        self._stderr = sys.stderr
        sys.stderr = self._str_stderr = StringIO()
        return self

    def __exit__(self, *_args):
        self.stdout.extend(self._str_stdout.getvalue().splitlines())
        self.stderr.extend(self._str_stderr.getvalue().splitlines())
        sys.stdout = self._stdout
        sys.stderr = self._stderr
