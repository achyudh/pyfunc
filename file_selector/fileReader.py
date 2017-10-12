import re

class Reader():

    """
    Class for reading a file and extracting all docstrings that
    contain variable or return descriptions
    """

    def __init__(self, regex_string):
        """
        :param regex_string: string
            Specifies what is the form of variable type
            specifications - may differ between projects
        """

        self.regex_string = regex_string

    def parse_file(self, file_name):
        """
        Main function - with assistance of helper functions finds all
        variable declarations matching regex_string inside the file
        and returns them inside a list.

        :param file_name: string
            Name of the file from which variable specifications are to be identified.
        :return: list
            List of strings where each item in a list is a docstring containing
            a variable specification.
        """

        with open(file_name, "r") as input_file:
            file_contents = input_file.read()

        """
        Regex is done on line by line basis - to ensure that irrespective
        of the formatting all docstrings are identified and all variable
        specifications are found.
        """
        file_contents = file_contents.replace("\n", "NEWLINE")

        docstrings = self.get_docstrings(file_contents)
        variable_declarations = self.select_variable_declarations(docstrings)
        variable_declarations = [x.replace("NEWLINE", "\n") for x in variable_declarations]
        return variable_declarations

    def get_docstrings(self, file_contents):
        """
        Extracts all comments within 3x single or double quotes.

        :param file_contents: string
            The whole text file obtained by reading it.
        :return: array
            List of strings, each item is a docstring (or other comment in triple quotes)
        """

        double_quotes_regex = '("""[^"""]*""")'
        single_quotes_regex = "('''[^''']*''')"

        docstrings = re.findall(double_quotes_regex + "|" + single_quotes_regex, file_contents)
        # Flatten the list of tuples produced by the use of "|" in a regex string
        docstrings = [item for sublist in docstrings for item in sublist if len(item) > 0]
        # Remove trailing characters ("""/''')
        return [x[3:-3] for x in docstrings]

    def select_variable_declarations(self, docstrings):
        """
        Iterates over all docstrings in a single file and returns only those
        that specify variable type
        :param docstrings: list
            List of strings, each item is a docstring that is queried for
            specifying variables/returns
        :return: list
            List of strings, each item is a docstring that specifies variable
            or return type
        """
        return [x for x in docstrings if self.docstring_contains_variable_declaration(x)]

    def docstring_contains_variable_declaration(self, docstring):
        """
        Attempts to find the specified regex_string in a docstring.
        Returns True if matched, False otherwise.

        :param docstring: string
            One comment in triple quotes that is examined for
            containing the regex_string.
        :return: bool
            True if regex_string matched, False otherwise.
        """
        found = re.search(self.regex_string, docstring)
        if found == None:
            return False
        return True
