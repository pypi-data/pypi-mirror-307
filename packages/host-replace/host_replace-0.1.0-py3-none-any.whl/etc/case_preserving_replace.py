def case_preserving_replace(m: regex.Match, replacement: T) -> T:
    """Returns the replacement string or bytes with any uppercasing in the
    original regex.Match object positionally applied. Does not convert
    uppercase letters in the replacement string to lowercase. Any characters in
    the replacement beyond the length of the regex.Match will be unchanged."""

    original = m.group()

    if isinstance(original, str) and isinstance(replacement, str):
            
        result_chars = [r.upper() if o.isupper() else r for o, r in zip(original, replacement)]
        result_chars.extend(replacement[len(original):])
        return ''.join(result_chars)

    if isinstance(original, bytes) and isinstance(replacement, bytes):
        result_bytes = bytearray()
        for o_byte, r_byte in zip(original, replacement):
            if 65 <= o_byte <= 90:  # ASCII 'A' to 'Z'
                if 97 <= r_byte <= 122:  # ASCII 'a' to 'z'
                    result_bytes.append(r_byte - 32)
                else:
                    result_bytes.append(r_byte)
            else:
                result_bytes.append(r_byte)
        result_bytes.extend(replacement[len(original):])
        return result_bytes

    raise TypeError("Both original and replacement must be of the same type (both str or both bytes).")
