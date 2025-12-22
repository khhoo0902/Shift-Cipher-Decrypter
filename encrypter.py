def classifyChar(char):
    if 65 <= ord(char) <= 90:
        return 1
    elif 97 <= ord(char) <= 122:
        return 0
    else: return -1

def shiftChar(char, type, shift):
    head = 65 if type else 97
    return chr((ord(char) - head + shift) % 26 + head)

def encrypt(text, shift, lettercase):
    chars = list(text if lettercase == "Adaptive" else text.upper() if lettercase == "Uppercase" else text.lower())
    charType = [classifyChar(char) for char in chars]
    encryptedText = ""
    for char, type in zip(chars, charType):
        if type == -1:
            encryptedText += char
        else:
            encryptedText += shiftChar(char, type, shift)
    return encryptedText