from qir.QiProg import *
from typing import List
from antlr4 import *
from antlr.QuietLexer import QuietLexer
from antlr.QuietParser import QuietParser
from QiVisitor.QuietVisitor import QuietVisitor
from pathlib import Path


def parse(filename: Path):
    input = ""
    with filename.open("r") as f:
        input = f.read()
    input2 = InputStream(input)
    lexer = QuietLexer(input2)
    tokens = CommonTokenStream(lexer)
    # get the CST.
    parser = QuietParser(tokens)
    quiet_cst = parser.prog()
    # convert the CST into QiProg
    visitor = QuietVisitor(qi_path=filename.parent)
    prog: QiProgram = visitor.visit(quiet_cst)
    qifile: QiFileSection = prog.file_section
    for i in qifile.file_name_list():
        file: QiFile = qifile.get_file(i)
        program_inc: QiProgram = parse(file.handle)
        for gate in program_inc.gate_section.infos:
            prog.add_define_gate(gate)
        for func in program_inc.body_section.functions:
            if not prog.body_section.has_func(func.func_name):
                prog.add_define_function(func)
    for func in prog.body_section.functions:
        for instr in func.body:
            if isinstance(instr, FunctionCall):
                instr.bind_function(prog.body_section.get_func(instr.opname))
    return prog
