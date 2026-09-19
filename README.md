# mayshel-esop

MES 操作指导书 - 美诗儿(浙江)环境智能电器有限公司

**部署：** Cloudflare Pages
**仓库：** `git@github.com:wanghongyec-beep/mayshel-esop.git`

> ⚠️ 这是 **操作手册 + SOP**，不是设备看板。

---

## 内容构成

| 分组 | 内容 | 生成方式 |
|------|------|---------|
| **MES** | 注塑 / 组装 / 设备维保 / 模具维保 / 质量检验 — 5 个操作手册 | `generate.py` |
| **APS** | 月度产能规划 + 车间排产规划 — 2 个操作手册 | `generate.py` |
| **SOP** | MSE001–MSE026 — 26 份标准作业流程 | `gen_sop.py` |
| **培训** | ESOP 从0到1制作流程 / ESOP制作流程指南 / 制作流程说明 | 独立 HTML |

**操作手册 vs SOP 的区别：**

- **操作手册**——面向岗位人员的「怎么点」：场景说明 → 流程图 → 操作步骤（含界面截图）。
- **SOP**——面向流程评审的「谁在什么时候做什么、跨哪些系统」：流程定义 + 泳道流程图（按系统分栏）+ 关键作业说明。

---

## 目录结构

```
mayshel-esop/
├── index.html              # 首页（MES + APS + SOP 入口，手工维护）
├── css/style.css           # 全局样式
├── js/main.js              # 交互脚本（ScrollSpy + Lightbox + toggleNav）
├── generate.py             # 操作手册生成器（内容内置在 CONTENT 字典）
├── gen_sop.py              # SOP 页面生成器（读 sop_data.json）
├── sop_data.json           # SOP 清单（26 条的编号/名称/部门/流程定义/图文件名）
├── server.py               # 本地测试 HTTP 服务器
├── PLAN.md / CHANGELOG.md  # 项目计划 / 变更日志
├── pages/
│   ├── injection.html      # MES - 注塑车间操作手册
│   ├── assembly.html       # MES - 组装车间操作手册
│   ├── equipment.html      # MES - 设备维保操作手册
│   ├── mold.html           # MES - 模具维保操作手册
│   ├── quality.html        # MES - 质量检验操作手册
│   ├── aps-monthly.html    # APS - 月度产能规划版本
│   ├── aps-workshop.html   # APS - 车间排产规划版本
│   └── MSE001.html … MSE026.html   # SOP - 26 份标准作业流程
├── images/
│   ├── production-injection/   # 注塑车间截图
│   ├── production-assembly/    # 组装车间截图
│   ├── equipment/              # 设备维保截图
│   ├── mold/                   # 模具维保截图
│   ├── quality/                # 质量检验截图
│   ├── aps/                    # APS 截图
│   └── sop/                    # SOP 流程图（26 张，1500px 宽）
└── assets/
    └── 美诗儿MES-SOP(26份)_纵向A3.pdf   # SOP 合订本（A3 横向，26 页）
```

---

## 操作手册的维护（MES / APS）

内容硬编码在 `generate.py` 的 `CONTENT` 字典里（不再从 Word 动态解析）。改文案直接改字典：

```bash
python generate.py
```

> ⚠️ `generate.py` 的 `generate_index()` 会整套重写 `index.html`，而 `index.html` 目前是**手工维护**的
> （含 MES / APS / SOP 三个分组，以及 SOP 的 26 张卡片）。改完若发现首页分组或卡片丢了，
> 用 `git checkout index.html` 恢复再手工补。

---

## SOP 的维护（MSE001–MSE026）

**不要手改 `pages/MSE*.html`** —— 它们是生成物，要改源头。

流程图在**独立目录**生成：

```
D:\Code\_sop_work\          ← SOP 生成器（不在本仓库）
├── flows_all.py / flows_rest.py   # 26 条流程的内容定义
├── align_rows.py                  # 跨泳道连线自动对齐
├── gen.py                         # .drawio 生成器
├── check.py / check_lane.py       # 校验器（改完必跑）
├── make_web.py                    # 生成网页用图 + PDF → web/
└── export_for_repo.py             # 导出 sop_data.json
```

完整重建步骤：

```bash
# 1) 生成 drawio 并校验
cd D:\Code\_sop_work
python flows_rest.py                 # → flows.json
python gen.py flows.json out         # → out/*.drawio
python check.py out                  # 应为 0 问题
python check_lane.py out             # 应为 0 问题

# 2) 渲染 PNG（需要 draw.io 桌面版）
for f in out/*.drawio; do
  "D:/drawio/draw.io/draw.io.exe" --export --format png --scale 2 --border 10 \
    --output "png/$(basename "$f" .drawio).png" "$(pwd)/$f"
done

# 3) 生成网页用图 + PDF，并导出清单
python make_web.py                   # → web/images/*.png + web/*.pdf
python export_for_repo.py ../mayshel-esop/sop_data.json

# 4) 拷进本仓库并生成页面
cp -r web/images/*  ../mayshel-esop/images/sop/
cp web/*.pdf        ../mayshel-esop/assets/
cd ../mayshel-esop
python gen_sop.py sop_data.json      # → pages/MSE001.html … MSE026.html

# 5) 更新首页 index.html（手工：SOP 分组与卡片）
```

改**单条** SOP 时，只要动 `flows_all.py` / `flows_rest.py` 里对应那段，再跑 1)–5)。

### 校验器

改完生成器必跑，两个都应为 **0 问题**：

| 校验器 | 检查内容 |
|---|---|
| `check.py` | mxCell id 唯一 / 连线两端存在 / 逐段无斜线 / 箭头不压节点 |
| `check_lane.py` | 节点是否画在本系统的泳道里 |

另有 `check_rowalign.py`（信息性）统计还有多少跨泳道连线两端不同行。

---

## SOP 排版约定（改生成器前必读）

- **版式**复用《美诗儿SOP模板1.drawio》：表头信息栏 / 流程定义条 / 阶段轴 / 系统泳道 / 关键作业说明列 / 标准图例。
- **字号**：公司名 33.87 / 表头·流程定义·说明 15.4 / 图形文字 11.29 / 色带 10.5 / 图例标题 14.0 / 阶段 12.5 / Y-N 11.29。
- **跨泳道箭头（箭头不能叠在一起）**：
  - 跨泳道且同一行 → 一笔**水平**直连
  - 跨泳道且目标在下方 → 源方块**下边**引出 → 横向 → 目标方块**上边**进入
  - 跨泳道且目标在上方 → 源方块**上边**引出 → 横向 → 目标方块**下边**进入
- **连线必须** `edgeStyle=none` + 显式拐点；用 `orthogonalEdgeStyle` 会整条不渲染。
- **mxCell id 必须唯一**，撞号会让 draw.io 静默丢单元格并连带断线。
- **标准图例列全部系统**（E10/MES/WMS/QMS/PLM/APS/钉钉/AGV/线下），不是只列本流程用到的。
- 责任部门 / 流程定义 **以《【美诗儿】流程清单_260401.xlsx》为准**；操作细节参考本仓库的操作手册，冲突时以 Excel 为准。

### 返工 / 报废流程的特殊约定

**ERP 下工单之后都需要 APS 排产**。MSE007 / MSE008 / MSE017 / MSE018 / MSE025 / MSE026 六条已统一为：

```
QMS 判定 → WMS 移库 → ERP 下工单 → APS 排产并补发生产批 → MES 执行
```

新增此类流程时记得带上 APS 泳道与节点。

---

## 开发

```bash
# 本地预览
python server.py
# 或直接双击 index.html（无后端依赖，纯静态）

# 提交部署
git add -A
git commit -m "update: ..."
git push origin main
# Cloudflare Pages 自动部署
```

## 体积注意

SOP 图已按 1500px 宽 + 128 色 PNG 压缩（`images/sop` 约 5.8M），
PDF 按 A3 横向 120dpi 生成（约 6.4M）。**再加大图前先确认是否必要**，仓库不是图床。
