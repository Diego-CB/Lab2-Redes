import numpy as np


def encodificador(trama):
    #Variables
    G1 = [1,1,1]
    G1 = [1,0,1]
    
    

def main():
    codigo = input("Ingrese la trama en binario:")
    codigo_codificado= encodificador(codigo)
    
    print("Mensaje codificado")
    print(codigo_codificado)
    
if __name__ == "__main__":
    main()