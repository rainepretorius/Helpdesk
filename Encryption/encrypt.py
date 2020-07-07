decrypt_dict = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j', 11: 'k', 12: 'l',
                13: 'm', 14: 'n', 15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 's', 20: 't', 21: 'u', 22: 'v', 23: 'w',
                24: 'x', 25: 'y', 26: 'z', 27: ' ', 28: '.', 29: '!', 30: ',', 31: '$', 32: '%', 33: '?', 34: '#',
                35: '9', 36: '8', 37: '7', 38: '6', 39: '5', 40: '4', 41: '3', 42: '2', 43: '1', 44: '0', 45: '\n',
                46: ':', 47: 'ã', 48: '¯', 49: 'â', 50: '€', 51: '˜', 52: 'ª', 53: '«', 54: '(', 55: ')', 56: '@',
                57: '<', 58: '>', 59: '^', 60: '&', 61: '*', 62: '+', 63: '=', 64: '/', 65: ';', 66: '|', 67: 'A', 68:
                    'B', 69: 'C', 70: 'D', 71: 'E', 72: 'F', 73: 'G', 74: 'H', 75: 'I', 76: 'J', 77: 'K', 78: 'L', 79: 'M',
                80: 'N', 81: 'O', 82: 'P', 83: 'Q', 84: 'R', 85: 'S', 86: 'T', 87: 'U', 88: 'V', 89: 'W', 90: 'X', 91: 'Y',
                92: 'Z'}

encrypt_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12,
                'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23,
                'x': 24, 'y': 25, 'z': 26, ' ': 27, '.': 28, '!': 29, ',': 30, '$': 31, '%': 32, '?': 33, "#": 34,
                '9': 35, '8': 36, '7': 37, '6': 38, '5': 39, '4': 40, '3': 41, '2': 42, '1': 43, '0': 44, '\n': 45,
                ':': 46, 'ã': 47, '¯': 48, 'â': 49, '€': 50, '˜': 51, 'ª': 52, '«': 53, '(': 54, ')': 55, '@': 56,
                '<': 57, '>': 58, '^': 59, '&': 60, '*': 61, '+': 62, '=': 63, '/': 64, ';': 65, '|': 66, 'A': 67, 'B':
                    68, 'C': 69, 'D': 70, 'E': 71, 'F': 72, 'G': 73, 'H': 74, 'I': 75, 'J': 76, 'K': 77, 'L': 78, 'M': 79,
                'N': 80, 'O': 81, 'P': 82, 'Q': 83, 'R': 84, 'S': 85, 'T': 86, 'U': 87, 'V': 88, 'W': 89, 'X': 90, 'Y':91,
                'Z': 92}

encryptedlist = []
decrypted = ''
decrypted_list = []
cypher = 4437790616319334326928


def encrypt(input):
    global encrypt_dict
    global encryptedlist
    global cypher
    encryptedlist = []
    for zyx in input:
        encryptedlist.append(str((encrypt_dict[zyx]) * cypher))
        encryptedpassword = ', '.join(encryptedlist)
    return encryptedpassword


def decrypt(decrypt):
    global decrypt_dict
    global decrypted_list
    global cypher
    decrypted_list = []
    decrypt = str(decrypt).replace("[('", "").replace("',)]", "").replace(" ", "")
    decrypt = decrypt.split(',')
    for item in decrypt:
        if item == '[' or item == ']' or item ==",":
            z = 5
        else:
            num = int(item)
            key = num / cypher
            decrypted_list.append(decrypt_dict[key])
            passworddecrypted = ''.join(decrypted_list)
    return passworddecrypted

