pre_help_dicts = {r"(?i)(\W|^)2ja(\W|$)": r'\g<1>tveggja\g<2>',
			    r"(?i)(\W|^)3ja(\W|$)": r'\g<1>þriggja\g<2>',
			    r"(?i)(\W|^)4ð(a|i)(\W|$)": r'\g<1>fjórð\g<2>\g<3>',
			    r"(?i)(\W|^)5t(a|i)(\W|$)": r'\g<1>fimmt\g<2>\g<3>',
			    r"(?i)(\W|^)6t(a|i)(\W|$)": r'\g<1>sjött\g<2>\g<3>',
			    r"(?i)(\W|^)7d(a|i)(\W|$)": r'\g<1>sjöund\g<2>\g<3>',
			    r"(?i)(\W|^)8d(a|i)(\W|$)": r'\g<1>áttund\g<2>\g<3>',
			    r"(?i)(\W|^)9d(a|i)(\W|$)": r'\g<1>níund\g<2>\g<3>',
			    
			    r"(?i)([a-záðéíóúýþæö]+)(\d+)": r'\g<1> \g<2>',
			    r"(?i)(\d+)([a-záðéíóúýþæö]+)": r'\g<1> \g<2>',
				  # if we have an uppercase token on one or both sides of a hyphen, insert space on BOTH sides
				  # of the hyphen (original: space only inserted on the side of definitely all uppercases)
				  # example: EFTA-ríkin should become EFTA - ríkin and not EFTA -ríkin.
			    r"(\W|^)([A-ZÁÐÉÍÓÚÝÞÆÖ]+)(\-)([A-ZÁÐÉÍÓÚÝÞÆÖa-záðéíóúýþæö]+)(\W|$)": r"\g<1>\g<2> \g<3> \g<4>\g<5>",
			    r"(\W|^)([A-ZÁÐÉÍÓÚÝÞÆÖa-záðéíóúýþæö]+)(\-)([A-ZÁÐÉÍÓÚÝÞÆÖ]+)(\W|$)": r"\g<1>\g<2> \g<3> \g<4>\g<5>",
			    r"(?i)([\da-záðéíóúýþæö]+)(°)": r'\g<1> \g<2>',
			    r"(?i)([\da-záðéíóúýþæö]+)(\%)": r'\g<1> \g<2>',
				# telephone number pattern: 555 1234 -> 555-1234
				r"(\d{3})( )(\d{4})": r" \g<1>-\g<3>",
			    r"(\W|^)(0?[1-9]|[12]\d|3[01])\.(0?[1-9]|1[012])\.(\d{3,4})(\W|$)": r" \g<1>\g<2>. \g<3>. \g<4>\g<5>",
				  # insert space between date elements like '14.3.' -> '14. 3.'
			    r"(\W|^)(0?[1-9]|[12]\d|3[01])\.(0?[1-9]|1[012])\.(\W|$)": r" \g<1>\g<2>. \g<3>. \g<4>",
				# date: 13/04/20 -> 13. 04. 20, should also fetch 13 / 04 / 20
				r"(\W|^)([0-3][0-9])\s*/\s*([01][0-9])\s*/\s*([12]?[0-9]?[0-9]{2})(\W|$)": r" \g<1>\g<2>. \g<3>. \g<4>\g<5>",
				# remove apostrophe before a two digit representation of a year, like '20 (for 2020) or '95 (for 1995)
				r"(\W|^)'([1-9][0-9])(\W|$)": r"\g<1> \g<2>\g<3>"}