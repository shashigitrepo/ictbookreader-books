#!/usr/bin/env python3
"""
Builds practicals/<class>/<subject>/practicals.json from the programs in .../src/.

Every program is really run here, and the JSON keeps its true output (the app never shows a
made-up output). Needs Python 3 with pandas + matplotlib + mysql-connector-python, and a local
MySQL/MariaDB server where root's password is "tiger" (the password shown in the programs).

  python3 scripts/practicals/build.py practicals/class-12/computer-science

Source files in src/ (run in name order):
  NN-name.py   Python program. Header lines "#: key: value" (removed from the shown code):
               id, group, title, title_hi, syllabus (yes = from CBSE's suggested list),
               inputs (keyboard input, separated by " | "), files (from src/data/),
               setup (an .sql file in src/data/ run before the program, not shown),
               reset (databases dropped before the run, not shown), note.
  NN-name.sql  SQL set. Header lines "--: key: value" as above. A "-- text" line before a
               statement is that query's question. Run with the mysql client; the shown
               output is the client's own (timings rounded to 0.00 sec).
  meta.json    subject, groups (id, title, title_hi), marks pattern, source.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
WRAP = os.path.join(HERE, "run_wrapped.py")


def header(path, mark):
    meta, body = {}, []
    with open(path, encoding="utf-8") as f:
        for line in f.read().splitlines():
            m = re.match(rf"^{re.escape(mark)}\s*(\w+):\s?(.*)$", line)
            if m and not body:
                meta[m.group(1)] = m.group(2).strip()
            else:
                body.append(line)
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    return meta, "\n".join(body) + "\n"


def run_setup(sql_path):
    with open(sql_path, encoding="utf-8") as f:
        subprocess.run(["mysql", "-uroot", "-ptiger"], stdin=f, check=True)


def run_python(src_dir, path, meta, img_dir, pid):
    _, code = header(path, "#:")
    reset(meta.get("reset", ""))
    if meta.get("setup"):
        run_setup(os.path.join(src_dir, "data", meta["setup"]))
    with tempfile.TemporaryDirectory() as work:
        for name in filter(None, (s.strip() for s in meta.get("files", "").split(","))):
            shutil.copy(os.path.join(src_dir, "data", name), os.path.join(work, name))
        prog = os.path.join(work, "program.py")
        with open(prog, "w", encoding="utf-8") as f:
            f.write(code)
        inputs = [s for s in meta.get("inputs", "").split(" | ")] if meta.get("inputs") else []
        env = dict(os.environ, PRACTICAL_INPUTS=json.dumps(inputs), MPLBACKEND="Agg",
                   PYTHONHASHSEED="0", PYTHONIOENCODING="utf-8")
        r = subprocess.run([sys.executable, WRAP, prog], cwd=work, env=env,
                           capture_output=True, text=True, timeout=120)
        out = r.stdout + r.stderr
        if r.returncode != 0 and "expect_error" not in meta:
            raise SystemExit(f"{path} failed:\n{out}")
        images = []
        for name in sorted(os.listdir(work)):
            if re.match(r"figure-\d+\.png$", name):
                os.makedirs(img_dir, exist_ok=True)
                target = f"{pid}-{len(images) + 1}.png"
                shutil.copy(os.path.join(work, name), os.path.join(img_dir, target))
                images.append(f"img/{target}")
        created = {}
        for name in sorted(os.listdir(work)):
            if name in ("program.py",) or name.endswith(".png") or name.startswith("__"):
                continue
            listed = [s.strip() for s in meta.get("files", "").split(",")]
            p = os.path.join(work, name)
            if os.path.isfile(p) and name.endswith((".txt", ".csv")) and (name not in listed or meta.get("show_files")):
                with open(p, encoding="utf-8", errors="replace") as f:
                    created[name] = f.read()
    files = {}
    for name in filter(None, (s.strip() for s in meta.get("files", "").split(","))):
        p = os.path.join(src_dir, "data", name)
        if name.endswith((".txt", ".csv")):
            with open(p, encoding="utf-8") as f:
                files[name] = f.read()
    return code, out.rstrip() + "\n", images, files, created, inputs


def split_sql(body):
    """[(question, statement)] in order; question = the '-- ' comment lines just before."""
    steps, question, buf = [], [], []
    for line in body.splitlines():
        s = line.strip()
        if not buf and s.startswith("--"):
            question.append(s.lstrip("-").strip())
            continue
        if not s and not buf:
            continue
        buf.append(line)
        if s.endswith(";"):
            steps.append((" ".join(question).strip(), "\n".join(buf).strip()))
            question, buf = [], []
    return steps


def reset(databases):
    """Drops the listed databases first (not shown), so every set starts from nothing."""
    for db in filter(None, (d.strip() for d in databases.split(","))):
        subprocess.run(["mysql", "-uroot", "-ptiger", "-e", f"DROP DATABASE IF EXISTS `{db}`"], check=True)


def run_sql(path):
    h, body = header(path, "--:")
    reset(h.get("reset", ""))
    steps = split_sql(body)
    script = "\n".join(stmt for _, stmt in steps) + "\n"
    r = subprocess.run(["mysql", "-uroot", "-ptiger", "-t", "-vvv", "--force"], input=script,
                       capture_output=True, text=True)
    text = r.stdout
    blocks = re.split(r"^-{14}\n", text, flags=re.M)
    # blocks: ['', stmt, result, stmt, result, ...]
    echoed = []
    i = 1
    while i + 1 < len(blocks):
        echoed.append(blocks[i + 1])
        i += 2
    # The client runs USE itself without echoing it; on screen it prints "Database changed".
    results = []
    for _, stmt in steps:
        if re.match(r"(?i)^use\s", stmt):
            results.append("Database changed\n")
        else:
            results.append(echoed.pop(0) if echoed else "")
    if echoed or len(results) != len(steps):
        raise SystemExit(f"{path}: {len(steps)} statements but {len(results)} results\n{text}\n{r.stderr}")
    errors = [re.sub(r" at line \d+:", ":", l) for l in r.stderr.splitlines() if l.startswith("ERROR")]
    out_steps, transcript = [], []
    err_i = 0
    for (q, stmt), res in zip(steps, results):
        res = re.sub(r"\((\d+)\.\d+ sec\)", "(0.00 sec)", res)
        res = re.sub(r"^Bye\s*$", "", res, flags=re.M).strip("\n")
        if not res.strip() and err_i < len(errors):
            res = errors[err_i]
            err_i += 1
        out_steps.append({"question": q, "sql": stmt, "result": res})
        transcript.append(f"mysql> {stmt}\n{res}\n")
    return body, steps, out_steps, "\n".join(transcript)


def main(subject_dir):
    src = os.path.join(subject_dir, "src")
    with open(os.path.join(src, "meta.json"), encoding="utf-8") as f:
        meta = json.load(f)
    img_dir = os.path.join(subject_dir, "img")
    if os.path.isdir(img_dir):
        shutil.rmtree(img_dir)
    practicals = []
    for name in sorted(os.listdir(src)):
        path = os.path.join(src, name)
        if name.endswith(".py"):
            h, _ = header(path, "#:")
            code, out, images, files, created, inputs = run_python(src, path, h, img_dir, h["id"])
            kind = h.get("type", "python")
            item = {"id": h["id"], "group": h["group"], "type": kind, "title": h["title"],
                    "title_hi": h.get("title_hi", ""), "syllabus": h.get("syllabus") == "yes",
                    "code": code, "inputs": inputs, "output": out}
            if files:
                item["inputFiles"] = files
            if created:
                item["outputFiles"] = created
            if images:
                item["images"] = images
        elif name.endswith(".sql"):
            h, _ = header(path, "--:")
            body, steps, out_steps, transcript = run_sql(path)
            item = {"id": h["id"], "group": h["group"], "type": "sql", "title": h["title"],
                    "title_hi": h.get("title_hi", ""), "syllabus": h.get("syllabus") == "yes",
                    "code": "\n\n".join(s for _, s in steps) + "\n", "steps": out_steps,
                    "output": transcript}
        else:
            continue
        if h.get("note"):
            item["note"] = h["note"]
        practicals.append(item)
        print(f"ok {item['id']:10} {item['type']:10} {item['title'][:60]}")
    ids = [p["id"] for p in practicals]
    assert len(ids) == len(set(ids)), "duplicate ids"
    groups = {g["id"] for g in meta["groups"]}
    for p in practicals:
        assert p["group"] in groups, f"{p['id']}: unknown group {p['group']}"
    meta = dict(meta)
    meta["practicals"] = practicals
    with open(os.path.join(subject_dir, "practicals.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"{len(practicals)} practicals → {subject_dir}/practicals.json")


if __name__ == "__main__":
    main(sys.argv[1])
