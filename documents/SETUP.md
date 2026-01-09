# Setup Guide - AI DJ Remixing Website

## Prerequisites Installation

You already have:
- ✅ Node.js
- ✅ Git

You need to install:

### 1. Python 3.11 or higher

**Windows:**
- Download from [python.org](https://www.python.org/downloads/)
- During installation, check "Add Python to PATH"
- Verify installation:
  ```powershell
  python --version
  ```
  Should show Python 3.11 or higher

### 2. FFmpeg (Required for audio processing)

**Windows:**
- Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use a Windows build from [here](https://www.gyan.dev/ffmpeg/builds/)
- Extract to a folder (e.g., `C:\ffmpeg`)
- Add to PATH:
  1. Open System Properties → Environment Variables
  2. Edit "Path" under System variables
  3. Add the `bin` folder path (e.g., `C:\ffmpeg\bin`)
- Verify installation:
  ```powershell
  ffmpeg -version
  ```

**Alternative (using package manager):**
- If you have Chocolatey: `choco install ffmpeg`
- If you have Scoop: `scoop install ffmpeg`

---

## Project Setup (After Prerequisites)

Once Python and FFmpeg are installed, follow these steps:

### Backend Setup

1. Navigate to the backend directory:
   ```powershell
   cd backend
   ```

2. Create a virtual environment:
   ```powershell
   python -m venv .venv
   ```

3. Activate the virtual environment:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```

4. Install Python dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

   Required packages:
   - `fastapi`
   - `uvicorn[standard]`
   - `pydantic`
   - `yt-dlp`
   - `librosa`
   - `soundfile`
   - `pydub`
   - `python-multipart`

### Frontend Setup

1. Navigate to the frontend directory:
   ```powershell
   cd frontend
   ```

2. Install npm dependencies:
   ```powershell
   npm install
   ```

   Required packages (will be in package.json):
   - `next`
   - `react`
   - `react-dom`
   - `axios` (or use fetch)
   - `zustand` (optional, for state management)

---

## Quick Verification

After installation, verify everything works:

1. **Python:**
   ```powershell
   python --version
   ```

2. **FFmpeg:**
   ```powershell
   ffmpeg -version
   ```

3. **Node.js:**
   ```powershell
   node --version
   npm --version
   ```

---

## Running the Project

### Backend (FastAPI)
```powershell
cd backend
.venv\Scripts\Activate.ps1
uvicorn main:app --reload --port 8000
```

### Frontend (Next.js)
```powershell
cd frontend
npm run dev
```

Frontend will run on `http://localhost:3000`
Backend will run on `http://localhost:8000`

---

## Troubleshooting

### FFmpeg not found
- Ensure FFmpeg is in your PATH
- Restart your terminal/PowerShell after adding to PATH
- Try `ffmpeg -version` in a new terminal window

### Python not found
- Ensure Python is added to PATH during installation
- Try `python3` instead of `python` on some systems

### Virtual environment activation fails
- On Windows, you may need to allow script execution:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```


