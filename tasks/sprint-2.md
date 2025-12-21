# Sprint 2 — Sessions, Queue Management, and Turntable UI

## Goal

Introduce the concept of a session with a current track and queue, and build the proper UI layout:

- Backend:
  - Session model.
  - Queue stored per session.
  - API to get/update session state.
- Frontend:
  - Top bar, turntable, queue layout as described in design.md.
  - Display of current track and queue.
  - Simple spin animation for record (no complex transition logic yet).

---

## 1. Backend: Session & Queue Models

### 1.1 SessionState Model

- [ ] In `/backend/models/session.py`, define:

```py
class SessionStatus(str, Enum):
    idle = "idle"
    loading = "loading"
    playing = "playing"
    transitioning = "transitioning"
    ended = "ended"

class SessionState(BaseModel):
    id: str
    current_track_id: str | None
    queue_track_ids: list[str]
    settings: UserSettings
    status: SessionStatus
```

- [ ] In `/backend/models/settings.py`:

```py
class UserSettings(BaseModel):
    target_genre: str | Literal["auto"] = "auto"
    target_bpm: float | Literal["auto"] = "auto"
    target_energy: Literal["chill", "medium", "hype", "auto"] = "auto"
```

### 1.2 Session Storage

- [ ] In `/backend/storage/sessions.py`, implement:
  - [ ] `SESSIONS: dict[str, SessionState] = {}`
  - [ ] `create_session(initial_track_id: str, settings: UserSettings) -> SessionState`
  - [ ] `get_session(session_id: str) -> SessionState | None`
  - [ ] `update_session(session: SessionState) -> None`
- [ ] Ensure sessions are stored in-memory for now.

---

## 2. Backend: Session APIs

### 2.1 Init Session

- [ ] Replace or extend Sprint 1 endpoint with session logic:
  - [ ] `POST /api/session/init`
    - [ ] Input:
      - `source_url: str`
      - Optional `UserSettings`
    - [ ] Behavior:
      - Download + analyze track (reuse Sprint 1 logic).
      - Create Track and save into `TRACKS`.
      - Create `SessionState`:
        - `current_track_id` = the new track id.
        - `queue_track_ids` = `[]` initially.
        - `settings` = provided or default.
        - `status` = `"playing"` (or `"idle"` if you want manual play).
    - [ ] Return:
      - `session`
      - `currentTrack`
      - `queue` (empty list for now).

### 2.2 Get Session State

- [ ] Implement `GET /api/session/{session_id}`:
  - [ ] Fetch `SessionState`.
  - [ ] Resolve `current_track` from `TRACKS`.
  - [ ] Resolve `queue_tracks` from `TRACKS` using `queue_track_ids`.
  - [ ] Return:

```json
{
  "session": {
    "id": "abcd",
    "status": "playing",
    "settings": { ... },
    "currentTrack": { ... },
    "queue": [ { ... }, { ... } ]
  }
}
```

### 2.3 Update Settings

- [ ] Implement `POST /api/session/{session_id}/settings`:
  - [ ] Input:
    - `UserSettings`
  - [ ] Behavior:
    - Update `session.settings`.
    - (AI logic will use settings in later sprint for real selection).
  - [ ] Output:
    - Updated session.

### 2.4 Dequeue Item (Backend Logic Only)

- [ ] Implement `DELETE /api/session/{session_id}/queue/{track_id}`:
  - [ ] Remove `track_id` from `session.queue_track_ids`.
  - [ ] Save session.
  - [ ] Return updated queue.

---

## 3. Backend: Placeholder AI Queue Filler

- [ ] For this sprint, implement a dummy queue filler (real scoring comes later):
  - [ ] In `dj_engine/selector.py`, implement:

```py
def fill_queue_for_session(session: SessionState, existing_tracks: dict[str, Track], max_queue_size: int = 3) -> None:
    # For now: simple logic
    # - If queue length < max_queue_size:
    #   - Add placeholder or re-use the current track as fake items (just to populate UI).
    ...
```

- [ ] For now, you can:
  - Duplicate the current track with different IDs (or stub tracks).
  - Or create dummy tracks pointing to the same audio for testing.
- [ ] Call this function:
  - After `session/init`.
  - After `DELETE /queue/{track_id}` if you want to ensure min queue size.

---

## 4. Frontend: Real Layout + Components

### 4.1 Global Layout

- [ ] Implement a main layout component that:
  - [ ] Uses CSS grid/flex to create:
    - Left/Center: Turntable (takes ~70–75% width).
    - Right: Queue panel (~25–30% width).
  - [ ] Applies a dark theme and padding.

### 4.2 Top Bar Component

- [ ] Create `TopBar` component:
  - [ ] Shows app name.
  - [ ] Placeholder session info (e.g. Playing / Idle).
  - [ ] Settings button (gear icon; toggles modal state).

### 4.3 Turntable Component (Static Animation)

- [ ] Create `Turntable` component with props:
  - `currentTrack`
  - `isPlaying`
- [ ] UI:
  - [ ] Large circular div for record.
  - [ ] Use `currentTrack.cover_art_url` as a background image inside the circle.
  - [ ] Under the circle:
    - Title and artist.
    - Simple text progress (e.g. `00:00 / 03:33` — can be static for now).
- [ ] Animation:
  - [ ] Add CSS keyframes for a slow rotation.
  - [ ] When `isPlaying` is true, add a class to enable rotation.
  - [ ] When `isPlaying` is false, pause rotation (e.g. using `animation-play-state: paused`).

### 4.4 Queue Panel Component

- [ ] Create `QueuePanel` component:
  - [ ] Props:
    - `queue: Track[]`
    - `onDequeue(trackId: string)`
  - [ ] UI:
    - [ ] Title: "Queue".
    - [ ] Scrollable list area.
    - [ ] Each item:
      - Mini cover image.
      - Title + artist.
      - Remove button (X).
  - [ ] On remove:
    - [ ] Call backend `DELETE /api/session/{session_id}/queue/{track_id}`.
    - [ ] Update local queue state from response.

---

## 5. Frontend: Session Initialization Flow

### 5.1 Starting a Session

- [ ] Replace Sprint 1 `/api/track/from-url` usage with `/api/session/init`.
- [ ] When user enters a URL and clicks "Start Session":
  - [ ] `POST` to `/api/session/init`.
  - [ ] On success:
    - Store:
      - `sessionId`
      - `currentTrack`
      - `queue`
      - `settings`
    - Set playback state to playing.

### 5.2 Polling Session State

- [ ] Implement a simple polling mechanism:
  - [ ] Every N seconds (e.g. 3–5s), call `GET /api/session/{session_id}`.
  - [ ] Update:
    - `currentTrack`
    - `queue`
    - `sessionStatus`
  - [ ] For now, backend session status might not change much; polling is for future behavior as well.

---

## 6. Audio Playback (Still Basic)

- [ ] Continue using HTML `<audio>` or a minimal hook, but:
  - [ ] Use `currentTrack.audio_path` as `src`.
  - [ ] Sync `isPlaying` state to play/pause button.
  - [ ] When `currentTrack` changes, reset audio `src`.
- [ ] No crossfades or transitions yet; track just jumps to the new one when changed.

---

## 7. Definition of Done (Sprint 2)

User can:

- Start a session with a YouTube URL.
- See:
  - Turntable with cover art for the current track.
  - A queue list on the right (dummy tracks are OK for now).
- Dequeue items from the queue (UI and backend).
- See persistent session data via API (`sessionId`, current track, queue).

Turntable:

- Spins when playing.
- Pauses when not playing.

Code:

- Session and queue logic implemented in backend.
- Frontend wired to session APIs, using `sessionId`.

