from collections import defaultdict
from pdfminer.layout import LTAnno, LTChar


class SymbolToDict:
    def __init__(self, char):
        self.char = char
        self.specific_keys = ['ncs', 'graphicstate']

    def transform(self):
        transformed = defaultdict(type(None))

        if isinstance(self.char, LTChar):
            transformed.update(self.char.__dict__)

            for specific_key in self.specific_keys:

                for key, value in transformed[specific_key].__dict__.items():
                    transformed['.'.join([specific_key, key])] = value

                del transformed[specific_key]

            del transformed['_text']

            transformed['lt_char'] = True
        elif isinstance(self.char, LTAnno):
            transformed['lt_char'] = False
        else:
            transformed = None

        return transformed
