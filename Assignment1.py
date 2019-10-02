#Input: string containing any number of lexemes seperated by whitespace or seperators
#Output: list of (token, lexeme) pairs for Identifier, Integer, Real, Keyword, Operator and Seperator tokens

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
digits = '1234567890'
seperators = '[]();:'
operators = '=-+*/%'
keywords = ['for', 'if', 'while', 'fi', 'return', 'True', 'False']

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
    S = S + ' ' #append space to end of file for final terminating character
    current_word = ''
    result = []
    for char in S:
        if char in seperators or char is ' ':
            if char in seperators:
                result.append(('Seperator', char))
            if char in operators:
                result.append(('Operator', char))
            if len(current_word) > 0:
                lexeme = current_word
                token = ''
                if getType(current_word[0]) is 'L':
                    token = step_State1(current_word)
                elif getType(current_word[0]) is 'D':
                    token = step_State2(current_word)
                else:
                    token = 'Invalid Token'
                #TODO: keyword check
                result.append((token, lexeme))
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

#TODO: state for operators to check for +=, ==, -= etc
s = "def sample_function(input): if x == 10.5: return True "
print(lexer(s))
