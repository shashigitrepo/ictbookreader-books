"""Turns the element card images in periodic-table/originals/ into light WebP cards for the app.

Put any image (jpg, png, webp) in periodic-table/originals/. Its name only has to say which element
it is: the atomic number ("47.jpg", "047-silver.png"), the symbol ("Ag.jpg") or the English name
("Silver card.png"). This script (run by the "Periodic table cards" GitHub Action on every upload):
  - writes periodic-table/cards/NNN.webp, at most 1080 px wide, WebP quality 80 (about half a JPG);
  - writes periodic-table/cards.json, which the app reads to know which elements have a card;
  - removes cards whose original was deleted.
Elements without a card still show in the app, with a simple card made from its built-in data.
"""
import hashlib, io, json, os, re, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, 'periodic-table', 'originals')
OUT = os.path.join(ROOT, 'periodic-table', 'cards')
ELEMENTS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'elements.json')))
BY_SYMBOL = {s.lower(): n for n, s, _ in ELEMENTS}
BY_NAME = {name.lower(): n for n, _, name in ELEMENTS}
BY_NAME.update({'aluminum': 13, 'sulphur': 16, 'caesium': 55, 'cesium': 55})
MAX_WIDTH, QUALITY = 1080, 80


def element_of(filename):
    """The atomic number a file is for, or None. A number anywhere in the name wins ("47.jpg",
    "Ag-47.jpeg", "047-silver.png"); otherwise an English name ("Silver.png") or a symbol ("Ag.jpg").
    Raises ValueError when the name's symbol or element name disagrees with its number."""
    stem = os.path.splitext(filename)[0].strip()
    numbers = [int(n) for n in re.findall(r'(?<!\d)0*(\d{1,3})(?!\d)', stem) if 1 <= int(n) <= 118]
    words = [w for w in re.split(r'[^A-Za-z]+', stem) if w]
    named = next((BY_NAME[w.lower()] for w in words if w.lower() in BY_NAME), None)
    symbol = next((BY_SYMBOL[w.lower()] for w in words if len(w) <= 2 and w.lower() in BY_SYMBOL), None)
    if numbers:
        number = numbers[0]
        for other in (named, symbol):
            if other is not None and other != number:
                raise ValueError(f'the name says element {other} but the number says {number}')
        return number
    return named if named is not None else symbol


def main():
    os.makedirs(OUT, exist_ok=True)
    cards, problems = {}, []
    for name in sorted(os.listdir(SRC)) if os.path.isdir(SRC) else []:
        if name.startswith('.') or name.lower() == 'readme.md':
            continue
        try:
            number = element_of(name)
        except ValueError as e:
            problems.append(f'{name}: {e}; rename it to just the atomic number, e.g. 23.jpg')
            continue
        if number is None:
            problems.append(f'{name}: cannot tell which element this is (start the name with the atomic number, e.g. 47.jpg)')
            continue
        if number in cards:
            problems.append(f'{name}: element {number} has two images; using {cards[number]["source"]}')
            continue
        try:
            image = Image.open(os.path.join(SRC, name))
            image.load()
        except Exception as e:  # not an image
            problems.append(f'{name}: not a readable image ({e})')
            continue
        image = image.convert('RGB')
        if image.width > MAX_WIDTH:
            image = image.resize((MAX_WIDTH, round(image.height * MAX_WIDTH / image.width)), Image.LANCZOS)
        buffer = io.BytesIO()
        image.save(buffer, 'WEBP', quality=QUALITY, method=6)
        data = buffer.getvalue()
        target = os.path.join(OUT, f'{number:03d}.webp')
        if not os.path.exists(target) or open(target, 'rb').read() != data:
            open(target, 'wb').write(data)
        cards[number] = {'source': name, 'file': f'cards/{number:03d}.webp',
                         'v': hashlib.sha1(data).hexdigest()[:10], 'bytes': len(data)}
    for old in os.listdir(OUT):
        m = re.match(r'^(\d{3})\.webp$', old)
        if not m or int(m.group(1)) not in cards:
            os.remove(os.path.join(OUT, old))
    index = {'cards': {str(n): {'file': c['file'], 'v': c['v']} for n, c in sorted(cards.items())}}
    with open(os.path.join(ROOT, 'periodic-table', 'cards.json'), 'w') as f:
        json.dump(index, f, indent=1)
        f.write('\n')
    total = sum(c['bytes'] for c in cards.values())
    print(f'{len(cards)} cards, {total // 1024} KB in all')
    for p in problems:
        print('PROBLEM:', p)
    # Problems are reported but do not stop the good cards from being published.


if __name__ == '__main__':
    sys.exit(main())
