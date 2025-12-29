def classifyChar(char):
    if 65 <= ord(char) <= 90:
        return 1
    elif 97 <= ord(char) <= 122:
        return 0
    else: return -1

def reverseShiftChar(char, type, shift):
    originalAscii = ord(char) - shift
    return chr(originalAscii + 26 if originalAscii < (65 if type else 97) else originalAscii)

def reverseShiftText(text, shift, lettercase):
    chars = list(text if lettercase == "Adaptive" else text.upper() if lettercase == "Uppercase" else text.lower())
    types = [classifyChar(char) for char in chars]
    shiftedText = ""
    for char, type in zip(chars, types):
        if type == -1:
            shiftedText += char
        else:
            shiftedText += reverseShiftChar(char, type, shift)
    return shiftedText

def findLetterMode(letters):
    distinctLetters = list(set(letters))
    letterCounter = [letters.count(letter) for letter in distinctLetters]
    return distinctLetters[letterCounter.index(max(letterCounter))]

ALPHABET = [chr(i) for i in range(65, 91)]
def arrangeLetter(letters):
    return sorted(ALPHABET, key=lambda x: letters.count(x), reverse=True)

def getFirstLetter(text):
    return [word[0] for word in text.upper().split() if word[0] in ALPHABET]

LETTER_ARR = ['E', 'A', 'N', 'L', 'Z']
FIRST_LETTER_ARR = ['T', 'A', 'W', 'F', 'Z']
def calculateConfidence(letterArr, firstLetterArr):
    index1 = [letterArr.index(letter) for letter in LETTER_ARR]
    index2 = [firstLetterArr.index(letter) for letter in FIRST_LETTER_ARR]
    passedCases = [index1[i + 1] <= index1[i + 2]for i in range(len(index1) - 2)] + [index2[i] <= index2[i + 1]for i in range(len(index2) - 1)]
    return passedCases.count(True) / (len(LETTER_ARR + FIRST_LETTER_ARR) - 3) * 100

def guessShift(text, lettercase):
    chars = list(text.upper())
    types = [classifyChar(char) for char in chars]
    letters = [char for char, type in zip(chars, types) if type != -1]
    mode = findLetterMode(letters)
    shift = ord(mode) - ord('E')
    if shift < 0: shift += 26
    getFirstLetter(text)
    letterArr = arrangeLetter([reverseShiftChar(letter, 1, shift) for letter in letters])
    firstLetterArr = arrangeLetter([reverseShiftChar(letter, 1, shift) for letter in getFirstLetter(text)])
    confidence = calculateConfidence(letterArr, firstLetterArr)
    return mode, shift, confidence, reverseShiftText(text, shift, lettercase)

def extractWords(text):
    words = []
    for phrase in text.upper().split():
        word = ""
        for char in phrase:
            if char in ALPHABET:
                word += char
        if word != "":
            words.append(word)
    return words

def matchKeywords(text, keywords, lettercase):
    keywords = [keyword.upper() for keyword in keywords]
    matchedKeywordsCounter = []
    for shift in range(26):
        words = extractWords(reverseShiftText(text, shift, "Uppercase"))
        matchedKeywordsCounter.append(sum([words.count(keyword) for keyword in keywords]))
    maxPossibleShift = matchedKeywordsCounter.index(max(matchedKeywordsCounter))
    nonZeroCounter = [n for n in matchedKeywordsCounter if n > 0]
    if nonZeroCounter == []:
        nonZeroCounter = [0]
        confidence = 0
    else: confidence = max(nonZeroCounter) / sum(nonZeroCounter) * 100
    return maxPossibleShift, confidence, max(nonZeroCounter), reverseShiftText(text, maxPossibleShift, lettercase)