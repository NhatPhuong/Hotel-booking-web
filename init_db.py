import psycopg2

def init_online_db():
    try:
        
        conn = psycopg2.connect(
            host="db.oawvygwmlkefpexsrbuu.supabase.co",
            database="postgres",
            user="postgres",
            password="VmTs24420943", 
            port="5432",
            sslmode="require" 
        )
        
        cursor = conn.cursor()
        print("--- Đang kết nối thành công, chuẩn bị tạo bảng ---")

        # 1. Bảng Ưu đãi
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS UU_DAI (
            MAPH TEXT PRIMARY KEY,
            TIEU_DE TEXT NOT NULL,
            MO_TA TEXT,
            ANH_URL TEXT,
            PHAN_TRAM_GIAM NUMERIC
        )
        ''')

        # CHÈN 10 DÒNG DỮ LIỆU MẪU VÀO ĐÂY
        du_lieu_uudai = [
            ('UD01', 'Ưu đãi Mùa Hè Rực Rỡ', 'Giảm 30% cho phòng Suite khi đặt trên 3 đêm.', 'mua_he_ruc_ro.jpg', 15.00),
            ('UD02', 'Gói Tuần Trăng Mật', 'Tặng bữa tối lãng mạn và trang trí phòng miễn phí.', 'tuan_trang_mat.jpg', 20.00),
            ('UD03', 'Siêu ưu đãi Cuối Tuần', 'Giảm ngay 20% khi đặt phòng vào Thứ 7 và Chủ Nhật.', 'sieu_sale_cuoi_tuan.jpg', 20.00),
            ('UD04', 'Ưu đãi Đặt Sớm', 'Đặt trước 30 ngày để nhận mức giá ưu đãi nhất.', 'uu_dai_dat_som.jpg', 5.00),
            ('UD05', 'Ưu đãi Thành Viên', 'Giảm thêm 10% cho thành viên đã đăng ký tài khoản.', 'thanh_vien.jpg', 15.00),
            ('UD06', 'Đón Xuân Ấm Áp', 'Tặng quà đặc sản địa phương cho mỗi phòng dịp Tết.', 'tet.jpg', 10.00)
        ]
        cursor.executemany("INSERT INTO UU_DAI VALUES (%s, %s, %s, %s, %s) ON CONFLICT (MAPH) DO NOTHING", du_lieu_uudai)

        # 2. Bảng Liên hệ
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS LIEN_HE (
            ID SERIAL PRIMARY KEY, 
            HO_TEN TEXT, 
            EMAIL TEXT, 
            SDT TEXT, 
            NOI_DUNG TEXT
        )
        ''')

        # 3. Bảng Đặt phòng
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS DAT_PHONG (
            ID SERIAL PRIMARY KEY,
            TEN_KHACH TEXT,
            NGAY_DEN TEXT NOT NULL,
            NGAY_DI TEXT NOT NULL,
            NGUOI_LON INTEGER DEFAULT 1,
            TRE_EM_6_11 INTEGER DEFAULT 0,
            TRE_EM_0_5 INTEGER DEFAULT 0,
            NGAY_TAO TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 4. Bảng Ảnh Giới Thiệu (Trang Chủ)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ANH_GIOI_THIEU (
            ID SERIAL PRIMARY KEY,
            MO_TA TEXT,
            ANH_URL TEXT
        )
        ''')

        # Chèn ảnh
        du_lieu_anh_home = [
            ('Phòng ngủ hướng rừng', 'https://www.pinterest.com/pin/16818198602975038/'),
            ('Bể bơi vô cực', 'https://www.pinterest.com/pin/1139340405760189190/'),
            ('Nhà hàng sang trọng', 'https://www.pinterest.com/pin/424112489934147826/')
        ]
        cursor.executemany("INSERT INTO ANH_GIOI_THIEU (MO_TA, ANH_URL) VALUES (%s, %s) ON CONFLICT (ID) DO NOTHING", du_lieu_anh_home)
        
        # 3. Bảng Phòng nghỉ
        # Tạo bảng PHONG_NGHI nếu chưa có
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS PHONG_NGHI (
            MA_PHONG TEXT PRIMARY KEY,
            TEN_PHONG TEXT NOT NULL,
            GIA_DEM INTEGER,
            DIEN_TICH TEXT,
            TIEN_ICH TEXT,
            MO_TA TEXT,
            ANH_URL TEXT
        )
        ''')

        # Danh sách 10 phòng dựa trên dữ liệu bạn cung cấp
        du_lieu_phong_forest = [
            ('FDR01', 'Forest Deluxe Room', 1800000, '35 m²', 
            'Giường King size, Ban công hướng rừng, Smart TV, Phòng tắm riêng, Trà & Cà phê miễn phí', 
            'Forest Deluxe Room mang đến không gian nghỉ dưỡng tinh tế giữa thiên nhiên xanh mát. Từ ban công riêng, du khách có thể tận hưởng khung cảnh rừng yên bình và bầu không khí trong lành.',
            '1.jpg'),

            ('PFR02', 'Premium Forest Room', 2200000, '40 m²', 
            'Giường King size, Ban công lớn, Bồn tắm sang trọng, Smart TV, WiFi tốc độ cao, Điều hòa cao cấp', 
            'Premium Forest Room kết hợp giữa sự sang trọng và vẻ đẹp thiên nhiên, mang đến trải nghiệm nghỉ dưỡng cao cấp cho những du khách yêu thích sự yên tĩnh.',
            '2.webp'),

            ('PAN03', 'Panorama Forest Room', 2500000, '42 m²', 
            'Giường King size, Cửa kính toàn cảnh nhìn ra rừng, Bồn tắm lớn, Smart TV, WiFi tốc độ cao', 
            'Với cửa kính toàn cảnh, Panorama Forest Room mang đến trải nghiệm hòa mình hoàn toàn vào thiên nhiên. Mỗi buổi sáng, bạn sẽ được thức dậy cùng ánh nắng và tiếng chim rừng.',
            '3.webp'),

            ('GSU04', 'Garden Suite', 3000000, '50 m²', 
            'Giường King size, Sân vườn riêng, Phòng khách nhỏ, Bồn tắm sang trọng', 
            'Garden Suite mang đến không gian riêng tư với khu vườn nhỏ, nơi du khách có thể thư giãn và tận hưởng sự yên bình của thiên nhiên.',
            '4.jpg'),

            ('THS05', 'Treehouse Suite', 3300000, '55 m²', 
            'Giường King size, Phòng ngủ trên cây, Bồn tắm giữa thiên nhiên, Smart TV', 
            'Treehouse Suite là trải nghiệm độc đáo như sống trong ngôi nhà trên cây, mang đến cảm giác gần gũi với thiên nhiên nhưng vẫn đầy đủ tiện nghi cao cấp.',
            '5.jpeg'),

            ('RFS06', 'Romantic Forest Suite', 2300000, '35 m²', 
            'Giường đôi sang trọng, Ban công riêng, Nến và trang trí lãng mạn', 
            'Romantic Forest Suite được thiết kế dành riêng cho các cặp đôi, mang đến không gian ấm áp, riêng tư và đầy lãng mạn giữa thiên nhiên.',
            '6.jpg'),

            ('FFS07', 'Family Forest Suite', 3200000, '70 m²', 
            'Giường King size, Ban công lớn, Smart TV, Bữa sáng cho 4 người, Trà và cà phê miễn phí', 
            'Family Forest Suite là lựa chọn hoàn hảo cho gia đình hoặc nhóm bạn, với không gian rộng rãi và đầy đủ tiện nghi cho kỳ nghỉ đáng nhớ.',
            '7.avif'),

            ('FPV08', 'Forest Pool Villa', 5500000, '110 m²', 
            'Giường King size, Hồ bơi riêng, Sân hiên lớn, Mini bar cao cấp, WiFi tốc độ cao', 
            'Forest Pool Villa mang đến trải nghiệm nghỉ dưỡng đẳng cấp với hồ bơi riêng giữa khu rừng xanh, nơi bạn có thể thư giãn hoàn toàn trong không gian riêng tư.',
            '8.jpg'),

            ('LFV09', 'Luxury Forest Villa', 8500000, '160 m²', 
            'Giường King size, Phòng khách sang trọng, Sân hiên toàn cảnh rừng, Hồ bơi lớn, Dịch vụ phòng 24/7', 
            'Luxury Forest Villa mang đến sự kết hợp hoàn hảo giữa thiên nhiên và sự sang trọng, dành cho những du khách muốn tận hưởng kỳ nghỉ đẳng cấp.',
            '9.jpg'),

            ('PFV10', 'Presidential Forest Villa', 10000000, '180 m²', 
            '2 phòng ngủ King size, Hồ bơi riêng, Phòng khách lớn, Phòng ăn riêng, Bồn tắm sang trọng, Mini bar cao cấp', 
            'Presidential Forest Villa là không gian nghỉ dưỡng đỉnh cao của khách sạn, mang đến sự riêng tư tuyệt đối cùng các dịch vụ cao cấp dành cho những vị khách đặc biệt.',
            '10.jpg'),
        ]

        cursor.executemany("INSERT INTO PHONG_NGHI VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (MA_PHONG) DO NOTHING", du_lieu_phong_forest)
        # 4. Bảng Giới thiệu Nhà hàng
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS GIOI_THIEU_NHA_HANG (
            ID INTEGER PRIMARY KEY,
            TEN_NHA_HANG TEXT,
            LOI_GIOI_THIEU TEXT,
            ANH_BIA_URL TEXT
        )
        ''')

        # Dữ liệu giới thiệu nhà hàng ViVuk
        gioi_thieu = [
            (1, 'Nhà hàng ViVuk', 
            'Tọa lạc giữa những cánh rừng đại ngàn, Nhà hàng ViVuk mang đến một không gian mộc mạc và gần gũi với thiên nhiên. Kiến trúc gỗ đặc trưng hòa quyện cùng mùi hương nhựa thông thoang thoảng tạo nên một không khí ấm cúng cho mỗi bữa tiệc. Thực đơn của chúng tôi được tuyển chọn từ những nguyên vật liệu tươi ngon nhất của núi rừng, mang đậm phong vị hoang sơ và tinh tế. Hãy để ViVuk dẫn dắt bạn vào một hành trình ẩm thực độc đáo, nơi vị giác và tâm hồn cùng được vỗ về.',
            'https://www.pinterest.com/pin/2181499816877034/')
        ]

        cursor.executemany("INSERT INTO GIOI_THIEU_NHÀ_HANG VALUES (%s, %s, %s, %s) ON CONFLICT (ID) DO NOTHING", gioi_thieu)

        # 5. Bảng Menu món ăn
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS MENU_MON_AN (
            MAMON TEXT PRIMARY KEY,
            TENMON TEXT NOT NULL,
            MO_TA TEXT,
            GIA INTEGER,
            LOAI TEXT, -- Nướng, Salad, Tráng miệng, Lẩu, Nước ngọt, Cocktail
            ANH_URL TEXT
        )
        ''')
        du_lieu_menu = [
            # 4 Món nướng
            ('NU01', 'Gà Đồi Nướng Ống Tre', 'Gà ta thả vườn nướng thơm lừng trong ống tre non.', 350000, 'Nướng', 'https://www.pinterest.com/pin/703687510568028432/'),
            ('NU02', 'Lợn Bản Nướng Mắc Khén', 'Thịt lợn bản dai giòn nướng cùng gia vị đặc trưng Tây Bắc.', 280000, 'Nướng', 'lonmackhen.jpg'),
            ('NU03', 'Thịt Trâu Gác Bếp Nướng Than Hồng', 'Hương vị hun khói nồng nàn, xé nhỏ nhắm cùng rượu ngô.', 420000, 'Nướng', 'traugacbep.png'),
            ('NU04', 'Cơm Lam Thịt Xiên Rừng', 'Sự kết hợp hoàn hảo giữa gạo nếp nương và thịt rừng nướng.', 150000, 'Nướng', 'comlamthitxien.jpg'),
            
            # 3 Món Salad
            ('SA01', 'Nộm rau dớn', 'Rau rừng tươi sạch thu hái trong ngày.', 95000, 'Salad', 'raudon.png'),
            ('SA02', 'Nộm Hoa Chuối Rừng Thịt Gác Bếp', 'Vị chát nhẹ của hoa chuối hòa cùng thịt khô đậm đà.', 120000, 'Salad', 'nomchuoi.png'),
            ('SA03', 'Gỏi Măng Chua Tai Heo', 'Măng chua giòn rụm thanh mát.', 110000, 'Salad', 'taiheo.png'),
            
            # 3 Món Tráng miệng
            ('TM01', 'Sữa Chua Nếp Cẩm', 'Vị ngọt dịu của nếp nương lên men.', 45000, 'Tráng miệng', 'sữa chua nếp cẩm.webp'),
            ('TM02', 'Chè Khoai Môn Rừng', 'Khoai môn dẻo bùi nấu cùng cốt dừa béo ngậy.', 40000, 'Tráng miệng', 'chè khoai môn rừng.jpg'),
            ('TM03', 'Hoa Quả Theo Mùa', 'Các loại trái cây tươi ngon từ địa phương.', 80000, 'Tráng miệng', 'hoa quả theo mùa.jpg'),
            
            # 2 Món Lẩu
            ('LA01', 'Lẩu Cá Tầm Măng Chua', 'Thịt cá tầm dai ngọt kết hợp măng rừng chua cay.', 650000, 'Lẩu', 'lẩu cá tầm măng chua.jpeg'),
            ('LA02', 'Lẩu Gà Đen Hầm Nấm Rừng', 'Món ăn bổ dưỡng với các loại nấm quý của đại ngàn.', 580000, 'Lẩu', 'lẩu gà đen hầm nấm rừng.jpg'),

            # Nước (Nước ngọt & Cocktail)
            ('DW01', 'Nước Ngọt Các Loại', 'Coca, Sprite, Fanta...', 25000, 'Nước ngọt', 'nước ngọt.jpg'),
            ('DW02', 'Cocktail Rừng Thông', 'Sự pha trộn giữa rượu Gin và tinh dầu lá thông độc đáo.', 120000, 'Cocktail', 'cocktail.jpg'),
        ]
        cursor.executemany("INSERT INTO MENU_MON_AN VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (MAMON) DO NOTHING", du_lieu_menu)

        conn.commit()
        conn.close()
        print("Đã tạo bảng thành công trên Supabase!")
    except Exception as e:
        print(f"Lỗi kết nối rồi bạn ơi: {e}")

if __name__ == "__main__":
    init_online_db()
