####################### print 구문 #######################
print("print(\"Hello\\nWorld\")") #escaper
print("\"C:\Download\\'hello\'.py\"") #escaper
print("\"!@#$%^&*()'") #escaper
print(B,A, sep='\n') # Seperator 한줄씩 띄기
print(float(input())+float(input()))
print('%n'% n) # n변수를 16진수(hexadecimal)로 표현 # print('%X'%n) # n변수를 16진수 대문자로 표현
print(f"{n:x}") # f-string으로 16진수 표현 # print(f"{n:x}") 대문자
n=int(input(),16); print('%o'%n) #받은걸,16진수로저장하고,8진수로출력
print(ord(input())) #10진수 유니코드 값으로 출력
print(chr(int((input())))) # 숫자 입력받아 유니코드 문자 출력하기
print(chr(ord(input())+1)) # 숫자 받아서 다음 문자 출력
print(n<<1)  #10을 2배 한 값인 20 이 출력된다.
print(n>>1)  #10을 반으로 나눈 값인 5 가 출력된다.
print(n<<2)  #10을 4배 한 값인 40 이 출력된다.
print(n>>2)  #10을 반으로 나눈 후 다시 반으로 나눈 값인 2 가 출력된다.
# print(a<<b) # a를 2에 b승한 수로 곱함
# 비교연산자 <, >, <=, >=, ==(같다), !=(다르다)
print(not bool(int(input())))
print(~int(input())) # 비트연산자 Not
# print(a if a>=b else b) # 삼항연산자
# 알파벳을 숫자로 : c=ord(input());t=ord('a'); while t<=c:print(chr(t));t+=1

a=int(input(),16)
for i in range(1, 16):
    print(f"{format(a,'X')}*{format(i,'X')}={format(a*i,'X')}") # 16진수 구구단

####################### '*' unpacking operator #######################
print(*lst); lst=[1, 2, 3, 4, 5]; # 1 2 3 4 5 # 리스트에 있는 걸 하나씩 띄어서 출력
print(*input().split(), sep="\n") # sep=변수 중간 구분자
print(*lst[::-1],sep=" "); # 리스트 뒤집기1
print(reversed(lst),sep=" ") # 리스트 뒤집기2
print(" ".join([input()]*3)) # 리스트를 공백으로 연결하여 출력
# join() 메서드는 문자열(str) 리스트만 가능.
#a=[1,2,3,4,5]; b=" ".join(map(str, a))
# 리스트 만들기, 19x19 a=[[0]*19 for _ in range(19)]

print(*a, end= " and "); arr = [1, 2, 3, 4, 5]; # 1 and 2 and 3 and 4 and 5 and # end=는 변수 끝에 구분자
a, b = map(float, input().split())
print(f"{a/b:.3f}") # f-string으로 숫자를 문자로 바꿔서 float 3째자리까지 출력
a, b = map(int, input().split())
print(a+b, a-b, a*b, a//b, a%b, f"{a/b:.2f}", sep="\n")
####################### map ####################### 
a=map(int,input().split()) # map object
a, b = map(int, input().split()) # int로 들어간다.
a=list(map(str,range(10)) # list 만들기
print(sum(map(int, input().split(' '))))
print(" ".join(map(str, lst))); #전제: lst=[1, 2, 3, 4, 5]; # 1 2 3 4 5 #리스트 원소를 str으로 map 객체로 만들어서 join으로 str만들기
# https://dojang.io/mod/page/view.php?id=2286

####################### List Comprehension #######################
[표현식 for 변수 in iterable]
print(sum([int(x) for x in input().split(' ')]))
print(*[a[i:i+2] for i in range(0,6,2)]); #전제: a=input()
a=[[0]*19 for _ in range(19)]
####################### 그 외 함수들 #######################
print(input().replace('-','')) #문자열 대체      
print(input().split(':')[1])
print(*input().split(' '),sep="")

####################### Strip #######################
import pandas as pd
topic = pd.read_csv("")
topic_revised = []
for topic in topic['topic']:
    topic2 = topic.replace('\n', ' ').strip()
    topic_revised.append(topic2)
topic_revised = pd.DataFrame({ "topic" : topic_revised })
topic_revised.to_csv("")

# 주어진 배열이 있을 때는 range로 for문, 특정 조건하에서는 while문이 편함!!!
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html
# while 문
while 1:
    i=input()
    if i=='q':
        print(i)
        break
    else:
        print(i)

input_n=int(input()); a=1; s=0
for i in range(1, input_n+1):
    s+=i
    if s>=input_n:
        print(i)
        break