#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Handles command line interface
"""
import argparse
from .gendoc import _make_standard_package, _write_doc
from .validate import paralex_validation
from .meta import gen_metadata
import logging

logging.basicConfig(level=logging.INFO)

def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands',
                                       description = 'valid subcommands')
    make_std = subparsers.add_parser("make_standard")
    make_std.set_defaults(func=_make_standard_package)
    make_doc = subparsers.add_parser("make_doc")
    make_doc.set_defaults(func=_write_doc)
    validate = subparsers.add_parser("validate")
    validate.add_argument("package", help="JSON description of the package to validate")
    validate.add_argument('--basepath', type=str,
                          help='Basepath for the package to validate.')
    validate.set_defaults(func=paralex_validation)
    meta = subparsers.add_parser("meta")
    meta.add_argument("config", help="YAML description of the package to describe.")
    meta.add_argument('--basepath', type=str,
                      help='Basepath for the generated .package.json file.')
    meta.set_defaults(func=gen_metadata)
    return parser.parse_args()


def main():
    args = parse_args()
    args.func(args)
