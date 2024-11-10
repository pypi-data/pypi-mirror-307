#!/usr/bin/env python3

import unittest
import logging
import string
import re
from host_replace import create_replacements, apply_replacements, encoding_functions, HYPHEN

#logging.basicConfig(level=logging.DEBUG)

class TestHostnameReplacement(unittest.TestCase):
    alphanumerics = tuple(string.ascii_letters + string.digits)

    hyphen = re.compile(HYPHEN)
    b_hyphen = re.compile(HYPHEN.encode("utf-8"))

    # These should act as delimiters, allowing the host to be replaced
    prefixes = ("",
                "https://",
                "href='",
                'href="',
                'b"',
                "b'",
                '=',
                '.',    # We don't want to match "undefined.example.com" for "example.com", but we do want to match, e.g., "=.example.com"
                '`',
                ".",
                " .",
                "=.",
                "-",    # A hyphen not preceded by a domain character is not a valid domain
                "%",    # A "%" prefix is ambiguous and will cause failures for domains beginning with hex codes
                "-.",
                "..",
                "a..",
                "a-."
                '\\',
                #"-a-", # These should act as delimiters but currently do not
                #".-",
                #"$-",
                #"*-",
                #"a*-"
    )

    # These should all act as delimiters, allowing the host to be replaced
    suffixes = ("",
                '"',
                "'",
                "`",
                "\\",
                "?",
                "?foo=bar",
                "/",
                "/path",
                "/path?foo=bar")

    # These should "attach" to the host or domain and prevent replacement
    negative_prefixes = ("a.", "a-", "a--", ".a.", "..a", "-a.", "A", "z")
    negative_suffixes = ("A", "z", "0", "9", "-a", ".a")

    def setUp(self):
        self.host_map = {
            # Basic subdomain change
            "web.example.com": "www.example.com",

            # Numbers
            "web-1a.example.com": "www-1a.example.com",

            # Partial hostname contained in subsequent hostnames
            "en.us.example.com": "en.us.regions.example.com",

            # Original is a partial match of a prior replacement
            "regions.example.com": "geo.example.com",

            # Deeper subdomain level in replacement
            "boards.example.com": "forums.en.us.example.com",

            # Deeper subdomain level in original; replacement inside original
            "en.us.wiki.example.com": "wiki.example.com",

            # Replacement has a hyphen while original does not
            "us.example.com": "us-east-1.example.net",

            # Map a second level domain to a different second level domain
			"example.net": "example.org",

            # Map both domain and subdomain
			"images.example.com": "cdn.example.org",
        }

        self.replacements  = create_replacements(self.host_map, binary=False)
        self.binary_replacements  = create_replacements(self.host_map, binary=True)

    def test_bad_unicode(self):
        bad_unicode = (
            b"\xe0\x80\x80",     # U+0800   - U+0FFF
            b"\xed\xbf\xbf",     # U+D000   - U+D7FF
            b"\xf0\x80\x80\x80", # U+10000  - U+3FFFF
            b"\xf4\xbf\xbf\xbf"  # U+100000 - U+10FFFF
        )

        for bad in bad_unicode:
            for original,replacement in self.host_map.items():
                for encoding_name, encoding_function in encoding_functions.items():
                    input_text = bad + encoding_function(original).encode("utf-8") + bad
                    expected_output = bad + encoding_function(replacement).encode("utf-8") + bad
                    actual_output = apply_replacements(input_text, self.binary_replacements)

                    if ("-" not in original and "-" in replacement) and encoding_name in ("url", "html_hex", "html_numeric"):
                        logging.debug("%s: Adjusting hyphens in comparison of %s to %s", self._testMethodName, expected_output, actual_output)
                        expected_output = re.sub(self.b_hyphen, b"-", expected_output)
                        actual_output = re.sub(self.b_hyphen, b"-", actual_output)
                    self.assertEqual(actual_output, expected_output, msg=f"{input_text} incorrectly results in {actual_output} under encoding '{encoding_name}'.")

    def test_all_host_map(self):
        """Tests every replacement in the test table for all encodings, with
        a sample of surrounding delimiters."""
        for original, replacement in self.host_map.items():
            for encoding_name, encoding_function in encoding_functions.items():

                # Test the prefixes and suffixes that should result in a replacement, in every combination
                for suffix in self.suffixes:
                    for prefix in self.prefixes:

                        # Encode the domain and the delimiters
                        #input_text = encoding_function(prefix + original + suffix)

                        # Encode only the domain
                        input_text = prefix + encoding_function(original) + suffix

                        if prefix != "" and suffix != "":
                            self.assertNotIn(input_text, self.host_map, msg="Invalid test conditions")

                        # Encode the domain and the delimiters
                        #expected_output = encoding_function(prefix + replacement + suffix)

                        # Encode only the domain
                        expected_output = prefix + encoding_function(replacement) + suffix
                        actual_output = apply_replacements(input_text, self.replacements)

                        if ("-" not in original and "-" in replacement) and encoding_name in ("url", "html_hex", "html_numeric"):
                            logging.debug("%s: Adjusting hyphens in comparison of %s to %s", self._testMethodName, expected_output, actual_output)
                            expected_output = re.sub(self.hyphen, "-", expected_output)
                            actual_output = re.sub(self.hyphen, "-", actual_output)
                        self.assertEqual(actual_output, expected_output, msg=f"{input_text} incorrectly results in {actual_output} under encoding '{encoding_name}'.")

    def test_all_host_map_negative(self):
        """Tests every replacement in the test table for all encodings, with
        a sample of surrounding non-delimiter strings."""
        for original in self.host_map:
            for encoding_name, encoding_function in encoding_functions.items():

                # Test the prefixes and suffixes that should not result in a replacement

                # The negative cases must be tested separately so that a failing negative case
                # (one that doesn't prevent replacement) is not "masked" by a successful one.

                for suffix in self.negative_suffixes + self.alphanumerics:
                    # Encode the domain and the suffix
                    #input_text = encoding_function(original + suffix)

                    # Encode only the domain
                    input_text = encoding_function(original) + suffix
                    self.assertNotIn(input_text, self.host_map, msg="Invalid test conditions")

                    # No change expected
                    expected_output = input_text
                    actual_output = apply_replacements(input_text, self.replacements)
                    self.assertEqual(actual_output, expected_output, msg=f"{input_text} incorrectly results in {actual_output} under encoding '{encoding_name}'.")

                for prefix in self.negative_prefixes + self.alphanumerics:
                    input_text = encoding_function(prefix + original)
                    self.assertNotIn(input_text, self.host_map, msg="Invalid test conditions")

                    # No change expected
                    expected_output = input_text
                    actual_output = apply_replacements(input_text, self.replacements)
                    self.assertEqual(actual_output, expected_output, msg=f"{input_text} incorrectly results in {actual_output} under encoding function '{encoding_name}'.")

    def test_no_change_undefined_subdomain(self):
        for original in self.host_map:
            for encoding_function in encoding_functions.values():
                self.assertNotIn(f"undefined.{original}", self.host_map, msg="Invalid test conditions")
                input_text = encoding_function("undefined." + original)
                expected_output = input_text
                self.assertEqual(apply_replacements(input_text, self.replacements), expected_output)

    def test_url_with_encoded_redirect(self):
        for original_url, replacement_url in self.host_map.items():
            for original_redirect, replacement_redirect in self.host_map.items():
                for encoding_name, encoding_function in encoding_functions.items():

                    # Main URL is not encoded, redirect parameter is encoded
                    encoded_original_redirect = encoding_function("https://" + original_redirect)
                    input_text = f"https://{original_url}?next={encoded_original_redirect}"
                    encoded_replacement_redirect = encoding_function("https://" + replacement_redirect)
                    expected_output = f"https://{replacement_url}?next={encoded_replacement_redirect}"
                    actual_output = apply_replacements(input_text, self.replacements)
                    if encoding_name in ("url", "html_hex", "html_numeric"):
                        if (("-" not in original_url and "-" in replacement_url) or ("-" not in original_redirect and "-" in replacement_redirect)):
                            logging.debug("%s: Adjusting hyphens in comparison of %s to %s", self._testMethodName, expected_output, actual_output)
                            expected_output = re.sub(self.hyphen, "-", expected_output)
                            actual_output = re.sub(self.hyphen, "-", actual_output)
                    self.assertEqual(actual_output, expected_output)

    def test_no_wildcard_dots(self):
        self.assertEqual(self.host_map["web.example.com"], "www.example.com", msg="Invalid test conditions")
        input_text = "webXexampleXcom"
        expected_output = input_text
        self.assertEqual(apply_replacements(input_text, self.replacements), expected_output, msg="The '.' character must be escaped so that it's not treated as a wildcard.")

    def test_no_bare_domain_replacement(self):
        self.assertNotIn("example.com", self.host_map, msg="Invalid test conditions")
        input_text = "example.com"
        expected_output = input_text
        self.assertEqual(apply_replacements(input_text, self.replacements), expected_output)

    def test_all_caps_hostname_all_caps_urlencoded(self):
        self.assertEqual(self.host_map["web.example.com"], "www.example.com", msg="Invalid test conditions")
        input_text = "WEB%2EEXAMPLE%2ECOM"
        expected_output = "WWW%2EEXAMPLE%2ECOM"
        self.assertEqual(apply_replacements(input_text, self.replacements), expected_output)

    def test_unencoded_case_preservation_binary(self):
        self.assertEqual(self.host_map["web.example.com"], "www.example.com", msg="Invalid test conditions")
        input_text = b"WEB.EXAMPLE.COM"
        expected_output = b"WWW.EXAMPLE.COM"
        self.assertEqual(apply_replacements(input_text, self.binary_replacements), expected_output)

    def _disabled_test_no_transitive(self):
        """Test that the mapping "{A: B, B: C}" does not result in A being
        mapped to C. Verify that it is not dependent on ordering."""

        mini_host_map = {
            "a.b": "c.d",
            "c.d": "e.f"
        }

        mini_host_map_reversed = {
            "c.d": "e.f",
            "a.b": "c.d"
        }

        mini_replacements = create_replacements(mini_host_map)
        mini_replacements_reversed = create_replacements(mini_host_map_reversed)

        for original, replacement in mini_host_map.items():
            input_text = original
            expected_output = replacement
            actual_output = apply_replacements(input_text, mini_replacements)
            self.assertEqual(actual_output, expected_output, msg=f"{input_text} incorrectly results in {actual_output} instead of {expected_output}")

        for original, replacement in mini_host_map_reversed.items():
            input_text = original
            expected_output = replacement
            actual_output = apply_replacements(input_text, mini_replacements_reversed)
            self.assertEqual(actual_output, expected_output, msg=f"{input_text} incorrectly results in {actual_output} instead of {expected_output}")

    def _disabled_test_case_preservation(self):
        """Tests whether casing is preserved for each encoding."""
        self.assertEqual(self.host_map["web.example.com"], "www.example.com", msg="Invalid test conditions")
        for encoding_function in encoding_functions.values():
            input_text = encoding_function("WEB.EXAMPLE.COM")
            expected_output = encoding_function("WWW.EXAMPLE.COM")
            actual_output = apply_replacements(input_text, self.replacements)
            self.assertEqual(apply_replacements(input_text, self.replacements), expected_output, msg=f"{input_text} incorrectly results in {actual_output} instead of {expected_output}")

if __name__ == '__main__':
    unittest.main()
