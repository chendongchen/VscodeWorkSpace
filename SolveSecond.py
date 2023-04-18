#原密码表UZ QSO VUOHXMOPV GPOZPEVSG ZWSZ OPFPESX UDBMETSX AIZ VUEPHZ HMDZSHZO WSFP APPD TSVP QUZW YMXUZUHSX EPYEPOPDZSZUFPO MB ZWP FUPZ HMDJ UD TMOHMQ
#单字母表频率下降表E T A O N I S R H L D C U P F M W Y B G V K Q X J Z
#双字母统计概率最大下降表30对 th   he   in   er   an   re   ed   on   es   st   en   at   to   nt   ha   nd   ou   ea   ng   as   or   ti   is   et   it   ar   te    se   hi   of
#三字母统计概率最大下降表20对 the  ing  and  her  ere   ent   tha   nth   was   eth   for   dth   hat   she   ionhis   sth   ers   ver

#密文
from SolveABC import SolveDict


miwen="UZ QSO VUOHXMOPV GPOZPEVSG ZWSZ OPFPESX UDBMETSX AIZ VUEPHZ HMDZSHZO WSFP APPD TSVP QUZW YMXUZUHSX EPYEPOPDZSZUFPO MB ZWP FUPZ HMDJ UD TMOHMQ "
'''
#字母统计
def OneWord(input):
    #去掉空格
    input=input.replace(' ','')
    #print(input)
    ResoultDict={}
    for key in input:
        ResoultDict[key]=input.count(key)
    
    ResoultDict=dict(sorted(ResoultDict.items(),key=lambda value: value[1],reverse=True))

    #for ikey in ResoultDict:
    #    print(f'"{ikey}":{ResoultDict[ikey]}')
    return ResoultDict
def TwoWords(input):
    #去掉空格
    #input=input.replace(' ','')
    #print(input)
    ResoultDict={}
    for index in range(len(input)):
        if index+1<len(input):
            if input[index+1]!=' ' and input[index]!=' ':
                tw=input[index]+input[index+1]
                ResoultDict[tw]=input.count(tw)
    
    ResoultDict=dict(sorted(ResoultDict.items(),key=lambda value: value[1],reverse=True))
#    for ikey in ResoultDict:
#       print(f'"{ikey}":{ResoultDict[ikey]}')
    return ResoultDict
def ThreeWords(input):
    ResoultDict={}
    for index in range(len(input)):
        if index+2<len(input):
            if input[index+1]!=' ' and input[index]!=' ' and input[index+2]!=' ':
                tw=input[index]+input[index+1]+input[index+2]
                ResoultDict[tw]=input.count(tw)
    
    ResoultDict=dict(sorted(ResoultDict.items(),key=lambda value: value[1],reverse=True))
#    for ikey in ResoultDict:
#        print(f'"{ikey}":{ResoultDict[ikey]}')
    return ResoultDict

Solve1=OneWord(miwen)
#单表统计结果
Solve2=TwoWords(miwen)
#双字母统计结果
Solve3=ThreeWords(miwen)
#三字母统计结果 

#解密表SolveDict=dict({'P','Z','U','S','O','M','H','E','D','V','X','W','F','Q','T','G','B','A','Y','I','J'})
SolveDict={}
#直接用一次频率
Onef="ETAONISRHLDCUPFMWYBGVKQXJZ"
i=0
for key in Solve1:
    SolveDict[key]=Onef[i]
    i=i+1
#
'''
SolveDict={'P':'E','Z':'N','U':'A','S':'G','O':'R','M':'H','H':'T','E':'S','D':'L','V':'R','X':'D','W':'C','F':'U','Q':'P','T':'F','G':'M','B':'W','A':'K','Y':'Q','I':'J','J':'I'}

#解密程序    
SolveOnestr=miwen
for index in range(len(SolveOnestr)):
    for key in SolveDict:
        if(SolveOnestr[index]==key):
            str=list(SolveOnestr)
            str[index]=SolveDict[key]
            SolveOnestr=''.join(str)
            break

print(SolveOnestr.title())