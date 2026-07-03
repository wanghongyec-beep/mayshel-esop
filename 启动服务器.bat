@echo off
chcp 65001 >nul
title MES操作手册 - HTTP服务器

:: ===== 获取本机局域网IP =====
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do set IP=%%a
set IP=%IP: =%

echo ============================================
echo   MES 操作指导书 - HTTP 服务器
echo ============================================
echo.
echo   [1/2] 配置防火墙...
:: 以管理员身份添加防火墙规则（静默）
net session >nul 2>&1
if %errorlevel% equ 0 (
    netsh advfirewall firewall add rule name="MES操作手册" dir=in action=allow protocol=TCP localport=8000 >nul 2>&1
    echo   ✅ 防火墙已放行端口 8000
) else (
    echo   ⚠ 请以管理员身份运行（右键→以管理员身份运行）
    echo     或手动在防火墙放行 8000 端口
    timeout /t 3 /nobreak >nul
)

echo.
echo   [2/2] 启动服务器...
echo.
echo   ========================================
echo       本机:    http://localhost:8000
echo       局域网:  http://%IP%:8000
echo   ========================================
echo.
echo   手机/其他电脑操作方法：
echo   ① 连接同一个 WiFi / 局域网
echo   ② 打开浏览器输入 http://%IP%:8000
echo.
echo   按 Ctrl+C 停止服务器
echo   ========================================
echo.

python server.py
pause