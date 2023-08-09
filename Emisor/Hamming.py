from functools import reduce
from util import *

P0_LIST = [2, 4, 6]
P1_LIST = [2, 5, 6]
P2_LIST = [4, 5, 6]

def get_trama_parity(trama:list) -> list[int|None]:
    new_trama = []
    
    for i in range(7):
        if i in [0, 1, 3]:
            new_trama.append(None)
        else:
            new_trama.append(trama.pop(0))
    
    return new_trama

def get_parity(p_list: list[int], trama: list[int|None]) -> int:
    bit_map = [trama[i] for i in p_list]
    return 0 if bit_map.count(1) % 2 == 0 else 1

def hamming_encode(trama: list[int]) -> str:
    trama = get_trama_parity(trama)

    trama[0] = get_parity(P0_LIST, trama)
    trama[1] = get_parity(P1_LIST, trama)
    trama[3] = get_parity(P2_LIST, trama)
    
    return reduce(
        (lambda acc, val: str(val) + str(acc)),
        trama
    )

def process_hamming(trama:str) -> str:
    trama = [int(bit) for bit in trama]
    sub_tramas = []

    while len(trama) > 0:
        new_sub_trama = [
            0 if len(trama) == 0 else trama.pop(0)
                for _ in range(4)
        ]

        sub_tramas.append(new_sub_trama)


    encoded_tramas = [hamming_encode(trama) for trama in sub_tramas]

    mensaje_devided:str = reduce(
        (lambda acc, val: acc + ' ' + val),
        encoded_tramas
    )

    mensaje:str = reduce(
        (lambda acc, val: acc + val),
        encoded_tramas
    )
    return mensaje, mensaje_devided




def main():
    msg_input = input("Ingrese un mensaje a enviar: ")
    trama = reduce(
        (lambda acc, val: acc + val),
        [char_to_extended_ascii_bits(char) for char in msg_input]
    )
    print('trama inicial:\n>', trama)
    encoded_trama, encoded_print = process_hamming(trama)
    print('trama procesada con hamming (7, 4):\n>', encoded_print)
    trama_ruido, cambios = add_ruido(encoded_trama)
    print('trama con ruido:\n', trama_ruido)
    print('> se hicieron', cambios, 'cambios')

if __name__ == "__main__":
    main()

