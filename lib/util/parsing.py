import ast


def fns_with_docstring(file_contents):
    fn_list = list()
    curr_module = ast.parse(file_contents)
    func_def_nodes = [node for node in curr_module.body if isinstance(node, ast.FunctionDef)]

    for node in func_def_nodes:
        if node.name[0] != '_' and ast.get_docstring(node) is not None:
            fn_list.append(node.name)
    return fn_list

if __name__ == "__main__":
	file_name = "/Users/nknyazev/Documents/Delft/Software_Analytics/project/MSR-Snapshot/scikit-learn-master/sklearn/datasets/rcv1.py"
	with open(file_name) as file:
		file_contents = file.read()
	print(fns_with_docstring(file_contents))