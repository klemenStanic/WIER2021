import lxml
import lxml.etree
import re


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


def extract_rtvslo_xpath(path):
    data = dict()
    tree = lxml.etree.parse(path, lxml.etree.HTMLParser())
    data['Author'] = tree.xpath('.//div[@class="author-name"]')[0].text
    data['PublishedTime'] = tree.xpath('.//div[@class="publish-meta"]')[0].text.split('<br>')[0].strip()
    data['Title'] = tree.xpath('.//h1')[0].text
    data['SubTitle'] = tree.xpath('.//div[@class="subtitle"]')[0].text
    data['Lead'] = tree.xpath('.//p[@class="lead"]')[0].text
    data['Content'] = tree.xpath('.//article[@class="article"]')[0]
    data['Content'] = clean_content(lxml.etree.tounicode(data['Content']))
    print(data)


def extract_overstock_xpath(path):
    data = []
    tree = lxml.etree.parse(path, lxml.etree.HTMLParser())

    list_selector = '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td'
    for item in tree.xpath(list_selector):
        try:
            data_item = dict()
            data_item['Title'] = item.xpath('.//a/b')[0].text
            data_item['Price'] = item.xpath('.//tr/td/s')[0].text
            data_item['ListPrice'] = item.xpath('.//tr/td/span/b')[0].text
            saving = item.xpath('.//tr/td/span[@class="littleorange"]')[0].text.split(' ')
            data_item['Saving'] = saving[0]
            data_item['SavingPercent'] = saving[1].replace('(', '').replace(')', '')
            data_item['Content'] = item.xpath('.//table/tbody/tr/td/span')[2].text
            data.append(data_item)
        except Exception as e:
            continue

    for i in data:
        print(i)


def extract_altstore_path(path):
    data = []
    tree = lxml.etree.parse(path, lxml.etree.HTMLParser())

    for item in tree.xpath('.//div[@class="card "]'):
        data_item = dict()
        data_item['Title'] = item.xpath('.//h4[@class="fixed-lines-2"]/a')[0].text
        data_item['Price'] = item.xpath('.//span[@class="old-price"]')[0].text
        data_item['ListPrice'] = item.xpath('.//span[@class="new-price"]')[0].text
        data_item['Description'] = clean_content(lxml.etree.tounicode(item.xpath('.//small[@class="options_list"]')[0]))
        data_item['Storage'] = item.xpath('.//div[2]/span')[0].text.strip()
        data.append(data_item)

    for i in data:
        print(i)


def run_xpath():
    extract_rtvslo_xpath(
        '../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html')
    extract_rtvslo_xpath(
        '../input-extraction/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html')

    extract_overstock_xpath('../input-extraction/overstock.com/jewelry01.html')
    extract_overstock_xpath('../input-extraction/overstock.com/jewelry02.html')

    extract_altstore_path('../input-extraction/altstore.si/Gaming prenosniki ACER - AltStore.html')
    extract_altstore_path('../input-extraction/altstore.si/Gaming prenosniki ASUS - AltStore.html')
