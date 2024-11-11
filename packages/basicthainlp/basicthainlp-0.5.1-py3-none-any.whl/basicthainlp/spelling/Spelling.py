import re
import os
from collections import Counter
THISDIR, THISFILENAME = os.path.split(__file__)
class Spelling():
    def __init__(self):
        self.WORDS_EN = Counter([])
        self.WORDS_TH = Counter([])
        self.biGram_En = Counter([])
        self.triGram_En = Counter([])
        self.biGram_Th = Counter([])
        self.triGram_Th = Counter([])
        self.letter_en   = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.letter_thC = ['ก','จ','ด','ต','บ','ป','ฎ','ฏ','ข','ฃ','ฉ','ฐ','ถ','ผ','ฝ','ศ','ษ','ส','ค','ฅ','ฆ','ง','ช','ซ','ฌ','ญ','ฑ','ฒ','ณ','ท','ธ','น','พ','ฟ','ภ','ม','ฬ','ฮ','ล','ร','ว','ย','ห','อ','ฤ','ฦ']
        self.letter_thV = ['เ','แ','ไ','ใ','โ','ิ','ี','ึ','ื','ั','็','า','ะ','ำ','ๅ','ุ','ู','์','ฺ','ํ','๎']
        self.letter_thT = ['่','้','๊','๋']
        self.letter_th = self.letter_thC + self.letter_thV + self.letter_thT
    def initDict(self,inputDict=os.path.join(THISDIR, "input/dict_lexitron.txt")):
        self.WORDS_EN,self.WORDS_TH,self.biGram_En,self.triGram_En,self.biGram_Th,self.triGram_Th = self.__intiWordCounter(self.words(open(inputDict).read()))
    def updateDict(self,inputDict):
        wordEn,wordTh,biGramEn,triGramEn,biGramTh,triGramTh = self.__intiWordCounter(self.words(open(inputDict).read()))
        self.WORDS_EN.update(wordEn)
        self.WORDS_TH.update(wordTh)
        self.biGram_En.update(biGramEn)
        self.triGram_En.update(triGramEn)
        self.biGram_Th.update(biGramTh)
        self.triGram_Th.update(triGramTh)
    def __intiWordCounter(self,listDat):
        listEn = []
        listTh = []
        biGramEn = []
        triGramEn = []
        biGramTh = []
        triGramTh = []
        for w in listDat: 
            if w != '':
                biGram,triGram = self.contectFreeGram(w)
                if self.checkEng(w):
                    listEn.append(w.lower())
                    biGramEn.extend(biGram)
                    triGramEn.extend(triGram)
                else:
                    listTh.append(w)
                    biGramTh.extend(biGram)
                    triGramTh.extend(triGram)
        return Counter(listEn),Counter(listTh),Counter(biGramEn),Counter(triGramEn),Counter(biGramTh),Counter(triGramTh)
    
    def contectFreeGram(self,word):
        biGram = []
        triGram = []
        if len(word) > 0:
            word = '<'+str(word)+'>'
            biGram.append(word[0]+word[1])
            for i in range(1,len(word) - 2):
                biGram.append(word[i]+word[i+1])
                triGram.append(word[i-1]+word[i]+word[i+1])
            biGram.append(word[-2]+word[-1])
            triGram.append(word[-3]+word[-2]+word[-1])
        return biGram,triGram
    def words(self,text): 
        return text.split()
    def P(self,word):
        if self.checkEng(word):
            return self.WORDS_EN[word] / sum(self.WORDS_EN.values())
        else: 
            return self.WORDS_TH[word] / sum(self.WORDS_TH.values())
    def getTriLetter(self,word,ind):
        if ind < len(word):
            bStr = ''
            eStr = ''
            b = ind - 1
            if b < 0: 
                b = 0
                bStr = '<'
            e = ind + 2
            if e >len(word): 
                e = len(word)
                eStr = '>'
            return bStr+word[b:e]+eStr
        return ''
    def getIndDiff(self,str1, str2):
        count = 0
        res = []
        for a, b in zip(str1, str2):
            if a != b:
                res.append(count)
            count += 1
        return res
    def getValTrigram(self,word,ind):
        triGram = self.getTriLetter(word,ind)
        valTrig = 0
        if self.checkEng(triGram) == True:
            if triGram in self.triGram_En: 
                valTrig = self.triGram_En[triGram]
        else:
            if triGram in self.triGram_Th: 
                valTrig = self.triGram_Th[triGram]
        return valTrig
    def cmpTriGram(self,word1,word2):
        indList = self.getIndDiff(word1,word2)
        if len(indList) > 0:
            for ind in indList:
                valTrig1 = self.getValTrigram(word1,ind)
                valTrig2 = self.getValTrigram(word2,ind)
                if valTrig2 > valTrig1:
                    return True
                elif valTrig2 < valTrig1:
                    return False
        return False
    def correction(self,word):
        # return max(self.candidates(word), key=self.P)
        topList = self.getTop(word,3) 
        if len(topList) > 0:
            maxWord = topList[0][0]
            maxScore = topList[0][1]
            for (word,score) in topList[1:]:
                if score == maxScore:
                    if self.cmpTriGram(maxWord,word) == True:
                        maxWord = word
            return maxWord
        else:
            return word
    def checkSpell(self,word): 
        return set(self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])
    def candidates(self,word): 
        return (set(self.known([word]) | self.known(self.edits1(word))) or self.known(self.edits2(word))) # Union
    def getTop(self,word,top):
        return [(c,self.P(c)) for c in sorted(self.candidates(word),key=lambda x:self.P(x),reverse=True)[:top]]
    def known(self,wordSet): 
        words = list(wordSet)
        if len(words) > 0:
            if self.checkEng(words[0]):
                return set(w for w in words if w in self.WORDS_EN)
            else:
                return set(w for w in words if w in self.WORDS_TH)
        else:
            return set()
    def edits1(self,word):
        letters = self.letter_th
        chEng = self.checkEng(word)
        if chEng:
            word = word.lower()
            letters = self.letter_en
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        # deletes    = [L + R[1:]               for L, R in splits if R]
        deletes = self.deletes_func(splits,chEng)
        # transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        transposes = self.transposes_func(splits,chEng)
        # replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        replaces = self.replaces_func(splits,chEng,letters)
        # inserts    = [L + c + R               for L, R in splits for c in letters]
        inserts = self.inserts_func(splits,chEng,letters)
        return set(deletes + transposes + replaces + inserts)
    def edits2(self,word):
        return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))
    def deletes_func(self,splits,chEng):
        result = []
        if len(splits) > 2:
            for L, R in splits:
                LL, RR= '<'+L, R+'>'
                if R:
                    biGram = LL[-1] + RR[1]
                    if chEng:
                        if biGram in self.biGram_En: result.append(L + R[1:])
                    else:
                        if biGram in self.biGram_Th: result.append(L + R[1:])
        return result  
    def transposes_func(self,splits,chEng):
        result = []
        if len(splits) > 2:
            for L, R in splits:
                LL, RR= '<'+L, R+'>'
                if len(R)>1:
                    triGram0 = LL[-1] + RR[1] + RR[0]
                    triGram1 = RR[1] + RR[0] + RR[2]
                    if chEng:
                        if triGram0 in self.triGram_En and triGram1 in self.triGram_En : 
                            result.append(L + R[1] + R[0] + R[2:])
                    else:
                        if triGram0 in self.triGram_Th and triGram1 in self.triGram_Th : 
                            result.append(L + R[1] + R[0] + R[2:])
        return result  
    def replaces_func(self,splits,chEng,letters):
        result = []
        if len(splits) > 2:
            for L, R in splits:
                LL, RR= '<'+L, R+'>'
                if R:
                    for c in letters:
                        triGram = LL[-1] + c + RR[1]
                        if chEng:
                            if triGram in self.triGram_En: 
                                result.append(L + c + R[1:] )
                        else:
                            if triGram in self.triGram_Th: 
                                result.append(L + c + R[1:] )
        return result       
    def inserts_func(self,splits,chEng,letters):
        result = []
        if len(splits) > 2:
            for L, R in splits:
                LL, RR= '<'+L, R+'>'
                for c in letters:
                    triGram = LL[-1] + c + RR[0]
                    if chEng:
                        if triGram in self.triGram_En: 
                            result.append(L + c + R)
                    else:
                        if triGram in self.triGram_Th: 
                            result.append(L + c + R)
        return result        
    def checkEng(self,text):
        return True if re.search(r'[a-zA-Z]+', text) != None else False

# SC = Spelling()
# SC.initDict()
# # SC.initDict('input/dict_lexitron.txt')
# print(SC.known('จุฑามาส'))
# print(SC.candidates('จุฑามาส'))
# print(SC.getTop('จุฑามาส',10))
# print(SC.correction('จุฑามาส'))