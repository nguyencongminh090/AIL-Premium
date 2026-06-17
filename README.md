# AIL-Premium — Aesthetic Intelligence Lab (Premium Workspace)

> **Dự án nghiên cứu học thuật** về **thẩm mỹ nhiếp ảnh (photographic aesthetics)**, tập trung vào các bài toán *gợi ý góc nhìn (viewpoint suggestion)* và *bố cục ảnh tối ưu (composition recommendation)*. Workspace tích hợp bộ công cụ phân tích tài liệu chạy trên Claude Code, xuất kết quả bằng **tiếng Việt học thuật**.

---

## Mục lục

1. [Tổng quan dự án](#1-tổng-quan-dự-án)
2. [Cấu trúc thư mục](#2-cấu-trúc-thư-mục)
3. [Kho bài báo (Paper Corpus)](#3-kho-bài-báo-paper-corpus)
4. [Hệ thống Skills — Phân tích tài liệu](#4-hệ-thống-skills--phân-tích-tài-liệu)
5. [Quy trình làm việc](#5-quy-trình-làm-việc)
6. [Hệ thống Notes](#6-hệ-thống-notes)
7. [Quy ước Git](#7-quy-ước-git)

---

## 1. Tổng quan dự án

Dự án này là một **workspace nghiên cứu học thuật chuyên sâu** hỗ trợ người nghiên cứu phân tích, tổng hợp và hệ thống hóa kiến thức từ các bài báo khoa học trong lĩnh vực:

- **Aesthetic viewpoint suggestion** — gợi ý góc nhìn thẩm mỹ cho máy ảnh
- **Photography composition recommendation** — bố cục ảnh tự động / thông minh
- **Image aesthetic assessment** — đánh giá thẩm mỹ hình ảnh
- **3D scene understanding for photography** — hiểu cảnh 3D phục vụ nhiếp ảnh

Workspace tích hợp tập hợp các **Worker skills** chạy trực tiếp qua Claude Code CLI, cho phép phân tích bài báo, xây dựng mindmap, trích xuất pipeline, tìm research gap, và nhiều tác vụ khác — tất cả xuất bản bằng **tiếng Việt học thuật** với thuật ngữ tiếng Anh được bảo tồn đầy đủ.

---

## 2. Cấu trúc thư mục

```
AIL-Premium/
├── papers/                  # Bài báo nguồn (PDF), đặt tên theo chuẩn NNN_Title.pdf
├── notes/                   # Kết quả phân tích do Workers xuất ra (Markdown)
│   └── INDEX.md             # Chỉ mục tất cả artifacts trong notes/
├── .claude/
│   ├── rules/
│   │   └── research-conventions.md   # Quy ước bắt buộc cho mọi Worker
│   └── skills/              # Định nghĩa các Worker skills
│       ├── research-orchestrator/
│       ├── paper-summary/
│       ├── paper-overview/
│       ├── methodology-read/
│       ├── vi-translate/
│       ├── paper-mindmap/
│       ├── knowledge-graph/
│       ├── knowledge-systemize/
│       ├── pipeline-extract/
│       ├── problem-expand/
│       ├── reading-triage/
│       ├── research-gap/
│       └── intuition/
├── .agents/
│   ├── rules/
│   │   └── git-management.md         # Quy ước Git bắt buộc
│   └── skills/              # Skills quản lý Git (git-branch, git-commit, git-deploy)
├── .gitignore
└── README.md
```

---

## 3. Kho bài báo (Paper Corpus)

Bài báo được lưu trong `papers/`, đặt tên theo chuẩn `NNN_Title_With_Underscores.pdf`. Tiền tố 3 chữ số là **canonical id** của bài báo, dùng xuyên suốt trong tất cả artifacts.

| ID | Tên bài báo | Venue | Chủ đề |
|----|-------------|-------|--------|
| `001` | Photography Perspective Composition: Towards Aesthetic Perspective Recommendation | NeurIPS 2025 | PPC — bố cục 3D, I2V generation, RLHF, PQA model |
| `003` | Geometric Viewpoint Learning with Hyper-Rays and Harmonics Encoding | — | Viewpoint learning, 3D geometric encoding |
| `004` | Image Aesthetic Assessment Based on Pairwise Comparison | — | Aesthetic assessment, pairwise comparison |
| `008` | Aesthetic Camera Viewpoint Suggestion with 3D Aesthetic Field | — | 3D aesthetic field, camera viewpoint suggestion |

> **Ưu tiên đọc** (theo reading-triage): `008` > `003` > `001` > `004` (dựa trên relevance với bài toán viewpoint suggestion).

---

## 4. Hệ thống Skills — Phân tích tài liệu

Tất cả skills được gọi qua **Claude Code CLI** bằng cú pháp `/skill-name [arguments]`. Mỗi skill nhận `$ARGUMENTS` là một trong:

- **paper id**: `003`
- **tên file / partial title**: `pairwise`, `004_Image_Aesthetic`
- **đường dẫn**: `papers/003_Geometric_Viewpoint...pdf`
- **`all`**: xử lý toàn bộ bài báo trong `papers/`

### Bảng Worker Skills

| Skill | Lệnh gọi | Mục đích | Output |
|-------|----------|----------|--------|
| **research-orchestrator** | `/research-orchestrator [goal]` | Orchestrator tổng — nhận mục tiêu lớn, phân rã, điều phối Workers | Synthesis report |
| **paper-summary** | `/paper-summary [id]` | Tóm tắt chi tiết theo từng section | `notes/<id>-summary.md` |
| **paper-overview** | `/paper-overview [id]` | Tổng quan nhanh: bài toán, đóng góp, kết quả | `notes/<id>-overview.md` |
| **methodology-read** | `/methodology-read [id]` | Phân tích chuyên sâu phương pháp | `notes/<id>-methodology.md` |
| **vi-translate** | `/vi-translate [id]` | Dịch toàn văn sang tiếng Việt học thuật | `notes/<id>-vi.md` |
| **paper-mindmap** | `/paper-mindmap [id]` | Sơ đồ tư duy cấu trúc bài báo (Mermaid) | `notes/<id>-mindmap.md` |
| **knowledge-graph** | `/knowledge-graph [id]` | Đồ thị thực thể + quan hệ | `notes/<id>-kg.md` |
| **knowledge-systemize** | `/knowledge-systemize [ids]` | Taxonomy + so sánh nhiều bài báo | `notes/knowledge-systemize-<slug>.md` |
| **pipeline-extract** | `/pipeline-extract [id]` | Pipeline tái tạo được + diagram | `notes/<id>-pipeline.md` |
| **problem-expand** | `/problem-expand [id]` | Khái quát hóa bài toán, situate trong lĩnh vực | `notes/<id>-expand.md` |
| **research-gap** | `/research-gap [ids]` | Khoảng trống nghiên cứu + hướng tương lai | `notes/research-gap-<slug>.md` |
| **intuition** | `/intuition [id]` | Giải thích trực quan, dễ hiểu (ELI5) | `notes/<id>-intuition.md` |
| **reading-triage** | `/reading-triage [question]` | Xếp hạng bài báo theo độ liên quan | `notes/reading-triage-<slug>.md` |

### Điểm bắt đầu được khuyến nghị

Với mục tiêu lớn hoặc đa bước, dùng `research-orchestrator` — nó tự phân rã thành các Worker tasks, chạy song song khi độc lập, và tổng hợp kết quả cuối:

```
/research-orchestrator So sánh phương pháp của bài 003 và 008, tìm research gap
```

---

## 5. Quy trình làm việc

```
1. Đặt bài báo vào papers/NNN_Title.pdf
2. Chạy /reading-triage <câu hỏi nghiên cứu>   → xác định thứ tự đọc
3. Chạy /paper-overview <id>                    → nắm bắt tổng quan
4. Chạy /methodology-read <id>                  → hiểu sâu phương pháp
5. Chạy /research-gap all                       → tìm khoảng trống nghiên cứu
6. Xem notes/INDEX.md                           → tra cứu tất cả artifacts
```

Với tác vụ nghiên cứu phức tạp (tổng hợp văn献, peer review, viết bài báo), sử dụng **ARS plugin** (`/ars-full`, `/ars-reviewer`, `/ars-lit-review`) thay vì chuỗi Worker thủ công.

---

## 6. Hệ thống Notes

Tất cả kết quả phân tích được lưu trong `notes/` theo quy tắc đặt tên:

- **Single-paper**: `notes/<id>-<worker>.md` (e.g., `notes/003-summary.md`)
- **Cross-paper**: `notes/<worker>-<slug>.md` (e.g., `notes/research-gap-viewpoint.md`)

Mỗi file bắt đầu bằng header chuẩn (paper id, title, worker, date) và kết thúc bằng bảng **Thuật ngữ (Glossary)**.

`notes/INDEX.md` là chỉ mục tổng, tự động cập nhật bởi research-orchestrator sau mỗi lần chạy.

---

## 7. Quy ước Git

Xem chi tiết tại [.agents/rules/git-management.md](.agents/rules/git-management.md). Tóm tắt:

- **Branch**: `<type>/<short-slug>` — e.g., `feat/add-003-summary`, `docs/update-readme`
- **Commit**: [Conventional Commits v1.0.0](https://www.conventionalcommits.org/) — `feat(notes): add paper-overview for 003`
- **Merge**: squash-and-merge vào `main`; rebase khi sync feature branch
- **Release**: semantic versioning `vMAJOR.MINOR.PATCH`, chỉ tag trên `main`
- **Không bao giờ**: force-push lên shared branches; commit secrets/`.env`

---

## Thuật ngữ (Glossary)

| English | Tiếng Việt | Giải thích ngắn |
|---------|------------|-----------------|
| Aesthetic Viewpoint Suggestion | Gợi ý góc nhìn thẩm mỹ | Bài toán tự động đề xuất vị trí/góc máy ảnh đẹp hơn |
| Photography Composition | Bố cục ảnh | Cách sắp xếp các yếu tố trong khung hình |
| Worker Skill | Skill Worker | Công cụ phân tích chuyên biệt cho một tác vụ cụ thể |
| Orchestrator | Điều phối viên | Skill trung tâm, phân rã mục tiêu lớn và điều phối Workers |
| Canonical ID | ID chuẩn | Tiền tố 3 chữ số định danh bài báo trong toàn hệ thống |
| Research Gap | Khoảng trống nghiên cứu | Vấn đề chưa được giải quyết trong lĩnh vực |
| ARS Plugin | Plugin ARS | Bộ công cụ nặng cho tổng hợp văn献, peer review, viết bài |
