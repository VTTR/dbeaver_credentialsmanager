import xml.etree.ElementTree as ET

class XMLHandler:
    def __init__(self, filepath: str) -> None:
        self.filepath : str = filepath
        self.xmldoc : ET = None
        self.allElements : list = []

    def _generateList(self) -> list:
        result = []
        for elem in self.xmldoc.iterfind(".//data-source"):
            d = {}
            d['name'] = elem.get('name')
            d['id'] = elem.get('id')
            d['user'] = elem.findall('.//connection')[0].get('user')
            d['password'] = elem.findall('.//connection')[0].get('password')
            result.append(d)
        return result
    
    def loadfile(self) -> None:
        self.xmldoc = ET.parse(self.filepath)
        self.allElements = self._generateList()

    def savefile(self) -> None:
        ET.ElementTree(self.xmldoc).write(self.filepath)

    def __str__(self) -> str:
        return f"XML-File ({self.filepath}) contains {len(self.allElements)} elements"
    
