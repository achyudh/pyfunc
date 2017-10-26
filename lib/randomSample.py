from fileRetriever import Retriever
import sys 
import random


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

    def retrieve_random_sample(self, root_folder, output_file_name = None):
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
        files_and_methods = {}
        all_methods = []
        #random sample
        k = 86
        #Get all variables from all pyhton files
        for id in range(len(paths)):
            path = paths[id]
            #if decoding of file fails, because of strange char
            file = open(path, "r", encoding="utf8")
            #file = open(path, "r")
            # Finds all methods and adds them to a list
            for line in file:
                if(line.startswith("def")):
                    all_methods.append(line)
        #Select k random variables
        print(len(all_methods))
        random_sample = random.sample(all_methods, k)
        for id in range(len(paths)):
            file_methods = []
            path = paths[id]
            #if decoding of file fails, because of strange char
            file = open(path, "r", encoding="utf8")
            #file = open(path, "r")
            # Finds all methods and adds them to a list
            for line in file:
                if(line.startswith("def")):
                    file_methods.append(line)
            #Check if any method of this file is in the random selection, if so add them to the list
            random_methods = list(set(random_sample) & set(file_methods))
            if len(random_methods) > 0:
                files_and_methods[path] = random_methods
        
        #Write result to specified file
        if output_file_name:
            with open(output_file_name, "w") as output_file:
                for key in files_and_methods.keys():
                    output_file.write(key + "\n")
                    for methods in files_and_methods[key]:
                        output_file.write(methods + "\n")
                    output_file.write("=" * 20 + "\n")


if __name__ == "__main__":
    retriever = Retriever()
    random_sample = RandomSample(retriever)


    if(len(sys.argv) < 2):
        raise Exception("Usage: python randomSample.py <path\\to\\root\\directory>") 
    root_folder = sys.argv[1]
    random_sample.retrieve_random_sample(root_folder, "./random sampling/scikit-learn.txt")
