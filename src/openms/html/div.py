from docx.enum.text import WD_BREAK

from .tag import TagDispatcher, replace_whitespaces
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

class DivDispatcher(TagDispatcher):
    def __init__(self):
        super(DivDispatcher, self).__init__()

    @classmethod
    def append_head(cls, element, container):
        # print("DIV Head")
        # print(" class={}".format(element.get("class")))
        if (element.get("class") == "footnote"):
            newp = cls.get_new_paragraph(container)
            newp = cls.get_new_paragraph(container)
            newp = cls.get_new_paragraph(container)
            pf = newp.paragraph_format
            pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
            pf.first_line_indent = Inches(0.0)
            # paragraph.add_run().add_break(WD_BREAK.PAGE)
            run = newp.add_run("Notes")
            run.bold = True
            container = newp
        return cls._append_div(element, container)

    @classmethod
    def append_tail(cls, element, container):
        pass

    @classmethod
    def _append_div(cls, element, container):
        """
        <div> Inspects a div element 
        """
        return container
