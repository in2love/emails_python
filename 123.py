import time

start = time.time()
time.sleep(5)
finish = time.time()

result = finish - start

print(int(result) / 60)
