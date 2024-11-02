## Mạng máy tính (CO3093) - HK241

## Thành viên nhóm

| STT | Mã số SV | Họ và Tên          | Email                          |
|:---:|:-------:|---------------------|--------------------------------|
| 1   | 2213001 | Trần Thành Tài      | tai.tranthanh@hcmut.edu.vn     |
| 2   | 2213298 | Nguyễn Trường Thịnh | thinh.nguyen04@hcmut.edu.vn    |
| 3   | 2212362 | Nguyễn Hữu Nhân     | nhan.nguyenhuucse@hcmut.edu.vn |
| 4   | 2210762 | Dương Thuận Đông    | dong.duong3949@hcmut.edu.vn    |

## Hướng dẫn cài đặt

### Chuẩn bị môi trường
1. Cài đặt **Python** từ [python.org](https://www.python.org/downloads/).
2. Cài đặt **MySQL** và cấu hình cơ sở dữ liệu.
    - Tải MySQL.
    - Mở tệp **db.sql** trong thư mục **tracker** để lấy các câu lệnh và tạo cơ sở dữ liệu.
    - Cấu hình tài khoản cho cơ sở dữ liệu trong tệp **tracker.py**.
3. Cài đặt thư viện **mysql-connector-python** để kết nối với mysql.
    ```bash
    pip install mysql-connector-python
    ```
    
### Chạy dự án
1. Chạy tệp **tracker.py** trong thư mục **tracker**.
2. Chạy tệp **client.py** trong các thư mục **clientx**.
3. Lưu ý với các ô nhập vào danh sách, cần nhập cách nhau bởi dấu phẩy. Nếu muốn chọn tất cả, nhập all.
