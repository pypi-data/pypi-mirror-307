from multiprocessing.pool import ThreadPool
import re
import os
from ..spelling import Spelling
THISDIR, THISFILENAME = os.path.split(__file__)
class FindSimilarityTerms(object):
    def __init__(self,gram=2,ignorant=2,candidate=2,num_processes=4):
        self.fix_gram = gram
        self.ignore = ignorant
        self.num_candidate = candidate
        self.pool = ThreadPool(processes=num_processes)
        self.th_char = r'[\u0E01-\u0E4F]+'
        self.en_char = r'[a-zA-Z]+'
        # Spelling candidate List
        self.SC_th = Spelling()
        self.SC_en = Spelling()
        
        self.resDictRe = None
        self.stEngine = False
    def initDict(self,dict_th=os.path.join(THISDIR, "input/dict_th.txt"),dict_en=os.path.join(THISDIR, "input/dict_en.txt")):
        self.SC_th.initDict(dict_th)
        self.SC_en.initDict(dict_en)
    def getStatus(self):
        return self.stEngine
    def compileKeywords(self,dictListWord):
        resDict = {}
        for k,v_list in dictListWord.items():
            resDict[k] = {}
            for l in ['th','en']:
                resDict[k][l] = {}
                resDict[k][l]['w'] = []
            for v in v_list:
                if self.checkLang(self.th_char,v) == True:
                    resDict[k]['th']['w'].append(v)
                elif self.checkLang(self.en_char,v) == True:
                    resDict[k]['en']['w'].append(v)
            for l in ['th','en']:
                candidateSet_kw = self.getCandidateSet(resDict[k][l]['w'])
                resDict[k][l]['re']= re.compile('|'.join(sorted(candidateSet_kw, key=len,reverse=True)),flags=re.I | re.X)
        if len(resDict) > 0:
            self.resDictRe = resDict
            self.stEngine = True
    def checkLang(self,reLang,text):
        return True if re.search(reLang, text) != None else False


    def find_all(self,strLine, keyWord):
        resList = [res.start() for res in re.finditer(keyWord, strLine)]
        return resList
    def splitByGrame(self,text,gram=2):
        if len(text) < gram+1:
            return [text]
        else:
            res_list = []
            for i in range(len(text)-(gram-1)):
                e = i + gram
                tri = text[i:e]
                res_list.append(tri)
            return  res_list
    def groupInd(self,b,cmpList):
        countContinue = 0 
        endInd = 0
        lastBlank = 0
        for v_list in cmpList:
            lastBlank += 1
            for v in v_list:
                if v > b:
                    # 2g 1ig dif=2
                    # 2g 2ig dif=3
                    # 3g 1ig dif=3
                    # 3g 2ig dif=4
                    if (v - b) <= (self.fix_gram + self.ignore): 
                        countContinue += 1
                        b = v
                        endInd = v + self.fix_gram
                        lastBlank = 0
                    break
            if lastBlank >= (self.fix_gram + self.fix_gram):
                break
        return countContinue, endInd, lastBlank
    def checklastChar(self,key_search,text, e_ind,lastInd):
        for x in range(1,lastInd):
            decre = x * -1
            for i in range(lastInd-1,-1,-1):
                # print(text[e_ind+i],key_search[decre])
                if text[e_ind+i] == key_search[decre]:
                    return e_ind + i + 1
        return e_ind
    def getBIndEInd(self,key_search,text,resList):
        
        # startIndex = 0
        startIndList = []
        endList = []
        continueList = []
        lastBlankList = []
        async_contList = []
        for startInd, firstList in enumerate(resList):
            # startIndex = startInd
            if len(firstList) > 0:
                for b in firstList:
                    async_contList.append(self.pool.apply_async(self.groupInd, (b,resList[startInd+1:])))
                    startIndList.append(b)
                for res in async_contList:
                    continueList.append(res.get()[0])
                    endList.append(res.get()[1])
                    lastBlankList.append(res.get()[2])
                break
        ind_sel = continueList.index(max(continueList))
        if continueList[ind_sel] > 0:
            b_ind = startIndList[ind_sel]# - startIndex
            # e_ind = endList[ind_sel] + lastBlankList[ind_sel]
            e_ind = self.checklastChar(key_search, text, endList[ind_sel], lastBlankList[ind_sel])
            return b_ind, e_ind, 
        else:
            return -1, -1
    def getIndexTermSimilality(self,key_search,text):
        biList = self.splitByGrame(key_search,self.fix_gram)
        async_result = []
        for bi in biList:
            async_result.append(self.pool.apply_async(self.find_all, (text, bi)))
        resList = []
        for res in async_result:
            resList.append(res.get())
        return self.getBIndEInd(key_search,text,resList)
# Spelling candidate List
    def checkEng(self,text):
        return True if re.search(r'[a-zA-Z]+', text) != None else False
    def getCandidateSet(self,keyList):
        SC = self.SC_th
        candidateList = []
        for key in keyList:
            if self.checkEng(key):
                key = key.lower()
                SC = self.SC_en
            if self.num_candidate == 1:
                candidateList.extend(SC.edits1(key))
            else:
                candidateList.extend(SC.edits2(key))
        return set(candidateList)
    def checkText(self,key,text):
        if key in text:
            return key
        return ''
    def searchSimKey(self,text,re_key):
        text = text.lower()
        candidateList = []
        candidateList = re_key.findall(text)
        if len(candidateList) > 0:
            return text.find(candidateList[0]), candidateList[0]
        return -1, ''
# findNextKey
    def findNextKey(self,sInd, keyList, text, limitLen):
        for k in keyList:
            fInd = text[sInd:].find(k)
            if fInd < limitLen:
                return sInd+fInd+len(k)
        return sInd
# Find Similarity Terms
    def getIndexTermSimilality_byIndex(self,listword,text):
        res_list = []
        for key_search in listword:
            ind_b,ind_e = self.getIndexTermSimilality(key_search,text)
            if ind_b != -1:
                ind_b = ind_b - 5
                ind_e = ind_e + 5
                if ind_b < 0:
                    ind_b = 0
                res_list.append((ind_b,ind_e))
        return res_list
    def find_timilarity_terms(self,key,text,lang):
        listword_find = self.resDictRe[key][lang]['w']
        re_find = self.resDictRe[key][lang]['re']
        for kw in listword_find:
            bInd = text.find(kw)
            if bInd != -1:
                return bInd, bInd+len(kw)  
            
        listIndTS = self.getIndexTermSimilality_byIndex(listword_find,text)
        bInd = 0
        sskWord = ''
        for ind_tsb,ind_tse in listIndTS:
            bInd, sskWord = self.searchSimKey(text[ind_tsb:ind_tse],re_find)
            if bInd != -1:
                bInd = ind_tsb + bInd
                break
        return bInd, bInd+len(sskWord)


# import time
# from multiprocessing.pool import ThreadPool
# pool = ThreadPool(processes=4)
# dictListWord = {'abs':['บทคัดย่อ','abstract'],
#                 'kw':['คำสำคัญ','คําสําคัญ','keyword']}

# fst = FindSimilarityTerms()
# t0 = time.time()
# fst.initDict('../input/dict_th.txt',
#     '../input/dict_en.txt',
#     dictListWord)
# t1 = time.time()
# print('Init: %f sec.'%(t1-t0))
# if fst.getStatus() == True:
#     inputFile = '/opt/data/NLP/OCR/output/txt/output.txt'
#     with open(inputFile,'r') as fr:
#         text = fr.read()
#         fr.close()

#     # async_abs = pool.apply_async(fst.find_timilarity_terms, ('abs',text))
#     # async_kw = pool.apply_async(fst.find_timilarity_terms, ('kw',text))

#     t0 = time.time()
#     # bInd, eInd = async_abs.get()
#     bInd, eInd = fst.find_timilarity_terms('abs',text)
#     # if bInd > -1:
#     #     eInd = fst.findNextKey(eInd, ['\n',':',' '],text,5)
            
#     t1 = time.time()
#     print('find_timilarity_terms: %f sec.'%(t1-t0))
#     print(bInd, eInd)
#     print(text[bInd:eInd])

#     # bInd, eInd = async_kw.get()
#     bInd, eInd = fst.find_timilarity_terms('kw',text)
#     # if bInd > -1:
#     #     eInd = fst.findNextKey(eInd, ['\n',':',' '],text,5)
#     t2 = time.time()
#     print('find_timilarity_terms: %f sec.'%(t2-t1))
#     print(bInd, eInd)
#     print(text[bInd:eInd])