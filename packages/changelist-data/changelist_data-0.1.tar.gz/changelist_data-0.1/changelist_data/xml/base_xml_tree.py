""" XML Tree File Writing Abstract Class.
"""
from abc import ABCMeta, abstractmethod
from pathlib import Path
from xml.etree.ElementTree import ElementTree


class BaseXMLTree(metaclass=ABCMeta):
    """ A Base Abstract Class providing writing capabilities for an XML Tree class.
    """

    @abstractmethod
    def get_root(self) -> ElementTree:
        pass

    def write_tree(
        self, path: Path,
    ):
        """
        Write the Tree as XML to the given Path.
        """
        self.get_root().write(
            file_or_filename=path,
            encoding='utf-8',
            xml_declaration=True,
            method='xml',
        )
