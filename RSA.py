#生成密钥
import math


def is_sushu(input):
    i=2
    while(i<input/2):
        if input%i==0:
            return False
        i=i+1
    return True

gm=int(input("请输入一个数值来确定加密规模"))
p=gm+1
q=gm
while(is_sushu(p)==False):
    p=p+1
while(is_sushu(q)==False):
    q=q-1

print("p:",p,"q:",q)
n=p*q
#print(n)

fn=(p-1)*(q-1)
e=1
for i in range(13):
    if(math.gcd(i,fn)==1):
        e=i
#print(e,fn,math.gcd(e,fn))
d=1
while((d*e-1)%fn!=0):
        d=d+1
#print(d)
print("公钥:n",n,"e",e)
print("私钥:n",n,"d",d)
m=19
def Entry(a):
    em=1
    i=1
    while(i<=e):
        em=a*em%n
        i=i+1
    return em
def Solve(a):
    sm=1
    i=1
    while(i<=d):
        sm=sm*a%n
        i=i+1
    return sm#容易超限
temp=Entry(m)
mi=Solve(temp)
#print(m,temp,mi)
str="CQUINFORMATIONSECURITYEXP1"
print("原文：",str)
listDict=[]
for id in range(len(str)):
    temp=ord(str[id])
    listDict.append(Entry(temp))
print("密文数字序列:",listDict)

SolveList=[]
for index in range(len(listDict)):
    temp=listDict[index]
    SolveList.append(chr(Solve(temp)))

mingwen=''.join(SolveList)
print("解密后字符：",mingwen)
    