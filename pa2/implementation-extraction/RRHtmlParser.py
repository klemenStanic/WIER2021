from lxml import etree
from html.parser import HTMLParser
from bs4 import BeautifulSoup


class Element:
    is_square_start = False
    is_square_end = False
    is_optional = False

    def __init__(self, name, attrs, is_tag, is_end_tag):
        self.name = name
        self.attrs = attrs
        self.is_tag = is_tag
        self.is_end_tag = is_end_tag

    def __repr__(self):
        attrs = ' '
        if self.attrs is not None:
            for k in self.attrs:
                attrs += f'{k} '
        if self.is_optional:
            return f'({self.name}{attrs})?'
        elif self.is_square_start:
            return f'({self.name}{attrs}'
        elif self.is_square_end:
            return f'{self.name}{attrs})+'
        else:
            return self.name

    def __eq__(self, other):
        if self.name != other.name:
            return False
        elif self.attrs != other.attrs:
            return False
        else:
            return True


class RRHtmlParser(HTMLParser):
    data = []

    def handle_starttag(self, tag, attrs):
        self.data.append(Element("<"+ tag+ ">", attrs, True, False))

    def handle_endtag(self, tag):
        self.data.append(Element("</" + tag + ">", None, True, True))

    def handle_data(self, data):
        if data.strip() != '':
            self.data.append(Element(data, None, False, False))

    def preprocess_html_file(self, file_path):
        tree = etree.parse(file_path, etree.HTMLParser())
        head = tree.xpath('.//head')
        if len(head) > 0:
            tree.getroot().remove(head[0])

        def walk(node):
            cleaner_tag = ['script', 'input', 'button', 'select', 'style', 'iframe', 'form', 'figure', 'svg']
            cleaner_attrib = ['href', 'style', 'click-event', 'event-payload', 'rel', 'aria-expanded',
                              'js-id', 'role', 'tabindex', 'aria-live', 'aria-relevant', 'aria-haspopup',
                              'align', 'valign', 'nowrap', 'colspan', 'bgcolor', 'onclick', 'aria-hidden',
                              'height', 'width', 'border', 'cellpadding', 'cellspacing', 'aria-labelledby',
                              'shape', 'coords', 'target', 'onmouseover', 'topmargin', 'onload', 'data-locked',
                              'leftmargin', 'rightmargin', 'marginwidth', 'marginheight', 'text',
                              'data-commentsdisabled',
                              'data-toggle', 'data-target', 'ref', 'data-newsid', 'data-commentid',
                              'data-commentsmoderated']
            cleaner_attrib = []
            if node.tag in cleaner_tag:
                node.getparent().remove(node)
                return
            for attrib in cleaner_attrib:
                if attrib in node.attrib:
                    node.attrib.pop(attrib)
            for child in node:
                walk(child)

        walk(tree.getroot())  # cleanup and convert it to XHTML
        html_data = etree.tounicode(tree.getroot(), pretty_print=True, method='html').replace('\n', '').replace('\t', '')
        soup = BeautifulSoup(html_data, 'lxml')
        return str(soup)


if __name__ == '__main__':
    html_parser = RRHtmlParser()
    html_data = html_parser.preprocess_html_file('./test_page_1.html')
    html_parser.feed(html_data)

#    for i in html_parser.data:
#        print(i)
