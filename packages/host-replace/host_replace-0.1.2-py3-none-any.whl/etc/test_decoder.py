def test_decoder(self):
	for original, replacement in self.host_map.items():
		for encoding_name, encoding_function in encoding_functions:
			self.assertEqual(decode_hostname(encoding_function(original)), original)

