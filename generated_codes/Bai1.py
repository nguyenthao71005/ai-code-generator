n = int(input("Nhập một số nguyên n: "))
product = 1
for i in range(1, n + 1):
    product *= i
print("Tích từ 1 đến", n, "là:", product)