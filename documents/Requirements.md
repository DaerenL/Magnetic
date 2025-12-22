# AI DJ Remixing Website — Requirements

## 1. Project Vision
Build an AI-powered DJ/remixing website that:
- Feels like a live DJ controlling a continuous set.
- Lets the user pick an initial track and vibe/genre settings.
- Uses AI to analyze songs, select the next tracks, and blend/transform them so the playlist feels cohesive.

This is a learning project focused on audio processing, AI logic, and full-stack development. The architecture should remain scalable for future upgrades.

## 2. Core Experience (User Interface)

### 2.1 One-Page UI
The app is a single-page interface. Layout (desktop-first):

1. Top Bar
   - Left: App logo/name placeholder.
   - Center: Session status (e.g., “Session Live”, BPM, mode).
   - Right: Settings icon (gear) that opens a modal or slide-over panel.

2. Center: Turntable Area
   - Large turntable with a spinning record representing the current track.
   - Record uses the track’s cover art stretched/cropped into a circle.
   - Optional subtle vinyl grooves.
   - Track metadata displayed nearby (title, artist, progress bar).
   - Playback controls (play/pause, skip).
   - Transition animation when switching songs:
     - Record speeds up briefly.
     - Old record fades/slides/scales out.
     - New record replaces it and resumes slow spin.

3. Right Side: Queue Panel
   - Vertical list of upcoming tracks selected by the AI.
   - Each queued track includes:
     - Mini cover thumbnail.
     - Title and artist.
     - Optional BPM or vibe tag.
   - User can dequeue/remove any track.
   - Smooth removal animations.

### 2.2 Settings Panel
Accessible via the top-right gear icon. Contains:
- Target genre (dropdown).
- Target BPM (slider or numeric input, with Auto mode).
- Target energy (chill → medium → hype slider).
- Future: Transition style toggle (smooth vs chaotic).

Settings influence AI track selection and vibe transformation.

## 3. Functional Requirements

### 3.1 Track Source & Ingestion
- Primary dev source: YouTube audio via yt-dlp (local/educational use).
- System must:
  - Accept YouTube URLs or search input.
  - Use yt-dlp to download audio.
  - Extract metadata (title, artist/channel, cover art from thumbnail).
  - Store downloaded audio locally (temporary).
- Architecture must allow future support for local uploads or licensed platforms.

### 3.2 Audio Analysis
For each track, compute and store:
- Title, artist, coverArtUrl, duration.
- BPM/tempo.
- Key (optional but planned).
- Energy (loudness, RMS, dynamics).
- Brightness (spectral centroid).
- Approximate vibe/mood (optional ML later).

### 3.3 AI DJ Engine
Responsible for:
1. Maintaining session state.
2. Selecting the next tracks.
3. Respecting user settings.
4. Optionally modifying track vibe.

#### 3.3.1 Track Selection Logic
Input:
- Current track features.
- User settings.
- Pool of candidate tracks.

Behavior:
- Filter/score tracks based on:
  - BPM similarity to target or current.
  - Energy similarity.
  - Genre/vibe match.
  - Optional: key compatibility.
- Output:
  - Ordered next N tracks (queue).

Implementation phases:
- Phase 1: Rule-based scoring (feature-weighted).
- Phase 2: ML-enhanced transition quality prediction.

#### 3.3.2 Vibe Transformation
Small modifications to match target vibe.

Must-Have:
- Tempo adjustments (±5–10%).
- Basic EQ curves:
  - Techno: boost lows/highs.
  - Chill: soften highs.
  - Hype: boost clarity + loudness.
- Loudness normalization.

Nice-to-Have:
- Filter sweeps.
- Echo/reverb stabs.
- Sidechain effects.
- Section-aware transitions.

Long-Term:
- Generative AI (drums, genre morphing, AI transition segments).

### 3.4 Mixing & Playback
Must support continuous playback with transitions:
- Play current track.
- Prepare next track.
- Crossfade between tracks.
- Beatmatch based on BPM.
- Sync turntable UI with audio engine.

Transition types:
- Crossfade only.
- Crossfade + tempo match.
- Effects during transitions (optional).

Implementation approaches:
- Backend mixing: server handles DSP and provides audio stream.
- Frontend mixing: Web Audio API handles scheduling/mixing.

### 3.5 Queue Management
- AI maintains ordered queue of upcoming tracks.
- Queue displayed in right panel.
- User can remove queued tracks.
- AI refills queue when low (< 3).
- AI respects manual removals.

### 3.6 User Interactions
- Provide starting track.
- Play/pause.
- Skip track.
- Remove queued tracks.
- Adjust settings.
- Settings influence future selections and vibe matching.

## 4. Non-Functional Requirements
- Should remain simple enough for a small team vibecoding.
- Components should stay modular.
- UI must be responsive and smooth.
- Heavy processing should be off UI thread.
- yt-dlp usage restricted to private/local development.
- Public versions must remove or replace YouTube ingestion.
- Architecture should stay flexible for future AI and audio expansions.

## 5. Data & API Guidelines

### 5.1 Track Object
```ts
interface Track {
  id: string;
  title: string;
  artist: string;
  sourceUrl: string;
  audioPath: string;
  coverArtUrl: string;
  bpm: number | null;
  key?: string | null;
  energy: number | null;
  brightness?: number | null;
  genreTag?: string;
    durationSeconds?: number;
}
```

### 5.2 Queue

```ts
interface QueueItem {
  track: Track;
  position: number;
}

type Queue = QueueItem[];
```

### 5.3 User Settings

```ts
interface UserSettings {
  targetGenre: string | "auto";
  targetBpm: number | "auto";
    targetEnergy: "chill" | "medium" | "hype" | "auto";
}
```

### 5.4 AI Selection Function

```ts
function chooseNextTracks({
  currentTrack,
  queue,
  library,
    settings,
}): { updatedQueue: Queue }
```

---

## 6. Tech Stack Guidelines

- **Frontend:** React / Next.js / Vite, TailwindCSS, Web Audio API.
- **Backend:** Python (FastAPI/Flask) or Node.js.
- **Audio tools:** yt-dlp, ffmpeg, librosa, pydub.

**Project structure:**
- `/frontend`
- `/backend`
- `/docs/requirements.md`

---

## 7. Milestones (High-Level)

1. Download and analyze a track.
2. Turntable UI + static queue.
3. Real queue + AI track selection.
4. DSP transitions + vibe settings.
5. Vibe transformation + UI polish.

---

## 8. Non-Goals (Initial Version)

User accounts, cloud deployment, perfect DJ transitions, key modulation, mobile-first design, full generative remixing.


If you want this converted into a `project.yaml` or broken into separate reference files for Cursor, just tell me!
