#!/usr/bin/env python

__author__ = "Tom Zastrow"
__copyright__ = "Copyright 2023, Tom Zastrow"
__credits__ = ["Tom Zastrow"]
__license__ = "Apache"
__version__ = "2"
__maintainer__ = "Tom Zastrow"
__email__ = "thomas.zastrow@mpcdf.mpg.de"
__status__ = "Development"

import os

class Token(object):
    ''' A Token object contains the token itself, the lemma, the part of speech (POS), if it is an aplhanumeric string or a stop character..'''
    def __init__(self, token, lemma, pos, isAlpha, isStop):
        self.token = token
        self.lemma = lemma
        self.pos = pos
        self.isAlpha = isAlpha
        self.isStop = isStop
    
    def __str__(self):
        return " ".join([self.token, self.lemma, self.pos, str(self.isAlpha), str(self.isStop)])

class Sentence(object):
    ''' A Sentence object contains a list of Token objects'''
    def __init__(self):
        self.tokens =  []

    def display(self):
        for t in self.tokens:
            print(t.__str__())

    def displayAsTokens(self):
        for t in self.tokens:
            print(t.token, end=" ")
        print()

    def bagOfWords(self, annotation):
        b = set()
        for t in self.tokens:
            if annotation == "token":
                b.add(t.token)
            if annotation == "lemma":
                b.add(t.lemma)
            if annotation == "pos":
                b.add(t.pos)
        return b

    def __str__(self):
        temp = ""

        for t in self.tokens:
            temp = temp + t.__str__() + "\n"

        return temp

class Article(object):
    ''' An Article object contains a list of Sentence objects'''
    def __init__(self, id, url, title):
        self.id = id
        self.url = url
        self.title = title
        self.sentences = []

    def bagOfWords(self, annotation):
        b = set()
        for s in self.sentences:
            b = b.union(b, s.bagOfWords(annotation))
        return b

    def display(self):
        print("ID: ", str(self.id))
        print("Title: ", str(self.title))
        print("URL: ", str(self.url))
        print()
        for s in self.sentences:
            s.display()

class Subcorpus(object):
    ''' A Subcorpus object contains functions for reading corpora in wp-2022 format into a list of Article objects'''
    def __init__ (self, infile):
        self.articles = []  
        self.statistics = {}  
        self.name = infile.split("/")[-1]
        self.filename = infile
        f = open(infile, "r", encoding="utf8")
        lines = f.readlines()
        f.close()

        self.articles = []

        for line in lines:
            if line.startswith("<doc id=\""):
                rec = line.split("\" ")
                id = int(rec[0].replace("<doc id=\"", ""))
                url = rec[1].replace("url=\"", "")
                title = rec[2].replace("title=\"", "").replace("\">", "").strip()
                a = Article(id, url, title) 
            elif line.startswith("</doc>"):
                self.articles.append(a)
              
            elif line.startswith("<s>"):
                s = Sentence()
            elif line.startswith("</s>"):
                a.sentences.append(s)
            else:
                rec = line.strip().split("\t")
                if len(rec) != 5:
                    print("Length of token line is not 5:", line)
                else:
                    t = Token(rec[0],rec[1],rec[2],rec[3],rec[4])
                    s.tokens.append(t)
        
        self.statistics["articles"] = len(self.articles)
        self.statistics["sentences"] = 0
        self.statistics["tokens"] = 0
        for a in self.articles:
            self.statistics["sentences"] = self.statistics["sentences"] + len(a.sentences)
            for s in a.sentences:
                self.statistics["tokens"] = self.statistics["tokens"] + len(s.tokens)

    def getName(self):
        return self.name

    def bagOfWords(self, annotation):
        b = set()
        for a in self.articles:
            b = b.union(b, a.bagOfWords(annotation))
        return b

    def getArticleByID(self, id):
        for a in self.articles:
            if a.id == id:
                return a
        return None

class Corpus(object):
    ''' A Corpus object contains functions for reading corpora in wp-2022 format into a list of Article objects'''
    def __init__(self, basePath):
        self.basePath = basePath
        
    def getName(self):
        return self.name
    
    def setName(self,name):
        self.name = name

    def getSubcorpora(self):   
        liste = []
        for root, dirs, files in os.walk(self.basePath):
                path = root.split('/')
                for file in files:
                    liste.append(os.path.join(root, file))
        return liste
    
    def getFolderList(self):   
        liste = []
        for root, dirs, files in os.walk(self.basePath):
                path = root.split('/')
                for dir in dirs:
                    liste.append(os.path.join(dir))
        return liste
    
    def getSubcorporaOfFolder(self, folder):   
        liste = []
        folder = self.basePath + "/" + folder
        for root, dirs, files in os.walk(folder):
                path = root.split('/')
                for file in files:
                    liste.append(os.path.join(root, file))
        return liste

    def getFolders(self):
        return [d for d in os.listdir(self.basePath) if os.path.isdir(os.path.join(self.basePath, d))]

    def getArticleByPosition(self, position):
        rec = position.split("/")
        folder = rec[1]
        subcorpusPath = self.basePath + "/" + folder + "/" +  rec[2]
        artId = int(rec[3])
        subcorpus = Subcorpus(subcorpusPath)

        return subcorpus.getArticleByID(artId)


class Ner(object):
    ''' A Ner object contains functions for handling named entities in WP-2022 format'''
    basePath = ""
    def __init__(self, basePath):
        self.basePath = basePath


    def getNERbyArticle(self, position):
        rec = position.split("/")
        folder = rec[0]
        subcorpusPath = self.basePath + "/" + folder + "/" +  rec[1]
        artId = int(rec[2])
        #print("Subcorpuspath: ", subcorpusPath)
        #print("Article id: ", artId)

        infile = open(subcorpusPath, "r", encoding="utf-8")
        lines = infile.readlines()
        infile.close()

        ners = {}
        ners["PER"] = {}
        ners["LOC"] = {}
        ners["ORG"] = {}
        ners["MISC"] = {}
        id = ""

        for line in lines:
            line = line.strip()
            if line.startswith("<doc id=\""):
                rec = line.split("\" ")
                id = int(rec[0].replace("<doc id=\"", ""))
                url = rec[1].replace("url=\"", "")
                title = rec[2].replace("title=\"", "").replace("\">", "").strip()
            elif line.startswith("</doc>"):
                if id == artId:
                    id = ""
                    break
            else:
                if id == artId:
                    rec = line.split("\t")
                    type = rec[3]
                    if rec[0] in ners[type]:
                        ners[type][rec[0]] = ners[type][rec[0]] + 1
                    else:
                        ners[type][rec[0]] = 1 

        return ners


class Position(object):
    ''' A Position object contains functions for handling relative and absolute positions of any element in WP-2022 format'''
    corpus = ""
    folder = ""
    subcorpus = ""
    article = -1
    sentence = -1
    token = -1


    def getArticle(self):
        return self.corpus.strip("/") + "/" + self.folder.strip("/") + "/" + self.subcorpus.strip("/") + "/" + str(self.article).strip("/")
    
    def getSentence(self):
        return self.corpus.strip("/") + "/" + self.folder.strip("/") + "/" + self.subcorpus.strip("/") + "/" + str(self.article).strip("/") + "/" + str(self.sentence).strip("/")


    def toString(self):
        return self.corpus.strip("/") + "/" + self.folder.strip("/") + "/" + self.subcorpus.strip("/") + "/" + str(self.article).strip("/") + "/" + str(self.sentence) + "/" + str(self.token)

if __name__ == "__main__":
    print("These are objects for the lateco framework, call them from your own applications!")

