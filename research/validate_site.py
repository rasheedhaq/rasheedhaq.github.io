"""Check local HTML resources and PDF readability before publication."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import subprocess
import hashlib
import json

ROOT = Path(__file__).resolve().parent.parent


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get('id'):
            self.ids.add(values['id'])
        if tag == 'a' and values.get('name'):
            self.ids.add(values['name'])
        self.links.extend(value for key, value in attrs if key in ('href', 'src', 'data') and value)


def validate(root=ROOT):
    errors = []
    pages = {p.resolve(): Links() for p in root.rglob('*.html')
             if not any(part in {'.git', 'node_modules', '.venv'} for part in p.parts)}
    for page, parser in pages.items():
        parser.feed(page.read_text(encoding='utf-8'))
    for page, parser in pages.items():
        for link in parser.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                if url.scheme == 'file':
                    errors.append((str(page), 'Private file URL: ' + link))
                continue
            path = unquote(url.path)
            target = ((root / path.lstrip('/')) if path.startswith('/') else
                      (page.parent / path) if path else page).resolve()
            if target.is_dir():
                target = target / 'index.html'
            if not target.exists():
                errors.append((str(page), 'Missing resource: ' + link))
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append((str(page), 'Missing fragment: ' + link))
    pdfs = list(root.rglob('*.pdf'))
    try:
        from pypdf import PdfReader
    except ImportError:
        PdfReader = None
    for pdf in pdfs:
        try:
            if PdfReader:
                if not len(PdfReader(pdf).pages):
                    raise ValueError('No PDF pages')
            else:
                subprocess.run(['pdfinfo', str(pdf)], capture_output=True, check=True)
        except Exception as error:
            errors.append((str(pdf), 'Unreadable PDF: ' + str(error)))
    versions = root / 'cv/versions.json'
    if versions.exists():
        for version, metadata in json.loads(versions.read_text()).items():
            for extension, key in [('tex', 'source_sha256'), ('pdf', 'pdf_sha256')]:
                path = root / 'cv' / version / ('resume.' + extension)
                if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != metadata[key]:
                    errors.append((str(path), 'CV checksum mismatch'))
    archive = root / 'lab/archive'
    if archive.exists():
        files = [p for p in archive.rglob('*') if p.is_file()]
        if len(files) > 3 or any(p.suffix not in {'.html', '.pdf'} for p in files):
            errors.append((str(archive), 'Research collection exceeds three HTML/PDF files'))
    print(f'Checked {len(pages)} HTML pages and {len(pdfs)} PDFs. Errors: {errors}')
    return errors


if __name__ == '__main__':
    raise SystemExit(bool(validate()))
