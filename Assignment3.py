import argparse
from Assignment1 import lexer

class SemanticParser:
    def __init__(self):
        self.instr_address = 0
        self.token, self.lexeme = None, None
        self.corpus = None
        self.corpus_counter = 0
        self.f = None
        self.instr_table = []
        self.symbol_table = []
        self.jumpstack = []

    def parse(self):
        while self.corpus_counter < len(self.corpus):
            self.A()
            self.while_statement()
            self.I()
            self.compound()
            #self.SL()
            self.scan()
            self.p()
        self.f.write("\n Final Instruction Table: \n")
        self.f.write(str(self.instr_table))

    def gen_instr(self, op, oprnd):
        self.instr_table.append([0,0,0])
        self.instr_table[self.instr_address][0] = self.instr_address
        self.instr_table[self.instr_address][1] = op
        self.instr_table[self.instr_address][2] = oprnd
        self.f.write(str(self.instr_table[self.instr_address]) + '\n')
        self.instr_address += 1

    def lexer_next(self):
        self.f.write("\n")
        self.corpus_counter += 1
        if self.corpus_counter == len(self.corpus):
            self.token = 'EOF'
            self.lexeme = '$'
            return
        self.token, self.lexeme = self.corpus[self.corpus_counter]
        self.f.write("Token: %s \t Lexeme: %s \n" % (self.token, self.lexeme))

    def A(self):
        if self.token == 'Identifier':
            save = self.lexeme
            self.symbol_table.append(save)
            self.lexer_next()
            if self.lexeme == '=':
                self.lexer_next()
                self.E()
                self.gen_instr('POPM', str(self.symbol_table.index(save)))
            else:
                print("ERROR: = expected")
        else:
            print("ERROR: identifier expected, got %s" % self.lexeme)

    def E(self):
        self.T()
        self.Eprime()

    def Eprime(self):
        if self.lexeme == '+':
            self.lexer_next()
            self.T()
            self.gen_instr('ADD', 'nil')
            self.Eprime()

    def T(self):
        self.F()
        self.Tprime()

    def Tprime(self):
        if self.lexeme == '*':
            self.lexer_next()
            self.F()
            self.gen_instr('MUL', 'nil')
            self.Tprime()

    def F(self):
        if self.token == 'Identifier':
            self.gen_instr('PUSHM', str(self.symbol_table.index(self.lexeme)))
            self.lexer_next()
        elif self.token == 'Digit':
            self.gen_instr('PUSHM', str(self.lexeme))
            self.lexer_next()
        else:
            print('ERROR: Identifier expected')

    def while_statement(self):
        if self.lexeme == 'while':
            addr = str(self.instr_address)
            self.gen_instr('LABEL', 'nil')
            self.lexer_next()
            if self.lexeme == '(':
                self.lexer_next()
                self.C()
                if self.lexeme == ')':
                    self.lexer_next()
                    self.S()
                    self.gen_instr('JUMP', addr)
                    back_patch(self.instr_address)
                    self.lexer_next()
                else:
                    print('ERROR: ) expected.')
            else:
                print("ERROR: ( expected.")
        else:
            print("ERROR: while Expected.")

    def C(self):
        self.E()
        if self.lexeme in ['==','/=','>','<','=>','<=']:
            op = self.lexeme
            self.lexer_next()
            self.E()
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
        else:
            print("ERROR: R Token Expected.")

    def back_patch(self, jump_addr):
        addr = self.jumpstack.pop()
        instr_table[addr][3] = str(jump_addr)

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
        else:
            print("ERROR: if expected.")

#compound = {statementList}
    def compound(self):
        if self.lexeme == "{":
            addr = str(self.instr_address)
            self.gen_instr('LABEL', 'nil')
            self.lexer_next()
            self.SL()
            if self.lemxeme == "}":
                self.gen_instr('JUMP', addr)
                back_patch(self.instr_address)
                self.lexer_next()
            else:
                print('ERROR: } expected')
        else: print('ERROR: { expected')

#statementList = s | s * SL
    def SL(self):
        self.s()

#scan = get (ID) | ; **DO WE NEED SEMICOLON?????* HOW DO WE DO OR :(
    def scan(self):
        if self.lexeme == 'get':
            addr = str(self.instr_address)
            self.gen_instr('LABEL', 'nil')
            self.lexer_next()
            if self.lexeme == '(':
                self.lexer_next()
                self.id()
                if self.lexeme == ')':
                    self.lexer_next()
                else:
                    print('ERROR: ) expected')
            else:
                print('ERROR: ( expected')

    def id(self):
        if self.token == 'Identifier':
            save = self.lexeme
            self.symbol_table.append(save)
            self.lexer_next()
            if self.lexeme == ',':
                #do something
                self.id()
                self.lexer_next() #uhm how do we stop this lol
            else:
                print('ERROR: , expected')
        else:
            print('ERROR: identifier expected')

#print = put (expression);
    def p(self):
        if self.lexeme == 'put':
            addr = str(self.instr_address)
            self.gen_instr('LABEL', 'nil')
            self.lexer_next()
            if self.lexeme == '(':
                self.lexer_next()
                self.E()
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
