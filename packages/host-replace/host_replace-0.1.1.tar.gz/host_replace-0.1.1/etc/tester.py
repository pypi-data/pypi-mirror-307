#!/usr/bin/env python3

import host_replace

# Wait, but this is every possible representation, we don't need all of them
# just the one we are encoding
# we should be able to give it a lambda function
# or any function

# encoded_original_domain = encode_fn(original_domain)

# we really need to make this a dict
url_all = host_replace.encoding_functions[9][1]

print(url_all("www.examplE.coM"))
t = host_replace.generate_domain_pattern("www.example.com", url_all)

print(t)

