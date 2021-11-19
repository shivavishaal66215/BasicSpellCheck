from flask import Flask,redirect,url_for,render_template,request,jsonify
from flask.json import jsonify
from flask.templating import render_template_string
from collections import OrderedDict

app = Flask(__name__)

class TrieNode:
    def __init__(self):
        self.children = [None]*26
        self.isEndOfWord = False

class Trie:

    def __init__(self):
        self.root = self.getNode()

    def getNode(self):
        return TrieNode()

    def _charToIndex(self,ch):


        return ord(ch)-ord('a')


    def insert(self,key):

        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])

            if not pCrawl.children[index]:
                pCrawl.children[index] = self.getNode()
            pCrawl = pCrawl.children[index]
        pCrawl.isEndOfWord = True

    def search(self, key):

        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
            if not pCrawl.children[index]:
                return False
            pCrawl = pCrawl.children[index]

        return pCrawl.isEndOfWord


def initTrie(trie):
    f = open("words.txt", "r")
    content = f.read().split()
    l = []

    for item in content:
        flag = 1
        for i in range(len(item)):
            if(not((item[i] >= 'a' and item[i] <= 'z' ) or (item[i] >= 'A' and item[i] <= 'Z'))):
                flag = 0
        if(flag == 1):
            trie.insert(item)

def spellcheckHelper(trie,words):
    result = {}
    charCount = 0
    for item in words:
        if(not trie.search(item)):
            result[charCount+1] = item

        charCount += len(item) + 1

    return OrderedDict(sorted(result.items()))


#TODO
#NOTE: Use post method. GET method cannot handle large texts
@app.route("/autocomplete")
def autocomplete():
    data = request.form.to_dict()
    body = data["body"]
    return str(body)


#The following route handles the spell check functionality
#It takes a paragraph as input and returns:
#the index and value of mis-spelled words
@app.route("/spellcheck",methods=["POST"])
def spellcheck():

    trie = Trie()
    initTrie(trie)

    data = request.form.to_dict()
    body = data["body"]

    words = body.split()
    errors = spellcheckHelper(trie,words)

    return jsonify(errors)

if __name__ == "__main__":
    app.run(debug=True) 