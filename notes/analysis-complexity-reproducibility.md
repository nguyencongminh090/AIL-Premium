# Phân tích: Độ phức tạp & Khả năng Reproduce — Toàn bộ Papers

| Trường | Nội dung |
|--------|----------|
| **Scope** | Toàn bộ 4 papers (001, 003, 004, 008) |
| **Worker** | Orchestrator synthesis (cross-paper) |
| **Ngày** | 2026-06-18 |
| **Câu hỏi** | (1) Papers nào có code public? (2) Độ phức tạp lý thuyết + code? (3) Tự reimplementation được không? |

---

## 1. Tình trạng Code & Dataset công khai

| Paper | Venue | Code | Dataset | Base models/libs |
|-------|-------|------|---------|-----------------|
| **001** PPC | NeurIPS 2025 (arXiv 2026) | Chưa xác nhận (project page tồn tại: vivocameraresearch.github.io/ppc) | GAICD, SACD, FLMS, FCDB, Unsplash — đều public | Wan2.1 14B, CogVideoX 1.5, HunYuan I2V, Qwen2-VL-2B, ViewCrafter — đều open-source |
| **003** HRE | ICCV 2023 (Open Access) | Không nêu trong paper; bản thân paper open access qua CVF | ScanNet — public (cần request) | PointNet — open-source |
| **004** Pairwise | ICCV 2019 (Open Access) | Không nêu trong paper; bản thân paper open access qua CVF | AVA (~250k), FLICKER-AES (40k) — đều public | ResNet-50 pretrained — torchvision |
| **008** 3D Aesthetic | arXiv 2026 | Không nêu trong paper | RE10k, DL3DV — đều public | DepthSplat — open-source; VEN teacher — chưa xác nhận |

> **Kết luận:** Không có paper nào tuyên bố rõ ràng release code. Hướng kiểm tra thêm: trang GitHub của tác giả chính.

---

## 2. Đánh giá độ phức tạp & Khả năng tự Reimplementation

### Bảng tóm tắt

| Paper | Lý thuyết | Code | Compute | Tự implement? | Thời gian ước tính |
|-------|-----------|------|---------|--------------|-------------------|
| **004** Pairwise | Trung bình | Thấp-Trung bình | Nhẹ (GTX 1080Ti) | ✅ Hoàn toàn khả thi | 1–2 tuần |
| **003** HRE | Cao | Cao | Nhẹ (6h / 1× GTX 1080Ti) | ⚠️ Khó nhưng khả thi | 3–6 tuần |
| **008** 3D Aesthetic | Cao | Cao | Trung bình | ⚠️ Khả thi nếu dùng DepthSplat | 4–8 tuần |
| **001** PPC | Trung bình-Cao | Rất cao | **Rất nặng** (50+ H20 GPU hours) | ❌ Không thực tế | N/A |

---

### 004 — Pairwise Aesthetic Assessment ✅

**Lý thuyết cần biết:**
- Pairwise comparison matrix + Saaty's scaling method
- Eigenvalue decomposition (principal eigenvector → score vector)
- Modified Lloyd algorithm (tìm ngưỡng γ, θ cho ternary quantization)
- Không cần background đặc biệt; scipy xử lý phần toán

**Kiến trúc / Code:**
- ResNet-50 (torchvision pretrained) + 4 nhánh local xử lý quadrant của `res4` → cần viết tay nhưng đơn giản
- Siamese wrapper tiêu chuẩn
- `scipy.linalg.eig` cho eigenvalue decomposition
- Reference image selection pipeline — iterative, cần implement riêng

**Dependencies:** PyTorch + scipy + numpy — không cần gì exotic

**Rủi ro chính:** Modified Lloyd algorithm — paper mô tả ngắn, dễ implement sai ràng buộc `r_ij × r_ji = 1`

**Kết luận:** **Reproduce được trong 1–2 tuần.** Dataset public, kiến trúc rõ ràng, không cần GPU mạnh.

---

### 003 — Hyper-Rays & Harmonics Encoding ⚠️

**Lý thuyết cần biết:**
- SE(3) group, quaternion algebra (trung bình)
- Spherical harmonics trên S² (trung bình — tài liệu phong phú)
- **Hyper-spherical harmonics trên S³** (cao — ít tài liệu, công thức chỉ ở appendix paper)
- Spherical Voronoi diagram trên S² và S³

**Kiến trúc / Code:**
- PointNet backbone: có mã nguồn mở
- S² Voronoi pooling: `scipy.spatial.SphericalVoronoi` hỗ trợ ✅
- **S³ Voronoi pooling: KHÔNG có thư viện chuẩn** → phải tự implement nearest-neighbor trên quaternion space ❌
- Custom PyTorch CUDA kernel: paper đề cập nhưng không public → inference rất chậm nếu thiếu ❌
- View Cropping + Gaussian kernel trên Euler angles (Eq. 22–24): custom nhưng khả thi

**Compute:** Nhẹ — 6h trên 1× GTX 1080Ti. Dataset: ScanNet (public, cần request).

**Bottleneck:** S³ Voronoi pooling + CUDA kernel. Ưu tiên implement Location Branch (S²) trước, kiểm tra xong mới đụng Viewpoint Branch (S³).

**Kết luận:** Khả thi nếu nhóm có người hiểu spherical harmonics + quaternion geometry. **Ước tính 3–6 tuần.** Compute nhẹ là lợi thế lớn.

---

### 008 — 3D Aesthetic Field ⚠️

**Lý thuyết cần biết:**
- 3D Gaussian Splatting + feedforward reconstruction
- Feature distillation từ teacher model (MSE trên feature maps)
- Gradient ascent trên SE(3) pose space (5-DoF: 3D translation + yaw + pitch)
- Không cần background toán đặc biệt ngoài deep learning chuẩn

**Kiến trúc / Code:**
- **DepthSplat backbone** (open-source) → phức tạp nhưng có thể dùng lại hoàn toàn ✅
- VEN teacher model → availability chưa xác nhận; nếu không public cần tìm alternative aesthetic model ⚠️
- 3DGS rasterization: dùng pipeline của DepthSplat ✅
- Aesthetic Head + Transformer Downsampler: lightweight, custom nhưng đơn giản ✅
- Gradient ascent 5-DoF: Adam optimizer trên pose parameters — đơn giản khi đã có field ✅

**Compute:** Trung bình — dataset RE10k + DL3DV public; training details trong Supplementary Material.

**Rủi ro chính:** Cài đặt đúng Gaussian Splatting render pipeline; VEN teacher model phải tìm được.

**Kết luận:** Khả thi trong 4–8 tuần **nếu DepthSplat chạy được và VEN available.** Nếu không có VEN, cần tìm substitute 2D aesthetic model.

---

### 001 — Photography Perspective Composition ❌

**Vấn đề cốt lõi:** Phụ thuộc hoàn toàn vào **video foundation models 14B+:**
- Wan2.1 14B, CogVideoX 1.5, HunYuan I2V (I2V generation)
- Qwen2-VL-2B (PQA model)
- ViewCrafter (dataset generation)

**Compute cực nặng:**
- ~50 NVIDIA H20 GPU hours chỉ cho PQA training
- Fine-tuning Wan2.1 14B: cần multi-GPU high-memory setup
- Flow-DPO RLHF: thêm training pass nữa

**Lý thuyết:** Flow-DPO loss (Rectified Flow + DPO) — phức tạp nhưng không phải bottleneck chính.

**Kết luận:** **Không thực tế để tự implement từ đầu.** Nếu cần, hướng khả thi duy nhất: dùng base models open-source trực tiếp (Wan2.1, CogVideoX) + chỉ reimplementing phần fine-tuning pipeline + PQA model.

---

## 3. Thứ tự ưu tiên nếu muốn reproduce

| Thứ tự | Paper | Mục tiêu | Lý do |
|--------|-------|---------|-------|
| 1 | **004** | Hiểu & baseline aesthetic scoring | Nhanh nhất, clean nhất, kiến thức nền |
| 2 | **003** | Viewpoint representation research | Lý thuyết sâu nhất; compute nhẹ |
| 3 | **008** | Hệ thống viewpoint suggestion thực tế | Build on DepthSplat; state-of-the-art nhất |
| 4 | **001** | Chỉ tham khảo kiến trúc, không reproduce | Quá nặng về compute |

---

## Thuật ngữ (Glossary)

| English | Tiếng Việt | Giải thích ngắn |
|---------|-----------|----------------|
| Reimplementation | Tái triển khai | Tự viết lại code của phương pháp từ paper |
| Feature distillation | Chưng cất đặc trưng | Chuyển knowledge từ teacher sang student qua matching features |
| Eigenvalue decomposition | Phân rã trị riêng | Phân tích ma trận thành eigenvalue + eigenvector |
| Modified Lloyd algorithm | Thuật toán Lloyd biến thể | k-means 1D có ràng buộc, dùng tìm ngưỡng ternary |
| S³ Voronoi pooling | Voronoi pooling trên 3-sphere | Gán điểm vào Voronoi cell gần nhất trên không gian quaternion |
| Hyper-spherical harmonics | Điều hòa cầu siêu | Hàm cơ sở trực giao trên S³ (3-sphere), tổng quát của spherical harmonics |
| Flow-DPO | Flow-DPO | DPO kết hợp Rectified Flow cho video diffusion |
| Gradient ascent | Đi lên theo gradient | Tối ưu hóa bằng cách cập nhật theo hướng tăng gradient |
| Feedforward Gaussian Splatting | 3DGS truyền xuôi | Dự đoán 3D Gaussians trong một forward pass, không cần per-scene optimization |
