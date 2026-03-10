import os
import psycopg2
from psycopg2.extras import DictCursor
from flask import Flask, render_template, request

app = Flask(__name__)


def get_db():
    
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        conn = psycopg2.connect(db_url, sslmode='require')
    else:
        
        conn = psycopg2.connect(
            host="db.oawvygwmlkefpexsrbuu.supabase.co",
            database="postgres",
            user="postgres",
            password="VmTs24420943", 
            port="5432",
            sslmode="require"
        )
    return conn

# --- 1. TRANG CHỦ ---
@app.route('/')
def index():
    loi_tri_an = {
        "tieu_de": "Lời Tri Ân Từ F4 Hotel",
        "noi_dung": "Hành trình của chúng tôi không thể trọn vẹn nếu thiếu đi sự tin tưởng của Quý khách..."
    }
    db = get_db()
    
    cur = db.cursor(cursor_factory=DictCursor)
    cur.execute('SELECT * FROM ANH_GIOI_THIEU')
    images = cur.fetchall()
    cur.close()
    db.close()
    return render_template('index.html', tri_an=loi_tri_an, images=images)

# --- 2. TRANG ƯU ĐÃI ---
@app.route('/uu-dai')
def uu_dai():
    db = get_db()
    cur = db.cursor(cursor_factory=DictCursor)
    cur.execute('SELECT * FROM UU_DAI')
    danh_sach = cur.fetchall()
    cur.close()
    db.close()
    return render_template('uudai.html', danh_sach_uu_dai=danh_sach)

# --- 3. TRANG LIÊN HỆ ---
@app.route('/lien-he', methods=['GET', 'POST'])
def lien_he():
    if request.method == 'POST':
        ten = request.form.get('ho_ten')
        email = request.form.get('email')
        sdt = request.form.get('sdt')
        noi_dung = request.form.get('noi_dung')
        
        db = get_db()
        cur = db.cursor()
        
        cur.execute('INSERT INTO LIEN_HE (HO_TEN, EMAIL, SDT, NOI_DUNG) VALUES (%s, %s, %s, %s)',
                    (ten, email, sdt, noi_dung))
        db.commit()
        cur.close()
        db.close()
        return "Cảm ơn bạn đã liên hệ!"
    
    return render_template('lienhe.html')

# --- 4. TRANG ĐẶT PHÒNG ---
@app.route('/dat-phong', methods=['GET', 'POST'])
def dat_phong():
    if request.method == 'POST':
        ten_kh = request.form.get('ten_khach')
        ngay_den = request.form.get('ngay_den')
        ngay_di = request.form.get('ngay_di')
        
        db = get_db()
        cur = db.cursor()
        
        cur.execute('INSERT INTO DAT_PHONG (TEN_KHACH, NGAY_DEN, NGAY_DI) VALUES (%s, %s, %s)',
                    (ten_kh, ngay_den, ngay_di))
        db.commit()
        cur.close()
        db.close()
        return "Đặt phòng thành công!"
        
    return render_template('datphong.html')

# --- 5. TRANG PHÒNG NGHỈ ---
@app.route('/all-rooms')
def all_rooms():
    db = get_db()
    cur = db.cursor()
    # Lấy toàn bộ danh sách 10 phòng từ bảng PHONG_NGHI
    cur.execute("SELECT * FROM PHONG_NGHI")
    rooms = cur.fetchall()
    cur.close()
    db.close()
    return render_template('all_rooms.html', rooms=rooms)

# --- 6. TRANG ẨM THỰC (NHÀ HÀNG VIVUK) ---
@app.route('/am-thuc')
def am_thuc():
    db = get_db()
    cur = db.cursor()
    
    # 1. Lấy thông tin giới thiệu nhà hàng ViVuk
    cur.execute("SELECT * FROM GIOI_THIEU_NHA_HANG WHERE ID = 1")
    restaurant_info = cur.fetchone()
    
    # 2. Lấy menu và phân loại theo LOAI để dễ hiển thị trên giao diện
    cur.execute("SELECT * FROM MENU_MON_AN")
    all_menu = cur.fetchall()
    
    # Phân loại món ăn ngay trong logic để Frontend chỉ việc hiển thị
    menu_divided = {
        'nuong': [m for m in all_menu if m[4] == 'Nướng'],
        'salad': [m for m in all_menu if m[4] == 'Salad'],
        'trang_mieng': [m for m in all_menu if m[4] == 'Tráng miệng'],
        'lau': [m for m in all_menu if m[4] == 'Lẩu'],
        'nuoc': [m for m in all_menu if m[4] in ['Nước ngọt', 'Cocktail']]
    }
    
    cur.close()
    db.close()
    return render_template('amthuc.html', info=restaurant_info, menu=menu_divided)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)