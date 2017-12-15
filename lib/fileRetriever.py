import os


class Retriever:
    """
    Class for retrieving all python files inside the folder.
    Those are then processed by fileReader to retrieve files
    containing docstrings specifying variable types
    """

    def __init__(self):
        pass

    @staticmethod
    def list_python_files(root_folder_name):
        """
        Build a list containing paths of all python files
        inside the specified folder or any of its descendants

        :param root_folder_name: string
            Name of the parent folder containing all files
            and subfolders that need to be evaluated
        :return: list
            List containing string names of all python files
        """
        file_names = []
        for path, directories, files in os.walk(root_folder_name):
            for file in files:
                if file.endswith(".py") and not file.startswith("_"):
                    file_names.append(os.path.join(path, file))
        return file_names

    @staticmethod
    def get_sampled_file_names_and_functions(lab_file_name, return_functions = False, unique_only = True):
        """
        Generates list of tuples or list of strings.
        If tuples, each tuple is name of the file
        and the name of the function that were randomly selected for
        manual labelling.
        If string then only file names.
        Goes over all manually labelled files in
        a folder. If multiple functions come from one file each one
        of them has its own tuple.
        :param root_folder_name: str
            folder inside which all files are evaluated (except
            samples_per_person.txt)
        :return: list of tuples | list of str
            tuples contain two strings (file_name, method_name)
            str are file_name
        """
        file_names = []
        function_names = []
        completeness = []
        mismatches = []
        dataset ={}
        with open(lab_file_name) as eval_file:
            lines = eval_file.readlines()
        file_names += [x.strip() for x in lines if x.startswith("../")]
        function_names += [x.strip() for x in lines if x.startswith("\t") and x[1] not in ["+", "-"]]
        completeness += [x.strip()[2:] for x in lines if x.startswith("\t") and x[1] == "+"]
        mismatches += [x.strip()[2:] for x in lines if x.startswith("\t") and x[1] == "-"]
        if (len(file_names) != len(function_names)):
            raise Exception("Number of files and functions extracted is different in {}".format(file))
        if return_functions:
            return list(zip(file_names, function_names, completeness, mismatches))
        if unique_only:
            for i in range(len(file_names)):
                #print(file_names[i])
                if file_names[i] not in dataset.keys():
                    dataset[file_names[i]] = []
                dataset[file_names[i]].append((function_names[i],completeness[i],mismatches[i]))
            return dataset
        return file_names

if __name__ == "__main__":
    r = Retriever()
    print(r.get_sampled_file_names_and_functions("../random sampling/networkx.txt", False, True))
