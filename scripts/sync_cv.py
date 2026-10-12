"""Sync a dated local CV into stable latest/previous repository paths."""
import argparse
import hashlib
import html
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def plain(text):
    text = re.sub(r"\\(?:textbf|textit|enquote)\{([^{}]*)\}", r"\1", text)
    return text.replace(r"\&", "&").replace(r"\%", "%").strip()

def update_web(source):
    text = source.read_text(encoding="utf-8")
    chevron = text.split(r"\subsection{Chevron", 1)[1].split(r"\end{itemize}", 1)[0]
    bullets = [plain(b) for b in chevron.split(r"\item ")[1:]]
    markup = "<ul>\n" + "\n".join("        <li>" + html.escape(b) + "</li>" for b in bullets) + "\n      </ul>"
    for name in ("index.html", "index_ats.html"):
        path = ROOT / name
        page = path.read_text(encoding="utf-8")
        org = page.index("Chevron Engine", page.index('<body>'))
        start = page.index('<ul>', org)
        end = page.index('</ul>', start) + len('</ul>')
        page = page[:start] + markup + page[end:]
        page = page.replace('Jun 2015 – Jun 2018 &nbsp;·&nbsp; 3 yrs', 'Jun 2015 – Jul 2018 &nbsp;·&nbsp; 3 yrs 1 mo')
        page = page.replace('Jun 2015 – Jun 2018 (3 yrs)', 'Jun 2015 – Jul 2018 (3 yrs 1 mo)')
        page = page.replace('Aug 2014 – Jun 2015 &nbsp;·&nbsp; 10 mos', 'Aug 2014 – Jun 2017 &nbsp;·&nbsp; Part-time alongside teaching')
        page = page.replace('Aug 2014 – Jun 2015 (10 mos)', 'Aug 2014 – Jun 2017 (2 yrs 11 mos; part-time alongside teaching)')
        page = page.replace('>Embedded Software Engineer<', '>Founder &amp; Senior Embedded Software Engineer<')
        page = page.replace('>Embedded Software Engineer <', '>Founder &amp; Senior Embedded Software Engineer <')
        page = page.replace('Aug 2013 – Jul 2014 &nbsp;·&nbsp; 12 mos', 'Sep 2013 – Jul 2014 &nbsp;·&nbsp; 11 mos')
        page = page.replace('Aug 2013 – Jul 2014 (12 mos)', 'Sep 2013 – Jul 2014 (11 mos)')
        page = page.replace('using OpenCV on Raspberry Pi with cross-team integration.', 'using MATLAB, OpenCV, and C++, evaluated on an ARM-based BeagleBoard-xM platform.')
        page = page.replace('OpenCV, YOLO, SlowFast', 'OpenCV, YOLOv8/YOLO11, Thermal Image Analysis, SlowFast')
        page = page.replace('OpenCV, YOLO v5/v8, SlowFast', 'OpenCV, YOLOv8/YOLO11, Thermal Image Analysis, SlowFast')
        page = page.replace('AWS, Azure, GCP, EC2, Git', 'Azure ML, Managed Endpoints, Model Registry, Azure Functions, MLflow, AWS Bedrock, Git')
        page = page.replace('AWS (EC2, Bedrock, Secrets Manager), Azure, GCP, Git, Docker', 'Azure ML, Managed Endpoints, Model Registry, Azure Functions, MLflow, AWS (EC2, Bedrock, Secrets Manager), Git')
        page = page.replace('including <strong>8 years in applied AI/ML</strong>', 'including <strong>8+ years across AI research and applied ML</strong>')
        marker = '<!-- cv-downloads -->'
        if marker not in page:
            downloads = marker + '\n<p style="padding:12px 20px;text-align:center"><a href="cv/latest/resume.pdf">Download latest CV (PDF)</a> | <a href="cv/index.html">Current and previous CV</a></p>\n'
            page = page.replace('<body>', '<body>\n' + downloads, 1)
        # Keep web research outputs beside the NIT role, as requested.
        if name == 'index.html':
            start = page.index('<section id="research">')
            end = page.index('</section>', start) + len('</section>')
            block = page[start:end]
            page = page[:start] + page[end:]
            org = page.index('MEA Engineering College', page.index('<body>'))
            insertion = page.rfind('<div class="exp-item">', 0, org)
            page = page[:insertion] + block + '\n\n' + page[insertion:]
            page = page.replace('8 years in AI/ML', '8+ years across AI research and ML')
            page = page.replace('8 years applied AI/ML', '8+ years across AI research and applied ML')
            page = page.replace('Production ML across vision, time-series, and LLM systems from research to deployment.', 'AI research and applied ML across vision, time-series, and LLM systems.')
        else:
            start = page.index('<!-- ===== PATENTS ===== -->')
            end = page.index('<div class="exp-entry">', start)
            project_marker = page.find('<!-- ===== SELECTED PROJECTS ===== -->', start, end)
            if project_marker >= 0:
                end = project_marker
            block = page[start:end]
            page = page[:start] + page[end:]
            org = page.index('MEA Engineering College', page.index('<body>'))
            insertion = page.rfind('<div class="exp-entry">', 0, org)
            page = page[:insertion] + block + page[insertion:]
            page = re.sub(r'<p class="pub-entry">[^\n]*Attention-Driven LSTM[^\n]*</p>', '<p class="pub-entry">Rahul Gandh D, Harigovindan V P, Rasheed Abdul Haq K P, and Amrtha Bhide, "Attention-driven LSTM and GRU deep learning techniques for precise water quality prediction in smart aquaculture," <em>Aquaculture International</em>, vol. 32, pp. 8455–8478, 2024. <a href="https://doi.org/10.1007/s10499-024-01574-5">DOI</a></p>', page)
        page = '\n'.join(line.rstrip() for line in page.splitlines()) + '\n'
        path.write_text(page, encoding='utf-8')

def sync(source, pdf, update_pages=True):
    source, pdf = source.resolve(), pdf.resolve()
    match = re.search(r'_Resume_(\d{2})([A-Z]{3})(\d{4})\.tex$', source.name)
    if not match:
        raise ValueError('Expected local filename: Rasheed_Abdul_Haq_Resume_DDMMMYYYY.tex')
    months = 'JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC'.split()
    date = datetime(int(match[3]), months.index(match[2]) + 1, int(match[1])).date().isoformat()
    if not source.is_file() or not pdf.is_file() or not pdf.read_bytes().startswith(b'%PDF-'):
        raise ValueError('A readable source and matching PDF are required.')
    if pdf.stem != source.stem or pdf.stat().st_mtime < source.stat().st_mtime:
        raise ValueError('Compile the matching dated PDF after saving the source before syncing.')
    cv = ROOT / 'cv'
    metadata = cv / 'versions.json'
    versions = json.loads(metadata.read_text()) if metadata.exists() else {}
    latest = versions.get('latest')
    if latest and date < latest['date']:
        raise ValueError('Cannot replace latest CV with an older date.')
    if latest and date > latest['date']:
        (cv/'previous').mkdir(exist_ok=True)
        for name in ('resume.tex', 'resume.pdf'):
            shutil.copy2(cv/'latest'/name, cv/'previous'/name)
        versions['previous'] = latest
    (cv/'latest').mkdir(exist_ok=True)
    for src, name in ((source, 'resume.tex'), (pdf, 'resume.pdf')):
        shutil.copy2(src, cv/'latest'/name)
    versions['latest'] = {'date': date, 'source_filename': source.name,
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'pdf_sha256': hashlib.sha256(pdf.read_bytes()).hexdigest()}
    metadata.write_text(json.dumps(versions, indent=2) + '\n', encoding='utf-8')
    entries = ''.join(f'<li><strong>{key.title()}: {value["date"]}</strong> — <a href="{key}/resume.pdf">PDF</a> · <a href="{key}/resume.tex">LaTeX</a></li>' for key, value in versions.items())
    (cv/'index.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CV Downloads — Rasheed Abdul Haq</title><style>body{font:18px/1.6 system-ui;max-width:760px;margin:40px auto;padding:0 20px}li{margin:16px 0}</style></head><body><h1>CV downloads</h1><p>Rasheed Abdul Haq Kozhiparamban</p><ul>' + entries + '</ul><p>Earlier versions remain available in Git history.</p><p><a href="../index.html">Portfolio</a> · <a href="../index_ats.html">Plain CV</a></p></body></html>\n', encoding='utf-8')
    if update_pages:
        update_web(source)
    print(f'Synced {date}. Latest/previous files retained; local dated originals preserved.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--pdf', type=Path)
    parser.add_argument('--no-web', action='store_true', help='Import an historical baseline without updating web pages')
    args = parser.parse_args()
    sync(args.source, args.pdf or args.source.with_suffix('.pdf'), not args.no_web)
