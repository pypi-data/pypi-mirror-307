import ast
import re
import codecs
import token
import tokenize
from io import StringIO, BytesIO


def _codec_factory(transforms, coding, args):

    def transformer(tokens):
        t_prev = next(tokens)
        for t in tokens:
            if (t.type == token.STRING and
                t_prev.type == token.NAME and
                t_prev.string in transforms.keys() and
                t_prev.start[1] + len(t_prev.string) == t.start[1]):

                orig_str = ast.literal_eval(t.string)
                raw_str = transforms[t_prev.string](orig_str, *args)
                new_str = repr(raw_str)
                new_start = (t.start[0], t.start[1]-1)
                new_t = tokenize.TokenInfo(t.type, new_str, new_start, t.end, t.line)
                t = new_t
            else:
                yield t_prev
            t_prev = t

        yield t_prev

    def transform(text):
        tokens = tokenize.generate_tokens(StringIO(text).readline)
        transformed = tokenize.untokenize(transformer(tokens))
        return transformed

    def encode(inp):
        enc = codecs.getencoder('utf8')
        payload, length = enc(inp)
        return (payload, length)

    def decode(inp):
        dec = codecs.getdecoder('utf8')
        text, length = dec(inp)
        text = transform(text)
        return (text, length)

    return encode, decode


def _search_function_factory(transforms, coding):
    coding_re = re.compile('^' + coding + '$')

    def search_function(coding):
        if m := coding_re.match(coding):
            encode, decode = _codec_factory(transforms, coding, m.groups())
            return codecs.CodecInfo(encode, decode)

    return search_function


def register(transforms, coding='x_strings'):
    search_function = _search_function_factory(transforms, coding)
    codecs.register(search_function)
