def test(num):
    if num<2:
        print(num, end='')
    else:
        test(num//2)
        print(num%2, end='')
test(20)
