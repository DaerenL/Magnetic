# AI DJ Remixing Website

An AI-powered DJ/remixing website that creates continuous, cohesive playlists with smooth transitions.

## Project Structure

```
Magnetic/
├── backend/          # FastAPI Python backend
├── frontend/         # Next.js React frontend
└── documents/        # Project documentation
```

## Prerequisites

- ✅ Python 3.11+ (you have Python 3.14.0)
- ✅ Node.js (installed)
- ✅ Git (installed)
- ⚠️ FFmpeg (needs to be added to PATH - see note below)

## Quick Start

### Backend Setup

1. Navigate to backend directory:
   ```powershell
   cd backend
   ```

2. Activate virtual environment:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Start the FastAPI server:
   ```powershell
   uvicorn main:app --reload --port 8000
   ```

   The backend will be available at `http://localhost:8000`
   API docs at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to frontend directory:
   ```powershell
   cd frontend
   ```

2. Start the Next.js dev server:
   ```powershell
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

## Important Notes

### FFmpeg Setup

FFmpeg is required for audio processing but wasn't found in your PATH. You need to:

1. Download FFmpeg from [ffmpeg.org](https://www.gyan.dev/ffmpeg/builds/) or use:
   ```powershell
   choco install ffmpeg  # if you have Chocolatey
   scoop install ffmpeg  # if you have Scoop
   ```

2. Add FFmpeg to your PATH:
   - Extract FFmpeg to a folder (e.g., `C:\ffmpeg`)
   - Add `C:\ffmpeg\bin` to your System PATH
   - Restart your terminal

3. Verify installation:
   ```powershell
   ffmpeg -version
   ```

**Note:** Audio processing features won't work until FFmpeg is properly installed and accessible.

## Development

### Backend Dependencies

All Python packages are installed in the virtual environment. To reinstall:
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Frontend Dependencies

All npm packages are installed. To reinstall:
```powershell
cd frontend
npm install
```

## Next Steps

See `documents/tasks/sprint-1.md` for the development roadmap and tasks.

## Documentation

- Requirements: `documents/Requirements.md`
- Design: `documents/Design.md`
- Setup Guide: `documents/SETUP.md`
- Sprint Tasks: `documents/tasks/`
