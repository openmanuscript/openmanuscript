from .tag import TagDispatcher, replace_whitespaces
from docx.oxml.shared import OxmlElement, qn

_list_style = {
    'ol': 'List Number',
    'ul': 'List Bullet'
}

class ListItemDispatcher(TagDispatcher):
    list_type = "List Number" 

    def __init__(self):
        super(ListItemDispatcher, self).__init__()

    @classmethod
    def append_head(cls, element, container):
        paragraph = cls.get_new_paragraph(container)

        # controlling the numbered list stuff
        # https://stackoverflow.com/questions/23446268/python-docx-how-to-restart-list-lettering 
        fmt = paragraph.paragraph_format
        numPr_elem = OxmlElement('w:numPr')
        ilvl_elem = OxmlElement('w:ilvl')
        ilvl_elem.set(qn('w:val'), str(0).encode("utf-8"))
        numId_elem = OxmlElement('w:numId')
        numId_elem.set(qn('w:val'), str(1).encode("utf-8"))

        fmt._element.pPr.append(numPr_elem)
        numPr_elem.append(ilvl_elem)
        numPr_elem.append(numId_elem)

        return cls._append_list_item(element, element.text, paragraph)

    @classmethod
    def append_tail(cls, element, container):
        paragraph = cls.get_current_paragraph(container)
        return cls._append_list_item(element, element.tail, paragraph)

    @classmethod
    def _append_list_item(cls, element, text, container):
        """
        <li> Create a list item element inside a docx container.
        Style it according to its parents list type.
        """
        text = replace_whitespaces(text)
        text = '' if text == ' ' else text

        if (element.getparent().tag == "ul"):
            ListItemDispatcher.list_type = "List Bullet" 
        elif (element.getparent().tag == "ol"):
            ListItemDispatcher.list_type = "List Number" 

        container.style = ListItemDispatcher.list_type
        container.add_run(text)

        return container
