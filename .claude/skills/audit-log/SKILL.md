---
name: audit-log
description: Append-only AI decision audit log — records only decisions that would make the project fundamentally different if made otherwise (materiality filter). Three event types survive that test: scope-decision (what's in/out of the analysis and why), synthesis-framing (how cross-paper conclusions are organized), cross-paper-assumption (non-obvious connections assumed between papers). Everything else — dispatches, re-dispatches, plan steps, failures, formatting — is discarded as reconstructable from artifacts. Field set follows NIST SP 800-92, EU AI Act Art.12, IEEE 7001-2021. Triggered by research-orchestrator at key moments. Use directly to append an entry, view recent entries, or summarize. Takes a JSON event spec, "summary", or "clear" via $ARGUMENTS.
argument-hint: <JSON event spec | summary | clear | (empty = last 10 entries)>
---

# Audit Log Worker

Records only decisions that pass the **materiality filter**:

> **"Nếu không có quyết định này → Project vẫn giống 90% → LOẠI.**
> **Nếu không có quyết định này → Project khác về bản chất → GHI."**

Applied to all candidate events, exactly three `event_type` values survive:

| `event_type` | Tại sao vượt ngưỡng | Không ghi → hậu quả |
|---|---|---|
| `scope-decision` | Quyết định paper / topic / khía cạnh nào thuộc / không thuộc phạm vi phân tích | Reader không hiểu tại sao paper X vắng mặt trong synthesis — coverage bị méo |
| `synthesis-framing` | Lens tổ chức cross-paper synthesis quyết định toàn bộ kết luận | Lens vô hình trong artifact; revision sau có thể vô tình đảo ngược |
| `cross-paper-assumption` | Kết nối ngầm giữa các bài báo (dataset dùng chung, thuật ngữ tương đương, kết luận kế thừa) | Assumption sai → nhiều notes hỏng mà không có trace để tìm nguồn |

**Bị loại (reconstructable from artifacts):** `dispatch`, `re-dispatch`, `plan-confirmed`,
`failure`, `escalation` — removing their log entry leaves the project identical.

## Standards basis (field set)

| Field | Standard mandate |
|-------|-----------------|
| `timestamp` | NIST SP 800-92 — mandatory for all log events |
| `session` | NIST 800-92 — correlate events within a working session |
| `actor` | NIST 800-92 · OCSF `subject` |
| `event_type` | NIST 800-92 `command` · OCSF `activity_id` |
| `target` | OCSF `object` · EU AI Act Art.12 |
| `decision` | EU AI Act Art.12 — output of the automated decision |
| `rationale` | EU AI Act Art.12 · IEEE 7001-2021 — decision logic, **mandatory** |
| `alternatives_considered` | IEEE 7001-2021 — rejected alternatives, transparency |
| `artifacts` | Project convention — paths written as a result |

## Input modes (`$ARGUMENTS`)

| Input | Behaviour |
|-------|-----------|
| JSON object string | Append one entry (schema below). |
| Path to a JSON file | Load spec from file, then append. |
| `summary` | Print digest: entry counts by type + last 10 decisions. Chat only. |
| `clear` | Archive log → `notes/audit-log-archive-<date>.md`, start fresh. |
| *(empty)* | Print the last 10 entry blocks in chat. |

## JSON event spec

```json
{
  "actor":                  "research-orchestrator",
  "event_type":             "scope-decision",
  "target":                 "paper 001",
  "decision":               "Loại paper 001 khỏi cross-paper viewpoint comparison",
  "rationale":              "Paper 001 dùng phương pháp 2D perspective; ba bài còn lại đều dùng 3D field — so sánh sẽ misleading",
  "alternatives_considered": ["giữ 001 với ghi chú hạn chế", "tạo nhóm riêng cho 2D"],
  "artifacts":              ["notes/research-gap-viewpoint.md"]
}
```

`actor` thường là `"research-orchestrator"` hoặc tên Worker phát hiện assumption.
`artifacts`: các file bị ảnh hưởng bởi quyết định này (không nhất thiết là file mới tạo).

## Procedure

1. **Resolve mode** từ `$ARGUMENTS`.

2. **Append mode (JSON spec):**
   a. Parse spec từ argument string hoặc file path.
   b. **Materiality check:** xác nhận `event_type` là một trong ba loại được phép. Nếu
      không → từ chối, giải thích bằng một câu tiếng Việt tại sao không đạt ngưỡng.
   c. Auto-fill `timestamp` (ISO 8601) và `entry_id` (đếm `####` headers hiện có + 1).
   d. Auto-fill `session` = ngày hôm nay (`YYYY-MM-DD`).
   e. Nếu `notes/audit-log.md` chưa tồn tại → tạo với header block trước.
   f. Append entry block (template dưới) vào cuối file.
   g. Xác nhận trong chat: một dòng tiếng Việt — ví dụ:
      *"Đã ghi [3] scope-decision · loại paper 001 khỏi viewpoint comparison."*

3. **Summary mode:**
   a. Đọc `notes/audit-log.md`.
   b. Đếm tổng entries, chia theo `event_type`.
   c. Liệt kê 10 entries gần nhất (id · type · target · decision) dạng bảng Markdown.
   d. **Không** ghi file mới — summary chỉ hiện trong chat.

4. **Clear mode:**
   a. Xác nhận với user (một câu tiếng Việt).
   b. Copy log hiện tại → `notes/audit-log-archive-<YYYY-MM-DD>.md`.
   c. Ghi đè `notes/audit-log.md` chỉ với header block.
   d. Báo cáo path archive và số entries đã lưu trữ.

5. **Empty arguments:** In 10 entry blocks gần nhất ra chat.

## Log file format

### Header (tạo một lần duy nhất)

```markdown
# Nhật ký Quyết định AI (AI Decision Audit Log)
> Bộ lọc: chỉ ghi quyết định làm project khác về bản chất nếu thiếu
> Chuẩn: NIST SP 800-92 · EU AI Act Art.12 · IEEE 7001-2021 · OCSF
> Dự án: Photographic Aesthetics — Aesthetic Viewpoint & Composition Recommendation

<!-- entries appended below — do not edit manually -->
```

### Entry block

```markdown
---
#### [<entry_id>] `<event_type>` · <timestamp>
| Trường | Giá trị |
|--------|---------|
| **Actor** | `<actor>` |
| **Session** | <session> |
| **Target** | <target> |
| **Decision** | <decision> |
| **Rationale** | <rationale> |
| **Alternatives considered** | <list, or "none recorded"> |
| **Artifacts affected** | <paths, or "none"> |
```

## Boundaries

- Chỉ append vào `notes/audit-log.md` — không sửa file nào khác.
- Từ chối mọi `event_type` không thuộc ba loại được phép; giải thích lý do từ chối.
- Không tự log các hành động của chính mình (no recursive self-logging).
- Nếu spec thiếu field bắt buộc (`actor`, `event_type`, `target`, `decision`, `rationale`)
  → báo lỗi validation bằng tiếng Việt, không append.
- Label cột dùng tiếng Việt; giá trị giữ tiếng Anh / tiếng Việt tùy actor —
  để file đọc được bởi collaborator không biết tiếng Việt.
