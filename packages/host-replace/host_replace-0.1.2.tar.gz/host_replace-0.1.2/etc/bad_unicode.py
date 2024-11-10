        bad_unicode = (
            b"\xe0\x80\x80",      # U+0800   - U+0FFF
            b"\xed\xbf\xbf",      # U+D000   - U+D7FF
            b"\xf0\x80\x80\x80",  # U+10000  - U+3FFFF
            b"\xf4\xbf\xbf\xbf",  # U+100000 - U+10FFFF
            b"\x80",                
            b"\xf5\x80\x80\x80",
            b"\xc2",
            b"\xe1\x80",
            b"\xf0\x90\x80",
            b"\xc1\x80"
        )

        bad_unicode = (
            b"\xe0\x80\x80",       # Overlong encoding for U+0800
            b"\xf0\x80\x80\x80",   # Overlong encoding for U+10000
            b"\xed\xa0\x80",       # Surrogate code point U+D800
            b"\xf4\x90\x80\x80",   # U+110000 (outside valid range)
            b"\x80",               # Single continuation byte
            b"\xbf",               # Another single continuation byte
            b"\xf5\x80\x80\x80",   # Invalid start byte (byte above 0xF4)
            b"\xf8\x88\x80\x80",   # Invalid start byte (UTF-8 allows only up to 4 bytes)
            b"\xc2",               # Incomplete 2-byte sequence
            b"\xe1\x80",           # Incomplete 3-byte sequence
            b"\xf0\x90\x80",       # Incomplete 4-byte sequence
            b"\xc1\x80",           # Overlong encoding for U+0000
        )

        for bad in bad_unicode:
            try:
                bad.decode("utf-8")
            except UnicodeDecodeError as e:
                print(e.args[1], e.args[4])
                #print(e)
