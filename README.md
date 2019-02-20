# PyFunc Signature Parser
Walks Python AST and parses doctrings to provide hints to MyPy for checking inconsistencies between docstrings and code.
 
## Modules
### lib.fileSelector
Adjust the parameters in the __main__ call to traverse a specified folder and retrieve all the file names where variable and/or return types are specified in the docstring as well as those docstrings. Additionally, the parameters allow you to either print the output to the console or write them to a file.
### lib.plantMyPy
Plants MyPy directives into a copy of the Python code by using the data types from the varExtractor module.
### lib.fileReader
Reads a file and extracts all docstrings that contain variable descriptions or return descriptions.
### lib.fileRetriever
Retrieves all python files inside the folder, which are then processed by fileReader to retrieve files containing docstrings specifying variable types
### lib.randomSample
With help of lib.fileRetriever, finds all the Python files in a specified folder, reads each of them and returns methods after random sampling.
### lib.varExtractor
Extracts variable type information from docstrings in a hybrid manner using both Python AST parsing and RegEx

## Contributing:
When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change. Ensure any install or build dependencies are removed before the end of the layer when doing a build. Update the README.md with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations and container parameters.

## License:
This project is licensed under the MIT License - see the LICENSE.md file for details
