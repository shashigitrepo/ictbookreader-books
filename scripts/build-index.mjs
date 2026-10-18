#!/usr/bin/env node
// Writes index.json: the books in this repository in the ICT Book Reader catalogue format.
// The app downloads it on every start, so files uploaded here appear without an app update.
// Runs automatically on every push (.github/workflows/build-index.yml); no dependencies.
//
// Layout: <section>/<subject>[/<book>]/NN-chapter-title.pdf, see README.md.
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

const errors = [];
const folders = new Map();
for (const path of walk(ROOT)) {
  if (!path.endsWith('.pdf')) continue;
  const parts = path.split('/');
  const file = parts.pop();
  if (parts.length < 2 || parts.length > 3) {
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
    publisher: info.publisher ?? 'ICT Book Reader',
    medium: info.medium ?? 'en',
    ...(info.section ? { section: info.section } : {}),
    chapters,
  });
}

if (errors.length) {
  console.error(`Fix these first:\n  ${errors.join('\n  ')}`);
  process.exit(1);
}

const index = { version: 1, grades: [...grades.values()], subjects: [...subjects.values()], books };
writeFileSync(join(ROOT, 'index.json'), JSON.stringify(index, null, 2) + '\n');
const count = books.reduce((n, b) => n + b.chapters.length, 0);
console.log(`index.json: ${grades.size} sections, ${subjects.size} subjects, ${books.length} books, ${count} chapters`);
