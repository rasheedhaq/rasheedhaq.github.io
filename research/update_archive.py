"""Refresh editorial presentation from dated Scholar and publisher metadata."""
from pathlib import Path
import html
import json
import re
import os
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
SCHOLAR = 'https://scholar.google.com/citations?user=ionCr1oAAAAJ&hl=en&pagesize=100'
DATE = '9 October 2026'


def fetch(url):
    response = requests.get(url, timeout=40)
    response.raise_for_status()
    return response


def clean(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())


def main():
    capture = os.environ.get('SCHOLAR_CAPTURE')
    soup = BeautifulSoup(Path(capture).read_text(encoding='utf-8') if capture else fetch(SCHOLAR).text, 'html.parser')
    assert soup.select_one('#gsc_prf_in'), 'Scholar unavailable; do not substitute cached figures'
    metrics = {}
    for row in soup.select('#gsc_rsb_st tbody tr'):
        cells = row.find_all('td')
        if len(cells) >= 2:
            metrics[cells[0].get_text(strip=True)] = cells[1].get_text(strip=True)
    articles = []
    for row in soup.select('tr.gsc_a_tr'):
        title = row.select_one('.gsc_a_at')
        cited = row.select_one('.gsc_a_ac')
        year = row.select_one('.gsc_a_y')
        if title:
            articles.append({'title': title.get_text(strip=True), 'citations': int(cited.get_text(strip=True) or 0) if cited else 0, 'year': year.get_text(strip=True) if year else ''})
    assert metrics and articles
    snapshot = {'checked': DATE, 'source': SCHOLAR, 'metrics': metrics, 'articles': articles, 'note': 'Profile contains duplicate titles; counts are not summed across duplicate entries.'}
    (ROOT / 'scholar_snapshot.json').write_text(json.dumps(snapshot, indent=2), encoding='utf-8')
    data = json.loads((ROOT / 'catalogue.json').read_text(encoding='utf-8'))
    crossref = fetch('https://api.crossref.org/works/10.1109/TAFE.2025.3569481').json()['message']
    assert 'Virtual Sensing' in crossref['title'][0]
    (ROOT / 'agrifood_metadata.json').write_text(json.dumps(crossref, indent=2), encoding='utf-8')
    for paper in data['papers']:
        if 'Deep Learning Enhanced Virtual' in paper['title']:
            paper.update(type='Journal article', status='Published, IEEE Transactions on AgriFood Electronics, 3(2), 486-496', dates='2025; issue metadata September 2025', confidence='Verified publisher-deposited Crossref metadata', doi='10.1109/TAFE.2025.3569481', metadata_source='https://api.crossref.org/works/10.1109/TAFE.2025.3569481')
        matches = [a for a in articles if clean(a['title']).startswith(clean(paper['title'])) or clean(paper['title']).startswith(clean(a['title']))]
        paper['scholar_citations'] = max((a['citations'] for a in matches), default=None)
        paper['citation_checked'] = DATE
    if not any(p.get('doi') == '10.1109/I3CS58314.2023.10127488' for p in data['papers']):
        record = fetch('https://api.crossref.org/works/10.1109/I3CS58314.2023.10127488').json()['message']
        data['papers'].append({'title': record['title'][0], 'type': 'Conference paper', 'status': 'Published conference paper, IEEE I3CS', 'dates': '2023', 'confidence': 'Verified publisher-deposited metadata and Scholar profile', 'doi': '10.1109/I3CS58314.2023.10127488', 'scholar_citations': next((a['citations'] for a in articles if clean(a['title']).startswith('randomforest')), None), 'citation_checked': DATE})
    journals = sorted([p for p in data['papers'] if p['type'] == 'Journal article'], key=lambda p: -(p['scholar_citations'] or 0))
    manuscripts = [p for p in data['papers'] if 'manuscript' in p['type'].lower()]
    conferences = sorted([p for p in data['papers'] if p not in journals + manuscripts], key=lambda p: -(p['scholar_citations'] or 0))
    data['papers'] = journals + manuscripts + conferences
    (ROOT / 'catalogue.json').write_text(json.dumps(data, indent=2), encoding='utf-8')
    def render(p):
        citations = f"{p['scholar_citations']} Scholar citations" if p.get('scholar_citations') is not None else 'Citation count not matched'
        link = f'<a class="button" href="https://doi.org/{p["doi"]}">Read paper / DOI &nearr;</a>' if p.get('doi') else '<span class="label">Publisher link awaiting verification</span>'
        return f'<article class="role"><div class="label">{html.escape(p["type"])} / {citations}</div><h3>{html.escape(p["title"])}</h3><p>{html.escape(p["status"])}</p><p class="date">{html.escape(p["dates"])}</p>{link}</article>'
    header = f'<div class="stats-panel"><a href="{SCHOLAR}"><strong>{html.escape(metrics.get("Citations", ""))}</strong><span>Scholar citations</span></a><div><strong>{html.escape(metrics.get("h-index", ""))}</strong><span>h-index</span></div><div><strong>{html.escape(metrics.get("i10-index", ""))}</strong><span>i10-index</span></div></div><p class="date">Google Scholar snapshot: {DATE}. Counts change over time.</p><p class="note">Journals are ordered by the matched Scholar citation count, not a claim of scientific quality. Duplicate title entries are not added together; the larger matching entry is shown. Unresolved manuscripts are separate; conferences are below.</p><div class="jump-links"><a href="#journals">Journal articles</a><a href="#manuscripts">Manuscripts</a><a href="#conferences">Conferences</a><a href="{SCHOLAR}">Google Scholar &nearr;</a></div>'
    groups = ''.join(f'<section id="{slug}"><h2>{label}</h2>{"".join(render(p) for p in items)}</section>' for slug, label, items in [('journals','Selected journal articles',journals),('manuscripts','Historical manuscripts / outcome unresolved',manuscripts),('conferences','Conferences & proceedings',conferences)])
    page = (ROOT / 'publications.html').read_text(encoding='utf-8')
    page = re.sub(r'<main>.*?(?=<footer>)', lambda _: '<main id="main-content">' + header + groups, page, flags=re.S)
    (ROOT / 'publications.html').write_text(page, encoding='utf-8')
    thesis = BeautifulSoup((ROOT / 'thesis.html').read_text(encoding='utf-8'), 'html.parser')
    abstract = next(s for s in thesis.find_all('section') if s.h2 and s.h2.get_text() == 'Abstract')
    # Repair PDF line wrapping from the existing abstract without adding new claims.
    text = ' '.join(p.get_text(' ', strip=True) for p in abstract.find_all('p'))
    text = text.replace('compu- i tational', 'computational')
    text = re.sub(r'([a-z])-\s+([a-z])', r'\1\2', text)
    for p in abstract.find_all('p'):
        p.decompose()
    for paragraph in re.split(r'(?=This research is motivated|The third work reported|The research works reported|Keywords:)', text):
        if paragraph.strip():
            tag = thesis.new_tag('p'); tag.string = paragraph.strip(); abstract.append(tag)
    (ROOT / 'thesis.html').write_text(str(thesis), encoding='utf-8')
    for name in ['index.html', 'index_ats.html']:
        path = ROOT.parent / name
        page = path.read_text(encoding='utf-8')
        page = page.replace('rasheedabdulhaqkp@gmail.com', 'rasheedabdulhaq@gmail.com')
        page = page.replace('Lead GenAI Developer', 'Lead AI/ML Engineer')
        page = page.replace('Two patents fully granted. One application published — all Indian Patent Office.', 'Three Indian patent grants, issued in 2022, 2024 and 2026. Certificates available in the PhD archive.')
        page = page.replace('Application 202341015286 A — Hybrid Deep Learning System for Aquaculture WQP', 'Indian Patent 579506 — Hybrid Deep Learning System for Aquaculture WQP')
        page = page.replace('Patent · Published', 'Patent · Granted')
        page = page.replace('Published 17 March 2023.', 'Granted 30 January 2026.')
        page = page.replace('Indian Patent 202341015286 (Granted)', 'Indian Patent 579506 (Granted)').replace('Granted 17 March 2023.', 'Granted 30 January 2026.')
        page = page.replace('maximum-scale=1.0', 'user-scalable=yes')
        if name == 'index.html' and 'Google Scholar</a>' not in page:
            page = page.replace('<a href="research/thesis.html">Read Thesis</a>', '<a href="research/thesis.html">Read Thesis</a><a href="' + SCHOLAR + '">Google Scholar</a>')
        path.write_text(page, encoding='utf-8')
    for path in ROOT.glob('*.html'):
        page = path.read_text(encoding='utf-8')
        page = page.replace('<title>Affordable monitoring.<br>Accurate prediction.', '<title>Affordable monitoring. Accurate prediction.')
        if 'skip-link' not in page:
            page = page.replace('<body>', '<body><a class="skip-link" href="#main-content">Skip to content</a>')
        page = page.replace('<main>', '<main id="main-content">')
        page = re.sub(r'(<a href="' + re.escape(path.name) + r'")(?! aria-current)', r'\1 aria-current="page"', page)
        if path.name == 'index.html' and '10.1109/TAFE.2025.3569481' not in page:
            page = page.replace('<h3>Patent Outcomes</h3>', '<p>Additional published continuation: <a href="https://doi.org/10.1109/TAFE.2025.3569481">Deep Learning Enhanced Virtual Sensing</a>, IEEE Transactions on AgriFood Electronics, 2025. <a href="publications.html">See all papers and citation details.</a></p><h3>Patent Outcomes</h3>')
        path.write_text(page, encoding='utf-8')
    print(json.dumps({'metrics': metrics, 'journal_order': [p['title'] for p in journals]}, indent=2))


if __name__ == '__main__':
    main()
