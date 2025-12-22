# Sprint 4 — Vibe Settings, Basic DSP, and Polish

## Goal

Wire the settings panel into the AI behavior and add basic DSP-based vibe transformations, plus UI polish:

- Settings (genre/BPM/energy) actually influence track selection.
- Simple EQ-style and tempo adjustments are applied server-side.
- Turntable and queue feel cohesive and minimal but polished.

---

## 1. Backend: Settings-Driven Behavior

### 1.1 Ensure Settings Are Used in Scoring

- [ ] Update `score_candidate` to fully respect `UserSettings`:
  - [ ] If `target_bpm` is a number:
    - BPM similarity is measured against this number.
  - [ ] If `target_bpm == "auto"`:
    - BPM similarity uses current track BPM.
  - [ ] Map `target_energy` to numeric target:
    - `chill` ~ 0.3
    - `medium` ~ 0.6
    - `hype` ~ 0.85
    - `auto` uses current track energy.
  - [ ] If `target_genre` is not `"auto"`:
    - Give extra score if candidate's `genre_tag` matches this string (even if genre_tag is rough or manually set).
- [ ] Tune weights `w1`, `w2`, `w3`, `w4` as constants.

### 1.2 Settings Update Endpoint Behavior

- [ ] When `POST /session/{id}/settings` is called:
  - [ ] Save new settings.
  - [ ] Optionally:
    - Recompute queue using `fill_queue_for_session`.
  - [ ] Return:
    - Updated session (with new queue).

---

## 2. Backend: Basic DSP Vibe Matching

### 2.1 Tempo Adjustment (Conceptual Implementation)

- [ ] Implement a helper in `mixing/dsp.py`:

```py
def adjust_tempo(audio: AudioSegment, original_bpm: float | None, target_bpm: float | None) -> AudioSegment:
    # If either BPM is None or difference is tiny, return audio unchanged.
    # Otherwise compute rate change and adjust:
    # new_rate = original_rate * (target_bpm / original_bpm)
    ...
```

- [ ] Use pydub with speedup or custom resampling if needed.
- [ ] For Sprint 4, you can:
  - Apply tempo adjustment only for small BPM differences (e.g. <10–15%).

### 2.2 Simple EQ Curves by Vibe

- [ ] Implement `apply_vibe_eq(audio: AudioSegment, target_energy: str) -> AudioSegment`:
  - [ ] For `chill`:
    - Slightly reduce high frequencies (low-pass feel).
  - [ ] For `medium`:
    - Minimal changes.
  - [ ] For `hype`:
    - Slightly increase highs (high-shelf feel) and maybe overall gain.
- [ ] Simplify:
  - Since pydub has limited built-in EQ, either:
    - Use basic filters if available, or
    - Approximate via volume adjustments on band-limited versions if you implement them.
- [ ] For Sprint 4, it's acceptable if DSP is simple but consistent.

### 2.3 Integrating DSP into Mixing or Audio Export

- [ ] Decide when to apply DSP per track:
  - [ ] Option A (simpler): Preprocess each track once when added to a session, based on current settings.
  - [ ] Option B (more dynamic): Apply adjustments during transition mixing per track.
- [ ] For Sprint 4, choose Option A:
  - [ ] After track is chosen for a session and before playback:
    - Load audio.
    - Apply `adjust_tempo` (if needed).
    - Apply `apply_vibe_eq`.
    - Save processed audio to a separate file path (e.g. `/data/processed/<session_id>/<track_id>.mp3`).
  - [ ] Update `audio_path` in context of this session to processed file.

---

## 3. Frontend: Settings Panel Wiring

### 3.1 Settings State

- [ ] In frontend global state:
  - [ ] Maintain `settings` object.
- [ ] `SettingsModal`:
  - [ ] Displays:
    - Dropdown for `targetGenre`.
    - Numeric/slider for `targetBpm`.
    - Slider or select for `targetEnergy`.
  - [ ] On save:
    - Update local state.
    - Call `POST /session/{sessionId}/settings` with the new settings.
    - Replace queue from response.

### 3.2 Feedback in UI

- [ ] Show currently active settings in:
  - [ ] Top bar text (e.g. "Mode: Techno / 130 BPM / Hype").
- [ ] Optionally color-code or tag queue items to reflect approximate vibe match.

---

## 4. Frontend: Turntable & Queue Polish

### 4.1 Turntable Visual Polish

- [ ] Improve the turntable visuals:
  - [ ] Add subtle shadow around record.
  - [ ] Add a "label" circle at the center (using cover art).
  - [ ] Keep overall design minimal and clean.
- [ ] Ensure:
  - [ ] Record always fills a nice portion of the screen (but not overflowing).
  - [ ] On very long titles, truncate with ellipsis and show full title on hover.

### 4.2 Queue UX Polish

- [ ] Add hover effect for queue items (slight scale or background change).
- [ ] When user clicks remove:
  - [ ] Queue item animates out smoothly.
- [ ] Display small text for BPM next to each track (if available).

---

## 5. Error Handling & Edge Cases

### 5.1 Frontend

- [ ] Display user-friendly error messages:
  - [ ] Invalid YouTube URL.
  - [ ] Backend error downloading/processing.
- [ ] If `currentTrack` is null:
  - [ ] Show a "No track loaded" message or prompt to start session.

### 5.2 Backend

- [ ] Wrap `yt-dlp` and analysis in try/except:
  - [ ] Return 4xx/5xx with clear error JSON if something fails.
- [ ] Validate `session_id` on each session endpoint:
  - [ ] Return 404-style error if not found.

---

## 6. Definition of Done (Sprint 4)

Settings (genre/BPM/energy) visibly affect queue composition (AI picks different tracks depending on settings).

Basic DSP applied:

- Tempo adjustments for moderate BPM differences.
- Simple EQ differences for chill/medium/hype.

Turntable and queue are visually clean and minimal, but polished enough to demo.

Errors are handled gracefully both on frontend and backend.

Overall experience:

User can:

- Start session.
- See a nice turntable.
- View/remove queue items.
- Skip tracks.
- Change settings and feel some difference in behavior.

