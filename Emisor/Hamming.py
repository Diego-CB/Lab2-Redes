from functools import reduce

#CORRECCION DE ERRORES HAMMING 
P0_LIST = [2, 4, 6]
P1_LIST = [2, 5, 6]
P2_LIST = [4, 5, 6]

def get_trama_parity(trama:list) -> list[int|None]:
    return [
        None if i in [0, 1, 3] else trama.pop(0)
            for i in range(7)
    ]

def get_parity(p_list: list[int], trama: list[int|None]) -> int:
    bit_map = [trama[i] for i in p_list]
    return 0 if bit_map.count(1) % 2 == 0 else 1

def hamming_encode(trama: list[int]) -> str:
    trama = get_trama_parity(trama)

    trama[0] = get_parity(P0_LIST, trama)
    trama[1] = get_parity(P1_LIST, trama)
    trama[3] = get_parity(P2_LIST, trama)
    
    return reduce((lambda acc, val: str(val) + str(acc)), trama)


def main():
    trama_input = input("Ingrese una trama en binario: ")
    trama = [int(bit) for bit in trama_input]

    mensaje_codificado = hamming_encode(trama)

    print("Trama codificada con Hamming:", mensaje_codificado)

if __name__ == "__main__":
    main()
