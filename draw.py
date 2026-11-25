from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SIZE = (1024, 1024)
ROOT = Path(__file__).resolve().parent
FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')
INK = '#20201e'
PAPER = '#faf8f1'
MARGIN = 56
WIDTH = SIZE[0] - 2 * MARGIN
STORIES = [
    (
        'HOUTHIS STRIKE SAUDI RAS TANURA OIL REFINERY',
        "Yemen's Houthis say they attacked Saudi Arabia's Ras Tanura oil refinery, causing fires.",
    ),
    (
        'ISRAELI STRIKE KILLS HAMAS SECURITY CHIEF IN GAZA',
        "The strike killed the head of Hamas's interior security service, his wife and two children.",
    ),
    (
        'HUAWEI CONVICTED OF STEALING TRADE SECRETS IN US',
        'A Brooklyn jury found Huawei guilty on 10 of 12 counts, including bank fraud, but cleared it of racketeering.',
    ),
    (
        "PAKISTAN'S FIRST ASTRONAUT REACHES TIANGONG STATION",
        "Shenzhou-24 docked with China's space station carrying a Pakistani astronaut, the first foreign national aboard.",
    ),
    (
        'AUSTRALIA-SOLOMONS TREATY BARS FOREIGN BASES',
        'Canberra and Honiara sign a treaty precluding any foreign military or security base in the Solomon Islands.',
    ),
]


def font(name, size):
    path = FONT_DIR / name
    if not path.exists():
        path = FONT_DIR / 'DejaVuSans-Bold.ttf'
    return ImageFont.truetype(str(path), size)


def wrap(draw, text, face, width):
    lines = []
    current = ''
    for word in text.split():
        candidate = f'{current} {word}' if current else word
        if current and draw.textlength(candidate, font=face) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def centered(draw, text, y, face):
    x = (SIZE[0] - draw.textlength(text, font=face)) / 2
    draw.text((x, y), text, font=face, fill=INK, anchor='lt')


def main():
    image = Image.new('RGB', SIZE, PAPER)
    draw = ImageDraw.Draw(image)
    masthead = font('DejaVuSerif-Bold.ttf', 64)
    title = 'THE DAILY SIGNAL'
    while draw.textlength(title, font=masthead) > WIDTH:
        masthead = font('DejaVuSerif-Bold.ttf', masthead.size - 1)
    centered(draw, title, 43, masthead)
    draw.line((MARGIN, 124, 1024 - MARGIN, 124), fill=INK, width=2)
    centered(draw, 'WEDNESDAY 25 NOVEMBER 2026', 139,
             font('DejaVuSans.ttf', 16))
    draw.line((MARGIN, 174, 1024 - MARGIN, 174), fill=INK, width=1)

    # Fit measured text into the story area, reserving room for the footer.
    top, bottom = 198, 938
    headline_size, subline_size = 29, 19
    while True:
        headline_font = font('DejaVuSerif-Bold.ttf', headline_size)
        subline_font = font('DejaVuSans.ttf', subline_size)
        headline_step, subline_step = headline_size + 7, subline_size + 7
        blocks = []
        for headline, subline in STORIES:
            headlines = wrap(draw, headline, headline_font, WIDTH)
            sublines = wrap(draw, subline, subline_font, WIDTH)
            height = len(headlines) * headline_step + 8 + len(sublines) * subline_step
            blocks.append((headlines, sublines, height))
        total_height = sum(block[2] for block in blocks)
        if total_height + 4 * 26 <= bottom - top:
            break
        headline_size -= 1
        subline_size -= 1
        if subline_size < 14:
            raise ValueError('Stories cannot fit legibly in the page area')

    gap = (bottom - top - total_height) / 4
    y = float(top)
    for index, (headlines, sublines, height) in enumerate(blocks):
        block_top = y
        for line in headlines:
            draw.text((MARGIN, y), line, font=headline_font, fill=INK, anchor='lt')
            y += headline_step
        y += 8
        for line in sublines:
            draw.text((MARGIN, y), line, font=subline_font, fill=INK, anchor='lt')
            y += subline_step
        y = block_top + height
        if index < len(blocks) - 1:
            rule_y = round(y + gap / 2)
            draw.line((MARGIN, rule_y, 1024 - MARGIN, rule_y), fill=INK, width=1)
            y += gap

    draw.line((MARGIN, 960, 1024 - MARGIN, 960), fill=INK, width=1)
    centered(draw, 'Sources: Just Security - SCMP - AP - Reuters - Tribune',
             980, font('DejaVuSans.ttf', 15))
    image.save(ROOT / 'entry.png')


if __name__ == '__main__':
    main()
