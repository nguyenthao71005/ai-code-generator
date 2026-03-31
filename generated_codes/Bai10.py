n = int(input("Nhập một số nguyên dương: "))

if n % 2 == 0 or n % 3 == 0:
    print(f"{n} chia hết cho 2 hoặc cho 3 hoặc cả hai.")
else:
    print(f"{n} không chia hết cho 2 cũng không chia hết cho 3.")