以下是与 Git 提交相关的常用命令行操作指南，以及推荐的提交规范要求：

---

### **常用 Git 提交命令行**

#### 1. **初始化仓库**
```bash
git init
```

#### 2. **添加文件到暂存区**
```bash
# 添加所有修改/新增文件
git add .

# 添加特定文件
git add path/to/file

# 添加所有修改（不包括新增文件）
git add -u
```

#### 3. **提交更改**
```bash
# 基础提交
git commit -m "提交描述"

# 添加所有修改并提交（跳过暂存区）
git commit -a -m "提交描述"

# 修改最近一次提交（未推送时）
git commit --amend
```

#### 4. **查看状态和历史**
```bash
# 查看当前状态
git status

# 查看提交历史
git log

# 简洁历史
git log --oneline --graph
```

#### 5. **分支操作**
```bash
# 创建新分支
git branch new-feature

# 切换分支
git checkout new-feature
# 或
git switch new-feature

# 创建并切换分支
git checkout -b hotfix
```

#### 6. **推送与拉取**
```bash
# 首次推送
git push -u origin main

# 后续推送
git push

# 拉取远程更新
git pull
```

#### 7. **撤销操作**
```bash
# 撤销工作区修改
git checkout -- file.txt

# 撤销暂存区文件
git reset HEAD file.txt

# 回退到指定提交
git reset --hard commit_id
```

---

### **Git 提交规范要求**

推荐使用 **Conventional Commits** 规范，格式如下：
```
<类型>[可选范围]: <描述>

[可选正文]

[可选脚注]
```

#### 1. **提交类型（必填）**
| 类型       | 说明                          | 示例                  |
|------------|-------------------------------|-----------------------|
| `feat`     | 新增功能                      | `feat: 添加登录功能`  |
| `fix`      | 修复 bug                      | `fix: 解决空指针异常` |
| `docs`     | 文档更新                      | `docs: 更新API文档`   |
| `style`    | 代码格式/样式调整             | `style: 格式化代码`   |
| `refactor` | 重构（非功能新增/修复）       | `refactor: 重构模块A` |
| `perf`     | 性能优化                      | `perf: 优化渲染速度`  |
| `test`     | 测试相关                      | `test: 添加单元测试`  |
| `chore`    | 构建/依赖更新                 | `chore: 更新依赖包`   |
| `ci`       | CI/CD 配置                    | `ci: 添加GitHub Actions` |
| `revert`   | 回退提交                      | `revert: 撤销某次提交` |

#### 2. **范围（可选）**
指定影响模块：
```bash
feat(auth): 添加OAuth支持
fix(api): 修复分页错误
```

#### 3. **描述（必填）**
- 使用祈使句（如"添加"而非"添加了"）
- 首字母小写，不加句号
- 简明扼要（50字符内）

#### 4. **正文（可选）**
详细说明修改原因和实现细节：
```
添加用户管理模块

- 实现用户增删改查接口
- 添加权限验证中间件
```

#### 5. **脚注（可选）**
关联 issue 或标记重大变更：
```
Closes #123
BREAKING CHANGE: 数据库结构变更
```

---

### **优秀提交示例**
```bash
feat(auth): 添加JWT认证支持

- 实现token生成/验证中间件
- 添加refresh token机制

Closes #45
```

```bash
fix(api): 修复分页偏移量计算错误

当pageSize=0时导致除零异常，现增加边界检查
```

```bash
chore: 更新Spring Boot至3.2.0

BREAKING CHANGE: 需要JDK17运行环境
```

---

### **团队协作建议**
1. **原子提交**：每个提交只解决一个问题
2. **频繁提交**：小步快跑，避免巨型提交
3. **先拉后推**：推送前先执行 `git pull --rebase`
4. **分支策略**：
   - `main`：稳定版本
   - `develop`：开发主干
   - `feature/xxx`：功能分支
5. **使用 `.gitignore`**：排除无关文件

通过遵循这些规范，可以提高代码可追溯性，简化版本管理，并自动生成更清晰的变更日志。