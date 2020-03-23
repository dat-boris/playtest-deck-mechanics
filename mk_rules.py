#!/usr/bin/env python
"""A script responsible for generating the rules from docstrings

./mk_rules.py [optional file]
"""
import os
import argparse
from inspect import cleandoc
from importlib import import_module


def get_docs(module_name: str) -> str:

    rule_modules = import_module(module_name + ".rules")

    rule_docs = getattr(rule_modules, "RULE_TESTS", None)
    assert rule_docs, "Should see rules.py contains RULE_TESTS"

    doc = [
        cleandoc(d.__doc__ if not isinstance(d, str) else d)
        for d in rule_docs
        if d.__doc__ is not None
    ]
    return "\n\n".join(doc) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate rule file.")
    parser.add_argument("game", help="Game ID (folder name) to generate rules")
    args = parser.parse_args()
    doc_to_write = os.path.join(args.game, "RULES.md")

    with open(doc_to_write, "w") as f:
        f.write(get_docs(args.game))

    print(f"Written to {doc_to_write}")
