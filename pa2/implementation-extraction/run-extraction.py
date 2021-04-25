import regexp_extraction
import xpath_extraction
import road_runner
import sys


def main():
    if sys.argv[1] == "A":
        regexp_extraction.run_regex()
    elif sys.argv[1] == "B":
        xpath_extraction.run_xpath()
    elif sys.argv[1] == "C":
        # test pages
        # wrapper_path = '../input-extraction/test_pages/test_page_1.html'
        # sample_path = '../input-extraction/test_pages/test_page_2.html'

        # alstore
        wrapper_path = '../input-extraction/altstore.si/Gaming prenosniki ASUS - AltStore.html'
        sample_path = '../input-extraction/altstore.si/Gaming prenosniki ACER - AltStore.html'
        print("RoadRunner - Ran on altstore: ")
        rr = road_runner.RoadRunner(wrapper_path, sample_path)
        rr.main()
        print(str(rr))
        print("------------------------------------------")

        # rtv
        wrapper_path = '../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html'
        sample_path = '../input-extraction/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html'
        print("RoadRunner - Ran on rtvslo.si: ")
        rr = road_runner.RoadRunner(wrapper_path, sample_path)
        rr.main()
        print(str(rr))
        print("------------------------------------------")

        # overstock
        wrapper_path = '../input-extraction/overstock.com/jewelry01.html'
        sample_path = '../input-extraction/overstock.com/jewelry02.html'
        print("RoadRunner - Ran on overstock: ")
        rr = road_runner.RoadRunner(wrapper_path, sample_path)
        rr.main()
        print(str(rr))
        print("------------------------------------------")


if __name__ == "__main__":
    main()
