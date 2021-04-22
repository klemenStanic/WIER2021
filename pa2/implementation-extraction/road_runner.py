import lxml
import lxml.etree
import copy


def preprocess_html(path):
    tree = lxml.etree.parse(path, lxml.etree.HTMLParser(remove_comments=True))
    head = tree.xpath('.//head')[0]
    tree.getroot().remove(head)

    def walk(node):
        cleaner_tag = ['img', 'script', 'input', 'button', 'select', 'style', 'iframe', 'form', 'figure', 'svg']
        cleaner_attrib = ['href', 'style', 'click-event', 'event-payload', 'rel', 'aria-expanded',
                          'js-id', 'role', 'tabindex', 'aria-live', 'aria-relevant', 'aria-haspopup',
                          'align', 'valign', 'nowrap', 'colspan', 'bgcolor', 'onclick', 'aria-hidden',
                          'height', 'width', 'border', 'cellpadding', 'cellspacing', 'aria-labelledby',
                          'shape', 'coords', 'target', 'onmouseover', 'topmargin', 'onload', 'data-locked',
                          'leftmargin', 'rightmargin', 'marginwidth', 'marginheight', 'text', 'data-commentsdisabled',
                          'data-toggle', 'data-target', 'ref', 'data-newsid', 'data-commentid', 'data-commentsmoderated']
        if 'id' in node.attrib and 'bar-share-icons' == node.attrib['id']:
            print("hoy")
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


def compare_node(node1, node2):
    if node1.tag != node2.tag:
        return False
    if len(node1.attrib) != len(node2.attrib):
        return False
    for att in node1.attrib:
        if att not in node2.attrib:
            return False
        elif node1.attrib[att] != node2.attrib[att]:
            return False
    return True


def road_runner(wrapper_page, comparison_page):
    """
    Each page (wrapper and comparison) have their own 2 queues. At each iteration we take nodes from one (picking) queue and fill the other.
    At the end of each iteration we switch these queues.
    :param wrapper_page:
    :param comparison_page:
    :return:
    """
    wrapper_queue = [[wrapper_page.getroot()], []]
    comparison_queue = [[comparison_page.getroot()], []]
    q_idx = 0

    while max(len(wrapper_queue[0]), len(wrapper_queue[1]), len(comparison_queue[0]), len(comparison_queue[1])) > 0:  # stops when all 4 queues are empty
        fill_idx = (q_idx + 1) % 2  # we are filling the other queue
        while min(len(wrapper_queue[q_idx]), len(comparison_queue[q_idx])) > 0:  # stops whene one picking queue is empty
            wrapper_node = wrapper_queue[q_idx].pop(0)
            comparison_node = comparison_queue[q_idx].pop(0)
            comp_result = compare_node(wrapper_node, comparison_node)


        queue_idx = fill_idx


if __name__ == '__main__':
    path_altstore1 = '../input-extraction/altstore.si/Gaming prenosniki ASUS - AltStore.html'
    path_overstock1 = '../input-extraction/overstock.com/jewelry01.html'
    path_rtv1 = '../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html'
    path_rtv2 = '../input-extraction/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html'

    body1 = preprocess_html(path_rtv1)
    body2 = preprocess_html(path_rtv2)

    road_runner(body1, body2)

    # print(lxml.etree.tounicode(body1))
    # body1.write('test_page_1.html', pretty_print=True)
