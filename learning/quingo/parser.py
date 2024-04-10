from antlr4 import *
from pyquiet.antlr.QuietLexer import QuietLexer
from pyquiet.antlr.QuietParser import QuietParser
from pyquiet.QiVisitor.QuietVisitor import *

import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("asm_file", help="File path of QUIET-S assembly")

    return parser.parse_args()


def gen_cst(stmts: str):
    input = InputStream(stmts)
    lexer = QuietLexer(input)
    tokens = CommonTokenStream(lexer)
    parser = QuietParser(tokens)
    return parser.prog()


def check_gen_prog(stmts: str, path: Path = None) -> QiProgram:
    # make sure the cst exists.
    cst = gen_cst(stmts)
    assert cst is not None

    # make sure the visitor can generate the QiProgram.
    if path is not None:
        visitor = QuietVisitor(qi_path=path)
    else:
        visitor = QuietVisitor(qi_path=Path(__file__).parent)
    prog = visitor.visit(cst)
    assert prog is not None
    return prog


def main():
    """"""
    args = parse_args()
    with open(args.asm_file, "r") as f:
        prog_str = f.read()
        prog = check_gen_prog(prog_str)
    # from my_parser import parse
    # parse(Path(args.asm_file))


if __name__ == "__main__":
    main()
