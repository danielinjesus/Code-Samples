####################### print 구문 #######################
print("print(\"Hello\\nWorld\")") #escaper
print("\"C:\Download\\'hello\'.py\"") #escaper
print("\"!@#$%^&*()'") #escaper
print(B,A, sep='\n') # Seperator 한줄씩 띄기
print(float(input())+float(input()))
print('%n'% n) # n변수를 16진수(hexadecimal)로 표현 # print('%X'%n) # n변수를 16진수 대문자로 표현
print(f"{n:x}") # f-string으로 16진수 표현 # print(f"{n:x}") 대문자
n=int(input(),16); print('%o'%n) #받은걸,16진수로저장하고,8진수로출력

####################### '*' unpacking operator ####################### 
print(*lst); lst=[1, 2, 3, 4, 5]; # 1 2 3 4 5 # 리스트에 있는 걸 하나씩 띄어서 출력
print(*input().split(), sep="\n") # sep=변수 중간 구분자
print(*lst[::-1],sep=" "); # 리스트 뒤집기1
print(reversed(lst),sep=" ") # 리스트 뒤집기2
print(" ".join([input()]*3)) # 리스트를 공백으로 연결하여 출력
print(*a, end= " and "); arr = [1, 2, 3, 4, 5]; # 1 and 2 and 3 and 4 and 5 and # end=는 변수 끝에 구분자

####################### map ####################### 
a=map(int,input().split()) # map object
a=list(map(str,range(10)) # list 만들기
print(sum(map(int, input().split(' '))))
print(" ".join(map(str, lst))); #전제: lst=[1, 2, 3, 4, 5]; # 1 2 3 4 5 #리스트 원소를 str으로 map 객체로 만들어서 join으로 str만들기
# https://dojang.io/mod/page/view.php?id=2286

####################### List Comprehension #######################
[표현식 for 변수 in iterable]
print(sum([int(x) for x in input().split(' ')]))
print(*[a[i:i+2] for i in range(0,6,2)]); #전제: a=input()

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

# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html
