import threading
import concurrent.futures
import os

"""
Реализация Таймера в Python. По истечению таймера программа закрывается системно.
Events уже используются.
"""
class Factorization:
    def __init__(self, input_filename, output_filename, num_threads, timeout):
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.num_threads = num_threads

        self.pause_event = threading.Event()
        self.pause_event.set()

        self.flag_exit = False
        self.file_read_flag = False
        
        self.timeout = timeout
        self.timer = threading.Timer(timeout, self.time_is_up)

    def time_is_up(self):
        print("Время вышло")
        self.flag_exit = True
        self.pause_event.set()
        os._exit(0)

    def process_number(self, num):
        factors = self.factorize(num)
        return f"{num} = {' * '.join(map(str, factors))}\n"

    def factorize(self, n): # алгоритм факторизации числа
        if n < 2:
            return [n]
        i = 2
        primfac = []
        while i * i <= n:
            while n % i == 0:
                primfac.append(i)
                n //= i
            i += 1
        if n > 1:
            primfac.append(n)
        return primfac

    def keyboard(self):
        while not self.file_read_flag:
            user_input = input('Что сделать с программой - exit, pause, resume: ')
            if user_input == "exit":
                self.flag_exit = True
                self.pause_event.set()
                break
            elif user_input == "pause":
                self.pause_event.clear()
            elif user_input == "resume":
                self.pause_event.set()

    def decomposition(self):
        keyboard_thread = threading.Thread(target=self.keyboard)
        keyboard_thread.start()

        self.timer.start()

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            # futures = []
            with open(self.input_filename, 'r') as f, open(self.output_filename, 'w') as w:
                for line in f:
                    if self.flag_exit:
                        break
                    line = line.strip()
                    if not line:
                        continue

                    nums = [num.strip() for num in line.split(',') if num.strip()]
                    for num_str in nums:
                        if self.flag_exit:
                            break
                        self.pause_event.wait()
                        num = int(num_str)

                        future = executor.submit(self.process_number, num)

                        result_str = future.result()
                        w.write(result_str)
                        w.flush()

        self.timer.cancel()
        self.file_read_flag = True
        keyboard_thread.join()

    @staticmethod
    def composition(fact):
        factors = list(map(int, fact.strip().split('*')))
        result = 1
        for fact in factors:
            result *= fact
        return result


if __name__ == "__main__":
    num_threads = int(input('Количество потоков: '))
    if not 1 <= num_threads <= 8:
        quit('Неправильное количество потоков. Завершение работы')

    timeout = int(input("Максимальное время работы программы: "))

    factorizer = Factorization('test.txt', 'zapis.txt', num_threads, timeout)
    factorizer.decomposition()
    print(factorizer.composition('2 * 2 * 2 * 2 * 7583'))
