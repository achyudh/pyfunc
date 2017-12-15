from fileRetriever import Retriever
import sys 
import random
import ast
import numpy as np


class RandomSample():

    """
    Main class that with help of fileRetriever finds all 
    python files in a specified folder, reads each
    of them and return k methods and their filename.
    """
    def __init__(self, retriever):
        """
        Object that is used for finding the files to
        analyse.

        :param retriever: object
        """
        self.retriever = retriever

    def fns_with_docstring(self, file_contents):
        fn_list = list()
        curr_module = ast.parse(file_contents)
        func_def_nodes = [node for node in curr_module.body if isinstance(node, ast.FunctionDef)]

        for node in func_def_nodes:
            if node.name[0] != '_' and ast.get_docstring(node) is not None and ("Parameters" in ast.get_docstring(node) or "Returns" in ast.get_docstring(node)):
                fn_list.append(node.name)
        return fn_list

    def retrieve_random_sample(self, root_folder, output_file_name, n_samples):
        """
        Retrieves random k sample methods from all the methods from the root folder and stores them in output file.
        :param root_folder: string
            Name of the folder where all the files are located
        :param output_file_name: string or None (optional)
            If specified, the files containing docstrings are written
            into the specified location together with their corresponding
            docstrings containing variable specification.
        :return: None
        """
        paths = self.retriever.list_python_files(root_folder)
        all_methods = []
        methods_per_file = {}
        #random sample
        #Get all variables from all pyhton files
        for id in range(len(paths)):
            path = paths[id]
            #if decoding of file fails, because of strange char
            file = open(path, "r", encoding="utf8")
            #file = open(path, "r")
            file_contents = file.read()
            # Finds all methods and adds them to a list
            relevant_methods = self.fns_with_docstring(file_contents)
            all_methods.extend([(path, x) for x in relevant_methods])
        #Select k random variables
        sample_value = np.min([n_samples, len(all_methods)])
        random_sample = random.sample(all_methods, sample_value)        
        #Write result to specified file
        print(output_file_name)
        count = 1
        if output_file_name:
            with open(output_file_name, "w") as output_file:
                for (x, y) in random_sample:
                    output_file.write(x + "\n\t" + y + "\n" + str(count) + " " + "="*20 + "\n")
                    count += 1

if __name__ == "__main__":
    retriever = Retriever()
    random_sample = RandomSample(retriever)
    random.seed(0)
    folder_paths = {"../MSR-Snapshot/django-master/": ("../random sampling/django.txt", 24),
                    "../MSR-Snapshot/matplotlib-master/": ("../random sampling/matplotlib.txt", 45),
                    "../MSR-Snapshot/networkx-master": ("../random sampling/networkx.txt", 40),
                    "../MSR-Snapshot/neupy-master": ("../random sampling/neupy.txt", 4),
                    "../MSR-Snapshot/scikit-image-master": ("../random sampling/scikit-image", 40),
                    "../MSR-Snapshot/scikit-learn-master/sklearn": ("../random sampling/scikit-learn", 86)}


    for key in folder_paths.keys():
        random_sample.retrieve_random_sample(key, folder_paths[key][0], folder_paths[key][1])
    
