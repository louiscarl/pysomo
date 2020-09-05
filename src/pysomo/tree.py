import xml.etree.ElementTree as ET

from .figures import Figure


class Root(object):
    def __init__(self, child: Figure):
        self.children = [child]

    def to_xcsg(self) -> ET.Element:
        """Recursively builds the xml as xcsg.
        """
        e = ET.Element('xcsg', {'version': '1.0'})
        for c in self.children:
            c.__sub_element__(e)
        return e

    def dump_xcsg(self) -> str:
        return ET.tostring(self.to_xcsg(), encoding='utf8').decode('utf8')
