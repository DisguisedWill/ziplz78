import numpy as np

class No:
    def __init__(self, char, valor):
        self.char = char
        self.valor = valor
        self.filhos = np.array([])
    
    def busca(self, string, nivel=0):
        if len(string) == nivel:
            return self.valor
        if self.char == "" or self.char == string[nivel-1]:
            for filho in self.filhos:
                if filho.char == string[nivel]:
                    return filho.busca(string, nivel+1)
                    break
            else:
                return None
    
    def addPalavra(self, str, n):
        if str == "":
            self.valor = n
            return 
        for filho in self.filhos:
                if filho.char == str[0]:
                    filho.addPalavra(str[1:], n)
                    break
        else:
            self.filhos = np.append(self.filhos, No(str[0], None))
            self.filhos[-1].addPalavra(str[1:], n)
    
    def print(self, nivel=0):
        print("--"*nivel, end='')
        print(f"{self.char}:{self.valor}")
        
        for filho in self.filhos:
            filho.print(nivel+1)