const { string_to_bits } = require('./util')

P0_LIST = [1, 3, 5, 7]
P1_LIST = [2, 3, 6, 7]
P2_LIST = [4, 5, 6, 7]

const get_parity = (trama, list) => {
    const subtrama = list.map(index => trama[index-1])
    const bit = subtrama.filter(b => b == 1).length % 2 == 0
    return bit ? 0 : 1
}

const hamming = trama => {
    // pre-process trama
    console.log('Trama inicial:', trama)
    trama = string_to_bits(trama)
    trama = trama.reverse()

    // Get parity bits
    const bit1 = get_parity(trama, P0_LIST)
    const bit2 = get_parity(trama, P1_LIST)
    const bit3 = get_parity(trama, P2_LIST)

    // convert to decimal
    const dirty_bit = parseInt(bit1.toString() + bit2.toString() + bit3.toString(), 2)
    
    if (dirty_bit > 0) {
        // Error Correction
        trama[dirty_bit - 1] = (trama[dirty_bit - 1] === 1) ? 0 : 1
        trama = trama.reduce((acc, bit) =>  bit.toString() + acc, '')

        // Print
        console.log('Se encontraron errores en el bit:', dirty_bit)
        console.log('Trama correcta:', trama)
    } else {
        console.log('No se encontraron errores en la trama')
    }
}

trama = '1001100'
trama = '1011100'
trama = '0110001'
trama = '1000110'
trama = '1000110'
trama = '0110001'
result = hamming(trama)
