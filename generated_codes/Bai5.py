so = int(input("Nhập một số nguyên dương: "))

if so > 0:
    if (so % 2 == 0) or (so % 3 == 0):
        print(f"Số {so} chia hết cho 2 hoặc cho 3 hoặc cả hai.")
    else:
        print(f"Số {so} không chia hết cho 2 và cũng không chia hết cho 3.")
else:
    print("Bạn phải nhập một số nguyên dương.")