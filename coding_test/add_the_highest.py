# 곱하기 혹은 더하기 : 가장 큰 수 만들기
# num_list = list(map(int, input()))
# print(num_list)
# # num_list=[0,2,0,4,5]
# total=num_list[0]
# for idx, i in enumerate(num_list):
#     if idx == 0:
#         pass
#     elif total<=1 or i<=1:
#         total+=i
#     else:
#         total*=i
# print(total)

data=input()
result=int(data[0])
for i in range(1, len(data)):
    # 두 수 중에서 하나라도 '0' 혹은 '1'인 경우, 곱하기보다는 더하기 수행
    num=int(data[i])
    if result <=1 or num <=1:
        result+=num
    else:
        result*=num
print(result)
# data = input()
# result=int(data[0])
# for i in range(1, len(data)):
# # 두 수 중에서 하나라도 '0' 혹은 '1'인 경우, 곱하기보다는 더하기 수행
#     num=int(data[i])
#     if num <=1 or result <=1:
#         result+=num
#     else:
#         result*=num
# print(result)
