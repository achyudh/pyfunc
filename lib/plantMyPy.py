
import sys, subprocess, os, re
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
                    if params[1] == 'missing':
                       mypy_str += 'Any, '
                    elif params[1] == 'extra':
                       mypy_str += ''
                    else:
                        #print (params)
                        mypy_str += get_mypy_type(params[1]) + ', '
                        #print ("param: " + params)
                mypy_str = mypy_str[:-2]
            mypy_str += ') -> Any'
            '''if len(funcs['returns']) > 0:
                for returns in funcs['returns']:
                    mypy_str += get_mypy_type(returns[1]) + ', '
                    #print ("return: " + returns)
                mypy_str = mypy_str[:-2]
            else:
                mypy_str += 'None' '''

            #print (funcs['name'])
            #print( mypy_str)
            comments[path].append({'method' : funcs['name'], 'line' : funcs['line'], 'comment': mypy_str})
            #print ("***")
    #print(comments)
    return comments

def get_mypy_type(words):
	strings = words.split(' ')
	for string in strings:
		if 'dict' in string.lower():
			return 'Dict'
		elif 'tuple' in string.lower():
			return 'Tuple'
		elif 'object' in string.lower():
			return "Any"
		elif 'type' in string.lower():
			return "Type"
		elif 'callable' in string.lower() or 'function' in string.lower():
			return "Callable"
		elif 'str' in string.lower() or 'text' in string.lower():
			return 'str'
		elif 'int' in string.lower() or 'scalar' in string.lower() or 'numeric' in string.lower():
			return 'int'
		elif 'float' in string.lower() :
			return 'float'
		elif 'double' in string.lower() :
			return 'Decimal'
		elif 'array' in string.lower() or 'list' in string.lower() or 'matrix' in string.lower() or 'sequence' in string.lower() or 'tensor' in string.lower():
			return 'List'
		elif 'bool' in string.lower():
			return 'bool'


	return 'None'

def plantComments(comments):
	filenames = []
	for item, value in comments.items():

		f = open(item, 'r')
		contents = f.readlines()
		f.close()
		for comment in value:
		#contents.insert(item['line']-1, item['comment'])
			line = contents[comment['line']-1][:-1]
			line = line + " " + comment['comment'] + "\n"
			contents[comment['line']-1] = line

		contents = ['from typing import Tuple, Dict, List, Any, Decimal, Type, Callable \n'] + contents
		filenames.append(item+'_')
		f2 = open(item+'_', 'w')
		contents = "".join(contents)
		f2.write(contents)
		f2.close()
		#print (contents)
		#print ("_____")
	return collect_output(filenames)

def collect_output(filenames):
	output = []
	for item in filenames:
		#output[item] = []
		#print (item)
		p= os.popen("mypy --py2 --follow-imports=silent --ignore-missing-imports "+item).read()
		print ('--')
		#print(p)
		# for argument mismatch
		m = re.findall('(.*?):([0-9]+):\s*(error:.*?incompatible type.*)', p, re.IGNORECASE)
		for (f,l,e) in m:
                        with open(item) as fp:
                            for i, line in enumerate(fp):
                                if i == int(l)-1:
                                    if 'def ' in line:
                                        g = re.search('\s*def\s*(.*?)\s*\(', line)
                                        #print(line)
                                        output.append((f, 'parameter', g.group(1), e))

		

    	
	return output


if __name__ == "__main__":
    retriever = Retriever()
    if(len(sys.argv) < 2):
        raise Exception("Usage: python3 plantMyPy.py path/to/root/folder")
    root_folder = sys.argv[1]
    py_files = retriever.list_python_files(root_folder)
    #samples = Retriever.get_sampled_file_names_and_functions(sys.argv[1], False, True) # get only the files from sample set
    #py_files = samples.keys()
    output_json = {}
    missing, partial, complete, total = 0, 0, 0, 0
    for py_file in py_files:
        declarations = Extractor.get_declarations(py_file)
        output_json[py_file] = declarations
        for method in declarations:
                       if method['tag'] == 'complete':
                           complete +=1
                       elif method['tag'] == 'incomplete':
                           missing +=1
                       elif method['tag'] == 'partial':
                           partial +=1
                       total += 1

 

    #print (output_json)
    comments = makeComment(output_json)
    out = plantComments(comments)
    mismatches = {}

    for k,v,a,b in out:
        print("\nfile: " + k)
        #for item in v:
        print('\n\t type: '+ v + '\n\t\tline: ' + a + '\n\t\t' + b)
        if k not in mismatches.keys():
            mismatches[k] = []
        if a not in mismatches[k]:
            mismatches[k].append(a)

    print('\n\n\n')
    print('number of mismatches: '+ str(len(mismatches.values())))

    print ("\n total\t complete\t partial\t missing")
    print ("\n "+ str(total)+"\t"+str(complete)+"\t"+str(partial)+"\t"+str(missing))
    '''unrolled_samples = []
    for (file_name, labels) in samples.items():


        file_ = output_json[file_name]
        #print(file_name)
        me = [x[0] for x in labels]
        #print(me)
        if file_ != None:
               for method in file_:
                   if method['name'] in me:
                       if method['tag'] == 'complete':
                           complete +=1
                       elif method['tag'] == 'incomplete':
                           missing +=1
                       elif method['tag'] == 'partial':
                           partial +=1
                       total += 1

        for (f,c,m) in labels:
            print(m)
            g = re.search('\s*(\d)\s*mismatch', m)
            if g is not None:
                if int(g.group(1)) > 0:
                    unrolled_samples.append((file_name, f, m, True))
                else:
                    unrolled_samples.append((file_name, f, m, False))

            else: # remove if don't want to consider n/a as a result of incomplete comments
                 unrolled_samples.append((file_name, f, m, False))

    for item in unrolled_samples:
        if item[3]:
           print (item[0] + '\t' + item[1] + '\t' + str(item[3]) +  "\t" + item[2] +'\n')


    print ("\n total\t complete\t partial\t missing")
    print ("\n "+ str(total)+"\t"+str(complete)+"\t"+str(partial)+"\t"+str(missing))

    FP, TP, TN, FN = 0,0,0,0
    for (file_name, method_name, _, label) in unrolled_samples:
         if label: # if true label is true
             if file_name+'_' in mismatches.keys(): # file name found in mismatches
                if method_name in mismatches[file_name+'_']: # got both file name and method
                     print('TP')
                     print(method_name)
                     TP +=1
                else: # got the file but not the method
                     print('FN')
                     print(method_name)
                     FN +=1
             else: # even file was not detected
                 print('FN')
                 print(method_name)
                 FN +=1
         else: # if we didn't detect it
            if file_name+'_' in mismatches.keys(): # file name found in mismatches
                 if method_name in mismatches[file_name+'_']: # got both file name and method
                     print('FP')
                     print(method_name)
                     FP +=1
                 else: # got the file but not the method
                     TN +=1
            else:
                TN +=1

    all_ = [(x[0]+'_', x[1]) for x in unrolled_samples]
    for f,m in mismatches.items():
        for method in m:
            if (f,method) not in all_:
                print('FP')
                print(method) 
                FP+=1       
    print ("TP\tTN\tFP\tFN\n")
    print(str(TP)+'\t'+str(TN)+'\t'+str(FP)+'\t'+str(FN)+'\n')


                
            '''
            








