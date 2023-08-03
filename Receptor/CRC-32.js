require('slice')
const { string_to_bits } = require('./util.js')

/**
 * Operates xor with a given trama and a polinom
 * @param {Array[int]} trama 
 * @param {Array[int]} polinom 
 */
const trama_xor = (trama, polinom) => trama.map((bit, i) => bit ^ polinom[i])

const get_usable_trama = trama => {
    let usable = []
    let operate = []
    let usable_end = false
    
    for (let i = 0; i < trama.length; i++) {
        if (usable_end) {
            operate.push(trama[i])
            continue
        }
        
        if (trama[i] === 1) {
            usable_end = true
            operate.push(trama[i])
            continue
        }

        usable.push(trama[i])
    }

    return [usable, operate]
}

/**
 * Process recived trama
 * @param {string} trama
 * @param {string} polinom
 */
const process_trama = (trama, polinom) => {
    trama = string_to_bits(trama)
    polinom = string_to_bits(polinom)
    let out_trama = []
    let operate_trama = trama.slice(0, polinom.length)
    trama = trama.slice(polinom.length, trama.length)
    trama = trama.reverse()
    
    while (trama.length > 0) {
        let result = trama_xor(operate_trama, polinom)
        
        if (trama.length === 0){
            out_trama = [...out_trama, ...result]
            continue
        }

        result = get_usable_trama(result)

        out_trama = [...out_trama, ...result[0]]
        operate_trama = result[1]

        while (operate_trama.length < polinom.length) {
            operate_trama.push(trama.pop())
        }

    }

    errors_founded = out_trama.includes(1)
    return errors_founded
}

const crc = (trama, polinom) => {
    const founded_errors = process_trama(trama, polinom)
    if (founded_errors) {
        console.log('> Se encontraron errores en la trama')
        console.log('> La trama se descarta')
    } else {
        console.log('> No se encontraron errores en la trama')
    }
}

// Main
trama = '110101011'
polinom = '1001'
crc(trama, polinom)