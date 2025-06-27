import threading


class Factorization:
    def __init__(self, input_filename, output_filename):
        self.input_filename = input_filename
        self.output_filename = output_filename

        self.num_ready = threading.Event()
        self.res_ready = threading.Event()
        self.pause_event = threading.Event()

        self.pause_event.set()  # не на паузе

        self.num = None
        self.res = None

        self.flag_exit = False
        self.file_read_flag = False
        self.pause_flag = False

    def factorize(self, n):  # алгоритм факторизации числа
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
            user_input = input()
            if user_input == "exit":
                self.flag_exit = True
                self.pause_event.set()
                break
            elif user_input == "pause":
                self.pause_flag = True
                self.pause_event.clear()
            elif user_input == "resume":
                self.pause_flag = False
                self.pause_event.set()

    def factorizator(self):
        while True:
            if self.flag_exit:
                break
            self.num_ready.wait()
            self.num_ready.clear()
            if self.num is None:
                break

            self.pause_event.wait()

            self.res = self.factorize(self.num)
            self.res_ready.set()

    def decomposition(self):
        thread = threading.Thread(target=self.factorizator)
        keyboard_thread = threading.Thread(target=self.keyboard)
        thread.start()
        keyboard_thread.start()

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
                    self.num = num
                    self.res_ready.clear()
                    self.num_ready.set()
                    self.res_ready.wait()

                    fact_str = f"{self.num} = {' * '.join(map(str, self.res))}\n"
                    w.write(fact_str)
                    w.flush()

        self.num = None
        self.num_ready.set()
        self.file_read_flag = True
        thread.join()

    @staticmethod
    def composition(fact):
        factors = list(map(int, fact.strip().split('*')))
        result = 1
        for fact in factors:
            result *= fact
        return result


if __name__ == "__main__":
    factorizer = Factorization('test.txt', 'zapis.txt')
    factorizer.decomposition()
    print(factorizer.composition('2 * 2 * 2 * 2 * 7583'))

"""
Выполнил вроде всё, кроме дополнительных потоков с выбором. Надо изучать ThreadPoolExecutor с его Future'сами.
"""
