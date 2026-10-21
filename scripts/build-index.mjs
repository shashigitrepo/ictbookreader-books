#!/usr/bin/env node
// Writes index.json: the books in this repository in the Padhaku app's catalogue format.
// The app downloads it on every start, so files uploaded here appear without an app update.
// Runs automatically on every push (.github/workflows/build-index.yml); no dependencies.
//
// Layout: <section>/<subject>[/<book>]/NN-chapter-title.pdf, and chapter-wise material in
// solutions/, notes/ and teacher-notes/: <folder>/class-N/<subject>[/<book>]/NN-chapter-title.pdf, where
// <subject> is one of scripts/subjects.json and NN is the textbook's chapter number. See README.md.
import { existsSync, readFileSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import { join, relative, sep } from 'node:path';

const ROOT = new URL('..', import.meta.url).pathname;
const BASE_URL = 'https://raw.githubusercontent.com/shashigitrepo/ictbookreader-books/main/';

const FILE_PATTERN = /^(\d\d)([a-z]?)-([a-z0-9]+(?:-[a-z0-9]+)*)\.pdf$/;
const FOLDER_PATTERN = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const SMALL_WORDS = new Set(['a', 'an', 'and', 'as', 'at', 'by', 'for', 'in', 'of', 'on', 'or', 'the', 'to', 'with', 'using']);
const ACRONYMS = new Set(['ict', 'it', 'ites', 'html', 'css', 'ai', 'ncert', 'cbse', 'scert', 'evs', 'pdf']);

const titleCase = (slug) => slug.split('-').map((word, i) => {
  if (ACRONYMS.has(word)) return word.toUpperCase();
  if (i > 0 && SMALL_WORDS.has(word)) return word;
  return word.charAt(0).toUpperCase() + word.slice(1);
}).join(' ');

const readInfo = (folder) => {
  const path = join(ROOT, folder, 'info.json');
  return existsSync(path) ? JSON.parse(readFileSync(path, 'utf8')) : {};
};

const walk = (dir) => readdirSync(dir).flatMap((name) => {
  if (name.startsWith('.') || name === 'scripts') return [];
  const full = join(dir, name);
  return statSync(full).isDirectory() ? walk(full) : [relative(ROOT, full).split(sep).join('/')];
});

// Notes belong to the class subjects of the app (scripts/subjects.json, made from its catalogue).
const NOTES_SECTIONS = {
  solutions: { type: 'solutions', label: 'NCERT Solutions', order: 50 },
  notes: { type: 'notes', label: 'Notes', order: 100 },
  'teacher-notes': { type: 'teacher_notes', label: 'Teacher Notes', order: 200 },
};
const SUBJECTS = JSON.parse(readFileSync(join(ROOT, 'scripts', 'subjects.json'), 'utf8'));

const errors = [];
const folders = new Map();
for (const path of walk(ROOT)) {
  if (!path.endsWith('.pdf')) continue;
  const parts = path.split('/');
  const file = parts.pop();
  if (NOTES_SECTIONS[parts[0]]) {
    const [section, classFolder, subjectFolder] = parts;
    if (parts.length < 3 || parts.length > 4) {
      errors.push(`${path}: put notes in ${section}/class-N/<subject>/ or ${section}/class-N/<subject>/<book>/`);
      continue;
    }
    if (!SUBJECTS[classFolder]) {
      errors.push(`${path}: "${classFolder}" must be class-6 … class-12`);
      continue;
    }
    if (!SUBJECTS[classFolder][subjectFolder]) {
      errors.push(`${path}: "${subjectFolder}" is not a subject of ${classFolder}. Use one of: ${Object.keys(SUBJECTS[classFolder]).join(', ')}`);
      continue;
    }
  } else if (parts.length < 2 || parts.length > 3) {
    errors.push(`${path}: put PDFs in <section>/<subject>/ or <section>/<subject>/<book>/`);
    continue;
  }
  const bad = parts.find((p) => !FOLDER_PATTERN.test(p));
  if (bad) errors.push(`${path}: folder name "${bad}" may only use lowercase letters, digits and hyphens`);
  if (!FILE_PATTERN.test(file)) errors.push(`${path}: file name must look like 01-chapter-title.pdf`);
  const folder = parts.join('/');
  if (!folders.has(folder)) folders.set(folder, []);
  folders.get(folder).push(file);
}

const grades = new Map();
const subjects = new Map();
const books = [];
const byPath = ([a], [b]) => a.localeCompare(b, 'en', { numeric: true });
for (const [folder, names] of [...folders].sort(byPath)) {
  if (NOTES_SECTIONS[folder.split('/')[0]]) {
    books.push(notesBook(folder, names));
    continue;
  }
  const [top, subjectFolder, bookFolder] = folder.split('/');
  const gradeMatch = /^grade-(\d+)$/.exec(top);
  if (gradeMatch && !(Number(gradeMatch[1]) >= 6 && Number(gradeMatch[1]) <= 12)) {
    errors.push(`${folder}: classes go from grade-6 to grade-12`);
    continue;
  }
  const gradeId = gradeMatch ? `g${gradeMatch[1]}` : top;
  if (!gradeMatch && !grades.has(gradeId)) {
    // Any other top-level folder is a section of its own on the home screen, e.g. cyber-safety.
    const sectionInfo = readInfo(top);
    grades.set(gradeId, { id: gradeId, title: sectionInfo.title ?? titleCase(top), order: sectionInfo.order ?? 100, kind: 'collection' });
  }
  const info = readInfo(folder);
  const subjectId = `${gradeId}-${subjectFolder}`;
  const subjectName = info.subject ?? titleCase(subjectFolder);
  if (!subjects.has(subjectId)) {
    subjects.set(subjectId, {
      id: subjectId,
      gradeId,
      name: subjectName,
      order: info.order ?? 50,
      medium: info.medium ?? 'en',
      ...(gradeMatch ? { productKey: subjectFolder.replaceAll('-', '_') } : {}),
    });
  }
  const bookId = bookFolder ? `${subjectId}-${bookFolder}` : subjectId;
  const defaultTitle = bookFolder ? titleCase(bookFolder) : gradeMatch ? `${subjectName} – Class ${gradeMatch[1]}` : subjectName;
  const chapters = names.filter((n) => FILE_PATTERN.test(n)).sort().map((name, i) => {
    const [, digits, letter, rest] = FILE_PATTERN.exec(name);
    const number = Number(digits);
    return {
      id: `${bookId}-${digits}${letter}`,
      title: info.chapters?.[name] ?? titleCase(rest),
      order: i + 1,
      source: { type: 'remote', url: `${BASE_URL}${folder}/${name}` },
      ...(number >= 1 && number <= 98 && !letter ? { number } : {}),
    };
  });
  books.push({
    id: bookId,
    gradeId,
    subjectId,
    title: info.title ?? defaultTitle,
    order: info.bookOrder ?? books.filter((b) => b.subjectId === subjectId).length + 1,
    publisher: info.publisher ?? 'Padhaku',
    medium: info.medium ?? 'en',
    ...(info.section ? { section: info.section } : {}),
    chapters,
  });
}

/** Notes of one subject (or one book of it): listed in the class subject, not as a section of its own. */
function notesBook(folder, names) {
  const [section, classFolder, subjectFolder, bookFolder] = folder.split('/');
  const { type, label, order } = NOTES_SECTIONS[section];
  const number = classFolder.slice('class-'.length);
  const subjectId = `g${number}-${subjectFolder}`;
  const info = readInfo(folder);
  const bookId = `${subjectId}-${section}${bookFolder ? `-${bookFolder}` : ''}`;
  const subjectName = SUBJECTS[classFolder][subjectFolder];
  return {
    id: bookId,
    gradeId: `g${number}`,
    subjectId,
    title: info.title ?? `${bookFolder ? titleCase(bookFolder) : subjectName} – ${label}`,
    order: info.bookOrder ?? order + books.filter((b) => b.subjectId === subjectId).length,
    publisher: info.publisher ?? 'Padhaku',
    medium: info.medium ?? 'en',
    type,
    chapters: names.filter((n) => FILE_PATTERN.test(n)).sort().map((name, i) => {
      const [, digits, letter, rest] = FILE_PATTERN.exec(name);
      const chapter = Number(digits);
      return {
        id: `${bookId}-${digits}${letter}`,
        title: info.chapters?.[name] ?? titleCase(rest),
        order: i + 1,
        source: { type: 'remote', url: `${BASE_URL}${folder}/${name}` },
        // 05a, 05b… are extra notes for chapter 5, so they keep its number.
        ...(chapter >= 1 && chapter <= 98 ? { number: chapter } : {}),
      };
    }),
  };
}

// YouTube lessons: videos.csv at the top of this repository, one row per video:
// class,subject,chapter,title,url  e.g.  10,science,1,Chemical reactions – part 1,https://youtu.be/…
// chapter may be empty for a video about the whole subject. The app shows them under Videos and
// as a Video button on that textbook chapter.
const videos = [];
const VIDEO_URL = /^https:\/\/(www\.|m\.)?(youtube\.com|youtu\.be)\//;
const parseCsvLine = (line) => {
  const cells = [];
  let cell = '';
  let quoted = false;
  for (let i = 0; i < line.length; i++) {
    const c = line[i];
    if (quoted) {
      if (c === '"' && line[i + 1] === '"') { cell += '"'; i++; } else if (c === '"') quoted = false; else cell += c;
    } else if (c === '"') quoted = true;
    else if (c === ',') { cells.push(cell); cell = ''; } else cell += c;
  }
  cells.push(cell);
  return cells.map((v) => v.trim());
};
const videosFile = join(ROOT, 'videos.csv');
if (existsSync(videosFile)) {
  const lines = readFileSync(videosFile, 'utf8').replace(/^\uFEFF/, '').split(/\r?\n/);
  lines.forEach((line, i) => {
    if (i === 0 || !line.trim()) return; // header
    const row = i + 1;
    const [klass, subject, chapter, title, url] = parseCsvLine(line);
    const classFolder = `class-${klass}`;
    if (!SUBJECTS[classFolder]) return errors.push(`videos.csv row ${row}: class must be 6 … 12`);
    if (!SUBJECTS[classFolder][subject]) {
      return errors.push(`videos.csv row ${row}: "${subject}" is not a subject of class ${klass}. Use one of: ${Object.keys(SUBJECTS[classFolder]).join(', ')}`);
    }
    if (chapter && !/^\d{1,2}$/.test(chapter)) return errors.push(`videos.csv row ${row}: chapter must be a number or empty`);
    if (!title) return errors.push(`videos.csv row ${row}: title is empty`);
    if (!VIDEO_URL.test(url ?? '')) return errors.push(`videos.csv row ${row}: url must be a YouTube link (https://youtu.be/… or https://www.youtube.com/…)`);
    videos.push({
      gradeId: `g${klass}`,
      subjectId: `g${klass}-${subject}`,
      ...(chapter ? { chapter: Number(chapter) } : {}),
      title,
      url,
    });
  });
}

if (errors.length) {
  console.error(`Fix these first:\n  ${errors.join('\n  ')}`);
  process.exit(1);
}

// Solutions are listed apart from the books: app versions that do not know them ignore the list.
const solutions = books.filter((b) => b.type === 'solutions');
const index = {
  version: 1,
  grades: [...grades.values()],
  subjects: [...subjects.values()],
  books: books.filter((b) => b.type !== 'solutions'),
  solutions,
  videos,
};
writeFileSync(join(ROOT, 'index.json'), JSON.stringify(index, null, 2) + '\n');
const count = books.reduce((n, b) => n + b.chapters.length, 0);
console.log(`index.json: ${grades.size} sections, ${subjects.size} subjects, ${books.length} books, ${count} chapters`);
