# Obsidian CLI: Command Reference

Obsidian 공식 CLI(v1.12.x+)를 사용하여 볼트를 제어하기 위한 명령어 모음입니다.

## 🔧 Basic Syntax
```bash
obsidian <command> [parameters] vault="MS_Brain.nosync" 2>/dev/null
```

## 📂 Command Groups
### 1. File CRUD
- **Create**: `obsidian create path="010 Inbox/note.md" content="내용"`
- **Read**: `obsidian read path="folder/note.md"`
- **Append/Prepend**: `obsidian append path="note.md" content="추가"`
- **Move/Rename**: `obsidian move path="A.md" to="B.md"` (링크 자동 업데이트)
- **Delete**: `obsidian delete path="temp.md"`

### 2. Search & Analysis
- **Search**: `obsidian search query="키워드" format=json`
- **Backlinks**: `obsidian backlinks file="NoteName" format=json`
- **Links**: `obsidian links file="NoteName" format=json`
- **Orphans/Deadends**: `obsidian orphans` / `obsidian deadends`

### 3. Properties & Tags
- **Properties**: `obsidian property:set file="Note" name="key" value="val"`
- **Tags**: `obsidian tags counts` / `obsidian tag name="TargetTag" verbose`

### 4. Daily Notes
- **Daily Read/Append**: `obsidian daily:read` / `obsidian daily:append content="..."`

## ⚙️ Advanced
- **JavaScript Eval**: `obsidian eval code="app.vault.getFiles().length"`
- **Plugins**: `obsidian plugins:enabled` / `obsidian plugin:reload id="..."`
