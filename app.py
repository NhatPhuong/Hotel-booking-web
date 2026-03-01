from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# =================================================================
# 1. CẤU HÌNH DATABASE DÙNG CHUNG
# =================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "hotel.db")

def get_db_connection():
    """Hàm kết nối DB dùng chung cho toàn bộ ứng dụng"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# =================================================================
# 2. DỮ LIỆU TĨNH (Rooms & Foods)
# =================================================================
rooms_data = [
    {"id": 1, "name": "Kingsize Beach View", "price": 2500000, "area": 50, "view": "Biển", "image_url": "images/room1.jpg", "description": "Phòng giường king rộng rãi, view biển, phù hợp cặp đôi hoặc gia đình nhỏ."},
    {"id": 2, "name": "Deluxe Garden View", "price": 1800000, "area": 40, "view": "Vườn", "image_url": "images/room2.jpg", "description": "Phòng deluxe ấm cúng, nhìn ra khu vườn xanh mát, yên tĩnh."},
    {"id": 3, "name": "Premium Ocean Suite", "price": 3500000, "area": 70, "view": "Biển", "image_url": "images/room3.jpg", "description": "Suite cao cấp với phòng khách riêng, ban công rộng, hướng biển toàn cảnh."},
    {"id": 4, "name": "Family City View", "price": 2200000, "area": 60, "view": "Thành phố", "image_url": "images/room4.jpg", "description": "Phòng gia đình 2 giường queen, view thành phố, phù hợp nhóm bạn hoặc gia đình 4 người."},
    {"id": 5, "name": "Standard Cozy Room", "price": 1300000, "area": 28, "view": "Nội khu", "image_url": "images/room5.jpg", "description": "Phòng tiêu chuẩn gọn gàng, đầy đủ tiện nghi, phù hợp khách công tác ngắn ngày."},
]

# =================================================================
# 3. CÁC ROUTE TRANG GIAO DIỆN
# =================================================================

@app.route('/')
def index():
    """Trang chủ: Kết hợp Top 3 phòng và Lời tri ân"""
    loi_tri_an = {
        "tieu_de": "Lời Tri Ân Từ F4 Hotel",
        "noi_dung": "Hành trình của chúng tôi không thể trọn vẹn nếu thiếu đi sự tin tưởng của Quý khách..."
    }
    
    conn = get_db_connection()
    # Lấy ảnh giới thiệu từ DB
    images = conn.execute('SELECT * FROM anh_gioi_thieu').fetchall()
    
    # Logic Top 3 phòng đặt nhiều nhất
    query = "SELECT room_id, COUNT(id) as count FROM bookings GROUP BY room_id ORDER BY count DESC"
    booking_counts = conn.execute(query).fetchall()
    conn.close()

    counts_dict = {row['room_id']: row['count'] for row in booking_counts}
    sorted_rooms = sorted(rooms_data, key=lambda x: counts_dict.get(x['id'], 0), reverse=True)
    featured_rooms = sorted_rooms[:3]

    return render_template('index.html', featured_rooms=featured_rooms, tri_an=loi_tri_an, images=images)

@app.route('/phong-nghi')
@app.route('/all-rooms')
def all_rooms_page():
    """Giao diện danh sách toàn bộ phòng"""
    return render_template('all_rooms.html', rooms=rooms_data)

@app.route('/room-detail/<int:room_id>')
def room_detail_page(room_id):
    """Trang chi tiết từng phòng"""
    room = next((r for r in rooms_data if r["id"] == room_id), None)
    if not room:
        return "Phòng không tồn tại", 404
    return render_template('room-detail.html', room=room)

@app.route('/uu-dai')
def uu_dai():
    """Trang ưu đãi lấy từ DB"""
    conn = get_db_connection()
    danh_sach = conn.execute('SELECT * FROM uu_dai').fetchall()
    conn.close()
    return render_template('uudai.html', danh_sach_uu_dai=danh_sach)

@app.route('/lien-he', methods=['GET', 'POST'])
def lien_he():
    """Trang liên hệ và xử lý gửi form"""
    if request.method == 'POST':
        ten = request.form.get('ho_ten')
        email = request.form.get('email')
        sdt = request.form.get('sdt')
        noi_dung = request.form.get('noi_dung')
        
        conn = get_db_connection()
        conn.execute('INSERT INTO lien_he (ho_ten, email, sdt, noi_dung) VALUES (?, ?, ?, ?)',
                     (ten, email, sdt, noi_dung))
        conn.commit()
        conn.close()
        return "Cảm ơn bạn đã liên hệ! Chúng tôi sẽ phản hồi sớm nhất."
    return render_template('lienhe.html')

@app.route('/dat-phong', methods=['GET', 'POST'])
def dat_phong_page():
    """Trang đặt phòng (giao diện lịch của bạn mình)"""
    return render_template('datphong.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

# =================================================================
# 4. CÁC API XỬ LÝ DỮ LIỆU (JSON)
# =================================================================

@app.route("/api/bookings", methods=["POST"])
def create_booking():
    """API Đặt phòng thông minh có kiểm tra trùng lịch"""
    data = request.get_json()
    try:
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
        # Kiểm tra trùng lịch
        conflict = conn.execute(
            "SELECT COUNT(*) as cnt FROM bookings WHERE room_id = ? AND check_in < ? AND check_out > ?",
            (room_id, check_out, check_in)
        ).fetchone()

        if conflict["cnt"] > 0:
            conn.close()
            return jsonify(success=False, message="Phòng đã có người đặt trong thời gian này"), 409

        # Lưu vào DB (Lưu ý: dùng bảng 'bookings' của bạn để khớp logic API)
        conn.execute(
            "INSERT INTO bookings (room_id, check_in, check_out, guest_name, guest_phone) VALUES (?, ?, ?, ?, ?)",
            (room_id, check_in, check_out, guest_name, guest_phone)
        )
        conn.commit()
        conn.close()
        return jsonify(success=True, message="Đặt phòng thành công!"), 201
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

@app.route("/api/rooms", methods=["GET"])
def get_rooms_api():
    return jsonify(rooms_data), 200

# =================================================================
# 5. KHỞI CHẠY
# =================================================================
if __name__ == "__main__":
    # Lưu ý: Bảng bookings sẽ tự tạo nếu bạn đã chạy file init_db hợp nhất
    app.run(host="0.0.0.0", port=8000, debug=True)