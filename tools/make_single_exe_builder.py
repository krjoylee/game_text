import os
import sys

# Divina_Console.html 읽기
html_path = "/mnt/d/game/Divina_Console.html"
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# C# 소스 생성: HTML 데이터를 리소스 또는 문자열 형태로 exe 내부에 100% 임베딩!
# 1.3MB HTML을 임베드하기 위해 base64로 인코딩하거나 임베디드 리소스로 컴파일!
csharp_code = """using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;

namespace DivinaLudus {
    static class Program {
        [STAThread]
        static void Main() {
            try {
                // exe 내부 임베디드 리소스에서 HTML 추출
                string tempDir = Path.Combine(Path.GetTempPath(), "DivinaLudus");
                if (!Directory.Exists(tempDir)) {
                    Directory.CreateDirectory(tempDir);
                }
                string tempHtml = Path.Combine(tempDir, "game.html");

                Assembly asm = Assembly.GetExecutingAssembly();
                using (Stream stream = asm.GetManifestResourceStream("game.html")) {
                    if (stream != null) {
                        using (FileStream fs = new FileStream(tempHtml, FileMode.Create, FileAccess.Write)) {
                            stream.CopyTo(fs);
                        }
                    }
                }

                if (!File.Exists(tempHtml)) return;

                // 앱 모드 독립 창으로 실행
                ProcessStartInfo psi = new ProcessStartInfo();
                psi.FileName = "msedge.exe";
                psi.Arguments = string.Format("--app=\\"file:///{0}\\" --window-size=880,860", tempHtml.Replace('\\\\', '/'));
                psi.UseShellExecute = true;

                try {
                    Process.Start(psi);
                } catch {
                    try {
                        psi.FileName = "chrome.exe";
                        Process.Start(psi);
                    } catch {
                        Process.Start(tempHtml);
                    }
                }
            } catch {
            }
        }
    }
}
"""

with open("/mnt/d/game/DivinaAppSingle.cs", "wb") as f:
    f.write(csharp_code.replace("\n", "\r\n").encode("utf-8"))

# compile_divina_exe.bat 갱신: /res:Divina_Console.html,game.html 옵션 추가!
bat_text = """@echo off
cd /d "%~dp0"

echo [1/2] Checking C# Compiler...
set CSC=C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\csc.exe
if not exist "%CSC%" (
    set CSC=C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\csc.exe
)

echo Compiler: %CSC%
echo [2/2] Embedding HTML into divina.exe (100% Standalone Single EXE) ...

"%CSC%" /target:winexe /optimize+ /platform:anycpu /res:"Divina_Console.html,game.html" /out:divina.exe DivinaAppSingle.cs

echo.
if exist divina.exe (
    echo ==============================================================================
    echo   [SUCCESS] 100% Pure Single Standalone divina.exe Generated!
    echo   You can copy ONLY divina.exe anywhere (Desktop, USB) without HTML!
    echo ==============================================================================
) else (
    echo [ERROR] Compilation failed.
)

echo.
pause
"""

with open("/mnt/d/game/compile_divina_exe.bat", "wb") as f:
    f.write(bat_text.replace("\n", "\r\n").encode("cp949"))

print("Single EXE Builder ready!")
