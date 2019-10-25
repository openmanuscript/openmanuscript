from docx.enum.text import WD_BREAK

from .tag import TagDispatcher, replace_whitespaces

class HorizontalRuleDispatcher(TagDispatcher):
    def __init__(self):
        super(HorizontalRuleDispatcher, self).__init__()

    @classmethod
    def append_head(cls, element, container):
        return cls._append_horizontal_rule(element, container)

    @classmethod
    def append_tail(cls, element, container):
        pass

    @classmethod
    def _append_horizontal_rule(cls, element, container):
        """
        <hr> Creates a horizontal rule 
        """
        return container
