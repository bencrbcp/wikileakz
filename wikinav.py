from bs4 import BeautifulSoup
import requests
import re
from collections import defaultdict, deque
from multiprocessing import Pool, cpu_count, Process, Manager
from itertools import repeat


# Basic Usage
# Construct the object like w = WikipediaNav()
#   -> Use Debug=True if you want debug print statements
#   -> maxt determines how many times to look for the end. maxt=50 is around 30 seconds fast, and 60 seconds normal
# Please only use the following methods:
#   runAll(start, end) -> Runs both a BFS and DFS search and returns all the paths in a list. Returns all paths found
#   runAllFast(start, end) -> Uses multiprocessing to run a BFS and DFS faster, but returns less paths. Is around 2x faster than runAll()
# BOTH START AND END ARE STRINGS! Some valid examples:
#     start = "/wiki/Roblox"
#     end = "/wiki/Minecraft"
#     start2 = "/wiki/Horse"
#     end2 = "/wiki/Rat"

class WikipediaNav:

    def __init__(self, maxt=50, debug=True):
        self.seen = set()
        self.retn = []
        self.stopcount = 0
        self.maxtimer = maxt
        self.debug = debug

    # DFS Search

    def runDFS(self, url, end, num=1, path=[], multip=None, multid=None):
        self.stopcount += 1
        if self.stopcount >= self.maxtimer * 2 * 100:
            return
        if self.debug:
            print(url, num, self.stopcount)
        if num == 5:
            return

        urls = self.getLinks(url)
        if end in urls:
            if self.debug:
                print('found')
            path.append(end)
            if multip == None:
                self.retn.append(path)
            else:
                multip.append(path)
            return
        for link in urls:
            repeat = True
            if multid == None:
                if link not in self.seen:
                    repeat = False
                    self.seen.add(link)
            else:
                if link not in multid:
                    repeat = False
                    multid[link] = 1
            if not repeat:
                # self.seen.add(link)
                if len(path) == 0:
                    path.append(url)
                p2 = path.copy()
                p2.append(link)
                self.runDFS(link, end, num + 1, p2, multip, multid)

    # BFS Search

    def runBFS(self, start, end, multip=None, multid=None):
        urls = self.getLinks(start)
        if end in urls:
            # print("found")
            # print([start, end])
            if multip == None:
                self.retn.append([start, end])
            else:
                multip.append([start, end])
            return
        urls = [[link, 1, [start]] for link in urls]
        urls = deque(urls)
        while len(urls) != 0:
            # print(count)
            if self.stopcount >= self.maxtimer:
                print("Too much")
                return
            url = urls.popleft()
            if self.debug:
                print(url[0], url[1])
            self.stopcount += 1
            if url[1] >= 5:
                continue
            links = self.getLinks(url[0])
            if end in links:
                # print("found")
                # print(count)
                found_path = url[2].copy()
                found_path.append(url[0])
                found_path.append(end)
                if multip == None:
                    self.retn.append(found_path)
                else:
                    multip.append(found_path)
                continue
            for link in links:
                repeat = True
                if multid == None:
                    if link not in self.seen:
                        repeat = False
                        self.seen.add(link)
                else:
                    if link not in multid:
                        repeat = False
                        multid[link] = 1
                if not repeat:
                    # self.seen.add(link)
                    ls = url[2].copy()
                    ls.append(link)
                    urls.append([link, url[1] + 1, ls])
        self.stopcount = 0

    # Misc
    def cleanParams(self):
        # Resetting the variables
        self.seen = set()
        self.stopcount = 0

    def clearResults(self):
        self.retn = []

    def getResults(self):
        return self.retn
    # Networking section

    def wikiFy(self, url: str):
        return f"https://en.wikipedia.org{url}"

    def getLinks(self, url: str):
        url = self.wikiFy(url)
        # requests module to access url
        source = requests.get(url)
        # check validity of url using raise_for_status
        source.raise_for_status()

        # create beautifulSoup object using html parser
        doc = BeautifulSoup(source.text, 'html.parser')

        # titles in wikipedia pages correspond to h1 tag
        title = doc.h1

        hyperlinks = []
        # a tags correspond to hyperlinks. Hyperlinks are stored in the href attribute of an 'a' tag
        aTags = doc.find_all('a', href=re.compile('wiki/'))

        for link in aTags:
            if 'href' in link.attrs:
                webstr = link.get('href')
                if webstr[:6] == "/wiki/":
                    if ":" not in webstr:
                        hyperlinks.append(link.get('href'))
        return hyperlinks

    def searchAll(self, start, end):
        self.cleanParams()
        self.clearResults()
        self.runBFS(start, end)
        self.runDFS(start, end)
        self.cleanParams()
        return self.getResults()

    def searchAllFast(self, start, end):
        manager = Manager()
        final_list = manager.list()
        final_set = manager.dict()
        p = Process(target=self.runBFS, args=(
            start, end, final_list, final_set))
        p2 = Process(target=self.runDFS, args=(
            start, end, 1, [], final_list, final_set))
        p.start()
        p2.start()
        p.join()
        p2.join()
        return list(final_list)


# if __name__ == "__main__":
#     w = WikipediaNav(maxt=25, debug=True)
#     start = "/wiki/Roblox"
#     end = "/wiki/Minecraft"
#     start2 = "/wiki/Horse"
#     end2 = "/wiki/Rat"
#     print(w.getLinks("/wiki/Rat"))
#     print(w.searchAll(start, end))
#     print(w.searchAll(start2, end2))
#
#     print(w.searchAllFast(start, end))
#     print(w.searchAllFast(start2, end2))
