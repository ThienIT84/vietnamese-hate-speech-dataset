@echo off
echo ========================================
echo SafeSense-Vi Demo - Quick Start
echo ========================================
echo.
echo Current directory: %CD%
echo.

echo Step 1: Testing Preprocessing...
echo.
python test_preprocessing.py
if errorlevel 1 (
    echo.
    echo ❌ Test failed! Check errors above.
    pause
    exit /b 1
)
echo.

echo ========================================
echo Step 2: Starting Streamlit Demo...
echo ========================================
echo.
echo Opening browser at http://localhost:8501
echo Press Ctrl+C to stop the server
echo.
streamlit run Safesense_VI.py
