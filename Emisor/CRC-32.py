from functools import reduce
import crcmod.predefined
import util as u

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
    #APLICACION: Solicitar mensaje
    trama = input("Ingrese el texto a enviar: ")
    print("Mensaje a enviar: "+trama)
    print("")
    #PRESENTACION: Codificar mensaje
    nueva_trama = u.char_to_extended_ascii_bits(trama)
    print("La trama en ascii: "+nueva_trama)
    print("")
    
    #ENLACE: Calcular integridad 
    crc_calculado = CRC32(nueva_trama)
    trama_con_crc = nueva_trama + crc_calculado
    print("Trama con CRC-32:", trama_con_crc)
    print("")
    #RUIDO
    trama_final = u.add_ruido(trama_con_crc)
    print("La trama con ruido: "+ trama_final)
    print("")
    # Simulando la recepción de la trama y verificación de errores
    #simulacion(trama)

def layer_implementation(msg_input) -> str:

    # Capa de presentacion (encoding)
    trama = reduce(
        (lambda acc, val: acc + val),
        [u.char_to_extended_ascii_bits(char) for char in msg_input]
    )

    # Capa de Enlace (hamming 7 4 implementation)
    encoded_trama, encoded_print = CRC32(trama)
    
    # Capa de ruido
    trama_ruido, cambios = u.add_ruido(encoded_trama)
    # print('> se hicieron', cambios, 'cambios (ruido)')
    
    return trama_ruido 

if __name__ == "__main__":
    # Code for socket connection below based on https://www.youtube.com/watch?v=nJYp3_X_p6c
    # and the examples seen in class
    import socket
    from pruebas import pruebas
    s = socket.socket()

        
    HOST = "127.0.0.1"  # IP, capa de Red. 127.0.0.1 es localhost
    PORT = 65432        # Puerto, capa de Transporte        
    
    s.connect((HOST, PORT))

    num_exitos = 0
    num_fracasos = 0
    
    print('---- Iniciando pruebas ----')
    for i in range(1000):
        for msg_input in pruebas:
            # Aplicar arquitectura de capas
            # msg_input = input("Ingrese un mensaje a enviar: ")
            trama = layer_implementation(msg_input)

            # Enviar trama por socket
            s.send(trama.encode())
            # print('Trama enviada correctamente')
            response = s.recv(1024).decode('utf-8')
            # print('response: ', response)
            if response == msg_input:
                num_exitos += 1
            else:
                num_fracasos += 1

        if 100 * (i + 1) % 10000 == 0:
            print(f'> {100 * (i + 1)} pruebas realizadas')

    print('\nExitos:', num_exitos)
    print('fracasos:', num_fracasos)
    porcentaje = (num_exitos / 100000) * 100
    porcentaje = round(porcentaje, 2)
    print(f'precision: {porcentaje}%')
    s.close()
    #main()
