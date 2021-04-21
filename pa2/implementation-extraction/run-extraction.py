import regexp_extraction
import xpath_extraction
import sys


def main():
    if sys.argv[1] == "A":
        regexp_extraction.run_regex()
    elif sys.argv[1] == "B":
        xpath_extraction.run_xpath()
    elif sys.argv[1] == "C":
        pass


if __name__ == "__main__":
    main()
