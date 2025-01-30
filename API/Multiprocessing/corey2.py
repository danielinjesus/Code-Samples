import multiprocessing; import time
start=time.perf_counter()
def do_something(str_list):
    a = 'Sleeping 1 second...'
    print(a)
    str_list.append(a)
    time.sleep(1)    
    b = 'Done Sleeping...'
    print('Done Sleeping...')
    str_list.append(b)
    print("bye", str_list)
if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')  # 'spawn' 메서드 설정
    with multiprocessing.Manager() as manager: # 매니저 생성
        str_list = manager.list() # value를 공유하는 리스트 생성
        p1 = multiprocessing.Process(target=do_something, args=(str_list,))
        p2 = multiprocessing.Process(target=do_something, args=(str_list,))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        str_list2 = list(str_list) # 공유 리스트를 일반 리스트에 할당
    print("hi", str_list2)
    finish=time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} second(s)')