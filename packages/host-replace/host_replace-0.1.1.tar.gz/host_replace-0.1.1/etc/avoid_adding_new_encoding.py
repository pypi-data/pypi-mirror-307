                # Avoid replacing an adding a new encoding type to the replacement 
                if encoded_original in self.replacements_table:

                    logging_args = (self.replacements_table[encoded_original], encoded_replacement, encoded_original)

                    if "%" not in self.replacements_table[encoded_original] and "%" in encoded_replacement:
                        logging.debug("Preferring %s over %s for %s since URL encoding not present", *logging_args)
                    elif "&#x" not in self.replacements_table[encoded_original] and "&#x" in encoded_replacement:
                        logging.debug("Preferring %s over %s for %s since HTML hex encoding not present", *logging_args)
                    elif "&#" not in self.replacements_table[encoded_original] and "&#" in encoded_replacement:
                        logging.debug("Preferring %s over %s for %s since HTML decimal encoding not present", *logging_args)
                    else:
                        self.replacements_table[encoded_original] = encoded_replacement
                else:
                    self.replacements_table[encoded_original] = encoded_replacement
