# ICT Book Reader – books

PDFs that the **ICT Book Reader** app shows and downloads on demand. NCERT books are not stored
here: the app links to ncert.nic.in directly.

**Anything you upload here appears in the app by itself**, usually within a few minutes:
GitHub rebuilds `index.json` after every change (Actions tab → "Build index"), and the app
downloads that list each time it starts. No app update is needed.

## Folder layout

```
grade-6/ … grade-12/          one folder per class
  <subject>/                  e.g. ict
    info.json                 optional: names and exact chapter titles
    00-preface.pdf            front matter (not numbered in the app)
    01-chapter-title.pdf      chapters, numbered by their prefix
    99-answer-key.pdf         back matter (not numbered in the app)
cyber-safety/                 any other top-level folder is a card on the home screen
  info.json                   optional: {"title": "Cyber Safety", "order": 101}
  handbook/                   a group of books (shown like a subject)
    01-….pdf                  …with its chapters directly inside
    new-guide/01-….pdf        …or several books, one folder each
teacher-resources/            same rules
career-counselling/           the two handbooks of the Career Counselling screen
  after-class-10/01-handbook.pdf    "What to choose after Class 10"
  after-class-12/01-handbook.pdf    "Career options after Class 12"
```

Career Counselling has its own screen in the app, so keep these two folder names exactly.
A handbook can be one PDF (opens straight in the reader) or several chapters
(`01-….pdf`, `02-….pdf`); until a PDF is uploaded the app shows "Soon" on its card.

## Rules

1. Folder and file names: lowercase letters, digits and hyphens only. No spaces.
2. Files start with a two-digit number that sets the order: `01-…` to `98-…` are chapters,
   `00-…` comes first and `99-…` last without a chapter number. Several front-matter files:
   `00a-…`, `00b-…`.
3. Without `info.json`, names come from the folder and file names:
   `03-word-processing.pdf` → "Word Processing". Use `info.json` for exact names.
4. Keep each PDF under 50 MB; chapters are better than whole books (less mobile data).

## info.json (all fields optional)

In a top-level section folder (not `grade-N`):

```json
{ "title": "Cyber Safety", "order": 101 }
```

In a subject or book folder:

```json
{
  "subject": "Cyber Safety",
  "title": "Cyber Safety Handbook",
  "publisher": "CBSE",
  "order": 1,
  "chapters": { "01-netizens-in-the-digital-world.pdf": "Netizens in the Digital World" }
}
```

## Adding a book from the GitHub website

1. Open the folder, e.g. `cyber-safety`, then **Add file → Upload files**.
2. To create a new folder, type its name followed by `/` in the file name box, or drag a whole
   folder from your computer onto the upload page.
3. **Commit changes**. After a minute, the **Actions** tab shows a green tick and the app shows
   the new book the next time it is opened.
