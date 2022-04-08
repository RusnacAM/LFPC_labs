import itertools
import copy
from operator import add

N = []
T = []
P = {}

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

    #print(N)
    #print(T)
    #print(P)


# get terminals, nonterminals
def addNT(lhs, rhs):
    if lhs not in N:
            N.append(lhs)

    if rhs != '$':
        symbols = list(rhs.strip())
        for symbol in symbols:
            if symbol.isupper() and symbol not in N:
                N.append(symbol)
            elif symbol.islower() and symbol not in T:
                T.append(symbol)


###STEP1###

#Eliminate eps productions
def step1(CFG):
    eps = [k for k in CFG if '$' in CFG.get(k)]
    removeEps(CFG, eps)     
    temp = copy.deepcopy(CFG)
    newTemp = {k: [getCombinations(curr, eps) for curr in temp.get(k) if getCombinations(curr, eps) != []] for k in temp}
    newTemp = {k: list(itertools.chain.from_iterable(newTemp.get(k))) for k in newTemp}
    CFG = Merge(temp, newTemp)
    if(checkEps(CFG)):
        step1(CFG)


#Delete eps prod/values from key
def removeEps(CFG, eps):
    for prod in eps:
        CFG[prod].remove('$')
        if len(CFG[prod]) == 0:
            del CFG[prod]


#Check if there are eps prod
def checkEps(CFG):
    check = False
    for k,v in CFG.items():
        for i in range(len(v)):
            if v[i] == '':
                v[i] = '$'
                check = True
    global P
    P = copy.deepcopy(CFG)
    printProd(P)
    return check


#Get all possible combinations after eps elimination
def getCombinations(curr, epsProd):
    index = [count for count, el in enumerate(curr) if el in epsProd]
    combinations = []
    [combinations.extend(itertools.combinations(index, i)) for i in range(1, len(index) + 1)]
    allComb = [''.join(curr[x] for x in range(len(curr)) if x not in i) for i in combinations]
    return allComb


#Merge two dictionaries
def Merge(dict1, dict2):
    for k,v in dict2.items():
        if k in dict1:
            dict1[k] += v
        else: 
            dict1[k] = v
    return {k:sorted(set(j),key=j.index) for k,j in dict1.items()}


###STEP2###

def step2(CFG):
    renamings = {k: list(v for v in CFG.get(k) if v in N) for k in CFG}
    CFG = {k: list(v for v in CFG.get(k) if v not in N) for k in CFG}
    renamings = dict([(k,v) for k, v in renamings.items() if len(v) > 0])
    #print(renamings)
    #print(CFG)
    replaceRenamings(renamings, CFG)
    CFG = Merge(CFG, renamings)
    global P
    P = copy.deepcopy(CFG)
    printProd(P)


#Replace productions in the place of removed unit prod
def replaceRenamings(ren, CFG):
    for key in ren:
        for value in ren.get(key):
            #print(CFG.get(value))
            ren[key] = list(CFG.get(value))
    return CFG


###STEP3###

def step3(CFG):
    accT = []
    getAccessed(CFG, accT)
    #print(accT)
    inaccT = list(set(N) - set(accT))
    #print(inaccT)
    for el in inaccT:
        del CFG[el]
    global P
    P = copy.deepcopy(CFG)
    printProd(P)


#Get list of accessible prod
def getAccessed(CFG, accT):
    for key in CFG:
            for value in CFG.get(key):
                for char in value:
                    if char.isupper() and char not in accT:
                        accT.extend(char)
    return CFG


###STEP4###

def step4(CFG):
    newT = [k for k in CFG]
    productive = []
    nonProd = []
    addProductives(CFG, productive)
    prelimProd = list(set(newT) - set(productive))
    checkDerivations(CFG, prelimProd, productive, nonProd)
    nonProd = list(set(nonProd) - set(productive))
    #print(nonProd)
    deleteNP(CFG, nonProd)
    global P
    P = copy.deepcopy(CFG)
    printProd(P)


#Get list of NT deriving directly into T
def addProductives(CFG, prod):
    for key in CFG:
        for value in CFG.get(key):
            if value in T and key not in prod:
                prod.extend(key)


#Check other NT if they are productive through derivations
def checkDerivations(CFG, prelim, prod, nonProd):
    for key in CFG:
        if key in prelim:
            for value in CFG.get(key):
                for char in value:
                    if char.isupper() and char in prod and key not in prod:
                        prod.extend(key)
                    elif key not in prod and key not in nonProd:
                        nonProd.extend(key)


#Eliminate non-productive symbols
def deleteNP(CFG, nonProd):
    for el in nonProd:
        del CFG[el]

    for key in CFG:
        for value in CFG.get(key):
            for char in value:
                if char in nonProd:
                    CFG[key].remove(value)


###STEP5 - CNF_CONVERSION###

def CNF(CFG):
    newT = []
    checkTerm(CFG, newT)
    addCombinations(CFG)

    chomskyT = {}
    substT(chomskyT, newT)
    inv_chomskyT = {v: k for k, v in chomskyT.items()}

    prelimChomsky = {}
    finalChomsky(CFG, prelimChomsky, inv_chomskyT, newT)
    prelimChomsky.update(chomskyT)
    #print(prelimChomsky)
    global P
    P = copy.deepcopy(prelimChomsky)
    return P


#Check terminals for substitution
def checkTerm(CFG, newT):
    for key in CFG:
            for value in CFG.get(key):
                for char in value:
                    if char.islower() and char not in newT:
                        newT.extend(char)


#Get combinations for production with length > 2
def addCombinations(CFG):
    chomskyNT = {}
    changes = True
    keyY = 'Y'
    while changes:
        changes = False
        for key, value in CFG.items():
            for i, v in enumerate(value):
                variables = new_split(v)
                if len(variables) > 2:
                    changes = True
                    getComb(CFG, keyY, key, i, chomskyNT, variables)
            
        for key, value in chomskyNT.items():
            CFG[key] = [value]
    return CFG


#split current value 
def new_split(string):
    split = []
    old_s = ''
    for s in string:
        if s.isdigit():
           old_s += s
        else:
            split.append(old_s)
            old_s = s
    split.remove('')
    split.append(old_s)
    return split


#Form the actual combinations
def getComb(CFG, keyY, key, i, chomskyNT, var):
    comb = keyY + str(len(chomskyNT)+1)
    replace = "".join(var[1:])
    existing = getKey(chomskyNT, replace)
    #print(existing)
   
    if existing:
        CFG[key][i] = var[0] + existing
        if key in chomskyNT.keys():
            chomskyNT[key] = var[0] + existing
    else:
        chomskyNT[comb] = replace
        CFG[key][i] = var[0] + comb
        if key in chomskyNT.keys():
            chomskyNT[key] = var[0] + comb


#Get the key for the value
def getKey(rule, value):
    for key, v in rule.items():
        if v == value:
            return key
    return None


#Substitute terminal values with NT values
def substT(chomskyT, newT):
    for el in range(len(newT)):
        newX = str(el+1)
        key = 'X' + newX
        chomskyT[key] = newT[el]
    return chomskyT


#Get final CNF
def finalChomsky(CFG, prelimChomsky, inv_chomskyT, newT):
    for key, values in CFG.items():
        for i in range(len(values)):
            value = values[i]
            for char in range(len(value)):
                if len(value) > 1 and value[char] in newT:
                    value = value.replace(value[char], inv_chomskyT[value[char]])
            if key in prelimChomsky:
                prelimChomsky[key].append(value)
            else:
                prelimChomsky[key] = [value]
    return prelimChomsky


###PRINT###

#Print in right form
def printProd(CFG):
    for key, value in CFG.items():
        print(key + " -> " + value[0], end=' ')
        for v in value[1:]:
            print("| " + v, end=' ')
        print()


def main():
    input("V9.txt")
    print("\nInitial Context Free Grammar: ")
    printProd(P)
    print("\nStep1, Eliminate Ɛ productions: ")
    step1(P)
    print("\nStep2, Eliminate renamings: ")
    step2(P)
    print("\nStep3, Eliminate inaccesible symbols: ")
    step3(P)
    print("\nStep4, Eliminate non-productive symbols: ")
    step4(P)
    print("\nConversion of context free grammar to chomsky normal form: ")
    CNF(P)
    printProd(P)

if __name__ == "__main__":
    main()