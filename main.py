"""
Main script for grammer Java9_v2 (version 2)

@author: Morteza Zakeri, (http://webpages.iust.ac.ir/morteza_zakeri/)
@date: 20201107

- Compiler generator:   ANTRL4.x
- Target language(s):   Python3.x,


-Changelog:
-- v4.2
--- Add name for grammar rules extensions
--- Remove Java attributes from grammar file.

- Course website:   http://parsa.iust.ac.ir/courses/compilers/
- Laboratory website:   http://reverse.iust.ac.ir/

"""

__version__ = '0.1.0'
__author__ = 'Morteza'

import os

from antlr4 import *

from gen.Java9_v2Lexer import Java9_v2Lexer
from gen.Java9_v2Parser import Java9_v2Parser
from variable_refactorer import EncapsulateFiledRefactoringListener

import argparse

variable_list = []

def main(args):

    global variable_list
    # Step 1: get all the files in the directory
    code_list = os.listdir(args.file)
    # Step 2: Load input source into stream one by one
    for item in code_list:
        stream = FileStream(args.file + '\\' + item, encoding='utf8')

        print('Input stream:')
        print(stream)

        # Step 3: Create an instance of AssignmentStLexer
        lexer = Java9_v2Lexer(stream)
        # Step 4: Convert the input source into a list of tokens
        token_stream = CommonTokenStream(lexer)
        # Step 5: Create an instance of the AssignmentStParser
        parser = Java9_v2Parser(token_stream)
        parser.getTokenStream()
        # Step 6: Create parse tree
        parse_tree = parser.compilationUnit()
        # Step 6: Create an instance of AssignmentStListener
        my_listener = EncapsulateFiledRefactoringListener(common_token_stream=token_stream)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        variable_list += my_listener.get__variable_list()

        print(variable_list)

        print('Compiler result:')
        print(my_listener.token_stream_rewriter.getDefaultText())

        with open('refactored code' + '\\' + item + '.refactored', mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-n', '--file',
        help='Input source', default='code')
    args = argparser.parse_args()
    main(args)
