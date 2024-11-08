#!/usr/bin/env -S python

from argparse import ArgumentParser
from os.path import realpath, dirname
import subprocess


def main():
    (source, filters) = parse_args()
    path = realpath(source)
    directory = dirname(path)
    input = script_from_file(path, filters)
    subprocess.run(["python"], text=True, cwd=directory, input=input)


def parse_args():
    parser = ArgumentParser(
        prog='okipy',
        description='Okipy test runner.'
    )
    parser.add_argument('source')
    parser.add_argument('filters', nargs='*')
    parsed = parser.parse_args()
    dict = vars(parsed)
    source = dict['source']
    filters = dict['filters']
    assert type(source) is str
    assert type(filters) is list
    return (source, filters)


def script_from_file(path: str, filters: list[str]):
    content = read_text_file(path)
    filters_strs = [f'"{filter}"' for filter in filters]
    filters_str = f'[{",".join(filters_strs)}]'
    return f"""
{content}

from okipy import get_inline_suite
get_inline_suite().run({filters_str})
"""


def read_text_file(path: str):
    with open(path, "r") as file:
        return "\n".join(file.readlines())


if __name__ == '__main__': main()
