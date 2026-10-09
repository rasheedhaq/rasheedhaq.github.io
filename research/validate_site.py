"""Check local HTML resources and PDF readability before publication."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import subprocess

ROOT = Path(__file__).resolve().parent


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        self.links.extend(value for key, value in attrs if key in ('href', 'src', 'data'))


errors = []
pages = [ROOT.parent / 'index.html', *ROOT.glob('*.html')]
for page in pages:
    parser = Links()
    parser.feed(page.read_text(encoding='utf-8'))
    for link in parser.links:
        url = urlsplit(link)
        if not url.scheme and not url.netloc and url.path:
            if not (page.parent / unquote(url.path)).exists():
                errors.append((str(page), link))
pdfs = list((ROOT / 'documents').rglob('*.pdf'))
for pdf in pdfs:
    result = subprocess.run(['pdfinfo', str(pdf)], capture_output=True)
    if result.returncode:
        errors.append((str(pdf), 'Unreadable PDF'))
print(f'Checked {len(pages)} HTML pages and {len(pdfs)} PDFs. Errors: {errors}')
assert not errors
