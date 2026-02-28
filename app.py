from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# =================================================================
# 1. CẤU HÌNH DATABASE (Dùng chung cho toàn hệ thống)
# =================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "hotel.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Tạo bảng bookings nếu chưa tồn tại khi chạy ứng dụng"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL,
            check_in TEXT NOT NULL,
            check_out TEXT NOT NULL,
            guest_name TEXT NOT NULL,
            guest_phone TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()

# =================================================================
# 2. KHO DỮ LIỆU TĨNH (Dùng cho cả Trang chủ và Trang phòng nghỉ)
# =================================================================
rooms = [
    {"id": 1, "name": "Kingsize Beach View", "price": 2500000, "area": 50, "view": "Biển", "image_url": "images/room1.jpg", "description": "Phòng giường king rộng rãi, view biển, phù hợp cặp đôi hoặc gia đình nhỏ."},
    {"id": 2, "name": "Deluxe Garden View", "price": 1800000, "area": 40, "view": "Vườn", "image_url": "images/room2.jpg", "description": "Phòng deluxe ấm cúng, nhìn ra khu vườn xanh mát, yên tĩnh."},
    {"id": 3, "name": "Premium Ocean Suite", "price": 3500000, "area": 70, "view": "Biển", "image_url": "images/room3.jpg", "description": "Suite cao cấp với phòng khách riêng, ban công rộng, hướng biển toàn cảnh."},
    {"id": 4, "name": "Family City View", "price": 2200000, "area": 60, "view": "Thành phố", "image_url": "images/room4.jpg", "description": "Phòng gia đình 2 giường queen, view thành phố, phù hợp nhóm bạn hoặc gia đình 4 người."},
    {"id": 5, "name": "Standard Cozy Room", "price": 1300000, "area": 28, "view": "Nội khu", "image_url": "images/room5.jpg", "description": "Phòng tiêu chuẩn gọn gàng, đầy đủ tiện nghi, phù hợp khách công tác ngắn ngày."},
]

foods = [
    {"id": 1, "name": "Hải sản nướng thập cẩm", "price": 450000, "category": "Seafood", "image_url": "images/food1.jpg", "description": "Tôm, mực..."},
    {"id": 8, "name": "Nước ép cam tươi", "price": 75000, "category": "Juice", "image_url": "images/drink_juice_orange.jpg", "description": "Cam tươi ép..."},
    # ... (Bạn có thể thêm tiếp danh sách foods của bạn ở đây)
]

# =================================================================
# 3. PHÂN ĐOẠN: TRANG CHỦ (INDEX)
# =================================================================
@app.route('/')
def index():
    """Hiển thị trang chủ với Top 3 phòng được đặt nhiều nhất"""
    conn = get_db_connection()
    # Đếm lượt đặt từng phòng trong Database
    query = "SELECT room_id, COUNT(id) as count FROM bookings GROUP BY room_id ORDER BY count DESC"
    booking_counts = conn.execute(query).fetchall()
    conn.close()

    counts_dict = {row['room_id']: row['count'] for row in booking_counts}
    
    # Sắp xếp danh sách phòng dựa trên lượt đặt (giảm dần)
    sorted_rooms = sorted(rooms, key=lambda x: counts_dict.get(x['id'], 0), reverse=True)
    
    # Chỉ lấy 3 phòng đầu tiên để hiện ở trang chủ
    featured_rooms = sorted_rooms[:3]
    return render_template('index.html', featured_rooms=featured_rooms)

# =================================================================
# 4. PHÂN ĐOẠN: PHÒNG NGHỈ (ROOMS)
# =================================================================

@app.route('/all-rooms')
def all_rooms_page():
    """Giao diện danh sách TOÀN BỘ phòng (Trang 'Xem thêm')"""
    return render_template('all_rooms.html', rooms=rooms)

@app.route('/room-detail/<int:room_id>')
def room_detail_page(room_id):
    room = next((r for r in rooms if r["id"] == room_id), None)
    if not room:
        return "Phòng không tồn tại", 404 # Thêm dòng này để tránh lỗi
    return render_template('room-detail.html', room=room)

@app.route("/api/rooms", methods=["GET"])
def get_rooms_api():
    """API trả về dữ liệu JSON của tất cả các phòng"""
    return jsonify(rooms), 200

# =================================================================
# 5. PHÂN ĐOẠN: ĐẶT PHÒNG (BOOKING) - LƯU VÀO DATABASE
# =================================================================
@app.route("/api/bookings", methods=["POST"])
def create_booking():
    """Xử lý yêu cầu đặt phòng từ khách hàng"""
    data = request.get_json()
    room_id = int(data.get("room_id"))
    check_in = data.get("check_in")
    check_out = data.get("check_out")
    guest_name = data.get("guest_name", "").strip()
    guest_phone = data.get("guest_phone", "").strip()

    # Kiểm tra logic ngày tháng
    d_in = datetime.strptime(check_in, "%Y-%m-%d").date()
    d_out = datetime.strptime(check_out, "%Y-%m-%d").date()
    if d_out <= d_in:
        return jsonify(success=False, message="Ngày trả phòng phải sau ngày nhận phòng"), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # Kiểm tra xem phòng đã bị ai đặt trùng ngày chưa
    cur.execute(
        "SELECT COUNT(*) as cnt FROM bookings WHERE room_id = ? AND date(check_in) < date(?) AND date(check_out) > date(?)",
        (room_id, check_out, check_in)
    )
    if cur.fetchone()["cnt"] > 0:
        conn.close()
        return jsonify(success=False, message="Phòng đã có người đặt trong thời gian này"), 409

    # Nếu ổn, tiến hành lưu vào Database
    cur.execute(
        "INSERT INTO bookings (room_id, check_in, check_out, guest_name, guest_phone) VALUES (?, ?, ?, ?, ?)",
        (room_id, check_in, check_out, guest_name, guest_phone)
    )
    conn.commit()
    conn.close()
    return jsonify(success=True, message="Đặt phòng thành công!"), 201

# =================================================================
# 6. PHÂN ĐOẠN: ẨM THỰC & KHÁC (FOODS & ABOUT)
# =================================================================
@app.route('/aboutus')
def aboutus():
    """Trang giới thiệu khách sạn"""
    return render_template('aboutus.html')

@app.route("/api/foods", methods=["GET"])
def get_foods_api():
    """API lấy danh sách món ăn"""
    return jsonify(foods), 200

# =================================================================
# CHẠY ỨNG DỤNG
# =================================================================
if __name__ == "__main__":
    init_db()  # Tự động tạo bảng khi bật server
    app.run(host="0.0.0.0", port=8000, debug=True)