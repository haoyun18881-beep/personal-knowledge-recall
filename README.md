# Personal Knowledge Recall

明确要查旧讨论、个人经验或历史资料时，让 Codex 从 Obsidian 里定向找。

适合查以前遇到过的故障、过去做过的决定、学习和创作记录，或者值得复用的过往经验。

## 它怎么找

召回顺序固定为：

`明确的召回问题 → Obsidian`

- 先从入口文件找到相关知识区，再只读最相关的少量笔记。
- 已经能回答就停止；没有找到时如实说明检查过的范围。

用户现在明确提供的信息和刚核实的事实优先。旧笔记和剪藏内容只作参考。

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

配置保存在本机的 `local-config.json`，脚本默认不会覆盖已有配置。

常用选项：

```powershell
python .\scripts\configure.py `
  --vault "$env:USERPROFILE\Documents\Obsidian Vault" `
  --entry "00-AI入口.md" `
  --entry "Home.md" `
  --restricted "个人档案"
```

完整示例见 [config.example.json](config.example.json)。

## 直接使用现有 Obsidian 目录

不需要重建知识库。`entry_files` 只指定优先入口，后续会按当前问题做小范围搜索。已有 vault 直接沿用；从零开始时，可以使用仓库里的空白 [Obsidian starter](assets/obsidian-starter/)。

## 隐私和安全边界

- v1 只读取 vault 里的笔记，不修改、整理或删除；安装时只会写入本机配置文件。
- 对 Obsidian 的读取只限于配置的 vault 根目录。
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

本项目采用 BUSL-1.1。个人学习和许可证所列范围内的使用免费，其他商业使用需要授权。详见 [LICENSE](LICENSE)。
