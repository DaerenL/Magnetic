# Design.md — AI DJ Remixing Website

## 1. Design Goals

- Build a single-page **desktop-first web app** that feels like an AI DJ.
- Use **Next.js** for the frontend and **Python (FastAPI)** for the backend.
- Do **all heavy processing in the backend**:
  - Audio download
  - Audio analysis
  - Mixing/transitions
  - AI track selection
- Frontend focuses on:
  - Visual turntable
  - Queue UI
  - Controls and settings
  - Displaying state from backend
- Keep the **visual design minimal** (no complex visualizers for now).

### Non-goals (for now):
- Mobile/responsive layouts.
- True generative remixing.
- User accounts/auth.
- Public deployment with full legal/ToS compliance.

---

## 2. High-Level Architecture

- **Frontend**
  - Framework: **Next.js** (App Router or Pages, single main route `/`).
  - Runs in the browser, renders:
    - Top bar (logo + settings).
    - Turntable with spinning record.
    - Queue panel.
  - Uses HTTP/JSON APIs to communicate with backend.
  - Streams/plays audio from backend-hosted files/streams.

- **Backend**
  - Framework: **FastAPI (Python)**.
  - Responsibilities:
    - Accept song input (YouTube URL or search term).
    - Use `yt-dlp` to download audio + metadata.
    - Use `ffmpeg` / `librosa` / other DSP tools to:
      - Convert audio to a standard format.
      - Analyze audio features (BPM, energy, brightness, etc.).
    - Store track metadata and file paths.
    - Maintain session and queue state.
    - Implement AI selection logic.
    - Perform audio mixing and generate transition segments.
    - Expose endpoints for session state and audio streaming.

- **Storage / Files**
  - Local file system for:
    - Raw downloaded audio.
    - Converted/normalized audio.
    - Mixed transition segments (if needed).
  - In-memory structures or simple local DB (e.g., SQLite) for:
    - Tracks metadata.
    - Session state.
    - Queues.

---

## 3. Frontend Design (Next.js)

### 3.1 Page Structure

- Single main route: `/`
- Core layout:
  - **Top bar** (header)
  - **Main content** split horizontally:
    - Center: Turntable area
    - Right: Queue panel
  - **Settings panel** as modal/overlay (triggered by gear icon)

Example structure (conceptual, not strict code):

```tsx
// app/page.tsx or pages/index.tsx
export default function HomePage() {
  return (
    <AppProvider>
      <MainLayout>
        <TopBar />
        <MainContent>
          <TurntableSection />
          <QueueSection />
        </MainContent>
        <SettingsModal />
      </MainLayout>
    </AppProvider>
  );
}
```

### 3.2 Frontend State Management

Global state lives in:

React Context or a small state library (Zustand/Recoil/etc.).

Core pieces of state on frontend:

sessionId (string or null)

currentTrack (Track object or null)

queue (list of Queue items)

settings (UserSettings)

playbackState (playing/paused/loading/transitioning)

positionSeconds (current playback position, handled by frontend timer)

State is synchronized with backend via periodic polling or event-based updates (polling is simpler for now).

### 3.3 Components

#### TopBar

Shows:

App name/logo.

Session status (e.g., “Idle”, “Playing”, “Transitioning”).

Settings button (gear icon).

Triggers open/close state of SettingsModal.

#### SettingsModal

Contains:

Target genre (dropdown).

Target BPM (slider or numeric).

Target energy (slider).

On save:

Calls backend API to update session settings.

Updates local settings state.

#### TurntableSection

Shows:

Large circular turntable.

Spinning record with cover art.

Current song title & artist.

Progress bar.

Playback controls:

Play/Pause button.

Skip button.

Uses CSS/JS animation for spinning.

Handles transition animation events when the backend changes the current track.

Logic:

When playbackState is PLAYING: record spins at normal speed.

When track change is initiated:

Temporary state triggers spin speed-up animation.

After transition is applied, record resets to normal speed with new cover.

#### QueueSection

Right-side vertical panel.

Renders list of upcoming tracks:

Mini cover art.

Title and artist.

Optional small BPM/genre text.

Each item includes a remove/dequeue button.

On remove:

Calls backend API to delete that queue item.

Updates local queue state.

#### TrackInputBar (optional)

Simple input (URL or search term).

Button: “Start Session”.

On click:

Calls backend to initialize session with the first track.

---

## 4. Backend Design (Python + FastAPI)

### 4.1 Main Modules

- **api/**

  - FastAPI routers and request/response models.

- **audio/**
  - Downloading with yt_dlp.
  - Audio conversion with ffmpeg.
  - Analysis using librosa or similar.

- **dj_engine/**
  - Track selection logic.
  - Queue management.
  - Session orchestration.

- **mixing/**
  - Crossfade and basic tempo adjustment.
  - EQ filters and loudness normalization (later).

- **models/**
  - Pydantic models for Track, Session, Settings, etc.

- **storage/**
  - Track registry and session store (in-memory or simple DB).

### 4.2 Core Data Models (Backend)

Conceptual Pydantic-style models (not exact code):

```py
class Track(BaseModel):
  id: str
  title: str
  artist: str
  source_url: str
  audio_path: str
  cover_art_url: str
  bpm: float | None
  key: str | None = None
  energy: float | None
  brightness: float | None = None
  genre_tag: str | None = None
  duration_seconds: float | None = None

class UserSettings(BaseModel):
  target_genre: str | Literal["auto"] = "auto"
  target_bpm: float | Literal["auto"] = "auto"
  target_energy: Literal["chill", "medium", "hype", "auto"] = "auto"

class SessionState(BaseModel):
  id: str
  current_track_id: str | None
  queue_track_ids: list[str]
  settings: UserSettings
  status: Literal["idle", "loading", "playing", "transitioning", "ended"]
```

---

## 5. Backend API Design

### 5.1 Session Endpoints

**POST /api/session/init**

- **Input:**
  - `source_type` (e.g. "youtube")
  - `source_value` (e.g. URL or search term)
  - Optional initial settings (genre/BPM/energy)

- **Behavior:**
  - Downloads audio via yt-dlp.
  - Analyzes track.
  - Creates a new SessionState.
  - Initializes queue with AI-selected next tracks.

- **Output:**
  - `sessionId`
  - `currentTrack` object
  - `queue` list

**GET /api/session/{session_id}**

- **Returns:**
  - `sessionState`
  - `currentTrack`
  - `queue`
  - `settings`

**POST /api/session/{session_id}/settings**

- **Input:**
  - `UserSettings`

- **Behavior:**
  - Updates stored settings.
  - Triggers re-evaluation of future queue items.

**POST /api/session/{session_id}/skip**

- **Behavior:**
  - Moves to next track in queue.
  - Initiates backend mixing for transition (if implemented).
  - Updates `current_track_id` and queue.
  - Returns updated state.

**DELETE /api/session/{session_id}/queue/{queue_item_id}**

- **Behavior:**
  - Removes that track from the queue.
  - Optionally replenishes queue with another AI-selected track.
  - Returns updated queue.

### 5.2 Audio Endpoints

**GET /api/audio/{track_id}**

- Sends audio file or streaming response for that track.
- Frontend uses this URL as the audio source.

**Optional (later): GET /api/audio/session/{session_id}/stream**

- A single mixed/streamed output if server-side mixing becomes more advanced.

---

## 6. Audio Processing Pipeline

### 6.1 Steps for First Track

1. Receive first track request (URL) from frontend.
2. Use yt-dlp to download audio (e.g., best audio only).
3. Use ffmpeg to:
   - Convert to uniform format (e.g., 44.1kHz, stereo, mp3/wav).
4. Use librosa or similar to:
   - Load audio.
   - Estimate BPM.
   - Estimate energy (RMS, loudness).
   - Estimate brightness (spectral centroid).
   - Optionally estimate key.
5. Create a Track object.
6. Store track metadata + audio file path.

### 6.2 Steps for Subsequent Tracks

When AI engine needs more tracks:

1. Decide where to get candidates from (e.g., related YouTube videos, previously downloaded tracks, etc.).
2. For each new candidate:
   - Download + analyze as above.
   - Store in track registry.

---

## 7. AI Selection Engine

### 7.1 Input and Output

**Inputs:**
- `currentTrack` features.
- `settings` (genre, BPM, energy).
- `candidateTracks` (subset of library).

**Output:**
- Ordered list of recommended next track IDs for the queue.

### 7.2 Rule-Based Scoring (Initial Implementation)

For each candidate track:

1. Compute:
   - `bpm_score`: closeness to `settings.target_bpm` or `currentTrack.bpm`.
   - `energy_score`: closeness to desired energy.
   - `genre_score`: match/mismatch with `settings.target_genre`.
   - `vibe_score`: similarity based on brightness/energy combination.

2. Combine scores:
   - `total_score = w1*bpm_score + w2*energy_score + w3*genre_score + w4*vibe_score`.

3. Sort candidates by `total_score`.

4. Choose top N for queue.

### 7.3 Future ML Extension

Keep design open to replacing the rule-based scorer with:

- A small ML model that predicts "transition quality" between current and candidate track.
- Use logged session data as training examples later.

---

## 8. Mixing & Transitions (Backend)

### 8.1 Requirements

- Implement simple crossfade transitions between current and next track.
- Optionally adjust playback tempo slightly to match BPM.

### 8.2 Basic Algorithm

**Given:**
- `trackA` (current)
- `trackB` (next)
- `transitionDuration` (e.g., 8 seconds)

**Steps:**

1. Extract tail segment from `trackA` (last N seconds).
2. Extract head segment from `trackB` (first N seconds).
3. Optionally:
   - Adjust playback rate of one or both to align beats (based on BPM).
4. Apply linear or curved fades:
   - `trackA` volume: 1 → 0
   - `trackB` volume: 0 → 1
5. Sum and export transition segment as part of stream or as a separate mixed file.

### 8.3 Integration with Turntable

When backend defines next track:

- Backend marks a `TRANSITIONING` state or includes a `transitionAt` timestamp.

Frontend:
- Triggers record speed-up animation when transition starts.
- Swaps to new cover art at the moment `trackB` becomes main.

---

## 9. Session State & Flow

### 9.1 Session State Machine

- **idle**
  - No track loaded.

- **loading**
  - First track being downloaded/analyzed.

- **playing**
  - A track is playing.

- **transitioning**
  - In the middle of a crossfade to next track.

- **ended**
  - No more tracks, or user stops session.

### 9.2 Typical Flow

1. User opens app (state: idle).

2. User enters YouTube URL and starts session:
   - Frontend → `POST /api/session/init`.
   - Backend downloads/analyzes track.
   - Backend returns `sessionId`, `currentTrack`, `queue`.
   - Frontend updates state and starts playback.

3. While playing:
   - Frontend polls session endpoint periodically for updates.
   - If backend queues additional tracks, frontend updates queue view.

4. User skips track:
   - Frontend → `POST /skip`.
   - Backend jumps to next track and updates state.
   - Frontend runs transition animation.

5. User removes queued track:
   - Frontend → `DELETE /queue/{queue_item_id}`.
   - Backend updates queue.

6. User modifies settings:
   - Frontend → `POST /settings`.
   - Backend recomputes queue for future tracks.

---

## 10. UX & Visual Behavior

**Visual style:**
- Dark theme.
- Minimal, clean, DJ/club vibe.

**Turntable:**
- Large and central.
- Record spin:
  - CSS keyframes or JS-based transform.
  - Speed-up animation on track change:
    - Temporary higher rotation speed.

**Queue:**
- Right side, scrollable if long.
- Hover effect per item.
- Remove button with small fade-out animation.

No complex waveform or spectrum visualizers for now.

---

## 11. Future Extensions (Design Hooks)

- Device responsiveness (mobile layout).
- User accounts and saved sessions.
- Stronger ML-based vibe classification and recommendations.
- Generative transitions and genre morphing.
- Multiple decks (A/B) and advanced visualizations.
- Integration with licensed audio sources.