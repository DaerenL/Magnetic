# Sprint 1 — Project Setup & Basic Audio Pipeline

## Goal

Set up the full-stack project structure (Next.js frontend + FastAPI backend) and implement the minimal end-to-end flow:

- User submits a YouTube URL.
- Backend downloads the audio, converts it, and analyzes basic features (BPM, duration).
- Frontend can request and display this basic info.
- Frontend can play the raw audio file (no mixing, no AI selection yet).

---

## 1. Repository & Environment Setup

### 1.1 Monorepo Structure

- [ ] Create a Git repo with the following top-level structure:
  - [ ] `/frontend` — Next.js app
  - [ ] `/backend` — FastAPI app
  - [ ] `/docs` — documentation (`requirements.md`, `design.md`, sprint tasks)
  - [ ] `/scripts` — helper scripts (optional)
  - [ ] Root `README.md` linking to requirements/design/tasks.

### 1.2 Backend Environment (Python + FastAPI)

- [ ] Install Python 3.11+ on dev machine.
- [ ] Under `/backend`:
  - [ ] Create a virtual environment (`python -m venv .venv`).
  - [ ] Create `requirements.txt` with at least:
    - `fastapi`
    - `uvicorn[standard]`
    - `pydantic`
    - `yt-dlp`
    - `librosa`
    - `soundfile`
    - `pydub`
    - `python-multipart`
  - [ ] Install dependencies: `pip install -r requirements.txt`.
- [ ] Ensure `ffmpeg` is installed on the dev machine and accessible in PATH.
  - [ ] Verify with `ffmpeg -version`.

### 1.3 FastAPI Skeleton

- [ ] In `/backend`, create:
  - [ ] `main.py` as FastAPI entrypoint.
  - [ ] `models/` package for Pydantic models (`__init__.py`, `track.py`, `session.py`, `settings.py`).
  - [ ] `audio/` package (`__init__.py`, `downloader.py`, `analysis.py`, `utils.py`).
  - [ ] `storage/` package (`__init__.py`, `tracks.py`, `sessions.py`).
- [ ] Implement basic FastAPI app:
  - [ ] Create an app instance in `main.py`.
  - [ ] Add CORS middleware to allow requests from `http://localhost:3000`.

```py
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```
- [ ] Add `if __name__ == "__main__"` block or docs for running:

`uvicorn main:app --reload --port 8000`.

### 1.4 Frontend Environment (Next.js)

- [ ] Under `/frontend`:
  - [ ] Initialize Next.js app (App Router or Pages; choose one and stick to it).
    - Example: `npx create-next-app@latest .`
  - [ ] Confirm dev server runs: `npm run dev` → check at `http://localhost:3000`.
  - [ ] Install UI and helper libraries (if desired):
    - `npm install axios` (or commit to using fetch only).
    - `npm install zustand` (or another state library, optional).
  - [ ] Set up basic global CSS with a dark theme background.

---

## 2. Backend: Track Model + Download + Analysis (Minimal)

### 2.1 Track Data Model

- [ ] In `/backend/models/track.py`, define a Pydantic Track model:

```py
class Track(BaseModel):
    id: str
    title: str
    artist: str
    source_url: str
    audio_path: str
    cover_art_url: str
    bpm: float | None = None
    duration_seconds: float | None = None
```

For now, ignore key/energy/brightness; they will be added in later sprints.

### 2.2 Audio Downloader (audio/downloader.py)

- [ ] Implement `download_youtube_audio(source_url: str) -> dict` that:
  - [ ] Uses `yt_dlp` to download audio-only from a YouTube URL.
  - [ ] Saves it to a configured directory (e.g. `/backend/data/raw/`).
  - [ ] Returns:
    - Final audio file path.
    - Title.
    - Channel name (as artist).
    - Thumbnail URL (cover_art_url).
  - [ ] Ensure:
    - Filenames are sanitized (no weird characters).
    - Extension is either `.mp3` or `.wav` depending on conversion.

### 2.3 Audio Conversion & Analysis (audio/analysis.py)

- [ ] Implement a function `analyze_audio(audio_path: str) -> dict` that:
  - [ ] Uses `librosa.load` with a consistent sample rate (e.g. 22050 or 44100).
  - [ ] Estimates BPM using `librosa.beat.tempo`.
  - [ ] Calculates `duration_seconds` using `librosa.get_duration`.
  - [ ] For now, ignore advanced features.
  - [ ] Ensure errors are handled:
    - If audio can't be loaded, raise a clean exception.

### 2.4 Track Storage (storage/tracks.py)

- [ ] Implement an in-memory track registry:
  - [ ] A global dict `TRACKS: dict[str, Track] = {}` for development.
  - [ ] Implement helper functions:
    - `save_track(track: Track) -> None`
    - `get_track(track_id: str) -> Track | None`

---

## 3. Backend: Minimal API for First Track

### 3.1 Endpoint: Initialize First Track (No Session Yet)

- [ ] Implement `POST /api/track/from-url` in `main.py` or `api/tracks.py`:
  - [ ] Input model:
    - `source_url: str`
  - [ ] Behavior:
    - Call `download_youtube_audio(source_url)`.
    - Call `analyze_audio(audio_path)`.
    - Construct Track instance with:
      - Generated id (e.g. `uuid4()` string).
      - Download metadata.
      - Analysis results.
    - Save track in `TRACKS`.
  - [ ] Output:
    - JSON Track object.

Example response:

```json
{
  "track": {
    "id": "uuid",
    "title": "Example Track",
    "artist": "Channel Name",
    "source_url": "https://youtube.com/...",
    "audio_path": "/static/audio/uuid.mp3",
    "cover_art_url": "...",
    "bpm": 128.0,
    "duration_seconds": 213.5
  }
}
```

### 3.2 Static / Media Serving

- [ ] Configure FastAPI to serve audio files under `/static/audio/`:
  - [ ] Use `StaticFiles` from `fastapi.staticfiles`.
  - [ ] Ensure `audio_path` that is returned to frontend is either:
    - A full URL (`http://localhost:8000/static/audio/...`), or
    - A path that frontend can build into a full URL.

---

## 4. Frontend: Minimal UI + First Track Flow

### 4.1 Layout Scaffold

- [ ] Create a simple page layout:
  - [ ] Dark background.
  - [ ] A top bar with:
    - App name text.
    - Placeholder settings icon (no functionality yet).
  - [ ] Main area split into:
    - Center: "Turntable area" placeholder.
    - Right: "Queue" placeholder.

### 4.2 Track Input Form

- [ ] Add a section (top or center) for:
  - [ ] Input field: YouTube URL.
  - [ ] Button: "Load Track".
  - [ ] On click:
    - Call `POST /api/track/from-url` with the URL.
    - Display a loading state.
  - [ ] On success:
    - Store returned track in frontend state as `currentTrack`.

### 4.3 Basic Turntable UI (Static)

- [ ] For Sprint 1, keep it simple:
  - [ ] Show a circle representing the record.
  - [ ] Use `currentTrack.cover_art_url` as a background image.
  - [ ] Show `currentTrack.title` and `currentTrack.artist` below it.
  - [ ] No animation logic yet (spinning, transitions will come later).

### 4.4 Basic Audio Playback

- [ ] Add an HTML `<audio>` element or custom audio hook that:
  - [ ] Uses `currentTrack.audio_path` as `src`.
  - [ ] Provides Play/Pause controls.
  - [ ] For Sprint 1:
    - Use the default browser controls, or a minimal custom play/pause button.
  - [ ] Confirm:
    - When you load a YouTube URL, you can play the downloaded audio in the browser.

---

## 5. Verification & Dev UX

- [ ] Test full flow locally:
  - [ ] Run FastAPI on port 8000.
  - [ ] Run Next.js on port 3000.
  - [ ] Input a YouTube URL.
  - [ ] Watch logs to ensure:
    - Download occurs.
    - Analysis runs.
    - Track info returns successfully.
  - [ ] Confirm audio is playable via frontend.
- [ ] Add minimal error handling in frontend:
  - [ ] Show a simple error message if backend returns an error (invalid URL, etc.).

---

## 6. Definition of Done (Sprint 1)

A developer can:

- Start backend and frontend.
- Paste a YouTube URL in the UI.
- Click "Load Track".
- See metadata (title, artist, BPM, duration).
- Play the audio in the browser from the backend-served file.

Code is committed with:

- Clear folder structure.
- Basic README for how to run backend and frontend.

