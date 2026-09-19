#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 SOP（标准作业流程）页面。

与 generate.py 的分工：
  · generate.py —— 从 Word 整理好的「操作手册」（场景说明 / 流程图 / 操作步骤）
  · 本脚本     —— 由 D:\\Code\\_sop_work 生成的 26 份 SOP 图（MSE001–MSE026）

用法:
    python gen_sop.py <sop_data.json>
其中 sop_data.json 由 `_sop_work/export_for_repo.py` 产出，
包含每份 SOP 的编号、名称、责任部门、流程定义、图文件名。

图片放在 images/sop/，PDF 合订本放在 assets/。
"""
import io
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(BASE_DIR, "pages")
IMG_DIR = "images/sop"
PDF_NAME = "美诗儿MES-SOP(26份)_纵向A3.pdf"

PAGE_TMPL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{code} {name} - MES操作指导书</title>
<link rel="stylesheet" href="../css/style.css">
</head>
<body>
  <div class="layout">
    <aside class="sidebar" id="sidebar">
      <div class="sidebar-header">
        <a href="../index.html" class="sidebar-home-link">
          <h2 class="sidebar-title">美诗儿 MES 操作指导书</h2>
        </a>
      </div>
      <nav class="sidebar-modules">
        <ul>
          {module_nav}
        </ul>
      </nav>
      <div class="sidebar-divider"></div>
      <nav class="sidebar-sections">
        <div class="sidebar-section-label">本页目录</div>
        <ul>
          <li><a href="#flow">流程图</a></li>
        </ul>
      </nav>
    </aside>
    <main class="main-content" id="main-content">
      <header class="page-header">
        <h1>{code} {name}</h1>
        <div class="meta-info">责任部门：{dept}　|　流程入口：{entry}　|　数据流向：{flow}</div>
      </header>
      <div class="sections">
        <section class="doc-section" id="def">
          <h2 class="section-title">流程定义</h2>
          <div class="section-content scenario-content">
            <p>{definition}</p>
          </div>
        </section>
        <section class="doc-section" id="flow">
          <h2 class="section-title">流程图</h2>
          <div class="section-content flowchart-content">
            <img class="sop-image" src="../{img}" alt="{code} {name}" loading="lazy">
          </div>
        </section>
      </div>
      <footer class="page-footer">
        <p>美诗儿（浙江）环境智能电器有限公司 - MES 操作指导书</p>
        <p class="footer-edit-hint">SOP 全本（26 份合订）见
          <a href="../assets/{pdf}">PDF</a></p>
      </footer>
    </main>
  </div>
  <script src="../js/main.js"></script>
</body>
</html>"""


def esc(t):
    if t is None:
        return ""
    return (str(t).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def sop_nav(sops, cur):
    """SOP 分组的侧边栏导航（页面内用）。"""
    out = []
    for s in sops:
        cls = ' class="active"' if s["code"] == cur else ""
        out.append('            <li><a href="%s.html"%s>%s %s</a></li>'
                   % (s["code"], cls, s["code"], esc(s["name"])))
    return "\n".join(out)


def render_page(s, sops):
    return PAGE_TMPL.format(
        code=s["code"], name=esc(s["name"]), dept=esc(s["dept"]),
        entry=esc(s.get("entry") or "—"), flow=esc(s.get("flow") or "—"),
        definition=esc(s["definition"]),
        img="%s/%s" % (IMG_DIR, s["image"]),
        module_nav=sop_nav(sops, s["code"]),
        pdf=PDF_NAME,
    )


def render_index_group(sops):
    """首页侧边栏里 SOP 分组的条目。"""
    return "\n".join(
        '              <li><a href="pages/%s.html">📄 %s %s</a></li>'
        % (s["code"], s["code"], esc(s["name"])) for s in sops)


def render_index_cards(sops):
    cards = []
    for s in sops:
        cards.append('''      <a href="pages/%s.html" class="module-card">
        <div class="card-icon">📄</div>
        <div class="card-body">
          <h3>%s %s</h3>
          <p class="card-dept">%s</p>
        </div>
      </a>''' % (s["code"], s["code"], esc(s["name"]), esc(s["dept"])))
    return "\n".join(cards)


def main():
    data = json.load(io.open(sys.argv[1], encoding="utf-8"))
    sops = data["sops"]
    os.makedirs(PAGES_DIR, exist_ok=True)

    for s in sops:
        path = os.path.join(PAGES_DIR, "%s.html" % s["code"])
        io.open(path, "w", encoding="utf-8").write(render_page(s, sops))
    print("已生成 %d 个 SOP 页面" % len(sops))

    # 供 generate.py / 手工更新首页时取用
    io.open(os.path.join(BASE_DIR, "_sop_nav.html"), "w", encoding="utf-8").write(
        render_index_group(sops))
    io.open(os.path.join(BASE_DIR, "_sop_cards.html"), "w", encoding="utf-8").write(
        render_index_cards(sops))
    print("已输出 _sop_nav.html / _sop_cards.html（首页片段）")


if __name__ == "__main__":
    main()
