import ast


def fns_with_docstring(file_contents):
    fn_list = list()
    curr_module = ast.parse(file_contents)
    func_def_nodes = [node for node in curr_module.body if isinstance(node, ast.FunctionDef)]

    for node in func_def_nodes:
        if node.name[0] != '_' and ast.get_docstring(node) is not None:
            fn_list.append(node.name)
    return fn_list


with open("../../test/t.py") as fd:
    file_contents = fd.read()
    print(fns_with_docstring(file_contents))