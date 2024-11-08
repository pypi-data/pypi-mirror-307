
from typing import Any, Callable, Optional, Union
from contextlib import contextmanager
from dataclasses import dataclass
from traceback import print_exception

from .utils import CaptureOutput
from .colors import red, green, bold, yellow
from .strategies import Sequential, Parallel


@dataclass
class Ctx:
    """
    Test context.
    """
    test: "Test"

    @contextmanager
    def assert_raises(self, except_kind: type[BaseException] = BaseException):
        """
        Asserts that a section of code will raise an exception.
        ```py
        @test()
        def it_works(ctx):
            a = 1
            with ctx.assert_raises():
                assert a + 1 == 3
        ```
        """
        try:
            yield
        except except_kind as exc:
            return exc
        raise AssertionError(f"No exception raised in test {self.test.name}.")


@dataclass
class TestFailure:
    test: "Test"
    stdout: list[str]
    stderr: list[str]
    exception: Optional[BaseException]

    def print(self, index: Union[int, None] = None):
        print()
        fail_name = self.test.name if index is None else str(index + 1) + ' ' + self.test.name
        print(f"   {red('Fail')} {bold(fail_name)}")
        print_exception(self.exception)

        if len(self.stdout) > 0:
            print(f" {yellow('Stdout')} {bold(str(len(self.stdout)))} {yellow('lines')}")
            for line in self.stdout:
                print(line)

        if len(self.stderr) > 0:
            print(f" {yellow('Stderr')} {bold(str(len(self.stderr)))} {yellow('lines')}")
            for line in self.stderr:
                print(line)
        print()


class Test:
    """
    Represents one test to run.
    """
    name: str
    procedure: Callable[[Ctx], Any]

    def __init__(self, name: str, procedure: Callable[[Ctx], Any]) -> None:
        """
        Takes the name of the test and the test content procedure.
        """
        self.name = name
        self.procedure = procedure

    def run(self):
        """
        Runs this test infallibly.

        Returns a `TestFailure` if the test failed or `None` if it succeeded.
        """
        with CaptureOutput() as capture:
            try:
                self.procedure(Ctx(self))
            except BaseException as ex:
                return TestFailure(self, capture.stdout, capture.stderr, ex)


class Suite:
    """
    A suite of tests.
    
    Append test with the `Suite.test` decorator.
    ```py
    suite = Suite("Feur")

    @suite.test()
    def it_works(ctx):
        assert 1 + 1 == 2

    suite.run()
    ```
    """
    name: Union[str, None]
    tests: list[Test]

    def __init__(self, name: Optional[str] = None) -> None:
        """
        Creates an empty test suite.

        Naming is optionnal.
        """
        self.name = name
        self.tests = []

    def test(self):
        """
        Decorator used to append a function into the suite as a test.
        ```py
        suite = Suite("Feur")

        @suite.test()
        def it_works(ctx):
            assert 1 + 1 == 2

        suite.run()
        ```
        """
        def decorate(procedure: Callable[[Ctx], Any]) -> Callable[[Ctx], Any]:
            name = procedure.__name__
            self.tests.append(Test(name, procedure))
            return procedure
        return decorate

    def run(self, filters: list[str] = [], parallel = False):
        """
        Runs the test suite.

        Optionnally filter to run by their name : Only keep tests which names contains all filters.
        """
        to_run = [*self.filter_tests(filters)]
        strategy = Parallel() if parallel else Sequential()
        if self.name is not None: print(" ", green("Suite"), bold(self.name))
        print(yellow('Running'), bold(str(len(to_run))), yellow('/'), bold(str(len(self.tests))), yellow('tests'))
        print()
        failures = [fail for fail in strategy.run_all(to_run, Suite.run_one) if fail is not None]
        print()
        print("", yellow('Failed'), bold(str(len(failures))), yellow('/'), bold(str(len(to_run))), yellow('tests'))
        for (index, failure) in enumerate(failures): failure.print(index)
        return failures

    @staticmethod
    def run_one(test: Test):
        failure = test.run()
        if failure is None:
            print(f"     {green('Ok')} {bold(test.name)}")
        else:
            print(f"    {red('Err')} {bold(test.name)}")
        return failure


    def filter_tests(self, filters: list[str]):
        for test in self.tests:
            oki = True
            for filter in filters:
                if filter not in test.name:
                    oki = False
            if oki:
                yield test


def get_inline_suite() -> Suite:
    """
    Accessor of a singleton the `Suite` containing all inline tests.

    Intended for internal use only.
    """
    existing: Optional[Suite] = globals().get('_okipy_inline_suite')
    if existing is None:
        globals()['_okipy_inline_suite'] = existing = Suite()
    return existing


def test():
    """
    Decorator for declaring inline tests.
    ```py
    @test()
    def it_works(ctx):
        a = 1
        with ctx.assert_raises():
            assert a + 1 == 3
    ```
    """
    def decorate(procedure: Callable[[Ctx], Any]) -> Callable[[Ctx], Any]:
        return get_inline_suite().test()(procedure)
    return decorate
