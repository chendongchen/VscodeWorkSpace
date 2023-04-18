#原密码表UZ QSO VUOHXMOPV GPOZPEVSG ZWSZ OPFPESX UDBMETSX AIZ VUEPHZ HMDZSHZO WSFP APPD TSVP QUZW YMXUZUHSX EPYEPOPDZSZUFPO MB ZWP FUPZ HMDJ UD TMOHMQ
#单字母表频率下降表E T A O N I S R H L D C U P F M W Y B G V K Q X J Z
#双字母统计概率最大下降表30对 th   he   in   er   an   re   ed   on   es   st   en   at   to   nt   ha   nd   ou   ea   ng   as   or   ti   is   et   it   ar   te    se   hi   of
#三字母统计概率最大下降表20对 the  ing  and  her  ere   ent   tha   nth   was   eth   for   dth   hat   she   ionhis   sth   ers   ver
print("hello ")

Onef="ETAONISRHLDCUPFMWYBGVKQXJZ"
Twof="th   he   in   er   an   re   ed   on   es   st   en   at   to   nt   ha   nd   ou   ea   ng   as   or   ti   is   et   it   ar   te    se   hi   of"
Threef="the  ing  and  her  ere   ent   tha   nth   was   eth   for   dth   hat   she   ionhis   sth   ers   ver"
Twof=Twof.split()
Threef=Threef.split()
#print(Threef)
#print(Twof)

#密文
miwen="UZ QSO VUOHXMOPV GPOZPEVSG ZWSZ OPFPESX UDBMETSX AIZ VUEPHZ HMDZSHZO WSFP APPD TSVP QUZW YMXUZUHSX EPYEPOPDZSZUFPO MB ZWP FUPZ HMDJ UD TMOHMQ "
EntryWord=miwen.split(" ")   #list
#测试划分是否正确
#print(EntryWord[1])

#单字母统计
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
'''"P":16
"Z":14
"U":10
"S":10
"O":9
"M":8
"H":7
"E":6
"D":6
"V":5
"X":5
"W":4
"F":4
"Q":3
"T":3
"G":2
"B":2
"A":2
"Y":2
"I":1
"J":1
'''
Solve2=TwoWords(miwen)
#双字母统计结果
'''"UZ":3
"OP":3
"PO":3
"ZW":3
"FP":3
"SX":3
"EP":3
"HM":3
"VU":2
"OH":2
"MO":2
"PE":2
"WS":2
"SZ":2
"UD":2
"TS":2
"HZ":2
"MD":2
"DZ":2
"ZS":2
"PD":2
"ZU":2
"QS":1
"SO":1
"UO":1
"HX":1
"XM":1
"PV":1
"GP":1
"OZ":1
"ZP":1
"EV":1
"VS":1
"SG":1
"PF":1
"ES":1
"DB":1
"BM":1
"ME":1
"ET":1
"AI":1
"IZ":1
"UE":1
"PH":1
"SH":1
"ZO":1
"SF":1
"AP":1
"PP":1
"SV":1
"VP":1
"QU":1
"YM":1
"MX":1
"XU":1
"UH":1
"HS":1
"PY":1
"YE":1
"UF":1
"MB":1
"WP":1
"FU":1
"UP":1
"PZ":1
"DJ":1
"TM":1
"MQ":1
'''
Solve3=ThreeWords(miwen)
#三字母统计结果 
'''"HMD":2
"DZS":2
"QSO":1
"VUO":1
"UOH":1
"OHX":1
"HXM":1
"XMO":1
"MOP":1
"OPV":1
"GPO":1
"POZ":1
"OZP":1
"ZPE":1
"PEV":1
"EVS":1
"VSG":1
"ZWS":1
"WSZ":1
"OPF":1
"PFP":1
"FPE":1
"PES":1
"ESX":1
"UDB":1
"DBM":1
"BME":1
"MET":1
"ETS":1
"TSX":1
"AIZ":1
"VUE":1
"UEP":1
"EPH":1
"PHZ":1
"MDZ":1
"ZSH":1
"SHZ":1
"HZO":1
"WSF":1
"SFP":1
"APP":1
"PPD":1
"TSV":1
"SVP":1
"QUZ":1
"UZW":1
"YMX":1
"MXU":1
"XUZ":1
"UZU":1
"ZUH":1
"UHS":1
"HSX":1
"EPY":1
"PYE":1
"YEP":1
"EPO":1
"POP":1
"OPD":1
"PDZ":1
"ZSZ":1
"SZU":1
"ZUF":1
"UFP":1
"FPO":1
"ZWP":1
"FUP":1
"UPZ":1
"MDJ":1
"TMO":1
"MOH":1
"OHM":1
"HMQ":1
'''

#频率分析
#下降表E T A O N I S R H L D C U P F M W Y B G V K Q X J Z
#统计  P Z U S O M H E D V X W F Q T G B A Y I J

#解密表SolveDict=dict({'P','Z','U','S','O','M','H','E','D','V','X','W','F','Q','T','G','B','A','Y','I','J'})
SolveDict={}
#直接用一次频率
i=0
for key in Solve1:
    SolveDict[key]=Onef[i]
    i=i+1
#

#解密程序    
SolveOnestr=miwen
for index in range(len(SolveOnestr)):
    for key in SolveDict:
        if(SolveOnestr[index]==key):
            str=list(SolveOnestr)
            str[index]=SolveDict[key]
            SolveOnestr=''.join(str)
            break
#print(SolveOnestr)
#AT PON LANSDINEL MENTERLOM TCOT NEUEROD AHWIRFOD YGT LAREST SIHTOSTN COUE YEEH FOLE PATC BIDATASOD REBRENEHTOTAUEN IW TCE UAET SIHV AH FINSIP    
