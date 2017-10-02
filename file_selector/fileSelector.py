from fileRetriever import fileRetriever
from fileReader import fileReader
import sys 

class fileSelector():

    """
    Main class that with help of fileRetriever and fileReader
    finds all python files in a specified folder, reads each
    of them and return the names of files that contain input
    variable or return specification i.e. name and type as
    well as the docstrings containing those specifications.
    """
    def __init__(self, retriever, reader):
        """
        Two objects that are used for finding the files to
        analyse and filtering out those that don't contain
        variable specifications.

        :param retriever: object
        :param reader: object
        """
        self.retriever = retriever
        self.reader = reader

    def retrieve_file_names(self, root_folder, output_file_name = None, verbose = True):
        """
        Retrieves all files which contain variable or return type specification
        that are located inside the root folder or any of its subfolders.
        :param root_folder: string
            Name of the folder where all the files are located
        :param output_file_name: string or None (optional)
            If specified, the files containing docstrings are written
            into the specified location together with their corresponding
            docstrings containing variable specification.
        :param verbose: bool
            If True, prints all files and relevant docstrings into the console
        :return: None
        """
        file_names = self.retriever.list_all_files_in_folder(root_folder)
        files_and_docstrings = {}
        for id in range(len(file_names)):
            file_name = file_names[id]
            # Finds all variable type specifications and adds them to a list
            variable_declarations = self.reader.parse_file(file_name)
            if len(variable_declarations) > 0:
                files_and_docstrings[file_name] = variable_declarations
        if verbose:
            for key in files_and_docstrings.keys():
                print key
                for docstring in files_and_docstrings[key]:
                    print docstring
        if output_file_name:
            with open(output_file_name, "w") as output_file:
                for key in files_and_docstrings.keys():
                    output_file.write(key + "\n")
                    for docstring in files_and_docstrings[key]:
                        output_file.write(docstring + "\n")
                    output_file.write("=" * 20 + "\n")




if __name__ == "__main__":
    retriever = fileRetriever()
    reader = fileReader("(Parameters|Returns).*[^ ]*( : )")
    selector = fileSelector(retriever, reader)


    if(len(sys.argv) < 2):
        raise Exception("Usage: python fileSelector.py <path\\to\\root\\directory>") 
    root_folder = sys.argv[1]
    selector.retrieve_file_names(root_folder, 'test.txt')
