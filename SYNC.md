# 编辑与同步

只编辑 `interview/` 下六个编号模块中的中文笔记。这里和 Obsidian 里的 `interview/` 是同一份文件。

## 两层更新

1. 本机保存后，后台任务每分钟检查一次；连续两次检查内容稳定才发布，通常约 1–3 分钟。重新生成模块目录、SVG、离线 HTML、下载 ZIP，并推送笔记与个人网站的对应文件。网站沿用现有 GitHub 部署流程。
2. Codex 本聊天的维护任务每小时检查一次变动，审阅英文镜像、相关模块引用和图示，验证后推送。尚未审阅的英文版本显示“翻译更新待完成”。只有文件变化时才需要内容维护；处理耗时受任务排队影响。

电脑需开机、联网并已登录 GitHub；Codex 维护还需要桌面应用运行和账号可用。睡眠或离线期间不会实时更新，恢复后继续处理。未变化时不发重复通知；失败或需要处理时通知。

## 手动操作

```sh
npm ci
npm run check
python3 scripts/sync.py --push
```

中文已更新但英文尚未审阅时，可用 `python3 scripts/sync.py --push --allow-stale`，英文页面会显示待更新提示。

后台状态：`.local/watch-state.json`。运行日志在 `~/Library/Logs/interview-atlas-sync.log`；错误日志在同目录的 `interview-atlas-sync-error.log`。后台同步失败会保留未同步状态，至少间隔 5 分钟再试。

停用文件监控：`launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/fun.yikun.interview-atlas-sync.plist`。Codex 的内容维护可在本聊天对应的自动化中暂停。

## 公开范围与文件所有权

六个编号模块、图示和英文镜像均属于公开仓库。个人草稿放 `_private/`。`.obsidian/`、`.local/`、依赖和日志不进入 Git。网站只有 Interview 组件、路由、目录数据、专用静态资源、导航与下载响应头属于这次同步；其他工作保持原样。

编程练习可以保留在模块文件夹中；从笔记链接到的源码会进入网站附件和离线 ZIP。`.env`、`.env.*`、`.venv/`、`venv/`、Python 缓存和依赖目录不参与笔记发现、文件监控或公开提交。真实密钥只留在本地环境配置中，不能写进笔记或源码。

删除或移动笔记时，一并修复引用和英文镜像。构建检查会提示断链和缺失译文。`public: false` 仅影响阅读页面，不会把已公开的 Git 文件变成私人文件。

## GitHub 下载

Release 的 `interview-atlas.zip` 包含可打开的 Obsidian 文件夹、SVG 和中英文离线 HTML。单文件 HTML 已内嵌各章图示，断网可读；交互总览另附独立 HTML。源码也可通过 GitHub 的 Code → Download ZIP 获取。每次成功推送后，GitHub Actions 更新下载 Release。

网站和离线 HTML 的代码块在构建时生成彩色语法高亮，无需联网加载脚本。代码围栏应注明语言，如 `python`、`sql`、`json`；流程图或纯文本使用 `text`，保留原有缩进。
