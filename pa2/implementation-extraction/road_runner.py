import lxml
import lxml.etree


def preprocess_html(path):
    tree = lxml.etree.parse(path, lxml.etree.HTMLParser(remove_comments=True))
    head = tree.xpath('.//head')[0]
    tree.getroot().remove(head)

    def walk(node):
        cleaner_tag = ['img', 'script', 'input', 'button', 'select', 'style']
        cleaner_attrib = ['href', 'style', 'click-event', 'event-payload', 'rel',
                          'js-id', 'role', 'tabindex', 'aria-live', 'aria-relevant',
                          'align', 'valign', 'nowrap', 'colspan', 'bgcolor',
                          'height', 'width', 'border', 'cellpadding', 'cellspacing',
                          'shape', 'coords', 'target', 'onmouseover', 'topmargin', 'onload',
                          'leftmargin', 'rightmargin', 'marginwidth', 'marginheight', 'text']
        if node.tag in cleaner_tag:
            node.getparent().remove(node)
            return
        for attrib in cleaner_attrib:
            if attrib in node.attrib:
                node.attrib.pop(attrib)
        for child in node:
            walk(child)

    walk(tree.getroot())
    return tree


def road_runner(page1, page2):
    pass


if __name__ == '__main__':
    path = '../input-extraction/altstore.si/Gaming prenosniki ASUS - AltStore.html'
    path = '../input-extraction/overstock.com/jewelry01.html'
    path = '../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html'
    body1 = preprocess_html(path)
    print(lxml.etree.tounicode(body1))
    body1.write('temp.html', pretty_print=True)