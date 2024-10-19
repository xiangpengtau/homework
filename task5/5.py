import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Execution time: {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def add_numbers(a, b):
    result = a + b
    print(f"The sum is: {result}")
    return result

@timer
def add_from_file(input_file='input.txt', output_file='output.txt'):
    with open(input_file, 'r') as file:
        a, b = map(int, file.read().split())
    result = a + b
    with open(output_file, 'w') as file:
        file.write(f"The sum is: {result}")
    print(f"The sum from file is: {result}")
    return result

# Test
add_numbers(3, 7)
add_from_file()

