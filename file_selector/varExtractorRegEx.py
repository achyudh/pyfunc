from fileRetriever import Retriever
import re
import json


class Extractor:

    """
    Evaluates a given file and for a file returns:
        Tuple - first entry is:
            Array of tuples
            Each tuple consists of
                1) String with each method's signature
                2) Array - items correspond to each docstring that can be in file.
                    Each item is a tuple. Each tuple consists of
                        1) Array of tuples for input types
                            Each tuple is a pair of var name and var type
                        2) Array of tuples for output types
                            Each tuple is a pair of var name and var type
            Second entry number of functions in file
    """

    def __init__(self, regex_string):
        self.regex_string = regex_string
        self.newline_placeholder = "NEWLINE_PLACEHOLDER"

    def get_declarations(self, file_name):
        # Read file
        with open(file_name) as inputFile:
            contents = inputFile.read()

        # Replace all newlines to enable whole-file regex
        contents_with_replacement = contents.replace("\n", self.newline_placeholder)

        # Split the whole text based on starts of method or class definitions
        split_by_defs = re.split(self.newline_placeholder + "\s*(def|class) ", contents_with_replacement)[1:]
        split = [split_by_defs[x] + " " + split_by_defs[x + 1] for x in range(0, len(split_by_defs), 2)]

        # Make tuples of (function, array of docstrings)
        # funs_and_docstrings = [(x, [y.replace(self.newline_placeholder, "\n") for y in self.get_docstrings(x)]) for x in split]
        funs_and_docstrings = [(x, [y for y in self.get_docstrings(x)]) for x in split]

        # Transfer class's variables to the init method as init has no docstring inside it
        for x in range(len(funs_and_docstrings)):
            one_fun_and_docstring = funs_and_docstrings[x]
            if one_fun_and_docstring[0].startswith("def __init__"):
                funs_and_docstrings[x] = (one_fun_and_docstring[0], funs_and_docstrings[x - 1][1])

        # Replace the newline placeholder and filter out instances corresponding class definition
        funs_and_docstrings = [\
            (self.get_method_signature(x[0].replace(self.newline_placeholder, "\n")), x[1])\
            for x in funs_and_docstrings if x[0].startswith("def ")\
        ]

        # For each docstring generate a tuple with 2 arrays as children
        for i in range(len(funs_and_docstrings)):
            (fun, docstrings) = funs_and_docstrings[i]
            variables = []
            for docstring in docstrings:
                variables.append(self.extract_variable_types_from_docstring(docstring))
            funs_and_docstrings[i] = (fun, variables)

        return funs_and_docstrings

    @staticmethod
    def get_method_signature(method_string):
        return re.search("def .*?(\n.*?)*?\):", method_string, re.MULTILINE).group(0)

    @staticmethod
    def get_docstrings(file_contents):
        """
        Extracts all comments within 3x single or double quotes.

        :param file_contents: string
            The whole text file obtained by reading it.
        :return: array
            List of strings, each item is a docstring (or other comment in triple quotes)
        """

        double_quotes_regex = '(""".*?""")'
        single_quotes_regex = "('''.*?''')"

        docstrings = re.findall(double_quotes_regex + "|" + single_quotes_regex, file_contents)
        # Flatten the list of tuples produced by the use of "|" in a regex string
        docstrings = [item for sublist in docstrings for item in sublist if len(item) > 0]
        # Remove trailing characters ("""/''')
        return [x[3:-3] for x in docstrings]

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
        if found is None:
            return False
        return True

    def extract_variable_types_from_docstring(self, docstring):
        """
        Takes in a docstring String and returns a tuple of two lists.
        First list contains tuples of input variable name and types.
        Second list contains tuples of return names and variable types.

        :param docstring:
        :return:
        """
        param_regex = "Parameters.*?-{1,}.*?(-{3,}|$)"
        return_regex = "Returns.*?-{1,}.*?(-{3,}|$)"

        params = re.search(param_regex, docstring)
        returns = re.search(return_regex, docstring)

        param_pairs, returns_pairs = None, None
        if params != None:
            param_pairs = self.extract_variables_types_from_substring(params)
        if returns != None:
            returns_pairs = self.extract_variables_types_from_substring(returns)
        return param_pairs, returns_pairs

    def extract_variables_types_from_substring(self, substring):
        # Space/tab/newline followed by an alhabetic char or underscore (only eligible
        # name starts, followed by alphanumerics + _, followed by space, colon, space
        definition_regex = "(\s\*?[A-Za-z_]+[A-Za-z_0-9]* ?\: ?.*)"
        type_pairs = []
        lines = substring.group(0).replace(self.newline_placeholder, "\n")
        type_lines = [x for x in re.findall(definition_regex, lines)]
        for pair in type_lines:
            split = pair.split(":")
            type_pairs.append((split[0].strip(), split[1].strip()))
        return type_pairs


if __name__ == "__main__":
    retriever = Retriever()
    extractor = Extractor("(Parameters|Returns).*[^ ]*( : )")
    py_files = retriever.list_all_files_in_folder("../test")
    output_json = {}

    for py_file in py_files:
        declarations = extractor.get_declarations(py_file)
        num_of_fun = len(declarations)
        output_json[py_file] = (declarations, num_of_fun)

    with open("test.json", "w") as write_file:
        json.dump(output_json, write_file, indent = 4)

