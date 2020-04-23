from .tag import TagDispatcher

import docx
from docx.oxml.shared import OxmlElement, qn

class LinkDispatcher(TagDispatcher):
    def __init__(self):
        super(LinkDispatcher, self).__init__()

    @classmethod
    def append_head(cls, element, container):
        return cls._append_link(element.text, element.get("href"), container)

    @classmethod
    def append_tail(cls, element, container):
        # print("TAIL: {}".format(element.text))
        return cls._append_link(element.tail, container)

    @classmethod
    def _append_link(cls, text, href, container):
        """
        <a> creates a link element inside a docx container element.
        """
        # container.add_run("{} to {}".format(text, href))
        cls.add_hyperlink(container, href, text, None, None)
        return container


    # The following function adds a hyperlink. Thanks to:
    # https://stackoverflow.com/questions/48374357/how-to-add-hyperlink-to-an-image-in-python-docx 
    #
    @classmethod
    def add_hyperlink(csl, paragraph, url, text, color, underline):
        """
        A function that places a hyperlink within a paragraph object.

        :param paragraph: The paragraph we are adding the hyperlink to.
        :param url: A string containing the required url
        :param text: The text displayed for the url
        :return: The hyperlink object
        """

        # This gets access to the document.xml.rels file and gets a new relation id value
        part = paragraph.part
        r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

        # Create the w:hyperlink tag and add needed values
        hyperlink = docx.oxml.shared.OxmlElement('w:hyperlink')
        hyperlink.set(docx.oxml.shared.qn('r:id'), r_id, )

        # Create a w:r element
        new_run = docx.oxml.shared.OxmlElement('w:r')

        # Create a new w:rPr element
        rPr = docx.oxml.shared.OxmlElement('w:rPr')

        # Add color if it is given
        if not color is None:
          c = docx.oxml.shared.OxmlElement('w:color')
          c.set(docx.oxml.shared.qn('w:val'), color)
          rPr.append(c)

        # Remove underlining if it is requested
        if not underline:
          u = docx.oxml.shared.OxmlElement('w:u')
          u.set(docx.oxml.shared.qn('w:val'), 'none')
          rPr.append(u)

        # bold
        b = docx.oxml.shared.OxmlElement('w:b')
        rPr.append(b)

        # Join all the xml elements together add add the required text to the w:r element
        new_run.append(rPr)
        new_run.text = text
        new_run.bold = True
        hyperlink.append(new_run)

        paragraph._p.append(hyperlink)

        return
