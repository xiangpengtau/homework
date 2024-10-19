def filter_str(filter_func, strings):
    return list(filter(filter_func, strings))

# Get a list of strings from user input
user_input = input("Enter a list of strings, separated by commas: ")
strings = [s.strip() for s in user_input.split(',')]

# Filter conditions
no_spaces = lambda s: ' ' not in s
not_start_with_a = lambda s: not s.startswith('a')
length_at_least_5 = lambda s: len(s) >= 5

# Test
print("Strings without spaces:", filter_str(no_spaces, strings))
print("Strings not starting with 'a':", filter_str(not_start_with_a, strings))
print("Strings with length at least 5:", filter_str(length_at_least_5, strings))

