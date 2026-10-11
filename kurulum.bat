@echo off
title AnimeAI - Otomatik Kurulum Sihirbazi (Setup Wizard)
cd /d "%~dp0"

echo =======================================================
echo         AnimeAI: Otomatik Kurulum Sihirbazi
echo         Automated Setup & Hardware Optimizer
echo =======================================================
echo.

:: 1. Python kontrolu
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [HATA / ERROR] Python bulunamadi!
    echo Lutfen Python 3.10, 3.11 veya 3.12 kurun ve "Add Python to PATH" secenegini isaretleyin.
    echo Please install Python 3.10+ and check "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

echo [1/4] Python ortam testi basarili.
python --version
echo.

:: 2. Pip guncelleme
echo [2/4] Paket yoneticisi hazirlaniyor...
python -m pip install --upgrade pip >nul 2>&1

:: 3. GPU Algilama ve PyTorch Kurulumu
echo [3/4] Donanim tespiti yapiliyor...
where nvidia-smi >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [BILGI] NVIDIA GPU tespit edildi! CUDA destekli PyTorch kuruluyor...
    echo [INFO]  NVIDIA GPU detected. Installing CUDA 12.4 PyTorch...
    python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
) else (
    echo [BILGI] Ayrilmis NVIDIA GPU tespit edilemedi. Standart PyTorch kuruluyor...
    echo [INFO]  No NVIDIA GPU detected. Installing standard PyTorch...
    python -m pip install torch torchvision torchaudio
)

echo.
echo Kutuphane bagimliliklari kuruluyor (requirements.txt)...
python -m pip install -r requirements.txt
echo.

:: 4. Modelleri indir ve dogrula
echo [4/4] Yapay zeka modelleri kontrol ediliyor ve indiriliyor...
echo [4/4] Verifying and downloading AI models from Hugging Face...
echo.
python scripts\download_models.py

echo.
echo =======================================================
echo   TEBRIKLER! Kurulum basariyla tamamlandi.
echo   CONGRATULATIONS! Setup completed successfully.
echo.
echo   Calistirmak icin 'baslat.bat' dosyasina cift tiklayin.
echo   Double-click 'baslat.bat' to launch AnimeAI Studio.
echo =======================================================
echo.
pause
