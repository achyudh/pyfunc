
import sys
from fileRetriever import Retriever
from varExtractor import Extractor
def plantComment(struct):
	print ("----")
	for files in struct:
		for funcs in files:
			print (funcs)
			for params in  funcs[1][0]:
				print (params)
			print ("***")

'''for returns in funcs[0]:
print returns'''


if __name__ == "__main__":
    retriever = Retriever()
    if(len(sys.argv) < 2):
        raise Exception("Usage: python plantMyPy.py <path\\to\\root\\directory>")
    root_folder = sys.argv[1]
    py_files = retriever.list_python_files(root_folder)

    output_json = {}

    for py_file in py_files:
        declarations = Extractor.get_declarations(py_file)
        output_json[py_file] = declarations
    print (output_json)
    #plantComment(output_json)
	
