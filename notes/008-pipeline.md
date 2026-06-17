# Pipeline Trích Xuất — Bài 008

| Trường | Nội dung |
|--------|----------|
| **Paper ID** | 008 |
| **Tiêu đề** | Aesthetic Camera Viewpoint Suggestion with 3D Aesthetic Field |
| **Source file** | `008_Aesthetic_Camera_Viewpoint_Suggestion_with_3D_Aesthetic_Field.pdf` |
| **Worker** | `pipeline-extract` |
| **Ngày** | 2026-06-18 |

---

## 1. Tổng quan hệ thống

Bài báo đề xuất một khung làm việc (framework) hai giai đoạn:

1. **Học 3D Aesthetic Field** — chưng cất (distill) tri thức từ mô hình đánh giá thẩm mỹ 2D vào một mạng 3D Gaussian Splatting feedforward, tạo ra một trường thẩm mỹ liên tục trong không gian 3D.
2. **Tìm kiếm Viewpoint** — dùng pipeline tìm kiếm thô (coarse sampling) + tinh chỉnh bằng gradient ascent để tìm camera pose tối ưu theo điểm thẩm mỹ.

---

## 2. Input và Output tổng thể

| | Mô tả |
|---|---|
| **Input** | N ảnh chụp thưa (sparse scene captures) `{I^i ∈ ℝ^(H×W×3)}_{i=1}^N` + camera poses tương ứng `{P^i ∈ ℝ^(3×4)}_{i=1}^N`. Số views N từ 2 đến 6 trong thực nghiệm. |
| **Output** | Một tập camera pose được gợi ý `P*` có điểm thẩm mỹ (aesthetic score) cao nhất trong không gian view liên tục của cảnh. |

---

## 3. Các bước pipeline chính

### Giai đoạn I — Distillation: Học 3D Aesthetic Field

#### Bước 1: Trích xuất đặc trưng đa góc nhìn (Multi-view Feature Extraction)

| Mục | Nội dung |
|-----|---------|
| **Input** | N ảnh sparse `{I^i}` + N camera poses `{P^i}` |
| **Output** | Multi-view features `{F^i_mv}_{i=1}^N` |
| **Module** | Multi-view Transformer (backbone DepthSplat [34]) |
| **Ghi chú** | Các features từ N view được fuse qua plane-sweep aggregation [4, 33]; enriched với monocular depth cues |

#### Bước 2: Trích xuất đặc trưng thẩm mỹ (Aesthetic Feature Extraction)

| Mục | Nội dung |
|-----|---------|
| **Input** | N ảnh sparse `{I^i}` |
| **Output** | Multi-scale aesthetic features `{F^i_aes}_{i=1}^N` |
| **Module** | CNN Aesthetic Encoder — lấy từ lớp feature extraction của teacher model VEN [29] |
| **Ghi chú** | VEN (Visual Evaluation Network) là pretrained 2D aesthetic model; lấy từ lớp 23^rd (14×14×512) làm distillation target |

#### Bước 3: Dự đoán 3D Gaussians với Aesthetic Embedding

| Mục | Nội dung |
|-----|---------|
| **Input** | `{F^i_mv}` (multi-view features) + `{F^i_aes}` (aesthetic features) |
| **Output** | Tập 3D Gaussians với aesthetic embedding: `{μ, Σ, α, f_aes}` — gồm vị trí μ, covariance Σ, opacity α, và aesthetic embedding f_aes (32-dim) |
| **Module** | Gaussian Head (DPT head [19]) + Aesthetic Head |
| **Ghi chú** | DPT head regress per-pixel depth để xác định trung tâm μ của mỗi Gaussian; Aesthetic Head predict per-Gaussian aesthetic embedding f_aes (compact 32-dim thay vì 512-dim của teacher) |

#### Bước 4: Render Aesthetic Feature Maps tại Novel View

| Mục | Nội dung |
|-----|---------|
| **Input** | 3D Gaussians `{μ, Σ, α, f_aes}` + novel view poses |
| **Output** | Predicted aesthetic feature maps `F̂_pred` |
| **Module** | Gaussian Splatting rasterization pipeline (DepthSplat [34]) |
| **Ghi chú** | Cùng rasterization pipeline với RGB rendering; render ra feature map thay vì pixel màu |

#### Bước 5: Alignment qua Transformer Downsampler

| Mục | Nội dung |
|-----|---------|
| **Input** | `F̂_pred` (rendered features, nhỏ hơn và sâu hơn F_gt) |
| **Output** | `F_pred` — feature map đã align |
| **Module** | Lightweight Transformer Downsampler |
| **Ghi chú** | Cần thiết vì teacher feature maps F_gt có kích thước nhỏ hơn F̂_pred; downsampler align chúng để tính loss |

#### Bước 6: Ground-Truth từ Teacher Model

| Mục | Nội dung |
|-----|---------|
| **Input** | Ground-truth novel view images |
| **Output** | GT feature maps `F_gt` (14×14×512) |
| **Module** | Teacher model VEN [29], frozen — lớp 23^rd |

---

### Giai đoạn II — Inference: Viewpoint Search Pipeline

Sau khi 3D Aesthetic Field đã được học, tại inference dùng two-stage search:

#### Bước 7 (Stage 1): Coarse Sampling — Lấy mẫu viewpoint thô

| Mục | Nội dung |
|-----|---------|
| **Input** | N input camera poses (trajectory) |
| **Output** | Top-K candidate viewpoints `{P^k_cand}_{k=1}^K` (K=2 trong thực nghiệm) |
| **Kỹ thuật** | (a) Nối N poses thành continuous camera trajectory bằng nội suy vị trí + orientation. (b) Lấy mẫu đều 16 camera poses dọc trajectory. (c) Quanh mỗi pose, tạo 8 neighboring poses với in-plane shift và directional jitter nhỏ → tổng 16×8 = 128 candidate poses. (d) Render mỗi candidate qua aesthetic field → đánh giá bằng aesthetic decoder → lấy điểm. (e) Chọn top-K candidates; lọc near-identical candidates bằng distance-based duplication check. |

#### Bước 8 (Stage 2): Gradient-based Refinement — Tinh chỉnh bằng gradient

| Mục | Nội dung |
|-----|---------|
| **Input** | Top-K candidate poses `{P^k_cand}` từ Stage 1 |
| **Output** | K refined poses; giữ top-scoring → trả về là **aesthetic viewpoint suggestions** cuối cùng |
| **Kỹ thuật** | Gradient ascent trực tiếp trên aesthetic score: `P_{t+1} = P_t + η∇_P score(P_t)`. Tối ưu vector 5 chiều: 3D translation + 2 rotation (yaw, pitch; bỏ roll). Optimizer: Adam [10], step size η=0.01, 25 steps cố định. |

#### Bước 9: Aesthetic Scoring (dùng trong cả Stage 1 & 2)

| Mục | Nội dung |
|-----|---------|
| **Input** | Aesthetic feature map `F̂` tại một camera pose |
| **Output** | Scalar aesthetic score |
| **Module** | Aesthetic Decoder — các lớp còn lại của teacher VEN [29] sau lớp distillation target |

---

## 4. Diagram dạng text

### 4a. Training Pipeline (Distillation)

```
Sparse Input Images {I^i}  +  Camera Poses {P^i}
          │                          │
          ├──────────────────────────┤
          ▼                          ▼
  [Aesthetic Encoder]        [Multi-view Transformer]
  (CNN từ VEN, frozen)       (DepthSplat backbone)
          │                          │
  {F^i_aes}                  {F^i_mv}
          │                          │
          └──────────┬───────────────┘
                     ▼
         [Gaussian Head + Aesthetic Head]
         (DPT Head: predict μ, Σ, α, f_aes)
                     │
         3D Gaussians {μ, Σ, α, f_aes}
                     │
                     ▼  (Gaussian Splatting Render)
         Rendered Feature Maps F̂_pred
                     │
         [Transformer Downsampler]
                     │
                     ▼
                  F_pred
                     │
                     │  MSE Loss
                     ▼
    F_gt ◄──── Teacher VEN (frozen, lớp 23^rd)
              (fed novel view ground-truth images)
```

### 4b. Inference Pipeline (Viewpoint Search)

```
Sparse Input Views + Poses
          │
          ▼
  [Build 3D Aesthetic Field]
  (feedforward pass qua Gaussian network)
          │
     3D Gaussians w/ f_aes
          │
    ┌─────┴──────────────────────────────────────┐
    │          STAGE 1: Coarse Sampling           │
    │  Interpolate trajectory → sample 16 poses  │
    │  + 8 neighbors each → 128 candidates       │
    │  Render → Aesthetic Score each             │
    │  → Top-K=2 diverse candidates              │
    └─────────────────────┬──────────────────────┘
                          │
    ┌─────────────────────▼──────────────────────┐
    │       STAGE 2: Gradient Refinement          │
    │  Adam optimizer, η=0.01, 25 steps          │
    │  P_{t+1} = P_t + η∇_P score(P_t)          │
    │  Optimize 5-dim (3D trans + yaw + pitch)   │
    └─────────────────────┬──────────────────────┘
                          │
              Suggested Viewpoints P*
              (top-scoring refined poses)
```

---

## 5. Training Pipeline chi tiết

| Yếu tố | Nội dung |
|--------|---------|
| **Dữ liệu huấn luyện** | RealEstate10k (RE10k) [41] — chủ yếu indoor videos; DL3DV [13] — cảnh đa dạng. Cả hai có camera parameters mỗi frame. |
| **Teacher model** | VEN [29] (Visual Evaluation Network) — CNN, frozen trong suốt training. Lớp 23^rd (14×14×512) làm distillation target. |
| **Loss function** | MSE (mean-squared error) giữa F_pred và F_gt trên rendered feature maps tại novel views. |
| **Modules frozen** | Multi-view Transformer backbone, DPT head, Aesthetic Encoder — giữ frozen để bảo toàn geometry prediction và 2D aesthetic perception. |
| **Modules trained** | Aesthetic Head + Transformer Downsampler — trained end-to-end. |
| **Resolution** | 256×256 (RE10k), 256×448 (DL3DV) |
| **Input views khi train** | 2 views (RE10k), 2–6 views (DL3DV) — theo protocol của DepthSplat [34] |
| **Framework** | PyTorch [17], backbone DepthSplat [34] |

---

## 6. Inference Pipeline chi tiết

| Yếu tố | Nội dung |
|--------|---------|
| **Stage 1 — Coarse Sampling** | 16 poses dọc trajectory × 8 neighboring poses = 128 candidates tổng. |
| **Stage 1 — Selection** | Top-K=2 candidates sau distance-based diversity filter. |
| **Stage 2 — Optimizer** | Adam [10], step size 0.01, 25 steps. |
| **Stage 2 — Search space** | 5-dim: 3D translation (x, y, z) + yaw + pitch (roll bỏ qua). |
| **Output cuối** | Top-scoring refined poses → render thành viewpoint gợi ý. |

---

## 7. Checklist Reproducibility

| Mục | Tình trạng |
|-----|-----------|
| **Code công khai** | Bài báo không nêu (not stated in the paper) |
| **Dataset công khai** | Có — RE10k [41] và DL3DV [13] là public datasets |
| **Teacher model công khai** | VEN [29] — bài báo tham chiếu nhưng không xác nhận availability |
| **Backbone DepthSplat** | DepthSplat [34] là public (referenced as open-source) |
| **Implementation details** | Có trong Supplementary Material (không đọc được trong bản PDF này) |
| **Hyperparameters** | Được nêu rõ: K=2 candidates, 25 refinement steps, η=0.01, 16 coarse samples, 8 neighbors |

---

## 8. Điểm kỹ thuật nổi bật

- **Vì sao không dùng RGB scoring trực tiếp?** RGB scoring nhạy cảm với rendering artifacts tại novel views và dao động mạnh qua các views lân cận, vì training data của teacher thiếu annotations cho các variations 3D. Feature-level distillation khắc phục bằng cách học smooth score landscape trong không gian latent.
- **View-conditioning:** Model được điều kiện trên camera poses (cả input lẫn novel views) vì aesthetic representation vốn phụ thuộc viewpoint. Ablation (Tab. 4) xác nhận view-conditioning cải thiện đáng kể.
- **Gradient landscape:** Distilled field tạo ra smooth, well-behaved gradient landscape (Fig. 3a, Tab. 3) — ΔVen=0.46 vs Baseline=0.20 trên RE10k — cho phép gradient ascent hội tụ ổn định.

---

## Thuật ngữ (Glossary)

| English | Tiếng Việt | Giải thích ngắn |
|---------|-----------|----------------|
| 3D Aesthetic Field | Trường thẩm mỹ 3D | Ánh xạ liên tục từ camera pose → aesthetic score, được mã hóa trong 3D Gaussians |
| Aesthetic Viewpoint Suggestion | Gợi ý góc nhìn thẩm mỹ | Nhiệm vụ tìm camera pose có chất lượng thẩm mỹ cao nhất |
| Sparse captures | Ảnh chụp thưa | Số lượng ảnh input nhỏ (2–6), không cần dense reconstruction |
| 3D Gaussian Splatting (3DGS) | Kết xuất Gaussian 3D | Biểu diễn cảnh 3D bằng tập hợp Gaussians có vị trí, hình dạng, màu sắc |
| Feedforward Gaussian Splatting | 3DGS truyền xuôi | Dự đoán 3D Gaussians trong một lần forward pass, không cần optimization per-scene |
| Feature distillation | Chưng cất đặc trưng | Chuyển knowledge từ teacher model sang student qua matching intermediate features |
| Teacher model / VEN | Mô hình giáo viên | Pretrained 2D aesthetic model được dùng làm supervision signal |
| Coarse sampling | Lấy mẫu thô | Giai đoạn 1 của search: uniformly sample candidates dọc trajectory |
| Gradient ascent | Đi lên theo gradient | Tối ưu hóa pose bằng cách cập nhật theo chiều tăng của gradient score |
| Camera pose | Tư thế camera | Ma trận 3×4 biểu diễn vị trí + hướng của camera trong không gian 3D |
| Aesthetic embedding / f_aes | Nhúng thẩm mỹ | Vector 32-dim gắn với mỗi Gaussian, mã hóa thông tin thẩm mỹ cục bộ |
| Novel view | Góc nhìn mới | Camera pose không thuộc tập input views, được render từ 3D representation |
| PLCC | Pearson Linear Correlation Coefficient | Đo tương quan tuyến tính giữa predicted và GT aesthetic scores |
| SRCC | Spearman Rank-order Correlation Coefficient | Đo tương quan thứ hạng giữa predicted và GT scores |
| DPT head | Dense Prediction Transformer head | Module decode features thành per-pixel predictions (depth, aesthetics) |
| Plane-sweep aggregation | Tổng hợp quét mặt phẳng | Kỹ thuật fuse multi-view features qua nhiều depth planes |
| View-conditioning | Điều kiện hóa theo góc nhìn | Cơ chế cho phép model nhận biết camera pose khi dự đoán |
| MSE loss | Hàm mất mát MSE | Mean Squared Error — đo sai số bình phương trung bình giữa F_pred và F_gt |
| Adam optimizer | Bộ tối ưu Adam | Thuật toán gradient descent với adaptive learning rate |
