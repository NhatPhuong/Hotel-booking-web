import sqlite3

def init_all_db():
    # 1. Kết nối đến file database duy nhất
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    # --- PHẦN 1: Cấu trúc bảng của bạn (Rooms) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL,
            image TEXT,
            amenities TEXT
        )
    ''')

    # --- PHẦN 2: Cấu trúc các bảng của bạn bạn (Ưu đãi, Liên hệ, Đặt phòng, Ảnh chủ) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uu_dai (
            id TEXT PRIMARY KEY,
            tieu_de TEXT NOT NULL,
            mo_ta TEXT,
            anh_url TEXT,
            gia_km INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lien_he (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            ho_ten TEXT, 
            email TEXT, 
            sdt TEXT, 
            noi_dung TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dat_phong (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ten_khach TEXT,
            ngay_den TEXT NOT NULL,
            ngay_di TEXT NOT NULL,
            nguoi_lon INTEGER DEFAULT 1,
            tre_em_6_11 INTEGER DEFAULT 0,
            tre_em_0_5 INTEGER DEFAULT 0,
            ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS anh_gioi_thieu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mo_ta TEXT,
            anh_url TEXT
        )
    ''')

    # --- PHẦN 3: Chèn dữ liệu mẫu (Xóa dữ liệu cũ để tránh trùng lặp) ---
    cursor.execute('DELETE FROM rooms')
    cursor.execute('DELETE FROM uu_dai')
    cursor.execute('DELETE FROM anh_gioi_thieu')

    # Dữ liệu phòng
    sample_rooms = [
        ('Luxury Forest Suite', 'Trải nghiệm không gian mở giữa rừng thông với nội thất gỗ cao cấp.', 2500000, 'images/room1.jpg', 'Wifi, Tủ lạnh, Ban công, Bồn tắm'),
        ('Grand Mountain View', 'Tầm nhìn panorama hướng thẳng ra thung lũng đại ngàn.', 3500000, 'images/room2.jpg', 'Wifi, Điều hòa, Smart TV, Mini Bar'),
        ('F4 Royal President', 'Căn hộ cao cấp nhất với dịch vụ quản gia riêng 24/7.', 8500000, 'images/room3.jpg', 'Tất cả dịch vụ cao cấp nhất')
    ]
    cursor.executemany('INSERT INTO rooms (name, description, price, image, amenities) VALUES (?, ?, ?, ?, ?)', sample_rooms)

    # Dữ liệu ưu đãi
    du_lieu_uudai = [
        ('UD01', 'Ưu đãi Mùa Hè Rực Rỡ', 'Giảm 30% cho phòng Suite khi đặt trên 3 đêm.', 'images/summer.jpg', 2500000),
        ('UD02', 'Gói Tuần Trăng Mật', 'Tặng bữa tối lãng mạn và trang trí phòng miễn phí.', 'images/honeymoon.jpg', 4500000),
        ('UD03', 'Siêu Sale Cuối Tuần', 'Giảm ngay 20% khi đặt phòng vào Thứ 7 và Chủ Nhật.', 'images/weekend.jpg', 1800000),
        ('UD04', 'Ưu đãi Đặt Sớm', 'Đặt trước 30 ngày để nhận mức giá ưu đãi nhất.', 'images/early.jpg', 1500000),
        ('UD05', 'Kỳ Nghỉ Gia Đình', 'Miễn phí ăn sáng cho 2 người lớn và 2 trẻ em.', 'images/family.jpg', 3200000),
        ('UD06', 'Tiệc Trưa Chủ Nhật', 'Buffet hải sản không giới hạn tại nhà hàng chính.', 'images/buffet.jpg', 850000),
        ('UD07', 'Thư Giãn Cùng Spa', 'Combo phòng ở kèm 60 phút massage toàn thân.', 'images/spa.jpg', 2900000),
        ('UD08', 'Khám Phá Hội An', 'Tour tham quan phố cổ miễn phí cho khách lưu trú từ 2 đêm.', 'images/hoian.jpg', 2100000),
        ('UD09', 'Ưu đãi Thành Viên', 'Giảm thêm 10% cho thành viên đã đăng ký tài khoản.', 'images/member.jpg', 1900000),
        ('UD10', 'Đón Xuân Ấm Áp', 'Tặng quà đặc sản địa phương cho mỗi phòng dịp Tết.', 'images/tet.jpg', 2700000)
    ]
    cursor.executemany("INSERT INTO uu_dai VALUES (?, ?, ?, ?, ?)", du_lieu_uudai)

    # Dữ liệu ảnh trang chủ
    du_lieu_anh_home = [
        ('Phòng ngủ hướng rừng', 'https://images.unsplash.com/photo-1618773928121-c32242e63f39'),
        ('Bể bơi vô cực', 'https://images.unsplash.com/photo-1571896349842-33c89424de2d'),
        ('Nhà hàng sang trọng', 'https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b')
    ]
    cursor.executemany("INSERT INTO anh_gioi_thieu (mo_ta, anh_url) VALUES (?, ?)", du_lieu_anh_home)

    conn.commit()
    conn.close()
    print("--- HOÀN TẤT: Đã hợp nhất và khởi tạo hotel.db thành công! ---")

if __name__ == '__main__':
    init_all_db()