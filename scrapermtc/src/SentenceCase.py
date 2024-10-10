# attribution: https://stackoverflow.com/a/71775403

def GetSentenceCase(source):
    output = ""
    isFirstWord = True

    for c in source:
        if isFirstWord and not c.isspace():
            c = c.upper()
            isFirstWord = False
        elif not isFirstWord and c in ".!?":
            isFirstWord = True
        else:
            c = c.lower()

        output = output + c

    return output