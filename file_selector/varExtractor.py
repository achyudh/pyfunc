import json, ast, re, sys
from fileRetriever import Retriever


class Extractor:

    @staticmethod
    def extract_variable_types_from_docstring(docstring):
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
            param_pairs = Extractor.extract_variables_types_from_substring(params)
        if returns is not None:
            returns_pairs = Extractor.extract_variables_types_from_substring(returns)
        return param_pairs, returns_pairs

    @staticmethod
    def extract_variables_types_from_substring(substring):
        # Space/tab/newline followed by an alhabetic char or underscore (only eligible
        # name starts, followed by alphanumerics + _, followed by space, colon, space
        definition_regex = "(\s\*?[A-Za-z_]+[A-Za-z_0-9]* ?\: ?.*)"
        type_pairs = dict()
        lines = substring.group(0).replace("NEWLINE_PLACEHOLDER", "\n")
        type_lines = [x for x in re.findall(definition_regex, lines)]
        for pair in type_lines:
            split = pair.split(":")
            type_pairs[split[0].strip()] = split[1].strip()
        return type_pairs

    @staticmethod
    def get_declarations(py_file):
        with open(py_file) as fd:
            file_contents = fd.read()
        curr_module = ast.parse(file_contents)
        func_def_nodes = [node for node in curr_module.body if isinstance(node, ast.FunctionDef)]
        declarations = list()

        for node in func_def_nodes:
            if ast.get_docstring(node) is not None:
                docstr_replaced = ast.get_docstring(node).replace("\n", "NEWLINE_PLACEHOLDER")
                param_types, return_types = Extractor.extract_variable_types_from_docstring(docstr_replaced)

                missed_arg_ctr = 0
                total_arg_ctr = 0
                param_types_out = dict()
                for argument in node.args.args:
                    if param_types is not None and argument.arg in param_types:
                        param_types_out[argument.arg] = param_types[argument.arg]
                    else:
                        missed_arg_ctr += 1
                    total_arg_ctr += 1

                declarations.append((node.name, ((param_types_out, total_arg_ctr, missed_arg_ctr), dict() if return_types is None else return_types)))
        return declarations


if __name__ == "__main__":
    retriever = Retriever()
    if len(sys.argv) < 2:
        raise Exception("Usage: python varExtractor.py <path\\to\\root\\directory>")
    root_folder = sys.argv[1]
    py_files = retriever.list_all_files_in_folder(root_folder)
    # py_files = retriever.list_all_files_in_folder("../scikit-learn-master/sklearn")
    output_json = {}

    for py_file in py_files:
        declarations = Extractor.get_declarations(py_file)
        output_json[py_file] = declarations

    with open("test.json", "w") as write_file:
        json.dump(output_json, write_file, indent=4)
