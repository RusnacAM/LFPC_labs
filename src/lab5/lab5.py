from operator import add
import itertools
from traceback import print_tb
from typing import final

N = []
T = []
NT = []
P = {}

first = {}
last = {}
precedenceMatrix = []
strList = []

word = "caadbeb"


###INPUT###

# get productions
def input(file):
    rules = open(file, "r")
    for rule in rules:
        r = rule
        lhs = r[0]
        rhs = r[5:]
        if lhs in P:
            P[lhs].append(rhs.strip())
        else:
            P[lhs] = [rhs.strip()]
        addNT(lhs, rhs)
    return P


# get terminals, nonterminals
def addNT(lhs, rhs):
    if lhs not in N:
            N.append(lhs)

    symbols = list(rhs.strip())
    for symbol in symbols:
        if symbol.isupper() and symbol not in N:
             N.append(symbol)
        elif symbol.islower() and symbol not in T:
            T.append(symbol)

### STEP1 - BUILD FIRST/LAST TABLE ###

def step1():
    for nt in N:
        first[nt] = []
        last[nt] = []
        key = P.get(nt)
        addFirst(key, nt)
        addLast(key, nt)
    print("First/Last Table:\n")
    printFirstLast()
    print()


#print the table  
def printFirstLast():
    print ("{:<5} {:<15} {:<15}".format('', 'FIRST', 'LAST'))
    for k, v in first.items():
        f = v
        l = last.get(k)
        print ("{:<5} {:<15} {:<15}".format(str(k), str(f), str(l)))


#get first
def addFirst(key, nt):
    for val in key:
        f = val[0]
        if f not in first.get(nt):
            first[nt].append(f)
            if f in N:
                newKey = P.get(f)
                addFirst(newKey, nt)


#get last
def addLast(key, nt):
    for val in key:
        l = val[-1]
        if l not in last.get(nt):
            last[nt].append(l)
            if l in N:
                newKey = P.get(l)
                addLast(newKey, nt)

### STEP2 - BUILD PRECEDENCE MATRIX ##

def step2():
    #print(first)
    #print(last, '\n')
    initialMatrix()
    for k, v in P.items():
        for val in v:
            #print(val)
            if len(val) > 1:
                for i in range(len(val) - 1):
                    #print(i)
                    pos1 = val[i]
                    pos2 = val[i+1]
                    rule1(pos1, pos2)
                    rule2(pos1, pos2)
                    rule3(pos1, pos2)


#prepare matrix to be completed
def initialMatrix():
    global NT
    global precedenceMatrix
    NT = N + T
    NT.append('$')
    precedenceMatrix = [[[] for x in range(len(NT) + 1)] for y in range(len(NT) + 1)]
    i = 1
    for el in NT:
        precedenceMatrix[i][0].append(el)
        precedenceMatrix[0][i].append(el)
        i += 1

    for i in range(1, len(NT) + 1):
        for j in range(1, len(NT) + 1):
            #print(i, j)
            #print(precedenceMatrix[i][0])
            if '$' in precedenceMatrix[i][0] and '$' not in precedenceMatrix[0][j]:
                precedenceMatrix[i][j].append('<')
            elif '$' not in precedenceMatrix[i][0] and '$' in precedenceMatrix[0][j]:
                precedenceMatrix[i][j].append('>')


#complete matrix if precedence operator is =
def rule1(pos1, pos2):
    if '=' not in precedenceMatrix[NT.index(pos1) + 1][NT.index(pos2) + 1]:
        precedenceMatrix[NT.index(pos1) + 1][NT.index(pos2) + 1].append('=')


#complete matrix if precedence operator is <
def rule2(pos1, pos2):
    if pos2 in N:
        for l in first[pos2]:
            if '<' not in precedenceMatrix[NT.index(pos1) + 1][NT.index(l) + 1]:
                precedenceMatrix[NT.index(pos1) + 1][NT.index(l) + 1].append('<')


#complete matrix if precedence operator is >
def rule3(pos1, pos2):
    if pos1 in N and pos2 in T:
        for l in last[pos1]:
            if '>' not in precedenceMatrix[NT.index(l) + 1][NT.index(pos2) + 1]:
                precedenceMatrix[NT.index(l) + 1][NT.index(pos2) + 1].append('>')
    elif pos1 in N and pos2 in N:
        for l in last[pos1]:
            for f in first[pos2]:
                if f in T:
                    if '>' not in precedenceMatrix[NT.index(l) + 1][NT.index(f) + 1]:
                        precedenceMatrix[NT.index(l) + 1][NT.index(f) + 1].append('>')
    

#print the precedence matrix
def printMatrix(matrix):
    for row in matrix:
        for col in row:
            print('{:<5}'.format(str(*col)), end='')
        print()
    print()

### STEP3 - PARSE THE WORD ###

#actual parsing with all 3 precedence operator cases
def parseStr():
    print("Word to be examined: ", word, "\n")
    toList(word)
    tempList = ["$"]
    for i in range(len(strList)):
        operator = []
        curr = strList[i]
        sign = precedenceMatrix[NT.index(tempList[-1]) + 1][NT.index(curr) + 1]
        #print(sign)
        if "<" in sign:
            tempList.append(curr)
            parsingRep(i, operator)
        elif "=" in sign:
            tempList.append(curr)
            substr = tempList[-1]
            #print(substr)
            for val in range(len(tempList) - 2, 0, -1):
                substr += tempList[val]
                substr = substr[::-1]
                #print(substr)
                for k, v in P.items():
                    if substr in P[k]:
                        del tempList[-len(substr):]
                        tempList.append(k)
            parsingRep(i, operator)
        elif ">" in sign:
            substr = tempList[-1]
            for k, v in P.items():
                    if substr in P[k]:
                        del tempList[-len(substr):]
                        tempList.append(k)
            parsingRep(i, operator)

        representation = tempList + operator
        printParsing(representation)
    
    tempList.remove("$")
    finalW = ""
    for val in range(len(tempList)):
        finalW += tempList[val]
        #print(finalW)
        for k, v in P.items():
            if finalW in P[k]:
                del tempList[-len(finalW):]
                tempList.append(k)
    print(*tempList)
    
    if 'S' in tempList:
        print("\nWord Accepted\n")
    else:
        print("\nWord Rejected\n")


#transform word into list of characters
def toList(strW):
    for ch in strW:
        strList.append(ch)
    strList.append("$")


#get the entire word at each step
def parsingRep(curr, operator):
    for j in range(curr+1, len(strList)):
        operator.append(strList[j])


#print the parsing process in the right format
def printParsing(word):
    for j in range(len(word)):
        if j == len(word) - 1:
            sign = precedenceMatrix[NT.index(word[j]) + 1][NT.index('$') + 1]
            print(word[j], end = '')
            print(*sign, end = '')
            print()
        else:
            sign = precedenceMatrix[NT.index(word[j]) + 1][NT.index(word[j + 1]) + 1]
            print(word[j], end = '')
            print(*sign, end = '')

def main():
    input("V21.txt")
    #print(P)
    #print(N)
    #print(T)
    step1()
    step2()
    print('----------------------------------------------------', '\n')
    print("Precedence Matrix:\n")
    printMatrix(precedenceMatrix)
    print('----------------------------------------------------', '\n')
    print('Parsing: \n')
    parseStr()
    

if __name__ == "__main__":
    main()