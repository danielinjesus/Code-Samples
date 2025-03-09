miro=[]
for _ in range(10):
    miro.append(list(map(int,input().split())))
miro[1][1]=9
x=1;y=1
while 1:#먹이찾기 루프시작!
    if miro[x][y+1]==2:#우측칸에(2)먹이발견!
        miro[x][y+1]=9#이동한 칸을9로 흔적남기기
        break
    elif miro[x][y+1]==0:#우측칸이(0)비어있으면
        miro[x][y+1]=9#이동한 칸을9로 흔적남기기
        y += 1  # 개미를 우측1칸이동
    elif miro[x][y+1]==1:#우측칸이(1)막혀있으면
        if miro[x+1][y]==2:#아래칸에(2)먹이발견!
            miro[x+1][y]=9
            break
        elif miro[x+1][y]==0:#아래칸이(0)비어있으면
            miro[x+1][y]=9#이동한 칸을9로 흔적남기기
            x+=1#개미를 아래측1칸이동
            continue
        elif miro[x+1][y]==1:#아래칸이(1)막혀있으면
            break
for i in miro:
    print(*i)

# a = int(input())
# b = int(input())
# print(a**b)
# a, b = map(int, input().split())
# print(a+b, a-b, a*b, a//b, a%b, f"{a/b:.2f}", sep="\n")
#
# # a,b,c = map(int, input().split())
# # print(a+b+c, f"{(a+b+c)/3:.2f}")
#
# print(int(input())<<1)
#
# # print(round(float(input()),3))
# print(ord(input()))
# print(chr(int((input()))))
# print(-int(input()))
# print(chr(ord(input())+1))

# a, b = map(int, input().split())
# print(a<=b)
# print(a* (2**b))

# print(not bool(int(input())))

# a, b = map(int, input().split())
# print(bool(int(a))==False and bool(int(b))==False)

# a, b, c = map(int, input().split())
# ab = a if a<b else b
# print( ab if ab < c else c)
#
# a=int(input())
# if a in [12, 1, 2]:print("winter")
# elif a in [3, 4, 5]:print("spring")
# elif a in [6, 7, 8]:print("summer")
# elif a in [9, 10, 11]:print("fall")

# n=int(input())
# c=0
# while c<=n:
#     print(c)
#     c+=1
#
# input_n=int(input()); a=1; s=0
# for i in range(1, input_n+1):
#     s+=i
#     if s>=input_n:
#         print(i)
#         break
# while 1:
#     s+=a
#     if s>=i:
#         print(a)
#         break
#     else:
#         a+=1

# for i in range(n+1):
#     if i%2==0:
#         s+=i
# print(s)

# print(ab = a if a<b else b
# print( ab if ab < c else c)

# print(~int(input()))

# a,b = map(int, input().split())
# for i in range(1,a+1):
#     for j in range(1,b+1):
#         print(i,j)

# a=int(input(),16)
# for i in range(1, 16):
#     print(f"{format(a,'X')}*{format(i,'X')}={format(a*i,'X')}")

# def test(num1, num2=100):
#     print('a= ', num1, 'b= ', num2)
# test(20)

# a=int(input())
# for i in range(1,a+1):
#     cnt=0
#     for j in str(i):
#         if int(j) in [3,6,9]:
#             cnt+=1
#     if cnt!=0:
#         print("X"*cnt,end=" ")
#     else:
#         print(i,end=" ")

# a, b, c = map(int, input().split())
# cnt=0
# for i in range(a):
#     for j in range(b):
#         for k in range(c):
#             print(i, j, k)
#             cnt+=1
# print(cnt)

# a, b, c = map(int,input().split())
# print(f"{a*b*c/8/1024/1024:.2f} MB")

# a = int(input())
# sum1 = 0
# for i in range(1, a+1):
#     sum1 += i
#     if sum1 >= a:
#         print(sum1)
#         break

# a = int(input())
# for i in range(1, a+1):
#     if i%3==0:
#         continue
#     print(i)

# a,b,c=map(int,input().split()) # 최소공배수 구하기
# d=1
# while 1:
#     if d%a==0 and d%b==0 and d%c==0:
#         print(d)
#         break
#     else:
#         d+=1

# n=int(input())
# call_num=map(int,input().split())
# pupil=[0]*23
# for i in call_num:
#     pupil[i-1]+=1
# for k in pupil:
#     print(k,end=" ")

# a=input()
# print(*input().split()[::-1])

# n=input()
# a=list(map(int,input().split()))
# m=a[0]
# for i in a[1:]:
#     m=i if m>i else m
# print

# a=[[0]*19 for _ in range(19)]
# n=int(input())
# a_list=[]
# for _ in range(n):
#     a_list.append(list(map(int,input().split())))
# for i in a_list:
#     a[i[0]-1][i[1]-1]=1
# for i in a:
#     print(*i)

# a=[1,2,3,4,5]
# b=" ".join(map(str, a))
# print(b)

# a_list=[] # 바둑판
# for _ in range(19):
#     a_list.append(list(map(int,input().split())))
# n=int(input())
# cross=[] # 뒤집기
# for _ in range(n):
#     cross.append(list(map(int,input().split())))
# for i in cross:
#     for k in range(len(a_list[i[0]-1])):
#         a_list[i[0]-1][k] = 1 if a_list[i[0]-1][k] == 0 else 0
#     for j in a_list:
#         j[i[1]-1]=1 if j[i[1]-1] == 0 else 0
# for i in a_list:
#     print(*i)

# h,w=map(int,input().split())
# board=[[0]*w for x in range(h)]
# n=int(input());b=[]
# for i in range(n):
#   b.append(list(map(int,input().split())))
# for i in b:
#     i[2]-=1; i[3]-=1
#     if i[1]==0:
#         for k in range(i[0]):
#             board[i[2]][i[3]+k]=1
#     elif i[1]==1:
#         for k in range(i[0]):
#             board[i[2]+k][i[3]]=1
# for i in board:
#     print(*i)