

class Parser:
    def __init__(self):
        pass

    # Helper function to remove spaces and comments
    def clean(self, code):
        res = []
        for line in code.split('\n'):
            line = line.split('//')[0].strip()
            if len(line) > 0:
                res.append(line)
        return res

    def parse(self, code):
        codelist = self.clean(code)
        return codelist
