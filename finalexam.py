# -*- coding: cp949 -*-

import requests, sys, re
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, url):
        self.url = url
        
    def get_data(self):
        r = requests.get(self.url)
        s = BeautifulSoup(r.content, "html.parser")
        lines = s.find_all(attrs={"id":"lyrics"})
        return lines[0].get_text()

class FileManager:
    def __init__(self, loc):
        self.loc = loc
        
    def load_file(self):
        with open(self.loc, 'r') as f:
            con = f.read()
        return con

    def save_file(self, data):
        with open(self.loc, 'w') as f:
            f.write(data)

class Counter:
    def __init__(self, data):
        self.data =data
        
    def count(self):
        c = dict()
        t = re.sub("[,()\']","",self.data.lower())
        r = t.split()
        for word in set(r):
            c[word] = r.count(word)
        return c

    def get_five(self, d):
        r = d.items()
        r.sort(key=lambda x: x[1], reverse=True)
        return r[:5] 

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: python [filename] {option1 | option2 | option3} target"
        print "options: -c, -h, -t"
        sys.exit(1)
    else:
        lyrics = Crawler('https://www.songtexte.com/songtext/freddie-mercury/bohemian-rhapsody-23982857.html')
        fm = FileManager(sys.argv[2])
        fm.save_file(lyrics.get_data())
        count = Counter(fm.load_file())
        
        if sys.argv[1] == "-c":
            print count.count()
        elif sys.argv[1] == "-h":
            for w1, w2 in count.count().items():
                print w1,":\t"+"*"*w2
        elif sys.argv[1] == "-t":
            d = count.count()
            for word in count.get_five(d):
                print word[0]
        else:
            print "unknown option"
        
    
    
        
