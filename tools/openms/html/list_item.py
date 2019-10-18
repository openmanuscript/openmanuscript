from .tag import TagDispatcher, replace_whitespaces

_list_style = dict(
    ol='List Number',
    ul='List Bullet'
)

class ListItemDispatcher(TagDispatcher):
    def __init__(self):
        super(ListItemDispatcher, self).__init__()

    @classmethod
    def append_head(cls, element, container):
        paragraph = cls.get_new_paragraph(container)
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

        container.style = _list_style.get(element.getparent().tag, 
                                            'List Bullet')
        container.add_run(text)

        return container
