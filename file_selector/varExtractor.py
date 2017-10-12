import json, ast, re
from fileRetriever import Retriever
from varExtractorRegEx import Extractor


if __name__ == "__main__":
    retriever = Retriever()
    extractor = Extractor(None)
    # py_files = retriever.list_all_files_in_folder("../scikit-learn-master/sklearn")
    py_files = retriever.list_all_files_in_folder("../scikit-learn-master")
    output_json = {}

    for py_file in py_files:
        with open(py_file) as fd:
            file_contents = fd.read()
        curr_module = ast.parse(file_contents)
        func_def_nodes = [node for node in curr_module.body if isinstance(node, ast.FunctionDef)]
        num_of_func = len(func_def_nodes)
        declarations = list()

        for node in func_def_nodes:
            if ast.get_docstring(node) is not None:
                docstr_replaced = ast.get_docstring(node).replace("\n", "NEWLINE_PLACEHOLDER")
                param_pairs, return_pairs = extractor.extract_variable_types_from_docstring(docstr_replaced)

                # Hash the type information for faster searching
                # TODO: Modify at source varExtractorRegEx, change list to dict
                param_types = dict()
                if param_pairs is not None:
                    for pair in param_pairs:
                        param_types[pair[0]] = pair[1]

                invalid_arg_ctr = 0
                param_types_out = list()
                for argument in node.args.args:
                    if argument.id in param_types:
                        param_types_out.append((argument.id, param_types[argument.id]))
                    else:
                        invalid_arg_ctr += 1

                declarations.append((node.name, ((param_types_out, invalid_arg_ctr), return_pairs)))

        output_json[py_file] = (declarations, num_of_func)

    with open("scikit.json", "w") as write_file:
        json.dump(output_json, write_file, indent = 4)