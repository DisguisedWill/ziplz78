import numpy as np
from trie import No
        
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

fEntrada = open("exemplo2mb.txt")
fSaida = open("testezip.zip", 'wb')
compressor = lz78
compressor.comprime(fEntrada, fSaida)