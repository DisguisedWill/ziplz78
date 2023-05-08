import numpy as np
from trie import No
import sys

class lz78:
    
    def comprime(fEntrada, fSaida):
        string = ""
        trie = No(string, 0)
        bytes = 0
        cod = 1
        counter = 0
        # Primeira passada
        while True:
            char = fEntrada.read(1)
            if not char:
                string = ''
                break
            
            busca = trie.busca(string + char)
            if busca != None:
                string = string + char
            else:
                counter += 1
                # print([trie.busca(string)])
                trie.addPalavra(string + char, cod)
                cod += 1
                string = ''

        # Determina numero de bytes
        if counter <= 255:
            bytes = 1
        elif counter <= 65535:
            bytes = 2
        elif counter <= 16_777_216:
            bytes = 3
        elif counter <= 200_000_000:
            bytes = 4
        
        fEntrada.seek(0) # volta pro inicio do arquivo
        fSaida.write(bytes.to_bytes(4, 'big'))
        
        # Segunda passada:
        trie = No(string, 0)
        cod = 1
        counter = 0
        while True:
            char = fEntrada.read(1)
            if not char:
                break
            busca = trie.busca(string + char)
            print(char)
            if busca != None:
                string = string + char
            else:
                counter += 1
                busca2 = trie.busca(string)
                # print([busca2.to_bytes(bytes, 'big'), char])
                fSaida.write(busca2.to_bytes(bytes, 'big'))
                fSaida.write(char.encode('utf-8'))
                trie.addPalavra(string + char, cod)
                cod += 1
                string = ''
        
    def decomprime(fEntrada, fSaida):
        
        return

def erroEntrada():
        print(f"Uso:\n {sys.argv[0]} -c <arquivo a ser comprimido>")
        print(f"{sys.argv[1]} -x <arquivo a ser decomprimido>")

def leEntrada():
    fEntrada = None
    try:
        if sys.argv[1] == '-c':
            fEntrada = open(sys.argv[2], 'r')
        elif sys.argv[1] == '-x':
            fEntrada = open(sys.argv[2], 'wb')
    except:
        print("Erro ao ler arquivo de entrada")
    
    print(sys.argv[2])
    return fEntrada 

def leSaida():
    nomesaida = ""
    if sys.argv[1] == '-c':
        if len(sys.argv) == 3:
            if "." in sys.argv[2]:
                nomesaida = sys.argv[2].split(".")[0] + ".z78"
            else:
                nomesaida = sys.argv[2] + ".z78"
        else:
            nomesaida = sys.argv[3]
    elif sys.argv[1] == '-x':
        if len(sys.argv) == 3:
            if "." in sys.argv[2]:
                nomesaida = sys.argv[2].split(".")[0] + ".txt"
            else:
                nomesaida = sys.argv[2] + ".txt"
        else:
            nomesaida = sys.argv[3]
    try:
        if sys.argv[1] == '-c':
            
            fSaida = open(nomesaida, 'wb')
            
        elif sys.argv[1] == '-x':
            fSaida = open(nomesaida, 'wb')
    except:
        print("Erro ao ler arquivo de saida")
    return fSaida

def main():
    if (len(sys.argv) != 3 and len(sys.argv) != 4) or (sys.argv[1] != '-c' and sys.argv[1] != '-x'):
        erroEntrada()
        return -1
    
    fEntrada = leEntrada()
    fSaida = leSaida()
    print(fEntrada)
    print(fSaida)
    
    compressor = lz78
    compressor.comprime(fEntrada, fSaida)

main()