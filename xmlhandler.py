import xml.etree.ElementTree as ET

class XMLHandler:
    def __init__(self, filepath: str = None) -> None:
        self.filepath : str = filepath
        self.xmldoc : ET = None
        self.allElements : dict = {}

    def _generateDict(self) -> dict:
        result = {}
        for elem in self.xmldoc.iterfind(".//data-source"):
            id: str = elem.get('id')
            result[id] = {}
            result[id]['name'] = elem.get('name')
            result[id]['user'] = elem.findall('.//connection')[0].get('user')
            result[id]['password'] = elem.findall('.//connection')[0].get('password')
        return result

    def updateDict(self) -> None:
        self.allElements = self._generateDict()

    def updateDictAfterProcessing(func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs )
            self.updateDict()
        return wrapper

    @updateDictAfterProcessing
    def setUser(self, id: str, newUser: str) -> None:
        if id not in self.allElements: raise NameError(f'{id} not in xml')
        element = self.xmldoc.find(f".//data-source[@id='{id}']/connection")
        element.set('user', newUser)


    @updateDictAfterProcessing
    def setPassword(self, id: str, newPassword: str) -> None:
        if id not in self.allElements: raise NameError(f'{id} not in xml')
        element = self.xmldoc.find(f".//data-source[@id='{id}']/connection")
        element.set('password', newPassword)

    def setPath(self, newPath: str) -> None:
        self.filepath = newPath

    @updateDictAfterProcessing
    def loadfile(self) -> None:
        self.xmldoc = ET.parse(self.filepath)

    def savefile(self) -> None:
        ET.ElementTree(self.xmldoc).write(self.filepath)

    def __str__(self) -> str:
        return f"XML-File ({self.filepath}) contains {len(self.allElements)} elements"

    def __len__(self) -> int:
        return len(self.allElements)
