#!/bin/python3
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
        while True:
            char = fEntrada.read(1)
            if not char:
                break
            busca = trie.busca(string + char)
            
            if busca != None:
                string = string + char
                
            else:
                busca2 = trie.busca(string)
                fSaida.write(busca2.to_bytes(bytes, 'big'))
                fSaida.write(char.encode('utf-8'))
                trie.addPalavra(string + char, cod)
                cod += 1
                string = ''
        fSaida.write(trie.busca(string).to_bytes(bytes, 'big'))
    
    
    def descomprime(fEntrada, fSaida):
        string = ''
        bytes = int.from_bytes(fEntrada.read(4), byteorder='big', signed=False)
        dicionario = {0: ""}
        cod = 1
        counter = 0
        while True:
            valor = int.from_bytes(fEntrada.read(bytes), byteorder='big', signed=False)
            
            char = ''
            byte = fEntrada.read(1)  # read one byte at a time
            while byte != b'':
                
                try:
                    char = byte.decode('utf-8')
                    
                    break  # stop reading after decoding one character
                except UnicodeDecodeError:
                    # the byte is not a complete character, continue reading
                    byte += fEntrada.read(1)

            if not char:
                if valor:
                    busca = dicionario[valor]
                    fSaida.write(busca + char)  
                break
            
            busca = dicionario[valor]
            fSaida.write(busca + char)           
            dicionario[cod] = busca + char
            cod += 1
        
        
        
        
def erroEntrada():
        print(f"Uso:\n{sys.argv[0]} -c <arquivo a ser comprimido>")
        print("Ou")
        print(f"{sys.argv[0]} -x <arquivo a ser decomprimido>")

def leEntrada():
    fEntrada = None
    try:
        if sys.argv[1] == '-c':
            fEntrada = open(sys.argv[2], 'r')
        elif sys.argv[1] == '-x':
            fEntrada = open(sys.argv[2], 'rb')
    except:
        print("Erro ao ler arquivo de entrada")
    
    
    return fEntrada 

def leSaida():
    nomesaida = ""
    if sys.argv[1] == '-c':
        if len(sys.argv) == 3:
            if "." in sys.argv[2]:
                nomesaida = sys.argv[2].rsplit(".", 1)[-2] + ".z78"
                
            else:
                nomesaida = sys.argv[2] + ".z78"
        else:
            nomesaida = sys.argv[3]
    elif sys.argv[1] == '-x':
        if len(sys.argv) == 3:
            if "." in sys.argv[2]:
                nomesaida = sys.argv[2].rsplit(".", 1)[-2] + ".txt"
            else:
                nomesaida = sys.argv[2] + ".txt"
        else:
            nomesaida = sys.argv[3]
    try:
        if sys.argv[1] == '-c':
            
            fSaida = open(nomesaida, 'wb')
            
        elif sys.argv[1] == '-x':
            fSaida = open(nomesaida, 'w')
    except:
        print("Erro ao ler arquivo de saida")
        exit()
    return fSaida

def main():
    if (len(sys.argv) != 3 and len(sys.argv) != 4) or (sys.argv[1] != '-c' and sys.argv[1] != '-x'):
        erroEntrada()
        return -1
    
    fEntrada = leEntrada()
    fSaida = leSaida()
    
    compressor = lz78
    if sys.argv[1] == '-c':
        compressor.comprime(fEntrada, fSaida)
    elif sys.argv[1] == '-x':
        compressor.descomprime(fEntrada, fSaida)
    else:
        erroEntrada()

main()