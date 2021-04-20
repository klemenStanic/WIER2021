import re
import sys
import json

json_rtv = {
    "Author": "",
    "PublishedTime": "",
    "Title": "",
    "SubTitle": "",
    "Lead": "",
    "Content": ""
}


def read_file(path):
    content = ""
    with open(path, "r") as file:
        content = file.readlines()
    return "".join(content)


def extract_rtv_regexp(html):
    """
    Do extraction.
    :param html:
    :return:
    """
    res = re.search('<div class="author-name">(?P<Author>.*?)</div>', html)
    Author = res.groupdict()["Author"].strip()

    res = re.search('<div class="publish-meta">(?P<PublishedTime>(.|\s)*?)<br>', html)
    PublishedTime = res.groupdict()["PublishedTime"].strip()

    res = re.search("<h1>(?P<Title>.*?)</h1>", html)
    Title = res.groupdict()["Title"].strip()

    res = re.search('<div class="subtitle">(?P<SubTitle>(.|\s)*?)</div>', html)
    SubTitle = res.groupdict()["SubTitle"].strip()

    res = re.search('<p class="lead">(?P<Lead>(.|\s)*?)</p>', html)
    Lead = res.groupdict()["Lead"].strip()

    res = re.search('<article class="article">(?P<Content>(.|\s)*?)</article>', html)
    Content = res.groupdict()["Content"].strip()

    json_rtv["Author"] = Author
    json_rtv["PublishedTime"] = PublishedTime
    json_rtv["Title"] = Title
    json_rtv["SubTitle"] = SubTitle
    json_rtv["Lead"] = Lead

    json_rtv["Content"] = clean_content(Content)

    print(json.dumps(json_rtv, indent=4, sort_keys=True).encode("utf8").decode("utf8"))


def clean_content(content):
    clean = re.compile('<script(.|\s)*?</script>', flags=re.MULTILINE)
    content = re.sub(clean, '', content)

    clean = re.compile('<figure(.|\s)*?</figure>', flags=re.MULTILINE)
    content = re.sub(clean, '', content)

    clean = re.compile('<div class="gallery(.|\s)*?</div>', flags=re.MULTILINE)
    content = re.sub(clean, '', content)

    clean = re.compile('\s\s+', flags=re.MULTILINE)
    content = re.sub(clean, '', content)

    clean = re.compile('<.*?>')
    content = re.sub(clean, '', content)
    return content


def main():
    if sys.argv[1] == "A":
        content = read_file(
            "../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html")
        extract_rtv_regexp(content)

        print(" ------------------------------------ ")

        content = read_file(
            "../input-extraction/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html")
        extract_rtv_regexp(content)







if __name__ == "__main__":
    main()
