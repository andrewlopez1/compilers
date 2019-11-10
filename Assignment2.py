import os
from Assignment1 import lexer

class SyntaxAnalyzer:
    def __init__(self):
        self.productions = []
        self.token, self.lexeme = None, None
        self.corpus = None
        self.corpus_counter = 0
        self.f = None

    def Rat19F(self):
        self.f.write("<Rat19F> ::= <Opt Function Definitions> %% <Opt Opt Declaration List> <Statement List> %% \n")
        self.productions.append("<Rat19F> ::= <Opt Function Definitions> %% <Opt Opt Declaration List> <Statement List> %%")
        self.OptFunctionDefs()
        if self.lexeme == "%%":
            self.lexer_next()
            self.OptDeclarationList()
            self.StatementList()
        else:
            print("ERROR: %%")
        if self.lexeme == "%%":
            self.lexer_next()
        else:
            print("ERROR: %%")
        if self.token is not "EOF":
            print("Expected EOF after %%")

    def OptFunctionDefs(self):
        self.f.write("<Opt Function Definitions> ::= <Function Definitions> | <Empty>\n")
        self.productions.append("<Opt Function Definitions> ::= <Function Definitions> | <Empty>")
        if self.FunctionDefs():
            return
        else:
            self.Empty()

    def FunctionDefs(self):
        self.f.write("<Function Definitions> ::= <Function> | <Function> <Function Definitions>\n")
        self.productions.append("<Function Definitions> ::= <Function> | <Function> <Function Definitions>")
        if self.Function():
            if not self.FunctionDefs():
                self.Empty()
                return True
            else: #another functionDef
                return True
        else:
            return False

    def Function(self):
        self.f.write("<Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>\n")
        self.productions.append("<Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
        if self.lexeme == "function":
            self.lexer_next()
            if self.token == "Identifier":
                self.lexer_next()
                if self.lexeme == "(":
                    self.lexer_next()
                    self.OptParameterList()
                    if self.lexeme == ")":
                        self.lexer_next()
                        self.OptDeclarationList()
                        self.Body()
                        return True
                    else:
                        print("ERROR ')' expected")
                else:
                    print("ERROR '(' expected")
            else:
                print("ERROR Identifier expected")
        else:
            return False

    def OptParameterList(self):
        self.f.write("<Opt Parameter List> ::= <Parameter List> | <Empty>\n")
        self.productions.append("<Opt Parameter List> ::= <Parameter List> | <Empty>")
        if self.ParameterList():
            return
        else:
            self.Empty()

    def ParameterList(self):
        self.f.write("<Parameter List> ::= <Parameter> | <Parameter> , <Parameter List>\n")
        self.productions.append("<Parameter List> ::= <Parameter> | <Parameter> , <Parameter List>")
        if self.Parameter():
            if self.lexeme == ",":
                self.lexer_next()
                if not self.ParameterList():
                    print ("ERROR Parameter expected")
                    return False
                else:
                    return True
            else:
                self.Empty()
                return True
        else:
            return False

    def Parameter(self):
        self.f.write("<Parameter> ::= <IDs> <Qualifier>\n")
        self.productions.append("<Parameter> ::= <IDs> <Qualifier>")
        if self.IDs():
            if self.Qualifier():
                return True
        return False

    def Qualifier(self):
        self.f.write("<Qualifier> ::= int | boolean | real\n")
        self.productions.append("<Qualifier> ::= int | boolean | real")
        if self.lexeme in ('int', 'boolean', 'real'):
            self.lexer_next()
            return True
        else:
            #print ("ERROR Invalid qualifier " + self.lexeme) #not always an error, look into fixing this
            return False

    def Body(self):
        self.f.write("<Body> := { <Statement List> }\n")
        self.productions.append("<Body> := { <Statement List> }")
        if self.lexeme == "{":
            self.lexer_next()
            self.StatementList()
            if self.lexeme == "}":
                self.lexer_next()
                return
            else:
                print("ERROR '}' expected")
        else:
            print("ERROR '{'' expected")

    def OptDeclarationList(self):
        self.f.write("<Opt Declaration List> ::= <Declaration List> | <Empty>\n")
        self.productions.append("<Opt Declaration List> ::= <Declaration List> | <Empty>")
        if self.DeclarationList():
            return
        else:
            self.Empty()

    def DeclarationList(self):
        self.f.write("<Declaration List> ::= <Declaration> ; | <Declaration> ; <Declaration List>\n")
        self.productions.append("<Declaration List> ::= <Declaration> ; | <Declaration> ; <Declaration List>")
        if self.Declaration():
            if self.lexeme == ';':
                self.lexer_next()
                if not self.DeclarationList():
                    self.Empty()
                    return True
                else:
                    return True
            else:
                print("ERROR ';' expected")
                return False
        else:
            return False

    def Declaration(self):
        self.f.write("<Declaration> ::= <Qualifier> <IDs>\n")
        self.productions.append("<Declaration> ::= <Qualifier> <IDs>")
        if self.Qualifier():
            if self.IDs():
                return True
        return False

    def IDs(self):
        self.f.write("<IDs> ::= <Identifier> | <Identifier> , <IDs>\n")
        self.productions.append("<IDs> ::= <Identifier> | <Identifier> , <IDs>")
        if self.token == "Identifier":
            self.lexer_next()
            if self.lexeme == ',':
                self.lexer_next()
                if not self.IDs():
                    print("ERROR expected Identifier")
                    return False
                else:
                    return True
            else:
                self.Empty()
                return True
        else:
            return False

    def StatementList(self):
        self.f.write("<Statement List> ::= <Statement> | <Statement> <StatementList>\n")
        self.productions.append("<Statement List> ::= <Statement> | <Statement> <StatementList>")
        if self.Statement():
            if not self.StatementList():
                self.Empty()
                return True
            else:
                return True
        else:
            return False

    def Statement(self):
        self.f.write("<Statement> ::= <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>\n")
        self.productions.append("<Statement> ::= <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>")
        if self.Compound() or self.Assign() or self.If() or self.Return() or self.Print() or self.Scan() or self.While():
            return True
        else:
            return False

    def Compound(self):
        self.f.write("<Compound> := { <Statement List> }\n")
        self.productions.append("<Compound> := { <Statement List> }")
        if self.lexeme == '{':
            self.lexer_next()
            if self.StatementList():
                if self.lexeme == '}':
                    self.lexer_next()
                    return True
                else:
                    print("ERROR '}' expected")
                    return False
            else:
                print("ERROR Statement List expected")
                return False
        else:
            return False

    def Assign(self):
        self.f.write("<Assign> := <Identifier> = <Expression> ;\n")
        self.productions.append("<Assign> := <Identifier> = <Expression> ;")
        if self.token == "Identifier":
            self.lexer_next()
            if self.lexeme == "=":
                self.lexer_next()
                if self.Expression():
                    if self.lexeme == ";":
                        self.lexer_next()
                        return True
                    else:
                        print("ERROR ; expected")
                        return False
                else:
                    print("ERROR Expression expected after =")
                    return False
            else:
                print("ERROR = expected after identifier")
        else:
            return False

    def If(self):
        self.f.write("<If> ::= if ( <Condition> ) <Statement> fi | if ( <Condition> ) <Statement> otherwise <Statement> fi\n")
        self.productions.append("<If> ::= if ( <Condition> ) <Statement> fi | if ( <Condition> ) <Statement> otherwise <Statement> fi")
        if self.lexeme == "if":
            self.lexer_next()
            if self.lexeme == "(":
                self.lexer_next()
                if self.Condition():
                    if self.lexeme == ")":
                        self.lexer_next()
                        if self.Statement():
                            if self.lexeme == "otherwise":
                                self.lexer_next()
                                if self.Statement():
                                    if self.lexeme == "fi":
                                        self.lexer_next()
                                        return True
                                    else:
                                        print("ERROR expected fi at end of if")
                                        return False
                                else:
                                    print("ERROR expected statement")
                                    return False
                            else:
                                if self.lexeme == "fi":
                                    self.lexer_next()
                                    return True
                                else:
                                    print("ERROR expected fi at end of if")
                                    return False
                        else:
                            print("ERROR expected statement")
                            return False
                    else:
                        print('ERROR ) expected')
                        return False
                else:
                    print("ERROR expected condition")
                    return False
            else:
                print("ERROR Expected ) after if")
                return False
        else:
            return False

    def Return(self):
        self.f.write("<Return> ::= return ; | return <Expression> ;\n")
        self.productions.append("<Return> ::= return ; | return <Expression> ;")
        if self.lexeme == "return":
            self.lexer_next()
            self.Expression() #not an if statement because we dont *need* the expression to be a valid return
            if self.lexeme == ";":
                self.lexer_next()
                return True
            else:
                print("ERROR ; expected after return")
        else:
            return False

    def Print(self):
        self.f.write("<Print> ::= put ( <Expression> ) ; \n")
        self.productions.append("<Print> ::= put ( <Expression> ) ; ")
        if self.lexeme == "put":
            self.lexer_next()
            if self.lexeme == '(':
                self.lexer_next()
                self.Expression()
                if self.lexeme == ")":
                    self.lexer_next()
                    if self.lexeme == ";":
                        self.lexer_next()
                        return True
                    else:
                        print("ERROR ; expected")
                        return False
                else:
                    print("ERROR expected )")
                    return False
            else:
                print("ERROR expected (")
                return False
        else:
            return False

    def Scan(self):
        self.f.write("<Scan> ::= get ( <IDs> ) ; \n")
        self.productions.append("<Scan> ::= get ( <IDs> ) ; ")
        if self.lexeme == "get":
            self.lexer_next()
            if self.lexeme == "(":
                self.lexer_next()
                if self.IDs():
                    if self.lexeme == ')':
                        self.lexer_next()
                        if self.lexeme == ';':
                            self.lexer_next()
                            return True
                        else:
                            print("ERROR expected ;")
                            return False
                    else:
                        print ("ERROR expected ) ")
                        return False
                else:
                    print("ERROR expected identifier(s)")
                    return False
            else:
                print("ERROR expected (")
                return False
        else:
            return False

    def While(self):
        self.f.write("<While> ::= while ( <Condition> ) <Statement>\n")
        self.productions.append("<While> ::= while ( <Condition> ) <Statement>")
        if self.lexeme == "while":
            self.lexer_next()
            if self.lexeme == "(":
                self.lexer_next()
                if self.Condition():
                    if self.lexeme == ")":
                        self.lexer_next()
                        if self.Statement():
                            return True
                        else:
                            print("ERROR expected statement")
                            return False
                    else:
                        print("ERRO expected )")
                        return False
                else:
                    print("ERROR expected condition")
                    return False
            else:
                print("ERROR expected (")
                return False
        else:
            return False

    def Condition(self):
        self.f.write("<Condition> ::= <Expression> <Relop> <Expression>\n")
        self.productions.append("<Condition> ::= <Expression> <Relop> <Expression>")
        if self.Expression():
            if self.Relop():
                if self.Expression():
                    return True
                else:
                    print("ERROR expected Expression")
                    return False
            else:
                print("ERROR expected relational operator")
                return False
        else:
            return False

    def Relop(self):
        self.f.write("<Relop> ::= == | /= | > | < | => | <=\n")
        self.productions.append("<Relop> ::= == | /= | > | < | => | <=")
        if self.lexeme in ['==','/=','>','<','=>','<=']:
            self.lexer_next()
            return True
        else:
            return False

    def Expression(self):
        self.f.write("<Expression> ::= <Term> <ExpressionPrime>\n")
        self.productions.append("<Expression> ::= <Term> <ExpressionPrime>")
        if self.Term():
            self.ExpressionPrime()
            return True
        else:
            print("ERROR expected term")
            return False

    def ExpressionPrime(self):
        self.f.write("<ExpressionPrime> ::= + <Term> <ExpressionPrime> | - <Term> <ExpressionPrime> | <Empty>\n")
        self.productions.append("<ExpressionPrime> ::= + <Term> <ExpressionPrime> | - <Term> <ExpressionPrime> | <Empty>")
        if self.lexeme in ['+','-']:
            self.lexer_next()
            if self.Term():
                self.ExpressionPrime()
            else:
                print("ERROR expected term")
        else:
            self.Empty()

    def Term(self):
        self.f.write("<Term> ::= <Factor> <TermPrime>\n")
        self.productions.append("<Term> ::= <Factor> <TermPrime>")
        if self.Factor():
            self.TermPrime()
            return True
        else:
            return False

    def TermPrime(self):
        self.f.write("<TermPrime> ::= * <Factor> <TermPrime> | / <Factor> <TermPrime> | <Empty>\n")
        self.productions.append("<TermPrime> ::= * <Factor> <TermPrime> | / <Factor> <TermPrime> | <Empty>")
        if self.lexeme in ['*','/']:
            self.lexer_next()
            if self.Factor():
                self.TermPrime()
            else:
                print("ERROR expected Factor")
        else:
            self.Empty()

    def Factor(self):
        self.f.write("<Factor> ::= - <Primary> | <Primary>\n")
        self.productions.append("<Factor> ::= - <Primary> | <Primary>")
        if self.lexeme == "-":
            self.lexer_next()
        elif self.Primary():
            return True

        print("ERROR expected primary")
        return False

    def Primary(self):
        self.f.write("<Primary> ::= <Identifier> | <Integer> | <Identifier> (<IDs>) | ( <Expression> ) | <Real> | true | false\n")
        self.productions.append("<Primary> ::= <Identifier> | <Integer> | <Identifier> (<IDs>) | ( <Expression> ) | <Real> | true | false")
        if self.token in ["Integer", "Real", "Digit"]:
            self.lexer_next()
            return True
        elif self.lexeme in ['true','false']:
            self.lexer_next()
            return True
        elif self.token == "Identifier":
            self.lexer_next()
            if self.lexeme == "(":
                self.lexer_next()
                if self.IDs():
                    if self.lexeme == ')':
                        self.lexer_next()
                        return True
                    else:
                        print("ERROR expected )")
                        return False
                else:
                    print("ERROR expected ID")
                    return False
            else:
                return True
        elif self.lexeme == "(":
            self.lexer_next()
            if self.Expression():
                if self.lexeme == ")":
                    self.lexer_next()
                    return True
                else:
                    print("ERROR expected )")
                    return False
            else:
                print("ERROR expected expression")
                return False
        else:
            return False

    def Empty(self):
        self.f.write("<Empty> ::= e\n")
        self.productions.append("<Empty> ::= e")
        return

    def lexer_next(self):
        self.f.write("\n")
        self.corpus_counter += 1
        if self.corpus_counter == len(self.corpus):
            self.token = 'EOF'
            self.lexeme = '$'
            return
        self.token, self.lexeme = self.corpus[self.corpus_counter]
        self.f.write("Token: %s \t Lexeme: %s \n" % (self.token, self.lexeme))
        #print (self.token, self.lexeme)

if __name__ == '__main__':
    SA = SyntaxAnalyzer()
    s = ""
    SA.f = open("output.txt", "w+")
    for path in os.listdir("./"):
        if path.endswith(".txt") and path != "output.txt":
            print("parsing %s" % path)
            SA.f.write("\n OUTPUT FOR %s\n" % path)
            with open(path, 'r') as file:
                s = file.read().replace('\n', ' ').replace('\t', ' ')
                SA.corpus = lexer(s)
                #for elem in SA.corpus:
                #    SA.f.write("%s %s \n" % elem)
    SA.token, SA.lexeme = SA.corpus[0]
    SA.f.write("Token: %s \t Lexeme: %s \n" % (SA.token, SA.lexeme))
    SA.Rat19F()
    print(SA.productions)
