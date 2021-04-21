import re
import json
import codecs

json_rtv = {
    "Author": "",
    "PublishedTime": "",
    "Title": "",
    "SubTitle": "",
    "Lead": "",
    "Content": ""
}

json_overstock = {
    "Title": "",
    "ListPrice": "",
    "Price": "",
    "Saving": "",
    "SavingPercent": "",
    "Content": ""
}

json_altstore = {
    "Title": "",
    "Price": "",
    "ListPrice": "",
    "Description": "",
    "Storage": ""
}


def read_file(path, encoding):
    with codecs.open(path, encoding=encoding) as file:
        content = file.readlines()
    return "".join(content)


def extract_rtv_regexp(html):
    """
    Extracts and prints the content of the webpage rtv.si.
    :param html: HTML page content
    :return: None
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

    print(json.dumps(json_rtv, indent=4, ensure_ascii=False))


def extract_overstock_regexp(html):
    """
        Extracts and prints the content of the overstock webpage.
        :param html: HTML page content
        :return: None
        """
    out = []
    results = re.findall('<td valign="top">..<a.*?</tbody></table></td>', html, flags=re.S)
    for el in results:
        item = {}
        res = re.search('<a href=".*?<b>(?P<Title>.*?)</b>', el)
        Title = res.groupdict()["Title"].strip()
        item["Title"] = Title

        res = re.search('<b>List Price:</b>.*<s>(?P<ListPrice>.*?)</s>', el)
        ListPrice = res.groupdict()["ListPrice"].strip()
        item["ListPrice"] = ListPrice

        res = re.search('<b>Price:</b>.*?<b>(?P<Price>.*?)</b>', el)
        Price = res.groupdict()["Price"].strip()
        item["Price"] = Price

        res = re.search('<b>You Save:</b>.*?littleorange">(?P<Saving>.*) \(', el)
        Saving = res.groupdict()["Saving"].strip()
        item["Saving"] = Saving

        res = re.search('<b>You Save:</b>.*?littleorange">.*?\((?P<SavingPercent>.*)\)', el)
        SavingPercent = res.groupdict()["SavingPercent"].strip()
        item["SavingPercent"] = SavingPercent

        res = re.search('<td valign="top"><span class="normal">(?P<Content>.*?)<br>', el, flags=re.S)
        Content = res.groupdict()["Content"].strip()
        item["Content"] = Content

        out.append(item)

    print(json.dumps(out, indent=4, ensure_ascii=False))


def extract_altstore_regexp(html):
    """
        Extracts and prints the content of the altstore webpage.
        :param html: HTML page content
        :return: None
    """
    out = []
    results = re.findall('<div class="card .*?</div>.</div>', html, flags=re.S)
    for el in results:
        item = {}
        res = re.search('<h4 class="fixed-lines-2"><a href.*?">(?P<Title>.*?)</a></h4>', el)
        Title = res.groupdict()["Title"].strip()
        item["Title"] = Title

        res = re.search('<span class="old-price">(?P<Price>.*?)</span>', el)
        Price = res.groupdict()["Price"].strip()
        item["Price"] = Price

        res = re.search('<span class="new-price">(?P<ListPrice>.*?)</span>', el)
        ListPrice = res.groupdict()["ListPrice"].strip()
        item["ListPrice"] = ListPrice

        res = re.search('<small class="options_list">(?P<Description>.*?)</small>', el)
        Description = res.groupdict()["Description"].strip().replace("<br>", "\n")
        item["Description"] = Description

        res = re.search('<div class="stock-info.*?<span>.(?P<Storage>.*?)<a href', el, flags=re.S)
        Storage = res.groupdict()["Storage"].strip()
        item["Storage"] = Storage

        out.append(item)

    print(json.dumps(out, indent=4, ensure_ascii=False))


def clean_content(content):
    clean = re.compile('<script(.|\s)*?</script>', flags=re.MULTILINE)
    content = re.sub(clean, '', content)

    clean = re.compile('<figure(.|\s)*?</figure>', flags=re.MULTILINE)
    content = re.sub(clean, '', content)

    clean = re.compile('<div class="gallery(.|\s)*?</div>', flags=re.MULTILINE)
    content = re.sub(clean, '', content)

    clean = re.compile('\s\s+', flags=re.MULTILINE)
    content = re.sub(clean, '', content)

    clean = re.compile('<.*?>', flags=re.MULTILINE)
    content = re.sub(clean, '', content)
    return content


def run_regex():
    # RTV SLO
    content = read_file(
        "../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html", "utf-8")
    extract_rtv_regexp(content)

    print(" ------------------------------------ ")

    content = read_file(
        "../input-extraction/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html",
        "utf-8")
    extract_rtv_regexp(content)

    print(" ------------------------------------ ")
    print(" ------------------------------------ ")

    # overstock
    content = read_file(
        "../input-extraction/overstock.com/jewelry01.html", "iso-8859-1")
    extract_overstock_regexp(content)

    print(" ------------------------------------ ")

    content = read_file(
        "../input-extraction/overstock.com/jewelry02.html", "iso-8859-1")
    extract_overstock_regexp(content)

    print(" ------------------------------------ ")
    print(" ------------------------------------ ")

    # Altstore
    content = read_file(
        "../input-extraction/altstore.si/Gaming prenosniki ACER - AltStore.html", "utf-8")
    extract_altstore_regexp(content)

    print(" ------------------------------------ ")

    content = read_file(
        "../input-extraction/altstore.si/Gaming prenosniki ASUS - AltStore.html", "utf-8")
    extract_altstore_regexp(content)
