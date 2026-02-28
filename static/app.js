const API_BASE_URL = window.location.origin;

// ================= DANH SÁCH PHÒNG (index.html) =================
async function loadRooms() {
    const container = document.getElementById("rooms-container");
    if (!container) return;

    try {
        const res = await fetch(`${API_BASE_URL}/api/rooms`);
        const rooms = await res.json();

        if (!rooms || rooms.length === 0) {
            container.innerHTML = '<p class="text-center text-muted">Không có phòng nào hiện sẵn.</p>';
            return;
        }

        container.innerHTML = rooms.map(room => `
            <div class="col-md-4 mb-5 animate__animated animate__fadeInUp">
                <div class="room-card">
                    <img src="${room.image_url}" alt="${room.name}">
                    
                    <div class="room-info-basic">
                        <h4 class="mb-0">${room.name}</h4>
                        <p class="text-muted small mb-0">${room.price.toLocaleString('vi-VN')} VNĐ / Night</p>
                    </div>

                    <div class="room-info-detail">
                        <h3 class="mb-2">${room.name}</h3>
                        <p class="small text-muted mb-3">Diện tích: ${room.area}m² | View: ${room.view}</p>
                        <h4 class="mb-4" style="color: var(--gold)">${room.price.toLocaleString('vi-VN')} VNĐ</h4>
                        <div class="d-flex justify-content-center">
                            <button class="btn-details" onclick="viewRoomDetail(${room.id})">Chi tiết</button>
                            <button class="btn-book-now" onclick="viewRoomDetail(${room.id})">Đặt ngay</button>
                        </div>
                    </div>
                </div>
            </div>
        `).join("");
    } catch (err) {
        console.error("Lỗi load rooms:", err);
    }
}

// ================= ẨM THỰC (index.html) =================
async function loadFoods() {
    const container = document.getElementById("foods-container");
    if (!container) return;

    try {
        const res = await fetch(`${API_BASE_URL}/api/foods`);
        const foods = await res.json();

        container.innerHTML = foods.map(food => `
            <div class="col-md-3 mb-4 animate__animated animate__fadeIn">
                <div class="card border-0 shadow-sm h-100 room-card" style="height: auto;">
                    <div style="height: 200px; overflow: hidden;">
                        <img src="${food.image_url}" class="w-100 h-100" style="object-fit: cover;" alt="${food.name}">
                    </div>
                    <div class="card-body text-center p-4">
                        <h6 class="text-uppercase mb-1" style="color: var(--gold); font-size: 0.7rem; letter-spacing: 2px;">${food.category}</h6>
                        <h5 class="fw-bold" style="font-family: 'Playfair Display', serif;">${food.name}</h5>
                        <p class="small text-muted mb-2">${food.description}</p>
                        <h6 class="fw-bold" style="color: var(--dark-forest);">${food.price.toLocaleString('vi-VN')} VNĐ</h6>
                    </div>
                </div>
            </div>
        `).join("");
    } catch (err) {
        console.error("Lỗi load foods:", err);
    }
}

function viewRoomDetail(roomId) {
    // Đảm bảo Flask route nhận /room-detail
    window.location.href = `/room-detail?id=${roomId}`;
}

// ================= CHI TIẾT PHÒNG (room-detail.html) =================

async function loadRoomDetail() {
    const container = document.getElementById("room-detail");
    if (!container) return;

    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");
    if (!id) return;

    try {
        const res = await fetch(`${API_BASE_URL}/api/rooms/${id}`);
        const room = await res.json();

        container.innerHTML = `
            <div class="row g-5 align-items-center animate__animated animate__fadeIn">
                <div class="col-md-6">
                    <div class="img-container rounded shadow-lg" style="overflow: hidden;">
                        <img src="${room.image_url}" class="img-fluid w-100 shadow" style="transition: 0.6s;" alt="${room.name}">
                    </div>
                </div>
                <div class="col-md-6">
                    <h6 class="text-uppercase" style="color: #c5a47e; letter-spacing: 3px;">Luxury Experience</h6>
                    <h1 class="display-5 fw-bold mb-3" style="font-family: 'Playfair Display', serif;">${room.name}</h1>
                    <div class="d-flex mb-4">
                        <span class="me-4"><i class="fa fa-expand text-warning me-2"></i>${room.area}m²</span>
                        <span><i class="fa fa-eye text-warning me-2"></i>${room.view}</span>
                    </div>
                    <h3 style="color:#c5a47e;" class="mb-4 fw-bold">
                        ${room.price.toLocaleString('vi-VN')} VNĐ <small class="text-muted" style="font-size: 1rem;">/ Night</small>
                    </h3>
                    <p class="text-muted mb-4" style="line-height: 1.8;">${room.description}</p>

                    <button id="show-booking-btn" class="btn btn-luxury px-5 py-3 fw-bold text-white shadow">
                        ĐẶT PHÒNG NGAY
                    </button>

                    <div id="booking-wrapper" class="mt-4 p-4 border-start border-warning border-4 bg-light shadow-sm" style="display:none;">
                        </div>
                </div>
            </div>
        `;

        document.getElementById("show-booking-btn").addEventListener("click", function() {
            const wrapper = document.getElementById("booking-wrapper");
            wrapper.style.display = "block"; // Hiện form
            this.style.display = "none";     // Ẩn nút đặt ngay
            renderBookingForm(room);
        });
    } catch (err) {
        container.innerHTML = "<p class='text-center text-danger'>Lỗi nạp dữ liệu.</p>";
    }
}

function renderBookingForm(room) {
    const wrapper = document.getElementById("booking-wrapper");
    wrapper.innerHTML = `
        <h4 class="mb-4" style="font-family: 'Playfair Display', serif;">Thông Tin Đặt Phòng</h4>
        <form id="booking-form">
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label class="form-label small fw-bold">Ngày nhận phòng</label>
                    <input type="date" class="form-control rounded-0" id="check-in" required>
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label small fw-bold">Ngày trả phòng</label>
                    <input type="date" class="form-control rounded-0" id="check-out" required>
                </div>
            </div>
            <div class="mb-3">
                <label class="form-label small fw-bold">Họ và tên khách hàng</label>
                <input type="text" class="form-control rounded-0" id="guest-name" placeholder="Nhập tên của bạn" required>
            </div>
            <div class="mb-3">
                <label class="form-label small fw-bold">Số điện thoại liên hệ</label>
                <input type="tel" class="form-control rounded-0" id="guest-phone" placeholder="Ví dụ: 0912345678" required>
            </div>
            <button type="submit" class="btn btn-dark w-100 py-3 fw-bold rounded-0 mt-2" style="letter-spacing: 1px;">
                XÁC NHẬN ĐẶT PHÒNG
            </button>
        </form>
        <div id="booking-message" class="mt-3"></div>
    `;
    setupBookingForm(room);
}

// =============== GỬI BOOKING TỚI BACKEND ===============

function setupBookingForm(room) {
    const form = document.getElementById("booking-form");
    const messageDiv = document.getElementById("booking-message");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        messageDiv.className = "mt-3 text-muted";
        messageDiv.textContent = "Đang gửi yêu cầu...";

        const checkIn = document.getElementById("check-in").value;
        const checkOut = document.getElementById("check-out").value;
        const guestName = document.getElementById("guest-name").value;
        const guestPhone = document.getElementById("guest-phone").value;

        try {
            const res = await fetch(`${API_BASE_URL}/api/bookings`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    room_id: room.id,
                    check_in: checkIn,
                    check_out: checkOut,
                    guest_name: guestName,
                    guest_phone: guestPhone,
                }),
            });

            const data = await res.json();

            if (res.ok && data.success) {
                messageDiv.className = "mt-3 text-success";
                messageDiv.textContent = data.message || "Đặt phòng thành công!";
                form.reset();
            } else {
                messageDiv.className = "mt-3 text-danger";
                messageDiv.textContent = data.message || "Đặt phòng thất bại.";
            }
        } catch (error) {
            console.error("Lỗi gửi booking:", error);
            messageDiv.className = "mt-3 text-danger";
            messageDiv.textContent = "Không kết nối được server.";
        }
    });
}

// ================= GẮN SỰ KIỆN CHUNG =================
document.addEventListener("DOMContentLoaded", () => {
    loadRooms();
    loadFoods();
    loadRoomDetail();
});

// Hiệu ứng Navbar khi cuộn
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }
});