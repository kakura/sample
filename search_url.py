#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import multiprocessing
from multiprocessing import Pool
from multiprocessing import Process
import urllib2
import argparse
import re


domain_pattern = '(http[s]?:\/\/([\w-]+\.)+[\w-]+)?'
path_pattern = '(\/[\w\- \.\/\?%&=]*)?'
exclude_pattern = '(?!.*\.(js|ico|css|js|jpe?g|png|gif|svg|map|mpg|flv|swf))'
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

    print(res)

def search(keyword, url):

    res = []
    base_url = url
    # queue
    queue = [url]
    #親子関係を保持
    tree = []

    search = Search(keyword, [])
    # レベル順探索
    while len(queue) > 0:
        url = queue.pop(0)
        childs = search.search_content(url)
        print(childs)
        if childs == True:
            # 探索終了
            break
        elif childs == False or len(childs) <= 0:
            continue

        # qに子ノードを追加
        queue.extend(childs)

        tree.append({url: childs})

    # 親子関係をたどってlist作成
    res.insert(0, url)
    while len(tree) > 0:
        node = tree.pop()
        if url in (node.values())[0]:
            url = (node.keys())[0]
            res.insert(0, url)
            
            
    return res

class Search():
    def __init__(self, keyword,exclude_url):
        self.keyword = keyword
        self.exclude_url = exclude_url
        self.reg = re.compile(pattern)
        self.reg_absolute_path = re.compile('http[s]?:\/\/([\w-]+\.)+[\w-]+')

    def __call__(self, url):
        return self.search_content(url)
                
    def search_content(self, url):
        content = self.__get_content(url)
            
        if content.find(self.keyword) > -1:
            return True
                
        else:
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
            if self.reg_absolute_path.match(url) is None:
                url = domain + url

            if url not in self.exclude_url:               
                res.append(url)
                self.exclude_url.append(url)

        return res
    



if __name__ == "__main__":
    main()

