@echo off
chcp 65001 > nul
cls

echo.
echo ════════════════════════════════════════════════════════════════════════
echo            🛡️  SAFESENSE-VI DEMO - IT GOT TALENT 2025
echo ════════════════════════════════════════════════════════════════════════
echo.
echo   📦 Model: PhoBERT-v2 (vinai/phobert-base-v2)
echo   🎯 Task:  Vietnamese Toxic Comment Detection
echo   📊 F1:    0.80+ (3-class classification)
echo.
echo ════════════════════════════════════════════════════════════════════════
echo.

REM Kiểm tra model path
set MODEL_PATH=C:\Học sâu\Dataset\TOXIC_COMMENT\models\phobert-hate-speech-final
if not exist "%MODEL_PATH%\config.json" (
    echo ❌ Model không tìm thấy tại: %MODEL_PATH%
    echo.
    echo 💡 Hướng dẫn:
    echo    1. Kiểm tra đường dẫn model
    echo    2. Hoặc train model mới bằng scripts/training/
    echo.
    pause
    exit /b 1
)

echo ✅ Model found: %MODEL_PATH%
echo.

REM Kiểm tra preprocessing module
if not exist "..\..\src\preprocessing\advanced_text_cleaning.py" (
    echo ❌ Preprocessing module không tìm thấy
    echo    Expected: src/preprocessing/advanced_text_cleaning.py
    echo.
    pause
    exit /b 1
)

echo ✅ Preprocessing module found
echo.

echo ════════════════════════════════════════════════════════════════════════
echo                    🚀 STARTING STREAMLIT DEMO
echo ════════════════════════════════════════════════════════════════════════
echo.
echo   🌐 URL: http://localhost:8501
echo   ⏹️  Stop: Press Ctrl+C
echo.
echo ────────────────────────────────────────────────────────────────────────
echo.

REM Chạy Streamlit
streamlit run Safesense_VI.py --server.headless true

echo.
echo ════════════════════════════════════════════════════════════════════════
echo                         DEMO STOPPED
echo ════════════════════════════════════════════════════════════════════════
echo.
pause
