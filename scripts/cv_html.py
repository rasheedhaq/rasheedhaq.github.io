"""Render this CV's supported LaTeX subset as accessible, single-column HTML.

Unknown commands fail visibly rather than silently dropping resume text.
"""
import html
import re


def inline(text):
    links = []

    def link(match):
        url, label = match.groups()
        if not url.startswith(('https://', 'http://', 'mailto:', 'tel:')):
            raise ValueError('Unsupported CV link scheme')
        links.append('<a href="' + html.escape(url, quote=True) + '">' + html.escape(label) + '</a>')
        return f'LINKTOKEN{len(links)-1}TOKEN'

    text = re.sub(r'\\href\{([^{}]*)\}\{([^{}]*)\}', link, text)
    for before, after in ((r'\&', '&'), (r'\%', '%'), (r'\_', '_'), (r'\hfill', ''), (r'\quad', ' | ')):
        text = text.replace(before, after)
    text = text.replace('\\\\', 'BREAKTOKEN')
    text = html.escape(text.strip())
    for command, tag in (('textbf', 'strong'), ('textit', 'em'), ('texttt', 'code')):
        text = re.sub(r'\\' + command + r'\{([^{}]*)\}', lambda m: '<' + tag + '>' + m[1] + '</' + tag + '>', text)
    text = re.sub(r'\\enquote\{([^{}]*)\}', r'&quot;\1&quot;', text)
    if re.search(r'\\[A-Za-z]+', text):
        raise ValueError('Unsupported LaTeX command in CV: ' + text[:160])
    text = text.replace('{', '').replace('}', '').replace('BREAKTOKEN', '<br>')
    for n, value in enumerate(links):
        text = text.replace(f'LINKTOKEN{n}TOKEN', value)
    return text


def block(text):
    pattern = r'\\begin\{(itemize|enumerate)\}(?:\[[^\]]*\])?(.*?)\\end\{\1\}'
    output = []
    cursor = 0
    for match in re.finditer(pattern, text, re.S):
        prefix = inline(text[cursor:match.start()])
        if prefix:
            output.append('<p>' + prefix + '</p>')
        tag = 'ul' if match[1] == 'itemize' else 'ol'
        items = re.split(r'\\item\s+', match[2])[1:]
        output.append('<' + tag + '>' + ''.join('<li>' + inline(item) + '</li>' for item in items) + '</' + tag + '>')
        cursor = match.end()
    remainder = inline(text[cursor:])
    if remainder:
        output.append('<p>' + remainder + '</p>')
    return '\n'.join(output)


def render(source):
    body = source.split(r'\begin{document}', 1)[1].split(r'\end{document}', 1)[0]
    body = re.sub(r'(?<!\\)%[^\n]*', '', body)
    first = re.search(r'\\section\*?\{', body)
    if not first:
        raise ValueError('No CV sections found')
    header = body[:first.start()]
    centers = re.findall(r'\\begin\{center\}(.*?)\\end\{center\}', header, re.S)
    contact = inline(centers[-1])
    name = re.search(r'\\Huge\\bfseries\s+([^}]+)', header)[1]
    body = body[first.start():]
    parts = re.split(r'\\(section\*?|subsection)\{([^{}]*)\}', body)
    content = []
    for i in range(1, len(parts), 3):
        level = 'h2' if parts[i].startswith('section') else 'h3'
        content.append(f'<{level}>' + inline(parts[i+1]) + f'</{level}>')
        content.append(block(parts[i+2]))
    return '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rasheed Abdul Haq - Plain CV</title><style>
body{font:11pt/1.45 Arial,Helvetica,sans-serif;color:#111;max-width:850px;margin:28px auto;padding:0 22px}
h1{font-size:23pt;margin-bottom:8px}h2{font-size:14pt;border-bottom:1px solid #777;margin-top:22px;break-after:avoid}h3{font-size:12pt;margin-bottom:4px;break-after:avoid}
p{margin:6px 0}li{margin-bottom:6px}ul,ol{padding-left:24px}a{color:inherit}code{font:inherit}.downloads{font-size:10pt}
@page{size:A4;margin:16mm}@media print{body{margin:0;padding:0;max-width:none}.downloads{display:none}li{break-inside:avoid}}
</style></head><body>
<!-- Generated from the canonical LaTeX CV by scripts/cv_html.py. -->
<p class="downloads"><a href="cv/latest/resume.pdf">Latest PDF</a> | <a href="cv/index.html">Version history</a> | <a href="index.html">Portfolio</a></p>
<h1>''' + html.escape(name) + '</h1><p>' + contact + '</p>\n' + '\n'.join(content) + '\n</body></html>\n'
