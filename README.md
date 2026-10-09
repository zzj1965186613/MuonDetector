# 🌌 MuonDetector — 宇宙线缪子物理实验与数据监测平台

> 基于 Streamlit 的缪子探测器数据分析工具，支持实验数据上传、交互式参数调节、泊松统计拟合与能谱可视化，并已封装为 Windows 独立可执行文件，双击即用。

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ 功能特性

- **数据导入**：支持上传 `.TXT` 格式的探测器原始数据，自动跳过参数头并清洗异常值
- **交互式参数**：侧边栏提供 ADC 噪声阈值滑块、时间积分窗口选择，实时联动所有图表
- **三大物理图表**：
  - 📈 缪子通量随时间的演化折线图
  - 📊 泊松分布拟合（自动提取 λ 参数）
  - ⚡ 沉积能谱分布（朗道样长尾特征）
- **演示模式**：未上传文件时自动生成符合物理特征的模拟数据，方便教学演示
- **零部署体验**：已封装为 Windows `.exe`，无需安装 Python 或配置环境

---

## 🚀 快速开始

### 方式一：直接运行 .exe（推荐）

前往 [Releases](https://github.com/zzj1965186613/MuonDetector/releases) 页面下载最新版本，解压后双击 `MuonDetector.exe` 即可。

> ⚠️ 首次启动需 15-30 秒解压依赖，请耐心等待终端出现 `You can now view your Streamlit app` 后，浏览器访问 http://localhost:8501

### 方式二：从源码运行

```bash
# 克隆仓库
git clone https://github.com/zzj1965186613/MuonDetector.git
cd MuonDetector

# 创建虚拟环境并安装依赖
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install streamlit pandas numpy matplotlib scipy

# 启动应用
streamlit run MuonDetector.py
```

### 方式三：自行打包为 .exe

```bash
pip install pyinstaller
pyinstaller run_main.spec --clean --noconfirm
```

构建产物位于 `dist/MuonDetector/` 目录。

---

## 📂 项目结构

```
MuonDetector/
├── MuonDetector.py      # Streamlit 主应用（数据处理 + 可视化）
├── run_main.py          # PyInstaller 打包入口 wrapper
├── run_main.spec        # PyInstaller 构建配置
├── .gitignore
└── README.md
```

---

## 🔧 技术路线

| 层级 | 技术选型 | 说明 |
|------|---------|------|
| 数据层 | Pandas | 解析 TXT 数据、清洗 INF、时间窗口聚合 |
| 分析层 | NumPy + SciPy | 统计计算 + 泊松分布 curve_fit 拟合 |
| 展示层 | Streamlit + Matplotlib | Web 交互界面 + 三大物理图表渲染 |
| 交付层 | PyInstaller → .exe | 解决 devMode 冲突，实现双击即用 |

---

## 🐛 已解决的打包问题

Streamlit 应用打包为 `.exe` 后常见崩溃，本项目已根治以下关键问题：

| 问题 | 根因 | 解决方案 |
|------|------|---------|
| `server.port` RuntimeError | Streamlit 检测到路径中无 `site-packages`，自动启用 `developmentMode` | 运行时 monkey-patch `config._global_development_mode` |
| `experimental_memo` AttributeError | Streamlit 1.58 移除了该 API | 替换为 `@st.cache_data` |
| `SyntaxWarning: invalid escape sequence` | Python 3.12 对 `\s` `\l` 等非法转义发出警告 | 改用原始字符串 `r'\s+'` 和 `r"""..."""` |

---

## 📄 License

MIT License

---

## 📧 联系

如有问题或建议，欢迎提交 [Issue](https://github.com/zzj1965186613/MuonDetector/issues)
