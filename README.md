# Rasheed Abdul Haq — portfolio and CV

Professional portfolio, current CV, previous CV, and research archive.

- [Portfolio](https://rasheedhaq.github.io/)
- [Latest CV — PDF](cv/latest/resume.pdf) · [LaTeX source](cv/latest/resume.tex)
- [Previous CV — PDF](cv/previous/resume.pdf) · [LaTeX source](cv/previous/resume.tex)
- [CV downloads and dates](cv/index.html)
- [Plain HTML CV](index_ats.html)
- [Public GitHub repository map](docs/github-repositories.md)
- [CV update workflow](docs/cv-workflow.md)

## Repository tree

```text
rasheedhaq.github.io/
├── index.html                 # Main portfolio
├── index_ats.html             # Plain HTML CV
├── typography.css
├── cv/
│   ├── index.html             # Download links and version dates
│   ├── versions.json          # Source dates and SHA-256 checksums
│   ├── latest/
│   │   ├── resume.tex
│   │   └── resume.pdf
│   └── previous/
│       ├── resume.tex
│       └── resume.pdf
├── docs/
│   ├── cv-workflow.md
│   └── github-repositories.md
├── scripts/
│   ├── sync_cv.py
│   └── test_sync_cv.py
└── research/
    ├── index.html
    ├── thesis.html
    ├── publications.html
    ├── patents.html
    ├── catalogue.json
    ├── theme.css
    ├── update_archive.py
    ├── validate_site.py
    ├── browser_check.cjs
    ├── agrifood_metadata.json
    ├── scholar_snapshot.json
    └── documents/
        ├── thesis-march-2024.pdf
        ├── chapters/          # Selected thesis chapters
        └── patents/           # Three grant certificates
```

Root hosting files `.nojekyll` and `_config.yml` are preserved. Git ignores LaTeX build intermediates and local tooling.

## Research archive

- [PhD research](research/index.html)
- [Thesis reader and chapter guide](research/thesis.html)
- [Papers and proceedings](research/publications.html)
- [Patent certificates](research/patents.html)

Publisher DOI links are used instead of redistributing restricted paper PDFs. Only selected thesis documents and three verified grant certificates belong in the research document folder. No correspondence, bank records, unpublished patent drafts or third-party reference patents are included.

The original thesis and selected chapter PDFs are published with the author's explicit approval. Research metadata is bounded by the underlying documents, not a claim that every historical manuscript was published.
