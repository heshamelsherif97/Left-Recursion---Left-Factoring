import re, argparse, os, math

class terminal:
    def __init__(self, name):
        self.name = name
        self.productions = []

class Grammar:
    def __init__(self, parsed):
        self.terminals = []
        self.grammarVariables = []
        self.result = []
        self.result2 = []
        self.handleParse(parsed)
        self.leftFactor()
        self.handleEpsilons()
        self.printResult()

    def handleEpsilons(self):
        for i in self.terminals:
            check = False
            newList = []
            for j in i.productions:
                if len(j) == 0:
                    check = True
                else:
                    newList.append(j)
            if check:
                newList.append(["epsilon"])
            i.productions = newList

    def commonprefix(self, m):
        "Given a list of pathnames, returns the longest common leading component"
        if not m: return ''
        s1 = min(m)
        s2 = max(m)
        for i, c in enumerate(s1):
            if c != s2[i]:
                return s1[:i]
        return s1


    def handleProd(self, j, prods):
        commonList = []
        for i in prods:
            commonList += [self.commonprefix([j]+[i])]
        return commonList

    def max(self, x):
        p = math.inf
        for i in x:
            if i:
                if len(i) < p:
                    p = len(i)
        return p

    def leftFactor(self):
        for idx2,i in enumerate(self.terminals):
            j = 0
            while j < len(i.productions):
                commonList = self.handleProd(i.productions[j], i.productions[j+1:])
                if commonList:     
                    maxCommonIndex= self.max(commonList)
                    if maxCommonIndex != math.inf:
                        letter = "".join(str(r) for r in i.productions[j][:maxCommonIndex])
                        matches = []
                        nomatches = []
                        for u in i.productions:
                            if "".join(str(r) for r in u[:maxCommonIndex]) == letter:
                                matches.append(u[maxCommonIndex:])
                            else:
                                nomatches.append(u)
                        nomatches.insert(j, i.productions[j][:maxCommonIndex]+[i.name+"'"])
                        i.productions = nomatches
                        v = terminal(i.name+"'")
                        v.productions = matches
                        j = -1
                        self.addNewTerminal(idx2+1, v)                       
                j += 1
                        
    def addNewTerminal(self, x, v):
        check1 = False
        check2 = False
        for i in self.terminals:
            if i.name == v.name:
                check1 = True
                if self.compareList(i.productions, v.productions):
                    check2 = True
                break
        if check1 and check2:
            return
        elif check1 and not check2:
            v.name += "'"
            self.terminals.insert(x, v)
        elif not check1 and not check2:
            self.terminals.insert(x, v)
        else:
            self.terminals.insert(x, v)

    def compareList(self, list1, list2):
        check = True
        if len(list1) == len(list2):
            for i in list1:
                if i not in list2:
                    check = False
        return check

    def printResult(self):
        output_file = open("task_4_2_result.txt", "w+", encoding="utf-8")
        for i in self.terminals:
            newList = []
            for x in i.productions:
                newList.append(" ".join(str(y) for y in x))
            last = " | ".join(str(x) for x in newList)
            output_file.write(i.name+" : "+last + "\n")

    def handleParse(self, parse):
        for i in parse:
            name = i.split(" ")
            x = terminal(name[0])
            self.grammarVariables.append(name[0])
            name.pop(0)
            name.pop(0)
            newList = []
            for j in name:
                if j == "|":
                    x.productions.append(newList)
                    newList = []
                else:
                    newList.append(j) 
            if newList:
                x.productions.append(newList)
            self.terminals.append(x)      

def parseInput(x):
    newList = []
    for i in x:
        new = i.replace("\n", "")
        newList.append(new)
    return newList


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                        metavar="file")

    args = parser.parse_args()

    print(args.file)
    lines = []
    with open(args.file, "r") as f:
        for line in f:
            lines.append(line)
    parsed = parseInput(lines)
    Grammar(parsed)