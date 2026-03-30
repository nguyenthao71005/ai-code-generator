so_nguyen = int(input("Nhập một số nguyên dương: "))

if so_nguyen % 2 == 0 or so_nguyen % 3 == 0:
    print(f"Số {so_nguyen} chia hết cho 2 hoặc cho 3 hoặc cả hai.")
else:
    print(f"Số {so_nguyen} không chia hết cho 2 hoặc cho 3.")