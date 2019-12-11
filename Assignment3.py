import argparse
from Assignment1 import lexer

class SemanticParser:
    def __init__(self):
        self.instr_address = 0
        self.memory_addr = 5000
        self.token, self.lexeme = None, None
        self.corpus = None
        self.corpus_counter = 0
        self.f = None
        self.instr_table = []
        self.symbol_table = {}
        self.jumpstack = []

    def parse(self):
        if self.lexeme == "%%":
            self.lexer_next()
            self.OptDeclarationList()
            self.SL()
        else:
            print("ERROR: %%")
        if self.lexeme == "%%":
            self.lexer_next()
        else:
            print("ERROR: expected %%, got %s " % self.lexeme)
        if self.token is not "EOF":
            print("Expected EOF after %%")

        self.f.write("\n Final Instruction Table: \n")
        self.f.write(str(self.instr_table))

    def gen_instr(self, op, oprnd):
        self.instr_table.append([0,0,0])
        self.instr_table[self.instr_address][0] = self.instr_address + 1
        self.instr_table[self.instr_address][1] = op
        self.instr_table[self.instr_address][2] = oprnd
        self.f.write(str(self.instr_table[self.instr_address]) + '\n')
        self.instr_address += 1

    def check_sym(self, symbol):
        if symbol in self.symbol_table:
            return True
        else:
            return False

    def print_sym(self):
        print(self.symbol_table)


    def lexer_next(self):
        self.f.write("\n")
        self.corpus_counter += 1
        if self.corpus_counter == len(self.corpus):
            self.token = 'EOF'
            self.lexeme = '$'
            return
        self.token, self.lexeme = self.corpus[self.corpus_counter]
        self.f.write("Token: %s \t Lexeme: %s \n" % (self.token, self.lexeme))

    def OptDeclarationList(self):
        if self.DeclarationList():
            return
        else:
            self.Empty()

    def DeclarationList(self):
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
        if self.Qualifier():
            if self.IDs():
                return True
        return False

    def Qualifier(self):
        if self.lexeme in ('int', 'boolean'):
            self.lexer_next()
            return True
        else:
            return False

    def A(self):
        if self.token == 'Identifier':
            save = self.lexeme
            if self.check_sym(save):
                print("ERROR: %s already declared." % save)
                #return
            self.lexer_next()
            if self.lexeme == '=':
                self.lexer_next()
                if self.check_sym(self.token) and self.token != self.symbol_table[save][1]:
                    print("ERROR: Type mismatch %s -> %s" % (self.token, self.symbol_table[save][1]))
                    #return
                if self.E():
                    self.gen_instr('POPM', str(self.symbol_table[save][0]))
                    if self.lexeme == ';':
                        self.lexer_next()
                        return True
                    else:
                        print("ERROR ; expected")
                        return False
                else:
                    print("ERROR: expected expression")
                    return False
            else:
                print("ERROR: = expected")
                return False
        else:
            return False

    def E(self):
        if self.T():
            self.Eprime()
            return True
        else:
            return False

    def Eprime(self):
        if self.lexeme == '+':
            self.lexer_next()
            if self.T():
                self.gen_instr('ADD', 'nil')
                self.Eprime()
            else:
                print("ERROR expected term")
        else:
            self.Empty()

    def T(self):
        if self.F():
            self.Tprime()
            return True
        else:
            return False

    def Tprime(self):
        if self.lexeme == '*':
            self.lexer_next()
            if self.F():
                self.gen_instr('MUL', 'nil')
                self.Tprime()
            else:
                print("ERROR expected Factor")
        else:
            self.Empty()

    # def F(self):
    #     if self.token == 'Identifier':
    #         print('reached factor')
    #         self.gen_instr('PUSHM', str(self.symbol_table[self.lexeme][0]))
    #         self.lexer_next()
    #     elif self.token == 'Digit':
    #         self.gen_instr('PUSHM', str(self.lexeme))
    #         self.lexer_next()
    #     #self.lexer_next()

    def F(self):
        if self.lexeme == "-":
            self.lexer_next()
        elif self.Primary():
            return True
        print("ERROR expected primary")
        return False

    def Primary(self):
        if self.token in ["Integer", "Real", "Digit"]:
            self.gen_instr('PUSHM', str(self.lexeme))
            self.lexer_next()
            return True
        elif self.lexeme in ['true','false']:
            self.lexer_next()
            return True
        elif self.token == "Identifier":
            self.gen_instr('PUSHM', str(self.symbol_table[self.lexeme][0]))
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
            if self.E():
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
        return

    def while_statement(self):
        if self.lexeme == 'while':
            addr = str(self.instr_address)
            self.gen_instr('LABEL', 'nil')
            self.lexer_next()
            if self.lexeme == '(':
                self.lexer_next()
                if self.C():
                    if self.lexeme == ')':
                        self.lexer_next()
                        if self.S():
                            self.gen_instr('JUMP', addr)
                            self.back_patch(self.instr_address)
                            return True;
                            #self.lexer_next()
                        else:
                            return False;
                    else:
                        print('ERROR: ) expected.')
                        return False;
                else:
                    return False;
            else:
                print("ERROR: ( expected.")
                return False;
        else:
            return False;


    def C(self):
        if self.E():
            if self.lexeme in ['==','/=','>','<','=>','<=']:
                op = self.lexeme
                self.lexer_next()
                if self.E():
                    if op == '<':
                        self.gen_instr('LES', 'nil')
                        self.jumpstack.append(self.instr_address)
                        self.gen_instr('JUMPZ', 'nil')
                    elif op == '>':
                        self.gen_instr('GRT', 'nil')
                        self.jumpstack.append(self.instr_address)
                        self.gen_instr('JUMPZ', 'nil')
                    elif op == '==':
                        self.gen_instr('EQU', 'nil')
                        self.jumpstack.append(self.instr_address)
                        self.gen_instr('JUMPZ', 'nil')
                    elif op == '/=':
                        self.gen_instr('NEQ', 'nil')
                        self.jumpstack.append(self.instr_address)
                        self.gen_instr('JUMPZ', 'nil')
                    elif op == '=>':
                        self.gen_instr('GEQ', 'nil')
                        self.jumpstack.append(self.instr_address)
                        self.gen_instr('JUMPZ', 'nil')
                    elif op == '<=':
                        self.gen_instr('LEQ', 'nil')
                        self.jumpstack.append(self.instr_address)
                        self.gen_instr('JUMPZ', 'nil')
                    return True
            else:
                print("ERROR: R Token Expected.")
                return False
        else:
            return False

    def back_patch(self, jump_addr):
        addr = self.jumpstack.pop()
        self.instr_table[addr][2] = str(jump_addr)

    def I(self):
        if self.lexeme == 'if':
            addr = self.instr_address
            self.lexer_next()
            if self.lexeme == '(':
                self.lexer_next()
                self.C()
                if self.lexeme == ')':
                    self.lexer_next()
                    self.S()
                    self.back_patch(self.instr_address)
                    if self.lexeme == 'fi':
                        self.lexer_next()
                    else:
                        print("ERROR: fi expected.")
                else:
                    print("ERROR: ) expected.")
            else:
                print("ERROR: ( expected.")


#compound = {statementList}
    def compound(self):
        if self.lexeme == "{":
            self.lexer_next()
            self.SL()
            if self.lexeme == "}":
                self.lexer_next()
        #    else:
                #print('ERROR: } expected')
    #    else:
             #print('ERROR: { expected')

#statementList = s | sSL
    def SL(self):

        if self.S():
            if not self.SL():
                #self.lexer_next()
                self.Empty()
                return True
            else:
                #self.lexer_next()
                return True
        else:
            return False

    def S(self):
        if self.A() or self.scan() or self.while_statement():
            return True
        else:
            return False

    def r(self):
        if self.lexeme == "return":
            self.lexer_next()
            self.E()
            if self.lexeme == ";":
                self.lexer_next()
                return True
            else:
                print("ERROR ; expected after return")
            self.gen_instr('JUMPZ', 'nil')
        else:
            return False

    def scan(self):
        if self.lexeme == 'get':
            addr = str(self.instr_address)
            self.lexer_next()
            if self.lexeme == '(':
                self.lexer_next()
                save = self.lexeme
                if self.IDs():
                    print(self.symbol_table)
                    self.gen_instr('STDIN', str(self.symbol_table[save][0]))
                    if self.lexeme == ')':
                        self.lexer_next()
                        if self.lexeme == ';':
                            self.lexer_next()
                            return True
                        else:
                            print('ERROR: ; expected')
                            return False
                    else:
                        print('ERROR: ) expected')
                        return False
                else:
                    print('ERROR: expected identifier')
                    return False
            else:
                print('ERROR: ( expected')
                return False
        else:
            return False

    def id(self):
        if self.token == 'Identifier':
            save = self.lexeme
            self.symbol_table[save] = [self.memory_addr]
            self.lexer_next()
            if self.lexeme == ',':
                self.lexer_next()
                self.id()
        else:
            print('ERROR: identifier expected')

    def IDs(self):
        if self.token == "Identifier":
            self.symbol_table[self.lexeme] = [self.memory_addr, self.token]
            self.memory_addr += 1
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

#print = put (expression);
    def p(self):
        if self.lexeme == 'put':
            self.lexer_next()
            if self.lexeme == '(':
                self.lexer_next()
                self.E()
                self.gen_instr('STDOUT', str(self.symbol_table[self.lexeme][0]))
                if self.lexeme == ')':
                    self.lexer_next()
                else:
                    print('ERROR: ) expected')
            else:
                print('ERROR: ( expected')

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("path")
    args = argparser.parse_args()
    SP = SemanticParser()
    s = ""
    SP.f = open("output.txt", "w+")
    path = args.path
    if path.endswith(".txt") and path != "output.txt":
        print("parsing %s" % path)
        SP.f.write("\n OUTPUT FOR %s\n" % path)
        with open(path, 'r') as file:
            s = file.read().replace('\n', ' ').replace('\t', ' ')
            SP.corpus = lexer(s)
            #for elem in SA.corpus:
            #    SA.f.write("%s %s \n" % elem)
    print(SP.corpus)
    SP.token, SP.lexeme = SP.corpus[0]
    SP.f.write("Token: %s \t Lexeme: %s \n" % (SP.token, SP.lexeme))
    SP.parse()
