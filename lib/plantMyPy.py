
import sys, subprocess, os, re, random
from fileRetriever import Retriever
from varExtractor import Extractor
def makeComment(struct):
	comments = {}
	for path,files in struct.items():
		#print(path)
		comments[path] = []
		for funcs in files:
			#print ("method name: " + funcs['name'])
			mypy_str = "# type: ( "

			if len(funcs['params']) > 0:
				for params in  funcs['params']:
					#print (params)
					mypy_str += get_mypy_type(params[1]) + ', ' 
					#print ("param: " + params)
				mypy_str = mypy_str[:-2]
			mypy_str += ') -> '
			if len(funcs['returns']) > 0:
				for returns in funcs['returns']:
					mypy_str += get_mypy_type(returns[1]) + ', ' 
					#print ("return: " + returns)
				mypy_str = mypy_str[:-2]
			else:
				mypy_str += 'None'

			#print (funcs['name'])
			#print( mypy_str)
			comments[path].append({'method' : funcs['name'], 'line' : funcs['line'], 'comment': mypy_str})
			#print ("***")
	#print(comments)
	return comments

def get_mypy_type(string):
	if 'str' in string.lower():
		return 'str'
	elif 'int' in string.lower():
		return 'int'
	elif 'float' in string.lower() :
		return 'float'
	elif 'array' in string.lower() :
		return 'List'
	elif 'boolean' in string.lower():
		return 'bool'
	elif 'dict' in string.lower():
		return 'Tuple'
	else:
		return 'None'

def plantComments(comments):
	filenames = []
	for item, value in comments.items():

		f = open(item, 'r')
		contents = f.readlines()
		f.close()
		for comment in value:
		#contents.insert(item['line']-1, item['comment'])
			line = contents[comment['line']-1][:-2]
			line = line + " " + comment['comment'] + "\n"
			contents[comment['line']-1] = line

		contents = ['from typing import Tuple, List \n'] + contents
		filenames.append(item+'_')
		f2 = open(item+'_', 'w')
		contents = "".join(contents)
		f2.write(contents)
		f2.close()
		#print (contents)
		#print ("_____")
	return collect_output(filenames)

def collect_output(filenames):
	output = {}
	for item in filenames:
		output[item] = []
		#print (item)
		p= os.popen("mypy --py2 "+item).read()
		print ('--')
		#print(p)
		# for argument mismatch
		m = re.findall('(.*?):([0-9]+):\s*(error:.*?incompatible type.*)', p, re.IGNORECASE)
		for (f,l,e) in m:
			output[f].append(('parameter', l, e))

		# return mismatch
		m = re.findall('(.*?):([0-9]+):\s*(error: missing return statement.*)',  p, re.IGNORECASE)
		for (f,l,e) in m:		
			output[f].append(('return', l,e))

		
	return output


if __name__ == "__main__":
    retriever = Retriever()
    if(len(sys.argv) < 2):
        raise Exception("Usage: python plantMyPy.py <path\\to\\root\\directory>")
    root_folder = sys.argv[1]
    py_files = retriever.list_python_files(root_folder)

    output_json = {}
    #random sample
    k = 100
    all_variable_declarations = list()
    for py_file in py_files:
         # Finds all variable type specifications and adds them to a list
         all_variable_declarations.extend(Extractor.get_declarations(py_file))
    #Select k random variables
    random_sample = random.sample(all_variable_declarations, k)
    for py_file in py_files:
        # Finds all variable type specifications and adds them to a list
        declarations = Extractor.get_declarations(py_file)
        #Check if any variable of this file is in the random selection, if so add them to the list
        #random_variable_declarations = list(set(random_sample) & set(declarations))
        #create set of dict values in the random_sample
        random_sample_name = set(d["name"] for d in random_sample)
        #Get the intersection between the random_sample and the variables of the py_file
        random_variable_declarations = [d for d in declarations if d["name"] in random_sample_name]
        if len(random_variable_declarations) > 0:
        	output_json[py_file] = random_variable_declarations
    comments = makeComment(output_json)
    out = plantComments(comments)

    for k,v in out.items():
        print("\nfile: " + k)
        for item in v:
            print('\n\t type: '+ item[0] + '\n\t\tline: ' + item[1] + '\n\t\t' + item[2])

	
