def count_numbers_in_file(filename):
    total_numbers = 0
    with open(filename, 'r') as f:
        for line in f:
            numbers = [num.strip() for num in line.strip().split(',') if num.strip()]
            total_numbers += len(numbers)
    return total_numbers

filename = 'numbers.txt'
count = count_numbers_in_file(filename)
print(f"Всего чисел в файле: {count}")
