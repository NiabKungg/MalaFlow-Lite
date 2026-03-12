@echo off
chcp 65001 > nul
TITLE MalaFlow POS Server

echo.
echo  ╔══════════════════════════════════════╗
echo  ║   🌶️  MalaFlow POS - Starting...    ║
echo  ╚══════════════════════════════════════╝
echo.

:: Check Python
python --version > nul 2>&1
if errorlevel 1 (
  echo [ERROR] Python is not installed or not in PATH.
  echo Please install Python 3.10+ from https://python.org
  pause
  exit /b 1
)

:: Change to script directory
cd /d "%~dp0"

:: Copy .env.example to .env if .env doesn't exist
if not exist .env (
  if exist .env.example (
    copy .env.example .env > nul
    echo [INFO] Created .env from .env.example - please configure your Telegram token!
  )
)

:: Install dependencies
echo [1/3] Installing dependencies...
pip install -r requirements.txt -q
if errorlevel 1 (
  echo [ERROR] Failed to install dependencies.
  pause
  exit /b 1
)

:: Seed data if DB does not exist
if not exist malaflow.db (
  echo [2/3] Setting up database and seeding initial data...
  python seed_data.py
) else (
  echo [2/3] Database already exists, skipping seed.
)

:: Start server
echo [3/3] Starting MalaFlow POS server...
echo.
echo  ┌─────────────────────────────────────────────────────┐
echo  │  🍲 MalaFlow POS is running!                        │
echo  │                                                     │
echo  │  Customer Menu : http://localhost:8000/order        │
echo  │  POS Dashboard : http://localhost:8000/pos          │
echo  │  Order Status  : http://localhost:8000/order-status │
echo  │  Sales History : http://localhost:8000/history      │
echo  │                                                     │
echo  │  Press CTRL+C to stop the server                    │
echo  └─────────────────────────────────────────────────────┘
echo.

python main.py

pause
