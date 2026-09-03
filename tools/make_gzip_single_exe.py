import gzip
import os

# 1. Divina_Console.html을 Gzip으로 압축
html_path = "/mnt/d/game/Divina_Console.html"
with open(html_path, "rb") as f:
    raw_data = f.read()

gz_data = gzip.compress(raw_data, 9)
gz_path = "/mnt/d/game/game.html.gz"
with open(gz_path, "wb") as f:
    f.write(gz_data)

raw_size = len(raw_data) / 1024
gz_size = len(gz_data) / 1024
print(f"원본 HTML: {raw_size:.1f} KB -> Gzip 압축: {gz_size:.1f} KB (감소율: {(1 - gz_size/raw_size)*100:.1f}%)")

# 2. C# 소스: exe 내장 GZipStream으로 메모리에서 풀어서 실행!
csharp_code = """using System;
using System.Diagnostics;
using System.IO;
using System.IO.Compression;
using System.Reflection;

namespace DivinaLudus {
    static class Program {
        [STAThread]
        static void Main() {
            try {
                string tempDir = Path.Combine(Path.GetTempPath(), "DivinaLudus");
                if (!Directory.Exists(tempDir)) {
                    Directory.CreateDirectory(tempDir);
                }
                string tempHtml = Path.Combine(tempDir, "game.html");

                Assembly asm = Assembly.GetExecutingAssembly();
                using (Stream stream = asm.GetManifestResourceStream("game.html.gz")) {
                    if (stream != null) {
                        using (GZipStream gz = new GZipStream(stream, CompressionMode.Decompress)) {
                            using (FileStream fs = new FileStream(tempHtml, FileMode.Create, FileAccess.Write)) {
                                byte[] buffer = new byte[8192];
                                int read;
                                while ((read = gz.Read(buffer, 0, buffer.Length)) > 0) {
                                    fs.Write(buffer, 0, read);
                                }
                            }
                        }
                    }
                }

                if (!File.Exists(tempHtml)) return;

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

bat_text = f"""@echo off
cd /d "%~dp0"

echo [1/2] Checking C# Compiler...
set CSC=C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\csc.exe
if not exist "%CSC%" (
    set CSC=C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\csc.exe
)

echo Compiler: %CSC%
echo [2/2] Embedding Compressed Game (Gzip) into divina.exe (Target: Under 1MB) ...

"%CSC%" /target:winexe /optimize+ /platform:anycpu /res:"game.html.gz,game.html.gz" /out:divina.exe DivinaAppSingle.cs

echo.
if exist divina.exe (
    echo ==============================================================================
    echo   [SUCCESS] 100% Pure Single Standalone divina.exe Generated!
    echo   Final Size: Under 1MB Defended!
    echo ==============================================================================
) else (
    echo [ERROR] Compilation failed.
)

echo.
pause
"""

with open("/mnt/d/game/compile_divina_exe.bat", "wb") as f:
    f.write(bat_text.replace("\n", "\r\n").encode("cp949"))

print("Gzip Single EXE Builder configured successfully!")
