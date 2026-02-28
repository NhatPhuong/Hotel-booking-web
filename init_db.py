import sqlite3

def init_db():
    # Kết nối đến file database
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    # 1. Tạo bảng rooms nếu chưa có
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

    # 2. Xóa dữ liệu cũ (nếu muốn làm sạch)
    cursor.execute('DELETE FROM rooms')

    # 3. Thêm dữ liệu mẫu (Khớp với giao diện Forest & Gold của bạn)
    sample_rooms = [
        ('Luxury Forest Suite', 
         'Trải nghiệm không gian mở giữa rừng thông với nội thất gỗ cao cấp.', 
         2500000, 
         'https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=800&q=80',
         'Wifi, Tủ lạnh, Ban công, Bồn tắm'),
        
        ('Grand Mountain View', 
         'Tầm nhìn panorama hướng thẳng ra thung lũng đại ngàn.', 
         3500000, 
         'https://images.unsplash.com/photo-1566665797739-1674de7a421a?auto=format&fit=crop&w=800&q=80',
         'Wifi, Điều hòa, Smart TV, Mini Bar'),
         
        ('F4 Royal President', 
         'Căn hộ cao cấp nhất với dịch vụ quản gia riêng 24/7.', 
         8500000, 
         'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80',
         'Tất cả dịch vụ cao cấp nhất')
    ]

    cursor.executemany('INSERT INTO rooms (name, description, price, image, amenities) VALUES (?, ?, ?, ?, ?)', sample_rooms)

    # Lưu và đóng kết nối
    conn.commit()
    conn.close()
    print("Đã khởi tạo dữ liệu phòng thành công!")

if __name__ == '__main__':
    init_db()