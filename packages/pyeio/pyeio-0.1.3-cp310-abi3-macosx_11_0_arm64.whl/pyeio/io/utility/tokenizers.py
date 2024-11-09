import re

# todo: need to implement tokenizer that can handle generator for dynamic tokenization


class Tokenizer:
    def __init__(self, patterns, require_match: bool):
        # patterns should be a list of tuples in the format (token_type, pattern)
        self.patterns = [
            (token_type, re.compile(pattern)) for token_type, pattern in patterns
        ]
        self.require_match = require_match

    def tokenize(self, text):
        tokens = []
        pos = 0

        while pos < len(text):
            match = None
            for token_type, pattern in self.patterns:
                match = pattern.match(text, pos)
                if match:
                    token_text = match.group(0)
                    tokens.append((token_type, token_text))
                    pos = match.end()  # Move past the matched token
                    break
            if (not match) and (self.require_match):
                raise ValueError(f"Unexpected character at position {pos}: {text[pos]}")
            else:
                pos += 1

        return tokens
