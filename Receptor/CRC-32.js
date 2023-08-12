const { string_to_bits, print, binaryToString } = require('./util.js')


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
    tramaBlocks = trama.split(' ');
    polinom = tramaBlocks[tramaBlocks.length - 1];

    trama = string_to_bits(trama)
    polinom = string_to_bits(polinom)
    let out_trama = []
    let operate_trama = trama.slice(0, polinom.length)
    trama = trama.slice(polinom.length, trama.length)
    trama = trama.reverse()

    if (trama.length == 0) {
        out_trama = trama_xor(operate_trama, polinom)
    }
    
    while (trama.length > 0) {
        let result = trama_xor(operate_trama, polinom)
        
        if (trama.length === 0){
            out_trama = [...out_trama, ...result]
            continue
        }

        result = get_usable_trama(result)
        if (result[0].length === 0){
            return true
        }

        out_trama = [...out_trama, ...result[0]]
        operate_trama = result[1]

        if (trama.length + operate_trama.length < polinom.length) {
            out_trama = [...out_trama, ...trama]
            trama = []
        }

        while (operate_trama.length < polinom.length && trama.length > 0) {
            operate_trama.push(trama.pop())
        }

    }

    errors_founded = out_trama.includes(1)
    // console.log(out_trama)
    return errors_founded
}

const crc = (trama, polinom) => {
    // console.log('Trama inicial:', trama)
    const founded_errors = process_trama(trama, polinom)
    if (founded_errors) {
        // console.log('> Se encontraron errores en la trama')
        // console.log('> La trama se descarta')
        return '0'
    } else {
        // console.log('> No se encontraron errores en la trama')
        return '1'
    }
}

// Code below based on https://www.youtube.com/watch?v=LFU7gJAOegA
var net = require('net')
const HOST = "127.0.0.1"  // IP, capa de Red. 127.0.0.1 es localhost
const PORT = 65432        // Puerto, capa de Transporte        

const server = net.createServer()

server.listen(PORT, () => {
    print(`server listening on port ${server.address().port}`)
})

server.on('connection', socket => {
    print('> conexion a socket iniciada')
    socket.on('data', data => {
        // print(`trama recibida: ${data}`)
        // print(`trama recibida: ${data.toString()}`)
        let trama =  data.toString()
        const tramaBlocks = trama.split(' ');
        const polinom = tramaBlocks[tramaBlocks.length - 1];
        // const polinom = "100000100110000010001110110110111";

        trama = trama.replace(' ', '')
        trama = trama.replace(' ', '')
        trama = trama.replace(' ', '')
        // Capa de enlace: verificar integridad 
        let result = crc(trama,polinom)
        // Capa de presentacion: Imprimir mensaje y devolver resultado
        // console.log('recibido: ', chars)
        socket.write(result)
    })

    socket.on('close', () => {
        print('> Comunicacion finalizada')
    })
    
    socket.on('error', err => {
        print(err.message)
    })
})