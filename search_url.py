#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
from multiprocessing import Pool
from multiprocessing import Process
import urllib2
import argparse
import re


domain_pattern = '(http[s]?:\/\/([\w-]+\.)+[\w-]+)?'
path_pattern = '(\/[\w\- \.\/\?%&=]*)?'
exclude_pattern = '(?!.*\.(js|css|js|jpe?g|png|gif|svg|map|mpg|flv|swf))'
pattern = '(href="' + domain_pattern
pattern += exclude_pattern
pattern += path_pattern+')'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--k', type=str, help='keyword', required=True)
    parser.add_argument('--u', type=str, help='url', required=True)
    parser.add_argument('--f', type=str, help='function name')
    args = parser.parse_args()

    if args.f:
        func = getattr(sys.modules[__name__], args.f)
    else:
        func = search

    res = func(args.k, args.u)



def search(keyword, url):

    res = [url]
    search = Search(keyword)
    # base url
    urls = search.search_content(url)
    if urls == True:
        return res
    elif urls == False:
        return 'missed url'

    urls = ['http://tredina.com/user/nodokappg/',
            'http://tredina.com/user/MereMerNOZAWA/',
            'http://tredina.com/user/sayakaaoe/',
            'http://tredina.com/salon/H000232020/'
    ]

    #pool = Pool(2)
    res = multi(keyword,urls,Pool(2),res)

    print(res)
    return res

def multi(keyword,urls,pool,parent):
    tmp = pool.map(Search(keyword), urls)
    try:
        index = tmp.index(True)
        parent.append(urls[index])
    except ValueError as e:
        print(e)
        for urls in tmp:
            multi(keyword,urls,pool,parent)

    return parent

class Search():
    def __init__(self, keyword):
        self.keyword = keyword
        self.exclude_url = []
        print(pattern)
        self.reg = re.compile(pattern)
        self.reg_absolute_path = re.compile('http[s]?:\/\/([\w-]+\.)+[\w-]+')

    def __call__(self, url):
        return self.search_content(url)
                
    def search_content(self, url):
        content = self.__get_content(url)
            
        if content.find(self.keyword) > -1:
            return True
                
        else:
            self.exclude_url.append(url)
            return self.__search_url(content,url)
                

    def __get_content(self, url):
        try:
            response = urllib2.urlopen(url)
            return response.read()
        except urllib2.URLError as e:
            print('error:' + url)

    def __search_url(self,content, current_url):
        urls = self.reg.findall(content)
        res = []
        domain = self.reg_absolute_path.match(current_url).group(0)

        for s in urls:
            url = s[0].replace('href="','')
            if url not in res and url not in self.exclude_url:
                if self.reg_absolute_path.match(url):
                    res.append(url)
                else:
                    res.append(domain + url)

        return res
    



if __name__ == "__main__":
    main()

