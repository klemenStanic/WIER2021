# WIER 2021: Programming assignment 2, Report
Klemen Stanič, 63150267 \
Luka Kavčič, 63150139


## 1. Introduction

## 2. Implementation
### I. Two additional web pages
The two additional web pages were selected from the site *altstore.si*. A data record and the data items within are presented in following image. 

![Altstore.si data record](AltStore_Data_record.png)

### II. Regular expressions implementation
```
RTV:
 Author: re.search('<div class="author-name">(?P<Author>.*?)</div>', html)
 PublishedTime: re.search('<div class="publish-meta">(?P<PublishedTime>(.|\s)*?)<br>', html)
 Title: re.search("<h1>(?P<Title>.*?)</h1>", html)
 SubTitle: re.search('<div class="subtitle">(?P<SubTitle>(.|\s)*?)</div>', html)
 Lead: re.search('<p class="lead">(?P<Lead>(.|\s)*?)</p>', html)
 Content: re.search('<article class="article">(?P<Content>(.|\s)*?)</article>', html)

Overstock:
 All data records: re.findall('<td valign="top">..<a.*?</tbody></table></td>', html, flags=re.S)
 Within a single data record:
  Title: re.search('<a href=".*?<b>(?P<Title>.*?)</b>', el)
  ListPrice: re.search('<b>List Price:</b>.*<s>(?P<ListPrice>.*?)</s>', el)
  Price: re.search('<b>Price:</b>.*?<b>(?P<Price>.*?)</b>', el)
  Saving: re.search('<b>You Save:</b>.*?littleorange">(?P<Saving>.*) \(', el)
  SavingPercent: re.search('<b>You Save:</b>.*?littleorange">.*?\\((?P<SavingPercent>.*)\)', el)
  Content: re.search('<td valign="top"><span class="normal">(?P<Content>.*?)<br>', el, flags=re.S)

Altstore:
 All data records: re.findall('<div class="card .*?</div>.</div>', html, flags=re.S)
 Within a single data record:
  Title: re.search('<h4 class="fixed-lines-2"><a href.*?">(?P<Title>.*?)</a></h4>', el)
  Price: re.search('<span class="old-price">(?P<Price>.*?)</span>', el)
  ListPrice: re.search('<span class="new-price">(?P<ListPrice>.*?)</span>', el)
  Description: re.search('<small class="options_list">(?P<Description>.*?)</small>', el)
  Storage: re.search('<div class="stock-info.*?<span>.(?P<Storage>.*?)<a href', el, flags=re.S)
```

### III. XPath implementation:
```
RTV:
 Author: tree.xpath('.//div[@class="author-name"]')[0].text
 PublishedTime: tree.xpath('.//div[@class="publish-meta"]')[0].text.split('<br>')[0].strip()
 Title: tree.xpath('.//h1')[0].text
 SubTitle: tree.xpath('.//div[@class="subtitle"]')[0].text
 Lead: tree.xpath('.//p[@class="lead"]')[0].text
 Content: tree.xpath('.//article[@class="article"]')[0]

Overstock:
 All data records: tree.xpath('/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td')
 Within a single data record:
  Title: item.xpath('.//a/b')[0].text
  Price: item.xpath('.//tr/td/s')[0].text
  ListPrice: item.xpath('.//tr/td/span/b')[0].text
  Saving: item.xpath('.//tr/td/span[@class="littleorange"]')[0].text.split(' ')[0]
  SavingPercent: saving[1].replace('(', '').replace(')', '')
  Content: item.xpath('.//table/tbody/tr/td/span')[2].text

Altstore:
 All data records: tree.xpath('.//div[@class="card "]'):
 Within a single data record:
  Title: item.xpath('.//h4[@class="fixed-lines-2"]/a')[0].text
  Price: item.xpath('.//span[@class="old-price"]')[0].text
  ListPrice: item.xpath('.//span[@class="new-price"]')[0].text
  Description: item.xpath('.//small[@class="options_list"]')
  Storage: item.xpath('.//div[2]/span')[0].text.strip()
```

### IV. RoadRunner implementation:
```
wrapper_index, sample_index = 0                                                                       # initialize indexes
while wrapper_index is not equal to wrapper.length and sample_index is not equal to sample.length:    # run until the end of either the wrapper or sample
    sample_element = sample[sample_index]
    wrapper_element = wrapper[sample_index]
    
    if sample_element is equal to wrapper_element:                                                    # check for tag mismatch, if the elements match, we continue 
        wrapper_index, sample_index ++                                                                # increment indexes
        continue

                                                                                                      # elements do not match, we could have a string mismatch
                                                                                                      # or we have a tag mismatch, which could represent a iterator
                                                                                                      # or an optional element, 
    
    if sample_element is not a tag and wrapper_element is not a tag:
        Mark the element in the wrapper as a #TEXT
    
                                                                                                      # from here on, we either stumbled upon an optional element,
                                                                                                      # or an iterator. We first check whether the element is an iterator,
                                                                                                      # if its not, it must be an optional element.
    if find_the_iterator returns false:
        find_the_optional
```
## 3. Results
Wrapper outputs are attached to the end of this report.

## 4. Conclusions


## 5. Wrapper outputs:
### rtvslo.si

### overstock.com

### altsore.si