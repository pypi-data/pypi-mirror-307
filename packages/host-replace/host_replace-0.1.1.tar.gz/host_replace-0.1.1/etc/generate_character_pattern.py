def generate_character_pattern(input_char: str, encoding_func: Callable) -> str:
    """
    Generate a regex pattern that matches the character c in all its possible
    encoded forms when used with IGNORECASE. Note that we are not explicity
    matching both unencoded cases, nor the possibly uppercase 'x' in HTML hex
    entity encoding, so IGNORECASE is mandatory.

    Args:
        input_char (str): The character to generate the pattern for.

    Returns:
        str: A regex pattern string.
    """

    c_lower = input_char.lower()
    c_upper = input_char.upper()

    print(encoding_func(c_lower))

    if c_lower == c_upper:
        patterns = [
            regex.escape(encoding_func(input_char)),
        ]
    else:
        patterns = [
            f"{c_lower}",
            f"(?:{encoding_func(c_lower)}|{encoding_func(c_upper)})"
        ]
        # All of them
        #patterns = [
        #    f"{c_lower}",
        #    f"%(?:{ord(c_lower):02x}|{ord(c_upper):02x})",
        #    f"&#x(?:{ord(c_lower):02x}|{ord(c_upper):02x});",
        #    f"&#(?:{ord(c_lower)}|{ord(c_upper)});"
        #]
    return "(?:" + "|".join(patterns) + ")"
