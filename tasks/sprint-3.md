# Sprint 3 — AI Track Selection & Basic Transitions

## Goal

Implement initial AI-like track selection for the queue and basic backend-driven transitions between tracks:

- Backend:
  - Real (but still simple) rule-based track selection logic using audio features.
  - Crossfade mixing to create seamless transitions.
  - Skip endpoint to trigger transitions.
- Frontend:
  - Skip button wired to backend.
  - Turntable transition animation (speed up on change).
  - UI updates smoothly when track changes.

---

## 1. Backend: Track Library & Candidates

### 1.1 Candidate Acquisition (Simplified)

- [ ] Decide how to get candidate tracks for now:
  - [ ] Option 1 (simple): user manually adds a few URLs via an extra endpoint.
  - [ ] Option 2 (slightly more automated): a separate script populates a small library of YouTube URLs in config.
- [ ] Implement a helper (`storage/tracks.py` or a new module) that:
  - [ ] Keeps a small list of preconfigured YouTube URLs as the "library".
  - [ ] For missing library tracks, on first request:
    - Download + analyze similarly to Sprint 1.
    - Save to `TRACKS`.

---

## 2. Backend: AI Selection (Rule-Based)

### 2.1 Feature Extensions (Optional but Recommended)

- [ ] Extend `Track` model to include:
  - `energy: float | None`
  - `brightness: float | None`
- [ ] In `audio/analysis.py`, compute:
  - [ ] Energy:
    - Use RMS or loudness: `librosa.feature.rms` → normalized value.
  - [ ] Brightness:
    - Use spectral centroid: `librosa.feature.spectral_centroid` → averaged → normalized.

### 2.2 Scoring Function

- [ ] In `dj_engine/selector.py`, implement:

```py
def score_candidate(
    current: Track,
    candidate: Track,
    settings: UserSettings,
) -> float:
    # 1. BPM similarity
    # 2. Energy similarity
    # 3. Genre match
    # 4. Vibe similarity (brightness/energy)
```

- [ ] Design the scoring:
  - [ ] BPM similarity:
    - If `settings.target_bpm` is numeric:
      - Score by closeness to target BPM.
    - Else:
      - Score by closeness to current track BPM.
  - [ ] Energy:
    - Map `settings.target_energy` (chill, medium, hype) to numeric targets (e.g. 0.3, 0.6, 0.9).
    - Score by distance to target.
  - [ ] Genre:
    - If `settings.target_genre != "auto"` and candidate `genre_tag` is not implemented:
      - Use simple heuristics from title or just give neutral score for now.
  - [ ] Vibe:
    - Use brightness and energy difference from current track.

### 2.3 fill_queue_for_session Implementation

- [ ] Overwrite placeholder `fill_queue_for_session` to a real implementation:
  - [ ] Input:
    - `session: SessionState`
    - `existing_tracks: dict[str, Track]`
    - `max_queue_size: int = 3`
  - [ ] Behavior:
    - If `current_track_id` is None, do nothing.
    - From library tracks, exclude:
      - Current track.
      - Already in queue.
    - For each candidate:
      - Compute `score_candidate`.
    - Sort by score desc.
    - Add top candidates to fill `queue_track_ids` until `max_queue_size`.
  - [ ] Call this function:
    - After `session/init`.
    - After dequeues.
    - After skips (if queue drops below desired size).

---

## 3. Backend: Skip & Transition Logic (Audio-Level)

### 3.1 Skip Endpoint

- [ ] Implement `POST /api/session/{session_id}/skip`:
  - [ ] Input: none.
  - [ ] Behavior:
    - If queue is empty:
      - Option 1: Set status to `ended`.
      - Option 2: Refill queue and pick new.
    - Else:
      - Take first queue track as `next_track_id`.
      - Remove it from queue.
      - Create a transition (see 3.2).
      - Update `current_track_id` → `next_track_id`.
      - Refill queue if needed.
  - [ ] Output:
    - Updated session, currentTrack, queue.

### 3.2 Crossfade Implementation

- [ ] Implement function `create_transition_segment(track_a: Track, track_b: Track, transition_seconds: float) -> str` in `mixing/engine.py`:
  - [ ] Load `track_a.audio_path` and `track_b.audio_path` using `pydub.AudioSegment` or similar.
  - [ ] Choose segments:
    - Tail of `track_a` = last `transition_seconds`.
    - Head of `track_b` = first `transition_seconds`.
  - [ ] Crossfade:
    - Use built-in `audio_a.append(audio_b, crossfade=transition_ms)` if using pydub.
  - [ ] Export a new mixed audio file or define segments to be played sequentially.
- [ ] For Sprint 3:
  - [ ] Simpler approach:
    - No pre-generated mixed file:
      - Just instant-switch audio on frontend.
    - But expose transition info for frontend to use for animation:
      - E.g., flag `transitioning` state during skip.
  - [ ] Note: If pre-mixing is too heavy for now, you can delay actual audio crossfade to Sprint 4 and only implement UI-level transitions in Sprint 3.

---

## 4. Frontend: Skip + Transitions

### 4.1 Skip Button Wiring

- [ ] Add a Skip button near the turntable controls.
- [ ] On click:
  - [ ] Call `POST /api/session/{session_id}/skip`.
  - [ ] Immediately:
    - Set a local `transitioning` flag to true.
    - Optionally disable skip button until response.
  - [ ] On response:
    - Update `currentTrack` and `queue` from response.
    - Clear `transitioning` flag.

### 4.2 Turntable Transition Animation

- [ ] In `Turntable` component:
  - [ ] Accept props:
    - `isPlaying`
    - `isTransitioning`
    - `trackChangeKey` (e.g. `currentTrack.id` to trigger animation resets).
  - [ ] Implement animations:
    - [ ] Normal spin:
      - When `isPlaying` is true and `isTransitioning` is false.
    - [ ] On `isTransitioning`:
      - Temporarily increase the rotation speed CSS class.
      - For example:
        - Apply a different animation with shorter duration.
    - [ ] Once transition is done (after some timeout or when new track id is set):
      - Back to normal spin with new cover art.

### 4.3 Audio Switch Behavior

- [ ] When `currentTrack.id` changes:
  - [ ] Update `<audio src>` to new `audio_path`.
  - [ ] Reset `currentTime` to 0.
  - [ ] If `isPlaying` is true:
    - Auto-play the new track.

---

## 5. Polling Refinements

- [ ] Update polling from Sprint 2 so that:
  - [ ] Poll interval can be adjusted (e.g. 2s).
  - [ ] When session status is `ended`, stop polling.
- [ ] Use session status to:
  - [ ] Display a "Session ended / No more tracks" message if applicable.

---

## 6. Definition of Done (Sprint 3)

Backend:

- Has a small track library.
- Implements rule-based AI selection.
- Fills queue based on feature scores.
- Supports `POST /skip` to move to the next track and update session state.

Frontend:

- Skip button triggers backend skip.
- On track change:
  - Turntable does a visible "transition" animation (spin-up then change).
  - Audio switches to the new track.
  - Queue visually updates and remains accurate.

System:

- Feels like an AI choosing at least somewhat reasonable next tracks from the limited library.

