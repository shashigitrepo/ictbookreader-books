/*
 * Padhaku Animated Science – shared player (books repo animations/player.js; the APK keeps a starter copy).
 *
 * A page has <svg id="scene" viewBox="…">…</svg> and calls Padhaku.animation({...}). Every step says which parts
 * to show (the rest are dimmed), which labels to show, its name and caption in English and Hindi, and an optional
 * tick(p, t) that moves things (p = 0…1 through the step, t = seconds since the step began).
 *
 *   Padhaku.animation({
 *     stepSeconds: 7,
 *     steps: [{ name: {en, hi}, text: {en, hi}, focus: ["mouth"], labels: ["l-mouth"], tick: (p, t) => {...} }]
 *   });
 *
 * In the SVG: class="part" on things that can be dimmed, class="lbl" on labels (text), class="lead" on label lines
 * (give a line the label's id plus "-line" to show it with its label); class="only" on things shown only in the steps
 * that list them in `only`; data-hi="…" on any <text> for Hindi.
 * Helpers: Padhaku.along(el, pathEl, p), Padhaku.flow(group, pathEl, t, speed), Padhaku.pulse(el, t, from, to).
 * The page is opened with ?lang=en|hi&theme=light|dark.
 */
(function () {
  const q = new URLSearchParams(location.search);
  const lang = q.get('lang') === 'hi' ? 'hi' : 'en';
  if (q.get('theme') === 'dark') document.documentElement.classList.add('dark');
  document.documentElement.lang = lang;
  const T = {
    en: { step: 'Step', of: 'of', play: '▶  Play', pause: '❚❚  Pause', again: '↻  Play again' },
    hi: { step: 'चरण', of: '/', play: '▶  चलाएँ', pause: '❚❚  रोकें', again: '↻  फिर से चलाएँ' },
  }[lang];
  const pick = (o) => (o == null ? '' : typeof o === 'string' ? o : (o[lang] || o.en || ''));

  function along(el, path, p) {
    if (!el || !path) return;
    const len = path.getTotalLength();
    const pt = path.getPointAtLength(Math.max(0, Math.min(1, p)) * len);
    el.setAttribute('transform', `translate(${pt.x},${pt.y})`);
  }
  // Moves every child of `group` along the path, spaced evenly and looping: blood cells, air, food, impulses.
  function flow(group, path, t, speed) {
    if (!group || !path) return;
    const kids = group.children; const n = kids.length;
    for (let i = 0; i < n; i++) along(kids[i], path, ((t * (speed || 0.25)) + i / n) % 1);
  }
  function pulse(el, t, from, to, period) {
    if (!el) return;
    const k = (Math.sin((t / (period || 1)) * Math.PI * 2) + 1) / 2;
    el.setAttribute('transform-origin', 'center');
    el.style.transformBox = 'fill-box';
    el.style.transformOrigin = 'center';
    el.style.transform = `scale(${from + (to - from) * k})`;
  }

  function animation(cfg) {
    const steps = cfg.steps || [];
    const stepMs = (cfg.stepSeconds || 7) * 1000;
    const svg = document.getElementById('scene');
    // Hindi labels.
    if (lang === 'hi') svg.querySelectorAll('text[data-hi]').forEach((t) => { t.textContent = t.getAttribute('data-hi'); });
    // Layout: stage + panel.
    const stage = document.createElement('div'); stage.id = 'stage';
    svg.parentNode.insertBefore(stage, svg); stage.appendChild(svg);
    const panel = document.createElement('div'); panel.id = 'panel';
    panel.innerHTML = '<div id="stepno"></div><div id="stepname"></div><div id="caption"></div>' +
      '<div id="controls"><button id="prev" aria-label="back">◀</button><button id="play" class="main"></button>' +
      '<button id="next" aria-label="next">▶</button></div><div id="dots"></div>';
    document.body.appendChild(panel);
    const $ = (id) => document.getElementById(id);
    const dots = $('dots');
    steps.forEach(() => dots.appendChild(document.createElement('span')));

    let index = 0, playing = false, startedAt = performance.now(), pausedAt = 0, done = false;

    function show(i) {
      index = Math.max(0, Math.min(steps.length - 1, i));
      const s = steps[index];
      $('stepno').textContent = `${T.step} ${index + 1} ${T.of} ${steps.length}`;
      $('stepname').textContent = pick(s.name);
      $('caption').textContent = pick(s.text);
      [...dots.children].forEach((d, k) => d.classList.toggle('on', k === index));
      const focus = s.focus || [];
      svg.querySelectorAll('.part').forEach((el) => {
        el.classList.toggle('dim', focus.length > 0 && !focus.includes(el.id) && !focus.some((f) => el.closest('#' + f)));
      });
      const labels = s.labels === 'all' ? null : (s.labels || []);
      svg.querySelectorAll('.lbl').forEach((el) => el.classList.toggle('off', labels !== null && !labels.includes(el.id)));
      svg.querySelectorAll('.lead').forEach((el) => {
        const base = el.id.replace(/-line$/, '');
        el.classList.toggle('off', labels !== null && !labels.includes(base));
      });
      // Parts that appear only in some steps (zoomed views, arrows): class="only", listed in the step's `only`.
      const only = s.only || [];
      svg.querySelectorAll('.only').forEach((el) => el.classList.toggle('hide', !only.includes(el.id)));
      if (s.enter) s.enter();
      startedAt = performance.now(); pausedAt = 0; done = false;
      setButton();
    }
    function setButton() { $('play').textContent = done ? T.again : (playing ? T.pause : T.play); }
    $('prev').onclick = () => { show(index - 1); };
    $('next').onclick = () => { show(index + 1); };
    $('play').onclick = () => {
      if (done) { playing = true; show(0); return; }
      playing = !playing;
      if (playing && pausedAt) startedAt += performance.now() - pausedAt;
      if (!playing) pausedAt = performance.now();
      setButton();
    };

    function frame(now) {
      const elapsed = (playing ? now : (pausedAt || now)) - startedAt;
      const s = steps[index];
      // Movement runs even when paused at the start, so every step shows its motion; Play only advances steps.
      if (s && s.tick) s.tick(Math.min(1, elapsed / stepMs), elapsed / 1000);
      if (playing && elapsed >= stepMs) {
        if (index < steps.length - 1) show(index + 1);
        else { playing = false; done = true; setButton(); }
      }
      requestAnimationFrame(frame);
    }
    show(0);
    requestAnimationFrame(frame);
    // Android WebView may report a height of 0 while the page first loads, which squeezed the drawing to nothing.
    // Size the page from the real window height now and whenever it changes.
    function fit() {
      const h = (window.visualViewport && window.visualViewport.height) || window.innerHeight || document.documentElement.clientHeight;
      if (h > 0) document.body.style.height = h + 'px';
      const free = (h || 0) - panel.offsetHeight - 16;
      stage.style.height = Math.max(240, free) + 'px';
    }
    fit();
    window.addEventListener('resize', fit);
    if (window.visualViewport) window.visualViewport.addEventListener('resize', fit);
    setTimeout(fit, 200); setTimeout(fit, 800);
  }

  window.Padhaku = { animation, along, flow, pulse, lang };
})();
