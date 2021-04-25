from RRHtmlParser import RRHtmlParser, Element
from copy import deepcopy


class RoadRunner():
    def __init__(self):
        return

    def preprocess(self, wrapper_path, sample_path):
        parser1 = RRHtmlParser()
        html_data = parser1.preprocess_html_file(wrapper_path)
        parser1.feed(html_data)
        wrapper = deepcopy(parser1.data)
        parser = RRHtmlParser()
        html_data = parser.preprocess_html_file(sample_path)
        parser.feed(html_data)
        sample = deepcopy(parser.data[len(wrapper):])
        return wrapper, sample

    def __repr__(self):
        out = ''
        flag = False
        for el in self.wrapper:
            if el.is_square_start:
                flag = True
            elif el.is_square_end:
                flag = False
            out += str(el) + ('\n' if not flag else ' ')
        return out

    def recursion_handler(self, wrapper, w_idx, sample, s_idx):
        """
        The only purpose of this function is to not repeat the same code
        """
        if wrapper is None or sample is None:
            wrapper = self.wrapper
            w_idx = self.wrapper_idx
            sample = self.sample
            s_idx = self.sample_idx
        return wrapper, w_idx, sample, s_idx

    #TODO fix params
    def square_match(self, lower_idx, upper_idx, on_wrapper=True):
        """
        :param lower_idx: next_terminal_idx
        :param upper_idx: terminal_idx
        :param on_wrapper: search on wrapper or sample
        :return: None or tag list
        """
        data = self.wrapper if on_wrapper else self.sample
        square = []
        data_a = data[upper_idx+1:lower_idx+1]  # --------
        data_a.reverse()                        # so zip()
        data_b = data[0:upper_idx+1]            # works
        data_b.reverse()                        # --------
        for lower_el, upper_el in zip(data_a, data_b):
            if lower_el.name == upper_el.name:
                square.append(lower_el)
                continue
            elif not lower_el.is_tag and not upper_el.is_tag and lower_el.name != upper_el.name:
                square.append(Element("#TEXT", None, False, False))
            else:
                return None  # TODO: recursion!

        square.reverse()  # Putting square elements in correct order, since We were adding it in reverse
        return square

    def find_square(self, wrapper, w_idx, sample, s_idx):
        terminal_tag = wrapper[w_idx - 1]
        square = None
        w_flag = False

        # finding square in wrapper
        idx = w_idx  # We assume iterator continues on wrapper
        while idx < len(wrapper):
            if wrapper[idx].name == terminal_tag.name:  # We found another terminal tag on wrapper
                square = self.square_match(idx, wrapper, w_idx - 1)  # We try to match square
                if square is not None:
                    w_flag = True  # We found it on wrapper!
                    break
            idx += 1

        # finding square in sample
        idx = s_idx  # We assume iterator continues on sample
        while idx < len(sample) and square is None:
            if sample[idx].name == terminal_tag.name:  # we found another terminal tag on sample
                square = self.square_match(idx, sample, s_idx - 1)  # We try to match square
                if square is not None:
                    break  # We found it on sample!
            idx += 1

        if square is None:  # We didn't find a square so it must be an optional
            return False

        square[0].is_square_start = True
        square[-1].is_square_end = True

        # TODO: handle idx na koncu wrapperja
        # finding the first and last occurence of square
        start_iterator_idx = self.wrapper_idx
        end_iterator_idx = start_iterator_idx  # + len(square)

        while 0 <= start_iterator_idx:
            if self.wrapper[start_iterator_idx - len(square)].name != square[0].name:
                break
            start_iterator_idx -= len(square)

        while end_iterator_idx < len(self.wrapper):
            tmp_idx = end_iterator_idx + len(square) - (1 if w_flag else 0)  # For any future questions: Just because!
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

    def find_other_squares(self):
        pass

    def find_iterator(self, wrapper, w_idx, sample, s_idx):
        if wrapper[w_idx - 1].name != sample[s_idx - 1].name:
            # prevous tags do not match, so we certainly are not on iterator
            return wrapper, w_idx, sample, s_idx, False
        result = self.find_square(wrapper, w_idx, sample, s_idx)
        if result:
            # looks like square was found, we search for previous/further squares in wrapper
            # and remove them with found square representing an iterator
            self.find_other_squares()
            #TODO: delete squares from wrapper
        return True

    def find_optional(self, wrapper, w_idx, sample, s_idx):
        for idx in range(w_idx, len(wrapper)):
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

    def main(self, wrapper, wrapper_idx, sample, sample_idx):
        # run until the end of either the wrapper or sample
        while wrapper_idx < len(wrapper) and sample_idx < len(sample):
            wrapper_element = wrapper[wrapper_idx]
            sample_element = sample[sample_idx]

            if wrapper_element.name == sample_element.name:
                # check for tag mismatch, if the elements match, we continue
                wrapper_idx += 1
                sample_idx += 1
                continue

            elif not wrapper_element.is_tag and not sample_element.is_tag and wrapper_element.name != sample_element.name:
                # elements do not match, we could have a string mismatch
                # or we have a tag mismatch, which could represent a iterator
                # or an optional element,
                wrapper_element[wrapper_idx] = Element("#TEXT", None, False, False)  # Mark the element in the wrapper as a  # TEXT

            else:
                # from here on, we either stumbled upon an optional element,
                # or an iterator. We first check whether the element is an iterator,
                # if its not, it must be an optional element.
                wrapper, wrapper_idx, sample, sample_idx, result = self.find_iterator(wrapper, wrapper_idx, sample, sample_idx)
                if not result:
                    self.find_optional(wrapper, wrapper_idx, sample, sample_idx)


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
    with open('../implementation-extraction/wrapper.html', 'w') as file:
        file.write(str(rr))

"""
ROAD_RUNNER IDEA

class Road_runner
    __init__():
        idx = 0    
        parse HTML
        self.wrapper <- wrapper_html_parser
        self.sample <- sample_html_parser


    main(wrapper=self.wrapper_list, sample=self.sample_list)
        while loop:
            tag mismatch check
            
            text mismatch check
            
            if iterator <- find iterator
                must be optional
                    
        return ? wrapper probably        

"""