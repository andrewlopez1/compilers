#Input: string containing any number of lexemes seperated by whitespace or separators
#Output: list of (token, lexeme) pairs for Identifier, Integer, Real, Keyword, Operator and Seperator tokens
import os

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
digits = '1234567890'
separators = '[]();:{},'
operators = '=-+*/<>%'
combination_operators = ['==', '/=', '=>', '<=', '%%']
keywords = [
            'function', 'int', 'boolean', 'real', 'if', 'fi', 'otherwise',
            'return', 'put', 'get', 'while', 'true', 'false'
        ]

def getType(char):
    if char in letters:
        return 'L'
    elif char in digits:
        return 'D'
    elif char in separators:
        return 'S'
    elif char in operators:
        return 'O'
    else:
        return char

def lexer(S):
    S = S + ' ' #append space to end of file for final terminating character
    current_word = ''
    result = []
    commented = False
    for index, char in enumerate(S):
        if commented:
            if char == ']' and S[index-1] == '*':
                commented = False
            continue
        if char in separators or char is ' ' or char in operators:
            if len(current_word) > 0 and current_word[0] not in operators:
                #print(current_word)
                lexeme = current_word
                token = ''
                if current_word in keywords:
                    token = 'Keyword'
                elif getType(current_word[0]) is 'L':
                    token = step_State1(current_word)
                elif getType(current_word[0]) is 'D':
                    token = step_State2(current_word)
                elif getType(current_word[0]) is 'O':
                    token = step_State4(current_word)
                else:
                    token = 'Invalid Token'

                result.append((token, lexeme))
                current_word = ''
            if char in separators:
                if char == '[' and S[index+1] == '*':
                    commented = True
                    continue
                result.append(('Seperator', char))
            if char in operators:
                current_word = current_word + char
                if current_word in combination_operators:
                    if current_word == '%%':
                        result.append(('Separator', current_word))
                        current_word = ''
                        continue
                    result.append(('Operator', current_word))
                    current_word = ''
                elif char + S[index + 1] in combination_operators:
                    continue
                else:
                    result.append(('Operator', current_word))
                    current_word = ''

        else:
            current_word = current_word + char
    return result

#step_stateN functions will take input of one potential lexeme and output the token value
def step_State1(lexeme):
    input = lexeme[0]

    if getType(input) in 'LD_':
        if len(lexeme) == 1:
            return 'Identifier'
        return step_State1(lexeme[1:])
    else:
        return 'Invalid Token'

def step_State2(lexeme):
    input = lexeme[0]
    if getType(input) is 'D':
        if len(lexeme) == 1:
            return 'Digit'
        return step_State2(lexeme[1:])
    elif getType(input) is '.':
        if len(lexeme) == 1:
            return 'Invalid Token' #no token ends with '.'
        return step_State3(lexeme[1:])
    else:
        return 'Invalid Token'

def step_State3(lexeme):
    input = lexeme[0]
    if getType(input) is 'D':
        if len(lexeme) == 1:
            return 'Real'
        return step_State3(lexeme[1:])
    else:
        return 'Invalid Token'


def step_State4(lexeme):
    input = lexeme[0]
    #print(lexeme)
    if len(lexeme) == 1:
        return 'Operator'
    elif len(lexeme) == 2 and (lexeme in operators or lexeme in combination_operators):
        if lexeme == '%%':
            return 'Separator' #hackey solution
        return 'Operator'
    else:
        return 'Invalid Token'

if __name__ == '__main__':
    s = ""
    f = open("output.txt", "w+")
    for path in os.listdir("./"):
        if path.endswith(".txt") and path != "output.txt":
            print("parsing %s" % path)
            f.write("\n OUTPUT FOR %s\n" % path)
            with open(path, 'r') as file:
                s = file.read().replace('\n', ' ').replace('\t', ' ')
                result = lexer(s)
                for elem in result:
                    f.write("%s %s \n" % elem)
