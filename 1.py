class INIParser:
    def __init__(self, filename):
        self.data = {}
        self.filename = filename

    def load_data(self):
        section = ''
        try:
            with open(f'{self.filename}') as f:
                for line in f:
                    line = line.split(';')[0].strip()  # убираем комментарии и лишние пробелы
                    if not line:  # убираем пустые строчки
                        continue

                    if line.startswith('[') and line.endswith(
                            ']'):  # обрабатываем секции и закидываем их в ключи словаря словарей
                        section = line[1:-1]
                        self.data[section] = {}

                    if '=' in line:
                        key, value = line.split('=')
                        self.data[section][key.strip()] = value.strip()  # делаем словарь словарей без лишних пробелов
            return self.data
        except FileNotFoundError:
            raise FileNotFoundError("Файл не найден")

    def get_value(self, section, parameter, type):
        try:
            value = self.data[section][parameter]
            return type(value)
        except KeyError:
            raise KeyError(f"Пара секция {section} и параметр {parameter} не найдена")
        except ValueError:
            raise ValueError(f"Не удалось преобразовать в {type}")


pars = INIParser('test.ini')
dictionary = pars.load_data()
print(dictionary)
print(pars.get_value('ADC_DEV', 'SampleRate', float))
print(pars.get_value('NCMD', 'SampleRate', float))
print(pars.get_value('DEBUG', 'DBAddressIP', str))
