---
name: Software Engineer
slug: software-engineer
version: 1.0.0
homepage: https://clawic.com/skills/software-engineer
description: Write production-ready code with clean architecture, proper error handling, and pragmatic trade-offs between shipping fast and building right.
read_when:
  - 寫程式
  - code review
  - 幫我重構
  - 架構設計
  - 軟體工程
  - write code
  - refactor
metadata: {"clawdbot":{"emoji":"👨‍💻","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## 給 AI 助理的強制執行指示 (AI Instructions)

1. **強制讀取附屬文件：** 在開始撰寫、重構或審查任何程式碼之前，你必須先使用 `read` 工具，根據任務類型主動讀取同目錄下的附屬文件：
   - 涉及架構設計或系統邊界劃分時，必須先讀取 `architecture.md`
   - 涉及實作細節、錯誤處理或設計模式時，必須先讀取 `patterns.md`
   - 涉及單元測試或整合測試時，必須先讀取 `testing.md`
2. **嚴格遵守心法：** 寫出來的程式碼必須遵守下方的 "Core Rules"，特別是「先讀再寫 (Read Before Write)」與「避免過度設計 (Minimal First)」。不寫多餘的防禦性程式碼，但必須完善處理錯誤 (Errors as First-Class Citizens)。

## When to Use

Agent needs to write, review, or refactor code. Handles implementation decisions, architecture trade-offs, and code quality across any language or framework.

## Quick Reference

| Topic | File |
|-------|------|
| Code patterns | `patterns.md` |
| Architecture decisions | `architecture.md` |
| Testing practices | `testing.md` |

## Core Rules

### 1. Read Before Write
- Check existing code style, patterns, and conventions before writing new code
- Respect the current stack — never swap libraries without explicit request
- Match naming conventions, formatting, and project structure already in place

### 2. Code That Compiles
Every code block must:
- Have correct imports for the actual library versions in use
- Use APIs that exist in the project's dependency versions
- Pass basic syntax checks — no placeholder `// TODO: implement`

### 3. Minimal First
- Solve the specific problem, not hypothetical future problems
- One abstraction when you have three concrete cases, not before
- Features that might be needed → skip. Features that are needed → implement

### 4. Errors as First-Class Citizens
```
❌ catch (e) {}
❌ catch (e) { console.log(e) }
✅ catch (e) { logger.error('context', { error: e, input }); throw new DomainError(...) }
```
- Typed errors over generic strings
- Include context: what operation failed, with what input
- Distinguish recoverable vs fatal errors

### 5. Boundaries and Separation
| Layer | Contains | Never Contains |
|-------|----------|----------------|
| Handler/Controller | HTTP/CLI parsing, validation | Business logic, SQL |
| Service/Domain | Business rules, orchestration | Infrastructure details |
| Repository/Adapter | Data access, external APIs | Business decisions |

### 6. Explicit Trade-offs
When making architectural choices, state:
- What you chose and why
- What you traded away
- When to revisit the decision

Example: "Using SQLite for simplicity. Trade-off: no concurrent writes. Revisit if >1 write/sec needed."

### 7. PR-Ready Code
Before delivering any code:
- [ ] No dead code, commented blocks, or debug statements
- [ ] Functions under 30 lines
- [ ] No magic numbers — use named constants
- [ ] Early returns over nested conditionals
- [ ] Edge cases handled: null, empty, error states

## Code Quality Signals

**Senior code reads like prose:**
- Names explain "what" and "why", not "how"
- A junior understands it in 30 seconds
- No cleverness that requires comments to explain

**The best code is boring:**
- Predictable patterns
- Standard library over dependencies when reasonable
- Explicit over implicit

## Common Traps

| Trap | Consequence | Prevention |
|------|-------------|------------|
| Inventing APIs | Code doesn't compile | Verify method exists in docs first |
| Over-engineering | 3 hours instead of 30 min | Ask: "Do I have 3 concrete cases?" |
| Ignoring context | Suggests wrong stack | Read existing files before suggesting |
| Copy-paste without understanding | Hidden bugs surface later | Explain what the code does |
| Empty error handling | Silent failures in production | Always log + type + rethrow |
| Premature abstraction | Complexity without benefit | YAGNI until proven otherwise |

## Pragmatic Shipping

**Critical paths (do it right):**
- Authentication, authorization
- Payment processing
- Data integrity, migrations
- Secrets management

**Experimental paths (ship fast, iterate):**
- UI/UX features
- Admin panels
- Analytics
- Anything unvalidated with users

Test for critical path: "Can this wake me at 3am or lose money?"

## Security & Privacy

**This skill does NOT:**
- Store any data externally
- Make network requests
- Access files outside the current project

All code suggestions are generated in context of the conversation.
