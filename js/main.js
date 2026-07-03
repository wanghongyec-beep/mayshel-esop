/**
 * 美诗儿 MES 操作指导书 - 交互脚本 v3
 */

document.addEventListener('DOMContentLoaded', function() {
    initScrollSpy();
    initImagePlaceholders();
    initSmoothScroll();
    initImageZoom();
});

/**
 * ScrollSpy: 滚动时高亮当前所在的章节
 */
function initScrollSpy() {
    var sidebarLinks = document.querySelectorAll('.sidebar-sections a');
    if (!sidebarLinks.length) return;

    var sections = [];
    sidebarLinks.forEach(function(link) {
        var href = link.getAttribute('href');
        if (href && href.startsWith('#')) {
            var target = document.getElementById(href.substring(1));
            if (target) {
                sections.push({
                    id: href.substring(1),
                    el: target,
                    link: link,
                });
            }
        }
    });

    if (!sections.length) return;

    // 初始检查
    updateActiveSection(sections);

    // 滚动时检查
    window.addEventListener('scroll', function() {
        updateActiveSection(sections);
    }, { passive: true });

    // 点击链接后高亮（抽屉已自动关闭）
    sections.forEach(function(s) {
        s.link.addEventListener('click', function() {
            sections.forEach(function(s2) {
                s2.link.classList.remove('active');
            });
            s.link.classList.add('active');
        });
    });
}

function updateActiveSection(sections) {
    var scrollPos = window.scrollY + 100;
    var currentId = sections[0]?.id;

    for (var i = 0; i < sections.length; i++) {
        var s = sections[i];
        if (s.el.offsetTop <= scrollPos) {
            currentId = s.id;
        }
    }

    sections.forEach(function(s) {
        s.link.classList.toggle('active', s.id === currentId);
    });
}

/**
 * 图片占位符点击提示
 */
function initImagePlaceholders() {
    document.querySelectorAll('.placeholder-box').forEach(function(box) {
        box.addEventListener('click', function() {
            var msg = '请将实际截图放入对应的 images/ 目录，并修改此占位符为 <img> 标签。\n\n示例：\n<img src="../images/xxx/fig-01.png" alt="图X">';
            alert(msg);
        });
    });
}

/**
 * 平滑滚动（兼容不支持 scroll-behavior 的浏览器）
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            var href = anchor.getAttribute('href');
            if (href === '#') return;
            var target = document.getElementById(href.substring(1));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

/**
 * 图片点击放大（lightbox）
 */
function initImageZoom() {
    // 创建遮罩层
    var overlay = document.createElement('div');
    overlay.className = 'img-overlay';
    var overlayImg = document.createElement('img');
    overlay.appendChild(overlayImg);
    document.body.appendChild(overlay);

    // 点击图片 → 放大
    document.querySelectorAll('.step-figure img, .flowchart-figure img, .step-pair-img img').forEach(function(img) {
        img.addEventListener('click', function(e) {
            e.stopPropagation();
            overlayImg.src = this.src;
            overlayImg.alt = this.alt;
            overlay.classList.add('show');
        });
    });

    // 点击 SVG 流程图 → 放大（序列化为 data URL）
    document.querySelectorAll('.flowchart-svg').forEach(function(svg) {
        svg.addEventListener('click', function(e) {
            e.stopPropagation();
            var serializer = new XMLSerializer();
            var svgStr = serializer.serializeToString(this);
            var svgBlob = new Blob([svgStr], { type: 'image/svg+xml;charset=utf-8' });
            var url = URL.createObjectURL(svgBlob);
            overlayImg.src = url;
            overlayImg.alt = '流程图';
            overlay.classList.add('show');
            // 释放 URL 对象（等图片加载完后）
            overlayImg.onload = function() {
                URL.revokeObjectURL(url);
                overlayImg.onload = null;
            };
        });
    });

    // 点击遮罩 → 关闭
    overlay.addEventListener('click', function() {
        this.classList.remove('show');
    });

    // ESC → 关闭
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && overlay.classList.contains('show')) {
            overlay.classList.remove('show');
        }
    });
}
