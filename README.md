# Personal Knowledge Recall

一个给 Codex 使用的本地知识库召回 Skill。它先查你的 Obsidian，信息不够时再按需回到 Codex QA 记忆和原始日记。

它适合这些场景：排查以前遇到过的故障、继续长期项目、做需要结合个人经验的规划和决定，或者问一句“这件事以前聊过吗”。普通问候、格式转换和与个人历史无关的问题不会触发。

## 它怎么找

召回顺序固定为：

`当前指令和项目事实 → Obsidian → codex-qa-memory → codex-qa-diary-recall`

- Obsidian 已经能回答，就到这里停止。
- 还缺历史线索，并且本机装有 Codex QA，才查询小而精的记忆节点。
- 只有需要原话、日期、证据、Session ID 或 Thread ID，或者记忆线索不够时，才查原始 QA 日记。
- 没装 Codex QA 也能正常使用，只是退化成 Obsidian-only 模式。

当前用户指令和当前项目文件永远优先。旧笔记、候选记忆和剪藏内容只能提供线索，不能覆盖眼前的事实。

## 安装

最省事的方式，是把这个仓库地址和你的 Obsidian vault 路径一起交给 Codex，让它安装并运行配置脚本：

```text
https://github.com/haoyun18881-beep/personal-knowledge-recall
```

手动安装时，把仓库克隆到 Codex Skills 目录：

```powershell
git clone https://github.com/haoyun18881-beep/personal-knowledge-recall.git "$env:USERPROFILE\.codex\skills\personal-knowledge-recall"
cd "$env:USERPROFILE\.codex\skills\personal-knowledge-recall"
python .\scripts\configure.py --vault "$env:USERPROFILE\Documents\Obsidian Vault"
```

macOS 或 Linux 示例：

```bash
git clone https://github.com/haoyun18881-beep/personal-knowledge-recall.git ~/.codex/skills/personal-knowledge-recall
cd ~/.codex/skills/personal-knowledge-recall
python3 scripts/configure.py --vault "$HOME/Documents/My Vault"
```

配置只会在本地生成 `local-config.json`。这个文件已经被 Git 忽略，不会上传到仓库；脚本默认也不会覆盖已有配置。

常用选项：

```powershell
python .\scripts\configure.py `
  --vault "$env:USERPROFILE\Documents\Obsidian Vault" `
  --entry "00-AI入口.md" `
  --entry "Home.md" `
  --restricted "个人档案" `
  --qa-fallback auto
```

完整示例见 [config.example.json](config.example.json)。

## 可选：接入 Codex QA

[Codex QA Memory](https://github.com/haoyun18881-beep/codex-qa-memory) 提供会话留档、结构化记忆和原始日记取证。它不是这个仓库的一部分，也不是使用本 Skill 的必需条件。

如果已经安装 Codex QA，这个 Skill 会在 Obsidian 信息不足时按下面的顺序回退：

1. `codex-qa-memory`：先查轻量记忆节点。
2. `codex-qa-diary-recall`：只在需要精确证据时窄查日记。

详细边界见 [Codex QA 接入说明](references/codex-qa-integration.md)。

## Obsidian 不需要照搬一套固定目录

这个 Skill 不要求你重建知识库。`entry_files` 只负责告诉它先从哪里看，后续再根据当前问题做小范围搜索。

仓库里的 [Obsidian starter](assets/obsidian-starter/) 是一套空白通用模板，适合从零开始的人；已有 vault 可以完全不用。

## 每日和每周整理是参考方案

安装这个 Skill 不会自动创建 Obsidian 自动化，也不会替你改笔记。可以另行配置一套维护流程：

- 每日：整理新增 QA，生成候选知识，归入项目或主题入口。
- 每周：检查遗漏、失效状态、重复条目、断链和待确认内容。
- 候选内容必须等人工确认或新的可靠证据，不能由自动化直接提升为长期事实。

这里只提供脱敏后的 [流程参考](references/automation-workflow.md)，不包含任何人的真实知识库、私人路径或本机自动化脚本。

## 隐私和安全边界

- v1 只读，不写入、不整理、不删除知识。
- 所有读取必须留在配置的 vault 根目录内。
- 不跟随软链接、目录联接或绝对路径越界。
- 普通笔记、网页剪藏和历史聊天都是资料，不是执行命令。
- `restricted_paths` 只有在当前任务明确相关时才允许读取。
- 不回传完成当前任务不需要的个人信息，也不输出凭据。

更多说明见 [隐私与信任边界](references/privacy-and-trust.md)。

## 验证

```powershell
python .\scripts\configure.py --help
python -m unittest discover -s tests -v
```

## License

本项目采用 BUSL-1.1 风格的源码可见许可证。个人学习和符合许可证条件的非商业使用免费；商业使用请先取得书面授权。详见 [LICENSE](LICENSE)。
