def interest(a, b, c):

    return a * b * c / 100

a = float(input("Enter the principal amount: "))
b = float(input("Enter the interest rate: "))
c = float(input("Enter the number of months: "))
result = interest(a, b, c)
print(f"The calculated interest is: {result}")
