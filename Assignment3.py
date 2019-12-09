


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

    def gen_instr(op, oprnd):
        self.instr_table.append((0,0,0))
        self.instr_table[instr_address][0] = instr_address
        self.instr_table[instr_address][1] = op
        self.instr_table[instr_address][2] = oprnd
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

    def A():
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
            print("ERROR: identifier expected")

    def E():
        self.T()
        self.Eprime()

    def Eprime():
        if self.lexeme = '+':
            self.lexer_next()
            self.T()
            self.gen_instr('ADD', 'nil')
            self.Eprime()

    def T():
        self.F()
        self.Tprime()

    def Tprime():
        if self.lexeme == '*':
            self.lexer_next()
            self.F()
            self.gen_instr('MUL', 'nil')
            self.Tprime()

    def F():
        if self.token == 'Identifier':
            self.gen_instr('PUSHM', str(self.symbol_table.index(self.lexeme)))
            self.lexer_next()
        else:
            print('ERROR: Identifier expected')

    def while_statement():
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

    def C():
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

    def back_patch(jump_addr):
        addr = self.jumpstack.pop()
        instr_table[addr][3] = str(jump_addr)

    def I():
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
