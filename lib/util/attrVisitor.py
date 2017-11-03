from docutils.nodes import GenericNodeVisitor
from docutils.utils import new_document
from docutils.frontend import OptionParser
from docutils.parsers.rst import Parser


class AttrVisitor(GenericNodeVisitor):

    def __init__(self, document):
        super().__init__(document)
        self.returns = list()
        self.args = dict()

    @staticmethod
    def get_attr_types(docstring):
        parser = Parser()
        default_settings = OptionParser(components=(Parser,)).get_default_values()
        document = new_document('test_data', default_settings)
        parser.parse(docstring, document)
        visitor = AttrVisitor(document)
        document.walk(visitor)
        return visitor.args, visitor.returns

    def __fetch_attr(self, node):
        if node.children[0].tagname == 'title' and (("Parameters" in node.children[0][0]) or ("Other Parameters" in node.children[0][0])):
            curr_index = 0
            if len(node.children) > 1:
                definition_items = node.children[1].children
                while curr_index < len(definition_items):
                    if ':' in definition_items[curr_index].rawsource:
                        node_rawsource = definition_items[curr_index].rawsource.split(':', 1)
                        if ',' in node_rawsource[0]:
                            var_list = [x.strip() for x in node_rawsource[0].split(',')]
                            for variable in var_list:
                                self.args[variable] = node_rawsource[1].split('\n')[0].strip()
                        else:
                            self.args[node_rawsource[0].strip()] = node_rawsource[1].split('\n')[0].strip()
                    curr_index += 1

        elif node.children[0].tagname == 'title' and ("Returns" in node.children[0][0]):
            curr_index = 0
            definition_items = node.children[1].children
            while curr_index < len(definition_items):
                if ':' in definition_items[curr_index].rawsource:
                    node_rawsource = definition_items[curr_index].rawsource.split(':', 1)
                    if ',' in node_rawsource[0]:
                        var_list = [x.strip() for x in node_rawsource[0].split(',')]
                        for variable in var_list:
                            self.returns.append((variable, node_rawsource[1].split('\n')[0].strip()))
                    else:
                        self.returns.append((node_rawsource[0].strip(), node_rawsource[1].split('\n')[0].strip()))
                curr_index += 1

    def visit_section(self, node):
        # Catch title nodes
        return self.__fetch_attr(node)

    def default_visit(self, node):
        # Pass all other nodes through
        pass

