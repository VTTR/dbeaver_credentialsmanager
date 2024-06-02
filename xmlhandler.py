import xml.etree.ElementTree as ET

class XMLHandler:
    def __init__(self, filepath: str) -> None:
        self.filepath : str = filepath
        self.xmldoc : ET = None
        self.allElements : dict = []

    def _generateDict(self) -> dict:
        result = {}
        for elem in self.xmldoc.iterfind(".//data-source"):
            id: str = elem.get('id')
            result[id] = {}
            result[id]['name'] = elem.get('name')
            result[id]['user'] = elem.findall('.//connection')[0].get('user')
            result[id]['password'] = elem.findall('.//connection')[0].get('password')
        print(result)
        return result
    
    def loadfile(self) -> None:
        self.xmldoc = ET.parse(self.filepath)
        self.allElements = self._generateDict()

    def savefile(self) -> None:
        ET.ElementTree(self.xmldoc).write(self.filepath)

    def __str__(self) -> str:
        return f"XML-File ({self.filepath}) contains {len(self.allElements)} elements"
    
