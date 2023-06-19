"""
The scripts implements different refactoring operations


"""
__version__ = '0.1.0'
__author__ = 'Morteza'

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

# import main
from gen.Java9_v2Lexer import Java9_v2Lexer
from gen.Java9_v2Parser import Java9_v2Parser
from gen.Java9_v2Listener import Java9_v2Listener
from gen.Java9_v2Visitor import Java9_v2Visitor


class EncapsulateFiledRefactoringListener(Java9_v2Listener):
    """
    To implement the encapsulate filed refactored
    Encapsulate field: Make a public field private and provide accessors
    """

    def __init__(self, common_token_stream: CommonTokenStream = None,
                 field_identifier: str = None):
        """
        :param common_token_stream:
        """
        self.token_stream = common_token_stream
        self.field_identifier = field_identifier
        self.__variable_list = []
        self.__class_name = ""
        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

    def enterNormalClassDeclaration(self, ctx: Java9_v2Parser.NormalClassDeclarationContext):
        self.__class_name = ctx.identifier().getText()

    def exitFieldDeclaration(self, ctx: Java9_v2Parser.FieldDeclarationContext):

        #print(self.__class_name + '.' + ctx.variableDeclaratorList().getText())
        self.__variable_list.append(self.__class_name + '.' + ctx.variableDeclaratorList().getText())


        if ctx.fieldModifier(0).getText() == 'public':
            self.token_stream_rewriter.replaceRange(
                from_idx=ctx.fieldModifier(0).start.tokenIndex,
                to_idx=ctx.fieldModifier(0).stop.tokenIndex,
                text='private')

            # generate accessor and mutator methods
            # Accessor body
            field_identifier = ctx.variableDeclaratorList().getText()
            new_code = '\n\t'
            new_code += 'public ' + ctx.unannType().getText() + ' get' + str.capitalize(field_identifier[0]) + field_identifier[1:]
            new_code += '() { \n\t\t return this.' + field_identifier + ';' + '\n\t}'

            # Mutator body
            new_code += '\n\t'
            new_code += 'public void set' + str.capitalize(field_identifier[0]) + field_identifier[1:]
            new_code += '(' + ctx.unannType().getText() + ' ' + field_identifier + ') { \n\t\t'
            new_code += 'this.' + field_identifier + ' = ' + field_identifier + ';' + '\n\t}\n'

            self.token_stream_rewriter.insertAfter(ctx.stop.tokenIndex, new_code)

            hidden = self.token_stream.getHiddenTokensToRight(ctx.stop.tokenIndex)
            self.token_stream_rewriter.replaceRange(from_idx=hidden[0].tokenIndex,
                                                    to_idx=hidden[-1].tokenIndex,
                                                    text='\t/*End of accessor and mutator methods!*/\n\n')

    def enterNormalClassDeclaration(self, ctx: Java9_v2Parser.NormalClassDeclarationContext):
        self.__class_name = ctx.identifier().getText()

    def exitAssignment(self, ctx:Java9_v2Parser.AssignmentContext):
        #print("////" + ctx.leftHandSide().getText())
        if len(ctx.leftHandSide().getText().split('.', 1)) > 1 and (ctx.leftHandSide().getText().split('.',1)[0] != 'this' or ctx.leftHandSide().getText().split('.',1)[0] != self.__class_name):
            #print("/////////" + ctx.leftHandSide().getText().split(".",1)[0])
            temp_class_name = ctx.leftHandSide().getText().split('.', 1)[0]
            temp_field_name = ctx.leftHandSide().getText().split('.', 1)[1]
            expr_code = self.token_stream_rewriter.getText(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                                           start=ctx.expression().start.tokenIndex,
                                                           stop=ctx.expression().stop.tokenIndex)
            # new_code = 'this.set' + str.capitalize(self.field_identifier) + '(' + ctx.expression().getText() + ')'
            new_code = temp_class_name + '.set' + str.capitalize(temp_field_name[0]) + temp_field_name[1:] + '(' + expr_code + ')'
            self.token_stream_rewriter.replaceRange(ctx.start.tokenIndex, ctx.stop.tokenIndex, new_code)

    def exitExpressionName2(self, ctx: Java9_v2Parser.PrimaryContext):
        #print("//////////////" + ctx.getText().split('.', 1)[0])
        if len(ctx.getText().split('.', 1)) > 1 and (ctx.getText().split('.', 1)[0] != 'this' or ctx.getText().split('.', 1)[0] != self.__class_name):
            temp_class_name = ctx.getText().split('.', 1)[0]
            temp_field_name = ctx.getText().split('.', 1)[1]
            new_code = temp_class_name + '.get' + str.capitalize(temp_field_name[0]) + temp_field_name[1:] + '()'
            self.token_stream_rewriter.replaceRange(ctx.start.tokenIndex, ctx.stop.tokenIndex, new_code)

    def exitFieldDeclaration(self, ctx: Java9_v2Parser.FieldDeclarationContext):

        #print(self.__class_name + '.' + ctx.variableDeclaratorList().getText())
        self.__variable_list.append(self.__class_name + '.' + ctx.variableDeclaratorList().getText())


        if ctx.fieldModifier(0).getText() == 'public':
            self.token_stream_rewriter.replaceRange(
                from_idx=ctx.fieldModifier(0).start.tokenIndex,
                to_idx=ctx.fieldModifier(0).stop.tokenIndex,
                text='private')

            # generate accessor and mutator methods
            # Accessor body
            field_identifier = ctx.variableDeclaratorList().getText()
            new_code = '\n\t'
            new_code += 'public ' + ctx.unannType().getText() + ' get' + str.capitalize(field_identifier[0]) + field_identifier[1:]
            new_code += '() { \n\t\t return this.' + field_identifier + ';' + '\n\t}'

            # Mutator body
            new_code += '\n\t'
            new_code += 'public void set' + str.capitalize(field_identifier[0]) + field_identifier[1:]
            new_code += '(' + ctx.unannType().getText() + ' ' + field_identifier + ') { \n\t\t'
            new_code += 'this.' + field_identifier + ' = ' + field_identifier + ';' + '\n\t}\n'

            self.token_stream_rewriter.insertAfter(ctx.stop.tokenIndex, new_code)

            hidden = self.token_stream.getHiddenTokensToRight(ctx.stop.tokenIndex)
            self.token_stream_rewriter.replaceRange(from_idx=hidden[0].tokenIndex,
                                                    to_idx=hidden[-1].tokenIndex,
                                                    text='\t/*End of accessor and mutator methods!*/\n\n')

    def get__variable_list(self):
        return self.__variable_list
