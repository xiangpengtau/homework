def palindrome(s: str) -> bool:
    # Directly check if the string is equal to its reverse
    return s == s[::-1]


user_input = input("Enter a string to check if it is a palindrome: ")


if palindrome(user_input):
    print("The string is a palindrome.")
else:
    print("The string is not a palindrome.")

