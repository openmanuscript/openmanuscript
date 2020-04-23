"""
Returns corresponding objects to call for creating
the different docx elements.
"""

from .blockquote import BlockquoteDispatcher
from .code import CodeDispatcher 
from .emphasis import EmphasisDispatcher
from .heading import HeadingDispatcher 
from .linebreak import LineBreakDispatcher
from .link import LinkDispatcher 
from .list_item import ListItemDispatcher
from .paragraph import ParagraphDispatcher
from .strong import StrongDispatcher 
from .rule import HorizontalRuleDispatcher 
from .div import DivDispatcher 

def get_tag_dispatcher(html_tag):
    """
    Returning the object creating OOXML for the given HTML tag
    """
    # print("TAG: {}".format(html_tag))
    return _dispatch_html.get(html_tag)


# map of HTML tags and their corresponding objects
heading_dispatcher = HeadingDispatcher()

_dispatch_html = dict(
    div=DivDispatcher(),
    hr=HorizontalRuleDispatcher(),
    p=ParagraphDispatcher(),
    a=LinkDispatcher(),
    li=ListItemDispatcher(),
    br=LineBreakDispatcher(),
    code=CodeDispatcher(),
    strong=StrongDispatcher(),
    em=EmphasisDispatcher(),
    h1=heading_dispatcher,
    h2=heading_dispatcher,
    h3=heading_dispatcher,
    h4=heading_dispatcher,
    h5=heading_dispatcher,
    h6=heading_dispatcher,
    blockquote=BlockquoteDispatcher(),
)
