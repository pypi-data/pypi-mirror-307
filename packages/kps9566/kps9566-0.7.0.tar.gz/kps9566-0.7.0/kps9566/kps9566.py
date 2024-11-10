from .kps9566_mapping import kps9566_mapping
from .replace_map import replace_map
import codecs

def kps9566_encode(input, errors='strict'):
    output = bytearray()
    for char in input:
        if ord(char) < 0x80:
            output.append(ord(char))
        elif char in kps9566_mapping:
            output.extend(kps9566_mapping[char])
        elif char in replace_map:
            output.extend(replace_map[char])
        else:
            raise UnicodeEncodeError("kps9566", char, -1, -1, "character not in mapping")
    return bytes(output), len(input)

def kps9566_decode(input, errors='strict'):
    output = []
    i = 0
    while i < len(input):
        if input[i] < 0x80:
            output.append(chr(input[i]))
            i += 1
        else:
            byte_pair = input[i:i+2]
            for char, byte_seq in kps9566_mapping.items():
                if byte_seq == byte_pair:
                    output.append(char)
                    break
            else:
                raise UnicodeDecodeError("kps9566", input, i, i+2, "byte sequence not in mapping")
            i += 2
    return ''.join(output), len(input)

class KPS9566IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        output = bytearray()
        for char in input:
            if ord(char) < 0x80:
                output.append(ord(char))
            elif char in kps9566_mapping:
                output.extend(kps9566_mapping[char])
            elif char in replace_map:
                output.extend(replace_map[char])
            else:
                raise UnicodeEncodeError("kps9566", char, -1, -1, "character not in mapping")
        return bytes(output)

class KPS9566IncrementalDecoder(codecs.IncrementalDecoder):
    def __init__(self, errors='strict'):
        super().__init__(errors)
        self.buffer = b''

    def decode(self, input, final=False):
        self.buffer += input
        output = []
        i = 0
        while i < len(self.buffer):
            if self.buffer[i] < 0x80:
                output.append(chr(self.buffer[i]))
                i += 1
            elif i + 1 < len(self.buffer):
                byte_pair = self.buffer[i:i+2]
                for char, byte_seq in kps9566_mapping.items():
                    if byte_seq == byte_pair:
                        output.append(char)
                        break
                else:
                    if final:
                        raise UnicodeDecodeError("kps9566", self.buffer, i, i+2, "byte sequence not in mapping")
                    return ''.join(output)
                i += 2
            else:
                break
        self.buffer = self.buffer[i:]
        return ''.join(output)

class KPS9566StreamReader(codecs.StreamReader):
    def decode(self, input, errors='strict'):
        return kps9566_decode(input, errors)

class KPS9566StreamWriter(codecs.StreamWriter):
    def encode(self, input, errors='strict'):
        return kps9566_encode(input, errors)
def getregentry():
    return codecs.CodecInfo(
        name='kps9566',
        encode=kps9566_encode,
        decode=kps9566_decode,
        streamreader=KPS9566StreamReader,
        streamwriter=KPS9566StreamWriter,
        incrementalencoder=KPS9566IncrementalEncoder,
        incrementaldecoder=KPS9566IncrementalDecoder,
    )


def kps9566_search_function(encoding):
    if encoding.upper() == 'KPS9566' or encoding == 'KPS-9566' or encoding == 'KPS_9566' or encoding == 'KPS 9566':
        return getregentry()
    return None

def register():
    codecs.register(kps9566_search_function)
