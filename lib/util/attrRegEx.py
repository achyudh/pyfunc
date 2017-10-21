import re


class AttrRegEx:
    @staticmethod
    def get_attr_types(docstring):
        """
        Takes in a docstring String and returns a tuple of two lists.
        First list contains tuples of input variable name and types.
        Second list contains tuples of return names and variable types.

        :param docstring:
        :return:
        """
        param_regex = "Parameters.*?-{1,}.*?(-{3,}|$)"
        return_regex = "Returns.*?-{1,}.*?(-{3,}|$)"

        params = re.search(param_regex, docstring)
        returns = re.search(return_regex, docstring)

        param_pairs, returns_pairs = None, None
        if params is not None:
            param_pairs = AttrRegEx.get_param_types(params)
        if returns is not None:
            returns_pairs = AttrRegEx.get_return_types(returns)
        return param_pairs, returns_pairs

    @staticmethod
    def get_param_types(substring):
        # Space/tab/newline followed by an alhabetic char or underscore (only eligible
        # name starts, followed by alphanumerics + _, followed by space, colon, space
        definition_regex = "(\s\*?[A-Za-z_]+[A-Za-z_0-9]* ?\: ?.*)"
        type_pairs = dict()
        lines = substring.group(0).replace("NEWLINE_PLACEHOLDER", "\n")
        type_lines = [x for x in re.findall(definition_regex, lines)]
        for pair in type_lines:
            split_vars = pair.split(':')
            if ',' in split_vars[0]:
                var_list = [x.strip() for x in split_vars[0].split(',')]
                for variable in var_list:
                    type_pairs[variable] = split_vars[1].strip()
            else:
                type_pairs[split_vars[0].strip()] = split_vars[1].strip()
        return type_pairs

    @staticmethod
    def get_return_types(substring):
        # Space/tab/newline followed by an alhabetic char or underscore (only eligible
        # name starts, followed by alphanumerics + _, followed by space, colon, space
        definition_regex = "(\s\*?[A-Za-z_]+[A-Za-z_0-9]* ?\: ?.*)"
        type_pairs = list()
        lines = substring.group(0).replace("NEWLINE_PLACEHOLDER", "\n")
        type_lines = [x for x in re.findall(definition_regex, lines)]
        for pair in type_lines:
            split = pair.split(":")
            type_pairs.append((split[0].strip(), split[1].strip()))
        return type_pairs