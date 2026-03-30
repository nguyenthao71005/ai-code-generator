number = int(input("Nhập một số nguyên dương: "))

if number % 2 == 0 and number % 3 == 0:
    print(f"Số {number} chia hết cho cả 2 và 3.")
elif number % 2 == 0:
    print(f"Số {number} chia hết cho 2 nhưng không chia hết cho 3.")
elif number % 3 == 0:
    print(f"Số {number} chia hết cho 3 nhưng không chia hết cho 2.")
else:
    print(f"Số {number} không chia hết cho 2 và cũng không chia hết cho 3.")