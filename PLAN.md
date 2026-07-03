# 美诗儿 MES 操作指导书 — 项目计划

## 项目概述

为美诗儿（浙江）环境智能电器有限公司制作 MES 系统操作指导书 HTML 版，用于客户培训与日常查阅。将 Word 文档内容转为统一风格的交互式 HTML 页面。

## 技术架构

- **生成器**：Python 3（`generate.py`）—— 内容以结构化 dict 定义，脚本渲染为 HTML
- **前端**：纯静态 HTML + CSS + JS，无第三方依赖
- **样式**：自定义 CSS（`css/style.css`），固定侧边栏 + 全宽布局
- **交互**：原生 JS（`js/main.js`），ScrollSpy + Lightbox 图片放大

## 目录结构

```
操作手册/
├── index.html              ← 总目录页（所有模块入口）
├── generate.py             ← HTML 生成器脚本
├── PLAN.md                 ← 本文件（项目计划）
├── CHANGELOG.md            ← 变更日志
├── css/
│   └── style.css           ← 全局样式
├── js/
│   └── main.js             ← 交互脚本
├── images/
│   ├── production-injection/   ← 注塑车间截图
│   ├── production-assembly/    ← 组装车间截图
│   ├── equipment/              ← 设备维保截图
│   ├── mold/                   ← 模具维保截图
│   └── quality/                ← 质量检验截图
├── pages/
│   ├── injection.html      ← 注塑车间操作手册
│   ├── assembly.html       ← 组装车间操作手册
│   ├── equipment.html      ← 设备维保操作手册
│   ├── mold.html           ← 模具维保操作手册
│   ├── quality.html        ← 质量检验操作手册
│   ├── iiot.html           ← IIoT 设备看板操作手册
│   └── sysconfig.html      ← 系统基础配置操作手册
└── 各部门原始 Word 文档/
    ├── 生产部/             ← 注塑 + 组装原始文档
    ├── 设备部/             ← 设备维保原始文档
    ├── 模具部/             ← 模具维保原始文档
    └── 质量部/             ← 质量检验原始文档
```

## 内容管理

### 如何修改内容

所有页面内容在 `generate.py` 的 `CONTENT` 字典中定义。每个模块包含：

```python
"module_key": {
    "title": "模块标题",
    "dept": "所属部门",
    "icon": "图标 emoji",
    "img_dir": "images/目录名",
    "scenario": ["段落1", "段落2"],          # 场景说明
    "steps": [                                # 操作步骤
        {
            "title": "1. 主步骤标题",
            "sub_steps": [
                {
                    "id": "1.1",
                    "name": "子步骤名",
                    "desc": "作业说明",
                    "remark": "备注（可选）",
                    "images": [{"img": "fig-01.png", "desc": "图注"}]
                }
            ]
        }
    ],
    "notes": ["注意事项1", "注意事项2"]        # 注意事项
}
```

### 如何添加新模块

1. 在 `CONTENT` 中添加新条目
2. 在 `MODULE_ORDER` 列表中添加 key
3. 运行 `python3 generate.py` 重新生成

### 图片管理

- 图片放在 `images/{模块目录}/` 下，命名为 `fig-01.png`、`fig-02.png`...
- `generate.py` 中的 `fig-XX.png` 引用需与实际文件一致
- 替换图片只需替换文件，无需修改 HTML

### 如何从 Word 提取图片

使用 `olefile` 从 .doc 文件的 Data 流中提取 PNG：

```python
python3 -c "
import olefile, struct
ole = olefile.OleFileIO('path/to/doc')
data = ole.openstream('Data').read()
# 扫描 PNG 签名 → 解析 chunk 结构 → 提取完整 PNG
"
```

## 生成与部署

```bash
# 重新生成所有 HTML
python3 generate.py

# 本地预览
python3 -m http.server 8080
# 打开 http://localhost:8080/
```

## 模块一览

| Key | 模块名 | 部门 | Word 源文档 |
|-----|--------|------|------------|
| injection | 注塑车间操作手册 | 生产部 | 注塑车间操作手册.doc |
| assembly | 组装车间操作手册 | 生产部 | 组装车间操作手册.doc |
| equipment | 设备维保操作手册 | 设备部 | 设备维保操作手册.doc |
| mold | 模具维保操作手册 | 模具部 | 模具维保操作手册.doc |
| quality | 质量检验操作手册 | 质量部 | 质量检验操作手册.doc |
| iiot | IIoT 设备看板操作手册 | 生产部/设备部 | 无（独立编写） |
| sysconfig | 系统基础配置操作手册 | 信息部 | 无（独立编写） |
