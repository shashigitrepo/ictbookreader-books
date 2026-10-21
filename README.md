# Padhaku – books

PDFs that the **Padhaku** app shows and downloads on demand. NCERT books are not stored
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

## NCERT Solutions, chapter notes (students) and teacher notes

```
solutions/                     everyone sees these (Home → NCERT Solutions, and the Solutions tab)
  class-10/
    science/
      01-chemical-reactions.pdf     answers to the exercises of chapter 1
      02-acids-bases-and-salts.pdf
```

NCERT Solutions follow exactly the same rules as notes below: the number is the textbook's
chapter number (the app shows a **Solutions** button on that chapter), and the subject folder is
one of the names in the table. Hindi-medium solutions: put them in a folder of their own, e.g.
`solutions/class-10/science/hindi-medium/`, with an `info.json` containing
`{ "title": "विज्ञान – NCERT समाधान", "medium": "hi" }`; the app then shows them to students who
chose Hindi.

```
notes/                         everyone sees these (Home → Chapter notes, and the Notes tab)
  class-10/
    science/
      01-chemical-reactions.pdf     01 = chapter 1 of the NCERT textbook
      01a-practice-questions.pdf    more notes for chapter 1
      02-acids-bases-and-salts.pdf
teacher-notes/                 only teachers see these (Teacher notes tab): presentations as PDF
  class-10/
    science/
      01-chemical-reactions.pdf
```

1. **The number is the textbook's chapter number.** The app shows a **Notes** button on that
   chapter. Extra files for the same chapter: `05a-…`, `05b-…`.
2. **The subject folder must be one of the names below** (exactly, lowercase). A typo stops the
   update and the **Actions** tab shows the right names.
3. **Presentations:** PowerPoint → *File → Save as → PDF*, then upload the PDF.
4. Subjects with several textbooks (e.g. English): put the notes of each book in a folder of its
   own, e.g. `notes/class-10/english/first-flight/01-a-letter-to-god.pdf`. These are listed in
   the Notes tab but not linked to chapters (the numbers would be ambiguous).

| Class folder | Subject folders |
|---|---|
| `class-6` | `english`, `hindi`, `sanskrit`, `mathematics`, `science`, `social-science`, `vocational-education`, `ict`, `arts`, `physical-education-and-well-being` |
| `class-7` | `english`, `hindi`, `sanskrit`, `mathematics`, `science`, `social-science`, `vocational-education`, `ict`, `arts`, `physical-education-and-well-being` |
| `class-8` | `english`, `hindi`, `sanskrit`, `mathematics`, `science`, `social-science`, `vocational-education`, `ict`, `arts`, `physical-education-and-well-being` |
| `class-9` | `english`, `hindi`, `sanskrit`, `mathematics`, `science`, `social-science`, `employability-skills`, `vocational-education`, `arts`, `physical-education-and-well-being`, `skill-education` |
| `class-10` | `english`, `hindi`, `sanskrit`, `mathematics`, `science`, `social-science`, `employability-skills`, `vocational-education`, `health-and-physical-education` |
| `class-11` | `english`, `hindi`, `sanskrit`, `mathematics`, `physics`, `chemistry`, `biology`, `accountancy`, `business-studies`, `economics`, `history`, `geography`, `political-science`, `psychology`, `sociology`, `employability-skills`, `vocational-education`, `biotechnology`, `computer-science`, `computers-and-communication-technology`, `creative-writing-and-translation`, `fine-art`, `graphics-design`, `health-and-physical-education`, `heritage-crafts`, `home-science`, `informatics-practices`, `knowledge-traditions-practices-of-india`, `sangeet` |
| `class-12` | `english`, `hindi`, `sanskrit`, `mathematics`, `physics`, `chemistry`, `biology`, `accountancy`, `business-studies`, `economics`, `history`, `geography`, `political-science`, `psychology`, `sociology`, `employability-skills`, `vocational-education`, `biotechnology`, `computer-science`, `creative-writing-and-translation`, `fine-art`, `heritage-crafts`, `home-science`, `informatics-practices`, `new-age-graphics-design`, `sangeet` |

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

## YouTube videos

Edit **`videos.csv`** at the top of this repository (on GitHub: open it → ✏️ Edit → Commit).
One row per video; keep the first line as it is:

```
class,subject,chapter,title,url
10,science,1,Chemical reactions – part 1,https://youtu.be/xxxxxxxxxxx
10,science,1,Chemical reactions – part 2,https://youtu.be/yyyyyyyyyyy
9,mathematics,,Number systems – full revision,https://www.youtube.com/watch?v=zzzzzzzzzzz
```

- **class** 6 … 12, **subject** one of the subject folder names in the table above.
- **chapter**: the textbook chapter number; the app shows a **Video** button on that chapter.
  Leave it empty for a video about the whole subject.
- **title**: put it in "double quotes" if it contains a comma.
- **url**: a YouTube link (`https://youtu.be/…` or `https://www.youtube.com/…`).

The videos appear in the app under **Home → Videos** about a minute after you commit.
The channel button on that screen comes from Firebase Remote Config: add the parameter
`youtube_channel_url` (e.g. `https://www.youtube.com/@yourchannel`) and publish.

## CBSE previous year papers

`cbse-papers.json` lists CBSE's official question papers (Class X and XII, main, compartment and
second board exams) with links to **cbse.gov.in**. The app shows them under **Home → Previous Year
Papers** and downloads each paper from CBSE when a student opens it; no paper is stored here.

To add a new year: send the updated CBSE page (https://www.cbse.gov.in/cbsenew/question-paper.html)
to the developer, or add entries in the same format: `{"year":2027,"grade":10,"exam":"main",
"subject":"Science","url":"https://www.cbse.gov.in/cbsenew/question-paper/2027/X/Science.zip","size":"40 MB"}`
(`exam` is `main`, `compartment` or `second`). The app picks up changes without an update.

