import crcmod.predefined

def CRC32(trama):
    # Polinomio estándar para CRC-32
    polinomio = "crc-32"

    #aqui se usa la funcion de la biblioteca que ayuda a con el polinomio se calcula para obtener el CRC
    crc_func = crcmod.predefined.Crc(polinomio)

    #Se pasa la trama a bytes
    trama_bytes = bytes(int(trama[i:i+8], 2) for i in range(0, len(trama), 8))

    #Se calcula el CRC-32 de la trama de bytes
    crc_final = crc_func.new(trama_bytes).digest()

    # Convierte el CRC-32 en una cadena binaria de 32 bits
    crc_bin = bin(int.from_bytes(crc_final, byteorder='big'))[2:].zfill(32)

    return crc_bin

def simulacion(trama):
    crc_temporal = trama[-32:]  #Obtiene los últimos 32 bits que son el CRC-32 recibido
    trama_sin_crc = trama[:-32]  #Obtiene la trama original sin el CRC-32 recibido

    # Calcular el CRC-32 de la trama recibida (sin el CRC-32)
    crc_calculado_recibido = CRC32(trama_sin_crc)

    if crc_calculado_recibido == crc_temporal:
        print("La trama no contiene errores.")
    else:
        print("Se detectaron errores en la trama.")
    
def main():
    trama = input("Ingrese la trama en binario: ")

    # Calcula el CRC-32 de la trama original
    crc_calculado = CRC32(trama)

    # Concatena el CRC-32 calculado con la trama original
    trama_con_crc = trama + crc_calculado

    print("Trama con CRC-32:", trama_con_crc)

    # Simulando la recepción de la trama y verificación de errores
    #simulacion(trama)
    

if __name__ == "__main__":
    main()
