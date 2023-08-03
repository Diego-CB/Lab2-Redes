import numpy as np


def encodificador(trama):
    #Variables
    G1 = [1,1,1]
    G2 = [1,0,1]
    
    r1=[0,0]
    r2=[0,0]
    
    codificado=""
    
    for bit in trama:
        r1.insert(0, int(bit))
        r2.insert(0, int(bit))
        
        #se hace le or para codificar los bits
        xor1 = sum( r1[i] * G1[1] for i in range(3)) % 2 
        xor2 = sum( r2[i] * G2[1] for i in range(3)) % 2 
        
        codificado += str(xor1) + str(xor2)
        
        r1.pop()
        r2.pop()
    
    return codificado

def main():
    codigo = input("Ingrese la trama en binario:")
    codigo_codificado= encodificador(codigo)
    
    print("Mensaje codificado")
    print(codigo_codificado)
    
if __name__ == "__main__":
    main()