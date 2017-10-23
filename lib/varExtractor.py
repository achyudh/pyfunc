import json, ast, re, linecache
from fileRetriever import Retriever
from util.attrVisitor import AttrVisitor
from util.attrRegEx import AttrRegEx

almost_missed = 0

class Extractor:

    @staticmethod
    def func_defn_endline(py_file, start_line):
        endsig_regex = r"\)[ \t]*:"
        while True:
            match = re.search(endsig_regex, linecache.getline(py_file, start_line))
            if match is not None:
                return start_line
            else:
                start_line += 1

    @staticmethod
    def get_declarations(py_file):
        global almost_missed
        with open(py_file) as fd:
            file_contents = fd.read()
        curr_module = ast.parse(file_contents)
        func_def_nodes = [node for node in curr_module.body if isinstance(node, ast.FunctionDef)]
        declarations = list()

        for node in func_def_nodes:
            if node.name[0] != '_' and ast.get_docstring(node) is not None:
                docstr_replaced = ast.get_docstring(node).replace("\n", "NEWLINE_PLACEHOLDER")

                param_types, return_types = AttrVisitor.get_attr_types(ast.get_docstring(node))
                param_types_alt, return_types_alt = AttrRegEx.get_attr_types(docstr_replaced)
                missed_arg_ctr = 0
                total_arg_ctr = 0
                param_types_out = list()
                max_line_num = node.lineno
                for argument in node.args.args:
                    if param_types is not None and argument.arg in param_types:
                        param_types_out.append((argument.arg, param_types[argument.arg]))
                    elif param_types_alt is not None and argument.arg in param_types_alt:
                        param_types_out.append((argument.arg, param_types_alt[argument.arg]))
                        almost_missed += 1
                    else:
                        missed_arg_ctr += 1
                    total_arg_ctr += 1
                    max_line_num = max(max_line_num, argument.lineno)

                return_types_alt = list() if return_types_alt is not None else return_types_alt
                declarations.append({"name": node.name, "line": Extractor.func_defn_endline(py_file, max_line_num), "params": param_types_out,
                                     "returns": return_types_alt if return_types is None else return_types,
                                     "count": {"total_params": total_arg_ctr, "missed_params": missed_arg_ctr}})
        return declarations


if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     raise Exception("Usage: python varExtractor.py <path\\to\\root\\directory>")
    # root_folder = sys.argv[1]
    # py_files = retriever.list_all_files_in_folder(root_folder)
    py_files = Retriever.list_python_files("../test")
    output_json = {}

    total_arg_ctr = 0
    missed_arg_ctr = 0

    for py_file in py_files:
        declarations = Extractor.get_declarations(py_file)
        for dec in declarations:
            total_arg_ctr += dec["count"]["total_params"]
            missed_arg_ctr += dec["count"]["missed_params"]
        output_json[py_file] = declarations

    print("Total args:", total_arg_ctr, "Missed args:", missed_arg_ctr, "Proportion missed:", missed_arg_ctr/total_arg_ctr, almost_missed)

    with open("scikit.json", "w") as write_file:
        json.dump(output_json, write_file, indent=4)
