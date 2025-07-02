import threading
import time

# lock = threading.Lock() # mutex

# def task(id):
#     with lock:  # автоматически вызывает acquire() и release()
#         print(f"{id} вошёл")
#         time.sleep(1)
#         print(f"{id} вышел")

# threads = []
# for i in range(5):
#     t = threading.Thread(target=task, args=(f"Поток {i}", ))
#     threads.append(t)

# for i in threads:
#     i.start()

event = threading.Event() # таймер

def task():
    if event.wait(timeout=5):
        print("Событие произошло")
    else:
        print("Таймаут")
    
t = threading.Thread(target=task)
t.start()
# event.set()