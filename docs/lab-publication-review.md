# AI & Research Lab publication review

Reviewed 12 October 2026. This is a curated first release, not clearance of every file in the work folder.

## Organisation
The existing local organisation remains unchanged. Public case studies live in `lab/` in the existing portfolio repository; research PDFs remain in `research/documents/`. No extra clone or repository is needed.

## Selected material
- DLEVS: local Repos_Main/DLEVS README and research catalogue; public implementation and DOI linked. Metrics attributed to the published study, not freshly reproduced.
- Hybrid water-quality prediction: local Repos_Main/time_series README, research overview and publication catalogue; existing public code and paper linked.
- Monitoring prototype: research overview and previously recovered CV demonstration link; thesis and certificates reused.
- NammaOpen: local project README; described as a local MVP, not a live production service.
- VLC playlist manager: local project README; public utility linked, no personal media inventory uploaded.
- Patent preparation templates: existing public repositories linked, not private patent draft packages.

## Material held back
The research workspace guide explicitly identifies external reference code, third-party datasets, under-review manuscripts, revision responses and administrative material. Those labels alone are not grounds to publish their contents.
- Publisher PDFs: use DOI links pending a check of the specific redistribution licence.
- Datasets: retain upstream references pending permission/licence and identifying-information review.
- Unpublished paper/patent drafts: inspect publication status and coauthor/institution permissions before any release.
- External reference code: do not present as original work; retain attribution and licence.
- Employment archives, personal records, credentials, submission correspondence and review responses: not needed for the public lab and not uploaded.
- Other application folders: require source, dependency, secret and personal-data checks before new public repositories are created.

No raw archive, new PDF, dataset or LaTeX bundle is included in this release. Existing public links do not certify that the complete repositories have undergone a fresh security audit.

## Updating
Add a case study only after reading its supporting source and checking every included asset. Keep claims tied to a paper or implementation. Prefer one canonical file/link over duplicate PDFs. When a source changes, update its case study and run the site validator plus desktop/mobile browser checks.

## Follow-up review
Mobile navigation now wraps instead of concealing links horizontally. Case studies use a visual section marker without incorrectly announcing the lab index as the current page. Removed defensive review-note phrasing while retaining published-result attribution and practical reproduction requirements. Card summaries are left aligned to avoid uneven word spacing.

Run `python research/validate_site.py` for local resources and PDF readability. Run `node scripts/check_lab.cjs` with Playwright available and Microsoft Edge installed for all six lab pages at 320, 390, 768 and 1440 pixels. The browser check covers overflow, navigation visibility, current-page indicators, story sections and safe new-tab links. Set `LAB_SCREENSHOTS` to an existing directory for visual review images.

The original Pages build succeeded but its deploy job remained waiting during review. The environment permits the main branch and has no listed required reviewers; the available API responses did not establish why deployment is waiting. No environment protection settings were changed.

