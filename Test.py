def sum_even_up_to_n(n):
    # Cộng các số chẵn từ 2 đến n, bước nhảy 2 giúp bỏ qua toàn bộ số lẻ.
    total = 0
    for i in range(2, n + 1, 2):
        total += i
    return total

if __name__ == "__main__":
    try:
        # Chuyển dữ liệu nhập vào thành số nguyên để tiện tính toán.
        n = int(input("Nhập số n: "))
        if n < 0:
            print("Vui lòng nhập một số không âm.")
        else:
            # Chỉ tính toán khi n hợp lệ, sau đó in kết quả ra màn hình.
            result = sum_even_up_to_n(n)
            print(f"Tổng các số chẵn từ 1 đến {n} là: {result}")
    except ValueError:
        # Bắt lỗi khi người dùng nhập chữ hoặc giá trị không ép được sang int.
        print("Đầu vào không hợp lệ. Vui lòng nhập một số nguyên.")
