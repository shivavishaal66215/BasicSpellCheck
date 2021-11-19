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

        self.root = TrieNode()
        self.word_sug_list = []
  
    def sNode(self):
        return TrieNode()

    def _charToIndex(self,ch):


        return ord(ch)-ord('a')


    def insert(self,key):

        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])

            if not pCrawl.children[index]:
                pCrawl.children[index] = TrieNode()
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

    def prefixPointer(self,key):
        p = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
            if not p.children[index]:
                return False
            p = p.children[index]
        return p
    def suggestionsRec(self, node, word):
        if node.isEndOfWord:
            self.word_sug_list.append(word)
        for n in range(26):
            if node.children[n]!=None:
                self.suggestionsRec(node.children[n], word+chr(ord('a')+n))
        # for a,n in node.children.items():
        #     self.suggestionsRec(n, word + a)
 
    def printAutoSuggestions(self, key):
        node = self.root
        not_found = False
        temp_word = ''
 
        for a in list(key):
            index = self._charToIndex(a)
            if not node.children[index]:
                not_found = True
                break
 
            temp_word += a
            node = node.children[index]
 
        if not_found:
            return 0
        elif node.isEndOfWord and not node.children:
            return -1
 
        self.suggestionsRec(node, temp_word)
 
        return jsonify(self.word_sug_list)



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
@app.route("/autocomplete", methods=["POST"])
def autocomplete():

    trie = Trie()
    initTrie(trie)
    data = request.json
    # print(data)
    body = data["body"]
    words = body.split()
    word_auto = words[-1]
    p = trie.printAutoSuggestions(word_auto)
    if(p == -1):
        return "No other String found with this prefix"
    elif p == 0:
        return "No String found with this prefix"
    return p



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