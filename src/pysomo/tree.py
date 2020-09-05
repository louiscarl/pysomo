from lxml import etree
from .figures import Figure

class Root(object):
    def __init__(self, child: Figure):
        self.children = [child]

    def to_xcsg(self) -> etree.Element:
        """Recursively builds the xml as xcsg.
        """
        e = etree.Element('xcsg', {'version': '1.0'})
        for c in self.children:
            c.__sub_element__(e)
        return e

    def dump_xcsg(self) -> str:
        return etree.tostring(self.to_xcsg(), encoding='utf8').decode('utf8')
