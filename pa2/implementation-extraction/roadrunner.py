from RRHtmlParser import RRHtmlParser, Element
from copy import deepcopy


class RoadRunner():
    wrapper = None
    sample = None
    sample_idx = 0
    wrapper_idx = 0

    def __init__(self, wrapper_path, sample_path):
        parser1 = RRHtmlParser()
        html_data = parser1.preprocess_html_file(wrapper_path)
        parser1.feed(html_data)
        self.wrapper = deepcopy(parser1.data)
        parser = RRHtmlParser()
        html_data = parser.preprocess_html_file(sample_path)
        parser.feed(html_data)
        self.sample = deepcopy(parser.data[len(self.wrapper):])

    def __repr__(self):
        out = ''
        for el in self.wrapper:
            out += str(el) + '\n'
        return out

    def square_match(self, lower_idx, upper_idx, on_wrapper = True):
        """
        :param lower_idx: next_terminal_idx
        :param upper_idx: terminal_idx
        :return: boolean
        """
        data = self.wrapper if on_wrapper else self.sample
        square = []
        data_a = data[upper_idx+1:lower_idx+1]
        data_a.reverse()
        data_b = data[0:upper_idx+1]
        data_b.reverse()
        for lower_el, upper_el in zip(data_a, data_b):
            if lower_el.name == upper_el.name:
                square.append(lower_el)
                continue
            elif not lower_el.is_tag and not upper_el.is_tag and lower_el.name != upper_el.name:
                square.append(Element("#TEXT", None, False, False))
            else:
                return None

        square.reverse()
        return square

    def find_square(self):
        terminal_tag = self.wrapper[self.wrapper_idx - 1]
        #   next_terminal_idx = self.wrapper_idx + 1
        idx = self.wrapper_idx
        square = None
        w_flag = False

        # finding square in wrapper
        while idx < len(self.wrapper):
            if self.wrapper[idx].name == terminal_tag.name:
                square = self.square_match(idx, self.wrapper_idx - 1)
                if square is not None:
                    w_flag = True
                    break
            idx += 1

        # finding square in sample
        idx = self.sample_idx
        while idx < len(self.sample) and square is None:
            if self.sample[idx].name == terminal_tag.name:
                square = self.square_match(idx, self.sample_idx - 1, on_wrapper=False)
                if square is not None:
                    break
            idx += 1

        if square is None:  # we are at the end, must be optional
            return False

        square[0].is_square_start = True
        square[-1].is_square_end = True

        # TODO: handle idx na koncu wrapperja
        # finding the first and last occurence of square
        start_iterator_idx = self.wrapper_idx
        end_iterator_idx = start_iterator_idx # + len(square)

        while 0 <= start_iterator_idx:
            if self.wrapper[start_iterator_idx - len(square)].name != square[0].name:
                break
            start_iterator_idx -= len(square)

        while end_iterator_idx < len(self.wrapper):
            tmp_idx = end_iterator_idx + len(square) - (1 if w_flag else 0)
            if tmp_idx >= len(self.wrapper) or self.wrapper[tmp_idx].name != square[-1].name:
                break
            end_iterator_idx += len(square)

        # removing squares from wrapper
        for i in range(start_iterator_idx, end_iterator_idx):
            self.wrapper.pop(start_iterator_idx)
        # inserting square into wrapper
        for el in square:
            self.wrapper.insert(start_iterator_idx, el)
            start_iterator_idx += 1
        # set wrapper index on the end of square iterator
        self.wrapper_idx = start_iterator_idx

        #TODO: sample vrtenje idx naprej
        while True:
                tmp_idx = self.sample_idx + len(square) - 1
                if tmp_idx >= len(self.sample):
                    break
                elif self.sample[tmp_idx].name == terminal_tag.name:
                    self.sample_idx += len(square)
                else:
                    break
        return True

    def find_iterator(self):
        # prevous tags do not match, so we certainly are not on iterator
        if self.wrapper[self.wrapper_idx - 1].name != self.sample[self.sample_idx - 1].name:
            return False
        return self.find_square()

    def find_optional(self):
        for idx in range(self.wrapper_idx, len(self.wrapper)):
            if self.wrapper[idx].name == self.sample[self.sample_idx].name:
                for el in self.wrapper[self.wrapper_idx:idx]:
                    el.is_optional = True
                    self.wrapper_idx += 1
                return
        for idx in range(self.sample_idx, len(self.sample)):
            if self.sample[idx].name == self.wrapper[self.wrapper_idx].name:
                for el in self.sample[self.sample_idx:idx]:
                    el.is_optional = True
                    self.wrapper.insert(self.wrapper_idx, el)
                    self.wrapper_idx += 1
                    self.sample_idx += 1
                return

    def main(self):
        while self.wrapper_idx < len(self.wrapper) and self.sample_idx < len(self.sample):  # run until the end of either the wrapper or sample
            sample_element = self.sample[self.sample_idx]
            wrapper_element = self.wrapper[self.wrapper_idx]

            if sample_element.name == wrapper_element.name:  # check for tag mismatch, if the elements match, we continue
                self.wrapper_idx += 1
                self.sample_idx += 1  # increment indexes
                continue

                # elements do not match, we could have a string mismatch
                # or we have a tag mismatch, which could represent a iterator
                # or an optional element,

            if not sample_element.is_tag and not wrapper_element.is_tag and sample_element.name != wrapper_element.name:
                self.wrapper[self.wrapper_idx] = Element("#TEXT", None, False, False)  # Mark the element in the wrapper as a  # TEXT

                self.wrapper_idx += 1
                self.sample_idx += 1  # increment indexes

                # from here on, we either stumbled upon an optional element,
                # or an iterator. We first check whether the element is an iterator,
                # if its not, it must be an optional element.
            else:
                result = self.find_iterator()
                if not result:
                    self.find_optional()

# test pages
wrapper_path = './test_page_1.html'
sample_path = './test_page_2.html'

# alstore
#wrapper_path = '../input-extraction/altstore.si/Gaming prenosniki ASUS - AltStore.html'
#sample_path = '../input-extraction/altstore.si/Gaming prenosniki ACER - AltStore.html'

# rtv
#wrapper_path = '../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html'
#sample_path = '../input-extraction/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html'

# overstock
#wrapper_path = '../input-extraction/overstock.com/jewelry01.html'
#sample_path = '../input-extraction/overstock.com/jewelry02.html'


# TODO: fix optional only in one line ()?

if __name__ == '__main__':
    rr = RoadRunner(wrapper_path, sample_path)
    rr.main()
    with open('wrapper.html', 'w') as file:
        file.write(str(rr))
