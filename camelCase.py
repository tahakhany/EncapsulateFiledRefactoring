class camelCase():

    @staticmethod
    def toCamelCase (string):
        answer = ''
        if len(string == 0): pass
        elif len(string == 1): answer = str.capitalize(string)
        elif len(string>1): answer = str.capitalize(string[0]) + string[1:]
        return answer
