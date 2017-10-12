import os


class Retriever():
    """
    Class for retrieving all python files inside the folder.
    Those are then processed by fileReader to retrieve files
    containing docstrings specifying variable types
    """

    def __init__(self):
        pass

    def list_all_files_in_folder(self, root_folder_name):
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
                if file.endswith(".py"):
                    file_names.append(os.path.join(path, file))
        return file_names

if __name__ == "__main__":
    it = Retriever()
    root_folder_name = "/Users/nknyazev/Documents/Delft/Software_Analytics/project/scikit-learn-master/"
    file_names = it.list_all_files_in_folder(root_folder_name)
