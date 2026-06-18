# INDEX — notes/

Thư mục này chứa toàn bộ artifacts phân tích cho 4 papers trong dự án.
Naming convention: `<id>-<worker>.md` cho per-paper · `analysis-<slug>.md` cho cross-paper.

---

## Per-paper artifacts

| Paper ID | Worker | Đường dẫn | Ghi chú |
|----------|--------|-----------|---------|
| 001 | paper-overview | [001-overview.md](001-overview.md) | Photography Perspective Composition (PPC) — paradigm mới vượt cropping 2D, đề xuất camera movement 3D |
| 001 | pipeline-extract | [001-pipeline.md](001-pipeline.md) | 3 pipeline: Dataset Generation, PPC Inference (I2V+RLHF), PQA Model (Qwen2-VL-2B) |
| 001 | vi-translate | [001-vi.md](001-vi.md) | Bản dịch tiếng Việt toàn văn — Abstract, Introduction, Related Work, Methodology §3.1–3.4, Experiments, Conclusion, Appendix A + Glossary |
| 003 | paper-overview | [003-overview.md](003-overview.md) | Geometric Viewpoint Learning — 6DoF hyper-ray + HRE, học phân phối viewpoint con người từ point cloud indoor |
| 003 | pipeline-extract | [003-pipeline.md](003-pipeline.md) | 2-stage hierarchical: Location Branch (S² optic-ray) → Viewpoint Branch (S³ hyper-ray + View Cropping) |
| 004 | paper-overview | [004-overview.md](004-overview.md) | Pairwise aesthetic comparator — unified approach: score regression + binary + personalized aesthetics |
| 004 | pipeline-extract | [004-pipeline.md](004-pipeline.md) | Siamese ResNet-50 → pairwise comparison matrix → eigenvalue decomposition → aesthetic score |
| 008 | paper-overview | [008-overview.md](008-overview.md) | 3D Aesthetic Field (Gaussian Splatting) gợi ý camera pose đẹp nhất từ sparse captures — SOTA Viewpoint Suggestion |
| 008 | pipeline-extract | [008-pipeline.md](008-pipeline.md) | 2-stage: Distillation (feedforward 3DGS + aesthetic head) → Two-stage Search (coarse + gradient ascent) |

---

## Cross-paper analysis

| Scope | Loại | Đường dẫn | Ghi chú |
|-------|------|-----------|---------|
| all (001, 003, 004, 008) | reading-triage | [reading-triage-viewpoint-suggestion.md](reading-triage-viewpoint-suggestion.md) | Triage 4 papers theo chủ đề Viewpoint Suggestion — 008 & 003 ưu tiên cao |
| all (001, 003, 004, 008) | analysis | [analysis-complexity-reproducibility.md](analysis-complexity-reproducibility.md) | Code availability + độ phức tạp lý thuyết/code + đánh giá khả năng tự reimplementation cho 4 papers |
