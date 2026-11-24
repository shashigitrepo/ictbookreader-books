# Animated Science (Padhaku app 111+112)

Moving diagrams of body systems and science processes, shown in the app under Fun Learning Zone → Animated Science
(and Study tab). Everything here reaches phones **without an app update**.

- `index.json` – the list. Bump `version` whenever you change it. `files` gives every file a version number: raise a
  file's number when you change that file, so phones download it again. `items` = one entry per animation:
  `id`, `grade` (6–12, 0 = all), `subject`, `chapter`, `chapter_title`/`_hi`, `title`/`title_hi`, `summary`/`summary_hi`,
  `file`, `order`, `new` (NEW badge), `colors` (two hex colours), `icon` (digestion, lungs, heart, kidney, nerve, eye,
  light, electricity, plant, earth, atom), `enabled` (false hides it).
- `player.js` / `player.css` – the shared player (Play/Pause, ◀ ▶ steps, captions in English/Hindi, light/dark).
- One `.html` page per animation: an inline `<svg id="scene">` (our own drawing) + `Padhaku.animation({ steps: [...] })`.
  Each step has `name` and `text` in `en`/`hi`, `focus` (parts shown bright), `labels`, optional `only` and a `tick`
  that moves things. See `digestive-system.html` as the model. `<text data-hi="…">` gives the Hindi label.
- Only our own drawings and text (owner's licence rule). Facts and terms follow the current NCERT book (EN + HI).

The app (Remote Config `animations_url`) reads `animations/index.json` from this repo; the APK carries a starter copy.
Full planned list (76 + geography): docs/animations/PLAN.md in the app repo.
