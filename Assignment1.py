#Input: string containing any number of lexemes seperated by whitespace or seperators
#Output: list of (token, lexeme) pairs for Identifier, Integer, Real, Keyword, Operator and Seperator tokens

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
digits = '1234567890'
seperators = '[]();'
operators = '=-+*/%'

def getType(char):
    if char in letters:
        return 'L'
    elif char in digits:
        return 'D'
    elif char in seperators:
        return 'S'
    elif char in operators:
        return 'O'
    else:
        return char

def lexer(S):
    current_word = []
    result = []
    while len(S) >= 0:
        char = ' '
        if len(S) > 0:
            char = S.pop(0) #pop first letter of string
        if char in seperators or char is ' ':
            if char in seperators:
                result.append(('Seperator', char))
            if len(current_word) > 0:
                lexeme = current_word
                token = ''
                if getType(current_word[0]) is 'L':
                    token = step_State1(current_word)
                elif getType(current_word[0]) is 'D':
                    token = step_State2(current_word)
                else:
                    token = 'Invalid Token'
                result.append((token, lexeme))
        else:
            current_word.append(char)
    return result

#step_stateN functions will take input of one potential lexeme and output the token value
def step_State1(lexeme):
    input = lexeme.pop(0)

    if getType(input) in 'LD_':
        if len(lexeme) == 0:
            return 'Identifier'
        return step_State1(lexeme)
    else:
        return 'Invalid Token'

def step_State2(lexeme):
    input = lexeme.pop(0)
    if getType(input) is 'D':
        if len(lexeme) == 0:
            return 'Digit'
        return step_State2(lexeme)
    elif getType(input) is '.':
        if len(lexeme) == 0:
            return 'Invalid Token' #no token ends with '.'
        return step_State3(lexeme)
    else:
        return 'Invalid Token'

def step_State3(lexeme):
    input = lexeme.pop(0)
    if getType(input) is 'D':
        if len(lexeme) == 0:
            return 'Real'
        return step_State3(lexeme)
    else:
        return 'Invalid Token'

#TODO: state for operators to check for +=, ==, -= etc
