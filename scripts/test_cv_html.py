import unittest
from pathlib import Path
from cv_html import render

SAMPLE = r"""\begin{document}
\begin{center}{\Huge\bfseries Example Name}\end{center}
\begin{center}Email: \href{mailto:example@example.com}{example@example.com} \\ Phone: +91 123\end{center}
\section{Professional Summary}
\begin{itemize}\item ML engineer with \textbf{Python}.\end{itemize}
\section{Experience}
\subsection{NIT Puducherry}\textbf{Research Fellow} \\ 2018 -- 2023
\begin{itemize}\item Research and deployment.\end{itemize}
\subsection{Patents}\begin{enumerate}\item Patent 123.\end{enumerate}
\section*{Skills}\begin{itemize}\item Python, Azure ML.\end{itemize}
\end{document}"""

class Conversion(unittest.TestCase):
    def test_preserves_contact_titles_skills_and_order(self):
        page=render(SAMPLE)
        for value in ('Example Name','mailto:example@example.com','Research Fellow','2018 -- 2023','Python, Azure ML','Patent 123'):
            self.assertIn(value,page)
        self.assertLess(page.index('NIT Puducherry'),page.index('<h3>Patents'))
        self.assertNotIn('<table',page)
        self.assertNotIn('float:',page)
        self.assertNotIn('\\textbf',page)
    def test_published_plain_cv_matches_canonical_source(self):
        root=Path(__file__).resolve().parents[1]
        source=(root/'cv/latest/resume.tex').read_text(encoding='utf-8')
        self.assertEqual(render(source),(root/'index_ats.html').read_text(encoding='utf-8'))

    def test_unknown_commands_are_not_silently_dropped(self):
        with self.assertRaises(ValueError):
            render(SAMPLE.replace('Python, Azure ML.',r'\unknown{Python}'))

if __name__=='__main__':
    unittest.main()
