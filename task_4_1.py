import re, argparse

class terminal:
    def __init__(self, name):
        self.name = name
        self.productions = []
        self.original = True

class Grammar:
    def __init__(self, parsed):
        self.terminals = []
        self.grammarVariables = []
        self.result = []
        self.result2 = []
        self.handleParse(parsed)
        self.substituteVars()
        self.printResult()

    def printResult(self):
        output_file = open("task_4_1_result.txt", "w+", encoding="utf-8")
        for i in self.terminals:
            newList = []
            for x in i.productions:
                newList.append(" ".join(str(y) for y in x))
            last = " | ".join(str(x) for x in newList)
            output_file.write(i.name+" : "+last + "\n")

    def replace(self, i, j):
        k = i - 1
        while j <= k:
            for x in self.terminals[i].productions:
                if x[0] == self.terminals[j].name:
                    x.pop(0)
                    f = x
                    newVal = []
                    for u in self.terminals[j].productions:
                        newVal.append(u+f)
                    newVal.reverse()
                    for f in newVal:
                        self.terminals[i].productions.insert(0, f)
                    self.terminals[i].productions.remove(x)
            j += 1

    def substituteVars(self):
        i = 0
        while i < len(self.terminals):
            if self.terminals[i].original:
                j = 0
                self.replace(i, j)
                alpha = []
                beta = []
                for u in self.terminals[i].productions:
                    if u[0] == self.terminals[i].name:
                        alpha.append(u[1:len(u)])
                    else:
                        beta.append(u)
                if alpha:
                    self.terminals[i].productions = self.putDash(beta, self.terminals[i].name)
                    second = terminal(self.terminals[i].name+"'")
                    second.productions = self.putDash(alpha, self.terminals[i].name)
                    second.productions.append(["epsilon"])
                    second.original = False
                    self.terminals.insert(i+1, second)
            i += 1
                

    def putDash(self, x, name):
        for i in x:
            i.append(name+"'")
        return x


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