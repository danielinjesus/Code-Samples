if (idx + 1) % 100 == 0:   # Rate limit 방지를 위해 1분 동안 최대 100개의 요청을 보내도록 합니다.
            end_time = time.time()
            elapsed_time = end_time-start_time            
            if elapsed_time < 60:
                wait_time = 60 - elapsed_time + 5
                print(f"Elapsed time: {elapsed_time:.2f} sec")
                print(f"Waiting for {wait_time} sec")
                time.sleep(wait_time)
            start_time = time. Time()