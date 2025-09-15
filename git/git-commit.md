# Git 撤销 Commit 操作笔记

## 📝 核心概念

### 工作区 → 暂存区 → 本地仓库 → 远程仓库
```
工作区 (修改文件) → git add → 暂存区 → git commit → 本地仓库 → git push → 远程仓库
```

## 🔄 撤销不同类型的修改

### 1. 撤销工作区的修改（未 `git add`）
```bash
# 撤销单个文件的修改
git checkout -- filename

# 撤销所有修改（谨慎使用！）
git checkout -- .
```

### 2. 撤销暂存区的修改（已 `git add`，未 `git commit`）
```bash
# 将文件从暂存区撤回工作区（保留修改）
git reset HEAD filename

# 将所有文件从暂存区撤回
git reset HEAD .
```

### 3. 撤销本地提交（已 `git commit`，未 `git push`）

#### 方法一：`git reset`（修改历史，谨慎使用）
```bash
# 软重置：撤销commit但保留修改内容在暂存区
git reset --soft HEAD~1

# 混合重置（默认）：撤销commit，修改内容保留在工作区
git reset --mixed HEAD~1

# 硬重置：彻底删除commit和所有修改（谨慎！）
git reset --hard HEAD~1

# 重置到特定commit
git reset --hard commit_id
```

#### 方法二：`git revert`（创建新提交来撤销更改）
```bash
# 撤销最近一次提交
git revert HEAD

# 撤销特定提交
git revert commit_id

# 撤销多个连续提交
git revert older_commit_id^..newer_commit_id
```

## 📊 Reset 三种模式的对比

| 模式 | 命令 | 影响提交历史 | 影响暂存区 | 影响工作区 |
|------|------|-------------|-----------|-----------|
| --soft | `git reset --soft HEAD~1` | ✅ 撤销 | ❌ 保留 | ❌ 保留 |
| --mixed | `git reset --mixed HEAD~1` | ✅ 撤销 | ✅ 撤销 | ❌ 保留 |
| --hard | `git reset --hard HEAD~1` | ✅ 撤销 | ✅ 撤销 | ✅ 撤销 |

## 🚨 重要注意事项

### 1. 已推送到远程仓库的撤销
```bash
# 如果已经push，需要强制推送（谨慎！会覆盖远程历史）
git push --force

# 更安全的强制推送（适用于团队协作）
git push --force-with-lease
```

### 2. 找回误删的提交
```bash
# 查看所有操作记录（包括已删除的commit）
git reflog

# 从reflog中找到commit hash，然后重置回去
git reset --hard commit_hash_from_reflog
```

### 3. 修改最后一次提交的信息
```bash
# 只修改提交信息
git commit --amend

# 修改提交信息和内容
git add .  # 添加新修改
git commit --amend
```

## 🎯 实用场景示例

### 场景1：撤销最近一次提交但保留修改
```bash
git reset --soft HEAD~1
```

### 场景2：完全撤销最近一次提交和所有修改
```bash
git reset --hard HEAD~1
```

### 场景3：撤销特定文件的上次提交
```bash
git checkout HEAD~1 -- path/to/file
```

### 场景4：安全地撤销已推送的提交（团队协作）
```bash
git revert commit_id
git push  # 不需要force
```

### 场景5：修改上次提交的消息
```bash
git commit --amend
# 编辑提交消息后保存
git push --force-with-lease  # 如果已推送
```

## ⚠️ 安全警告

1. **不要对已共享的提交使用 `git reset --hard`**（会破坏团队协作）
2. **使用 `--force-with-lease` 而不是 `--force`**（更安全）
3. **重要修改前先备份分支**：
   ```bash
   git branch backup-branch-name
   ```
4. **使用 `git reflog` 是最后的救命稻草**

## 🔍 查看历史记录

```bash
# 查看简洁提交历史
git log --oneline -10

# 查看所有操作记录（包括reset等）
git reflog -10

# 查看某个文件的修改历史
git log -p filename
```

## 💡 最佳实践

1. **小步提交**：频繁提交小修改，减少需要撤销的范围
2. **先 revert 后 reset**：对已推送的提交优先使用 revert
3. **备份重要分支**：在进行重大操作前创建备份分支
4. **团队沟通**：强制推送前通知团队成员

记住：**`revert` 是安全的，`reset` 是危险的**（特别是已推送的提交）！