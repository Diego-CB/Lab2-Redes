/**
 * Converst string to array of ints
 * @param {string} trama
 * @returns the trama in an array of ints
 */
const string_to_bits = trama => {
    trama = trama.split('')
    trama = trama.map(char => parseInt(char))
    return trama
}

const print = o => console.log(o)

const binaryToString = binaryString => {
    let result = '';

    // Divide la cadena de bits en grupos de 8 bits
    for (let i = 0; i < binaryString.length; i += 8) {
        const byte = binaryString.substr(i, 8); // Obtén un byte (8 bits)
        
        // Convierte el byte en un número entero
        const asciiCode = parseInt(byte, 2);
        
        // Convierte el código ASCII en un caracter y agrégalo al resultado
        result += String.fromCharCode(asciiCode);
    }

    return result;
}

module.exports = {
    string_to_bits,
    print,
    binaryToString
}