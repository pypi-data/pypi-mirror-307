#!/usr/bin/env python3
"""
Replace hostnames and second-level domains in text using encoding-aware transformations.

This module provides a command-line interface and API to replace hostnames in text, handling various text-compatible encodings
(URL, HTML entity), and preserving the case of the original text. Both the API 

The API consists of the following two functions:
- `create_replacements(host_map, binary=False)`: Returns a replacement table dictionary of compiled regex patterns for use with apply_replacements.
- `apply_replacements(text, replacement_table)`: Returns the input text with the substitutions made by supplied replacement table.

"""

from typing import TypeVar, Union, Dict, Callable
from functools import partial
import sys
import argparse
import json
import urllib.parse
import html
import regex

T = TypeVar('T', str, bytes)

def is_domain_char(c: str) -> bool:
    """Check if a character is valid in a domain name.

    Args:
        c (str): The character to check.

    Returns:
        bool: True if the character is alphanumeric or a hyphen, False otherwise.
    """
    return (c.isalnum() or c == '-') and len(c) == 1

encoding_functions = [
    # No encoding
    ('plain', lambda s: s),

    # Encode all non-alphanumeric characters except hyphens
    ('html_hex', lambda s: ''.join(f'&#x{ord(c):x};' if not is_domain_char(c) else c for c in s)),
    ('html_numeric', lambda s: ''.join(f'&#{ord(c)};' if not is_domain_char(c) else c for c in s)),
    ('url', lambda s: ''.join(f'%{ord(c):02x}' if not is_domain_char(c) else c for c in s)),

    # Encode all non-alphanumeric characters, including hyphens
    ('html_hex_not_alphanum', lambda s: ''.join(f'&#x{ord(c):x};' if not c.isalnum() else c for c in s)),
    ('html_numeric_not_alphanum', lambda s: ''.join(f'&#{ord(c)};' if not c.isalnum() else c for c in s)),
    ('url_not_alphanum', lambda s: ''.join(f'%{ord(c):02x}' if not c.isalnum() else c for c in s)),

    # Encode all characters
    ('html_hex_all', lambda s: ''.join(f'&#x{ord(c):x};' for c in s)),
    ('html_numeric_all', lambda s: ''.join(f'&#{ord(c)};' for c in s)),
    ('url_all', lambda s: ''.join(f'%{ord(c):02x}' for c in s))
]

def generate_character_pattern(input_char: str, encoding_func: Callable) -> str:
    """
    Generate a regex pattern that matches the encoded character c in both its
    upper and lowercase forms when used with IGNORECASE. Note that we are not
    explicity matching both unencoded cases, nor the possibly uppercase 'x' in
    HTML hex entity encoding, so IGNORECASE is mandatory.

    Args:
        input_char (str): The character to generate the pattern for.

    Returns:
        str: A regex pattern string.
    """

    c_lower = input_char.lower()
    c_upper = input_char.upper()

    if c_lower == c_upper:
        patterns = [
            regex.escape(encoding_func(input_char)),
        ]
    else:
        patterns = [
            f"{c_lower}",
            f"(?:{encoding_func(c_lower)}|{encoding_func(c_upper)})"
        ]

    return "(?:" + "|".join(patterns) + ")"

def generate_domain_pattern(domain: str, encoding_func: Callable) -> str:
    """
    Generate a regex pattern that matches the domain in all possible encoded forms.

    Args:
        domain (str): The domain to generate the pattern for.

    Returns:
        str: A regex pattern string.
    """
    # Split the domain into characters
    # Join the parts to form the full pattern
    return "".join([generate_character_pattern(c, encoding_func) for c in domain])

ALPHANUMERIC_HEX_CODES = "(4[1-9a-f]|5[0-9a]|6[1-9a-f]|7[0-9a]|3[0-9])"
ALPHANUMERIC_PLUS_DOT_HEX_CODES = f"(2e|{ALPHANUMERIC_HEX_CODES})"

ALPHANUMERIC_DECIMAL_CODES = "(4[89]|5[0-7]|6[5-9]|([78][0-9])|9[0,7-9]|1[01][0-9]|12[012])"
ALPHANUMERIC_PLUS_DOT_DECIMAL_CODES = "(4[689]|5[0-7]|6[5-9]|([78][0-9])|9[0,7-9]|1[01][0-9]|12[012])"

HTML_HEX_ENCODED_ALPHANUMERIC = rf"(&\#x{ALPHANUMERIC_HEX_CODES};)"

HTML_DECIMAL_ENCODED_ALPHANUMERIC = rf"(&\#{ALPHANUMERIC_DECIMAL_CODES};)"
URL_ENCODED_ALPHANUMERIC = rf"(%{ALPHANUMERIC_HEX_CODES})"

HTML_ENCODED_ALPHANUMERIC = f"""
(
    {HTML_HEX_ENCODED_ALPHANUMERIC}
|
    {HTML_DECIMAL_ENCODED_ALPHANUMERIC}
)
"""

ANY_ALPHANUMERIC = f"""
(
    [a-z0-9]
|
    {URL_ENCODED_ALPHANUMERIC}
|
    {HTML_ENCODED_ALPHANUMERIC}
)
"""

DOT = r"(\.|(%2e)|(&\#x2e;)|(&\#46;))"
HYPHEN = r"(-|(%2d)|(&\#x2d;)|(&\#45;))"

LEFT_SIDE = rf"""
# Look for any of...
(?<=
    (
        ^                                                               # ...the beginning of the string or line
    |
        [^a-z0-9\.;]                                                    # ...any character that's not alphanumeric, a dot, or a semicolon.
                                                                        #    Note that this includes hyphens, so apply an exclusion condition below
    |
        %(?!{ALPHANUMERIC_PLUS_DOT_HEX_CODES})[0-9a-f]{{2}}             # ...a URL-encoded character that's not alphanumeric or dot
    |
        {DOT}{{2,}}                                                     # ...two or more dots, since, e.g., "a...example.com" is not a subdomain of example.com
    |
        (?<=
            (?<!
                (&\#x({ALPHANUMERIC_PLUS_DOT_HEX_CODES}))
            |
                (&\#({ALPHANUMERIC_PLUS_DOT_DECIMAL_CODES}))
            )
        ;                                                               # ...a semicolon when not preceded by HTML-encoded alphanumeric or dot
        )
    ){DOT}?                                                         # Optional dot after any of the above
)
(?<!{ANY_ALPHANUMERIC}{HYPHEN}+)                                # Exclusion condition
"""

RIGHT_SIDE = rf"""
(?!
    (?=
        ({HYPHEN}|{DOT})?
        {ANY_ALPHANUMERIC}
    )
)
"""

# TODO: merge the two?
def decode_hostname(s: T) -> T:
    """Decodes URL-encoded and HTML-encoded sequences in a hostname string."""
    #if isinstance(s, bytes):

    # Decode HTML entities
    s = html.unescape(s)
    # Decode URL-encoded sequences
    s = urllib.parse.unquote(s)
    return s

def decode_hostname_bytes(b: bytes) -> bytes:
    """Decodes URL-encoded and HTML-encoded sequences in a hostname bytes object."""
    # Decode HTML entities
    s = b.decode('utf-8', errors='ignore')
    s = html.unescape(s)
    # Decode URL-encoded sequences
    s = urllib.parse.unquote(s)
    return s.encode('utf-8')

def adjust_encoded_sequences_case(s: str, uppercase: bool) -> str:
    """Adjusts the case of encoded sequences in the replacement string."""
    def replace_match(m):
        return m.group().upper() if uppercase else m.group().lower()
    # Adjust URL-encoded sequences
    s = regex.sub(r'%[0-9a-fA-F]{2}', replace_match, s)
    # Adjust HTML numeric entities
    s = regex.sub(r'&\#x?[0-9a-fA-F]+;', replace_match, s)
    return s

def adjust_encoded_sequences_case_bytes(b: bytes, uppercase: bool) -> bytes:
    """Adjusts the case of encoded sequences in the replacement bytes."""
    def replace_match(m):
        return m.group().upper() if uppercase else m.group().lower()
    # Adjust URL-encoded sequences
    b = regex.sub(b'%[0-9a-fA-F]{2}', replace_match, b)
    # Adjust HTML numeric entities
    b = regex.sub(b'&\\#x?[0-9a-fA-F]+;', replace_match, b)
    return b

def case_preserving_replace(m: regex.Match, replacement: T) -> T:
    """Returns the replacement string or bytes with any uppercasing in the
    original regex.Match object positionally applied. Does not convert
    uppercase letters in the replacement string to lowercase. Any characters in
    the replacement beyond the length of the regex.Match will be unchanged."""

    original = m.group()
    is_upper = False
    has_upper_encoded = False

    if isinstance(original, str) and isinstance(replacement, str):
        # Decode the original hostname
        decoded_original = decode_hostname(original)
        # Check if any character in the decoded original is uppercase
        if any(c.isupper() for c in decoded_original):
            is_upper = True

        # Check if any encoded sequences in the original are uppercase
        if regex.search(r'%[0-9A-F]{2}', original) or regex.search(r'&\#x?[0-9A-F]+;', original):
            has_upper_encoded = True

        # Adjust the replacement case
        replacement = replacement.upper() if is_upper else replacement.lower()

        # Adjust the case of encoded sequences in the replacement
        replacement = adjust_encoded_sequences_case(replacement, has_upper_encoded)

        return replacement

    if isinstance(original, bytes) and isinstance(replacement, bytes):
        # Decode the original hostname
        decoded_original = decode_hostname_bytes(original)
        # Check if any character in the decoded original is uppercase
        if any(65 <= b <= 90 for b in decoded_original):  # ASCII 'A' to 'Z'
            is_upper = True

        # Check if any encoded sequences in the original are uppercase
        if regex.search(b'%[0-9A-F]{2}', original) or regex.search(b'&\\#x?[0-9A-F]+;', original):
            has_upper_encoded = True

        # Adjust the replacement case
        replacement = replacement.upper() if is_upper else replacement.lower()

        # Adjust the case of encoded sequences in the replacement
        replacement = adjust_encoded_sequences_case_bytes(replacement, has_upper_encoded)

        return replacement

    raise TypeError("Both original and replacement must be of the same type (both str or both bytes).")

def apply_replacements(text: T, replacements_table: dict[regex.Pattern, T]) -> T:
    """Applies the supplied regex replacements table to the input text.

    Args:
        text: The input text (str or bytes) to process.
        replacements_table: A dictionary mapping compiled regex patterns to their replacement strings or bytes.

    Returns:
        The text after all replacements have been applied.
    """

    for p, r in replacements_table.items():
        text = p.sub(partial(case_preserving_replace, replacement=r), text)
    return text

def create_replacements(host_map: Dict[str,str], binary: bool=False) -> Dict[regex.Pattern, Union[str, bytes]]:
    """Create compiled regex patterns for replacing hostnames.

    Expands the host_map using the encodings defined in encoding_functions.
    The host_map must be a dict of UTF-8 strings, but the resulting dict values
    will be byte arrays if binary is True.

    Args:
        host_map (Dict[str, str]): A mapping of original hostnames to replacement hostnames.
        binary (bool, optional): Whether to treat the patterns and replacements as binary data.
            Defaults to False.

    Returns:
        Dict[regex.Pattern, Union[str, bytes]]: A dictionary of compiled regex patterns mapped to their replacements.
    """

    pattern_replacements: dict[regex.Pattern, str | bytes] = {}

    for original_domain, new_domain in host_map.items():
        for _, encode_fn in encoding_functions:
            #encoded_original_domain = encode_fn(original_domain)

            encoded_original_domain = generate_domain_pattern(original_domain, encode_fn)

            encoded_new_domain = encode_fn(new_domain)

            pattern_str = rf"""
{LEFT_SIDE}
    (?:encoded_original_domain)
{RIGHT_SIDE}
"""
    #{regex.escape(encoded_original_domain)}
            pattern: Union[regex.Pattern[str], regex.Pattern[bytes]]

            if binary:
                encoded_new_domain = encoded_new_domain.encode("utf-8")
                pattern = regex.compile(pattern_str.encode("utf-8"), flags=regex.I | regex.M | regex.X)
            else:
                pattern = regex.compile(pattern_str, flags=regex.I | regex.M | regex.X)

            # If we replace an encoded domain that does not have hyphens in it with one that does,
            # then should we encode the resulting hyphens? This ambiguity results in a one-to-many mapping.
            #
            # We resolve this by preferring the more encoded result.
            if pattern in pattern_replacements:
                if is_more_encoded(encoded_new_domain, pattern_replacements[pattern]):
                    pattern_replacements[pattern] = encoded_new_domain
            else:
                pattern_replacements[pattern] = encoded_new_domain
    return pattern_replacements

def is_more_encoded(value_a: T, value_b: T) -> bool:
    """Returns True if value_a is more encoded than value_b under either URL or
    HTML entity encoding."""

    if isinstance(value_a, bytes) and isinstance(value_b, bytes):
        ctrs = (b"%", b"&#")
    elif isinstance(value_a, str) and isinstance(value_b, str):
        ctrs = ("%", "&#")
    else:
        raise TypeError("Parameters must be of the same type (both str or both bytes).")

    return value_a.count(ctrs[0]) > value_b.count(ctrs[0]) or value_a.count(ctrs[1]) > value_b.count(ctrs[1])

def main():
    """Entry point for command-line invocation."""
    parser = argparse.ArgumentParser(description="Replace hostnames in the input file based on a provided host mapping.")

    parser.add_argument(
        "-i", "--input", type=str, default="-",
        help="Input text file to read from. Default: %(default)s (stdin)"
    )

    parser.add_argument(
        "-o", "--output", type=str, default=None,
        help="Output file to write the replaced content. If not provided, write to stdout"
    )

    parser.add_argument(
        "-m", "--mapping", type=str, required=True,
        help='JSON file that contains the host mapping dictionary (e.g. {"web.example.com": "www.example.net"})'
    )

    parser.add_argument(
        "-b", "--binary", action="store_true",
        help="Set this flag to treat the input and output as binary (default is UTF-8 string)"
    )

    args = parser.parse_args()

    if args.input == '-':
        input_text = sys.stdin.buffer.read() if args.binary else sys.stdin.read()

    else:
        with open(args.input, "rb" if args.binary else "r", encoding=None if args.binary else "utf-8") as infile:
            input_text = infile.read()

    with open(args.mapping, "r", encoding="utf-8") as mapping_file:
        host_map = json.load(mapping_file)

    replacements = create_replacements(host_map, binary=args.binary)
    output_text = apply_replacements(input_text, replacements)

    if args.output:
        with open(args.output, mode="wb" if args.binary else "w", encoding=None if args.binary else "utf-8") as outfile:
            outfile.write(output_text)
    else:
        if args.binary:
            sys.stdout.buffer.write(output_text)
        else:
            print(output_text, end="")

if __name__ == '__main__':
    main()
