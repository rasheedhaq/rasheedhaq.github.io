# Goal review / 19 October 2026

## Goal and current outcome

A professional portfolio and GitHub presence grounded in the CV, with selected research that visitors can understand and continue. The existing GitHub Pages repository remains the canonical website; no extra clone, paid domain or repository is needed for the site.

The portfolio, current/previous resume, five project stories, thesis reader, publication catalogue and three patent records are present. The public research collection is one self-contained HTML brief, with selected paper/code/thesis/certificate links and browser Print / Save as PDF. It is an overview, not a full-text consolidation of all specifications.

## Highest-value actions completed

- Replaced the original 60-version public file listing with one curated brief; the bulk publisher is retired locally. Original research sources were preserved.
- Extended validation to every site HTML page, directory indexes and fragment targets, every published PDF, private file URLs, CV checksums and the maximum-three-file collection limit.
- Added GitHub Actions checks for every push and pull request. Hosted validation and Pages deployment for commit `eb2bfcb` both completed successfully.
- Corrected the latest TeX checksum to match published LF bytes, retained its original import checksum and fixed future imports. The 12 October master text matches the published source after newline normalization; the PDF matches its master checksum. No CV content was changed by this repair.
- Added the brief to the standard lab browser checks: seven pages at 320, 390, 768 and 1440 pixels.

## Unnecessary work not to repeat

Recursive conversion of the entire work folder, generated experimental plots, administrative documents and historical draft variants does not improve a recruiter's or research collaborator's main journey. Publishing both TeX and PDF versions of the same draft created clutter. Automatic grouping by filename was not sufficient editorial review. Keep bulk inventory local; publish by contribution, not file count.

Do not create new repositories merely because a folder exists. A useful public repository needs a clear use case, runnable entry point, dependency instructions, attributable results and a sharing/licence review.

## Remaining gaps

- Full private archive: the current checkpoint has 78,217 pending files and 153 conversion failures out of 127,513 inventoried entries. It is not finished, not freshly rescanned, and not needed to publish this curated website. Counts are a checkpoint, not a claim about the whole current filesystem.
- Full patent text: the brief and grant certificates do not replace complete granted specifications/claims/drawings. Uncertain historical associations were deliberately removed from the public collection. A full-text edition needs document-by-document verification, not another automatic file dump.
- Reproduction: plot export tests passed previously, but the full research training/evaluation pipeline has not been rerun. No new numerical results are claimed.
- GitHub account: this pass does not certify every remote repository, profile setting, licence, dependency or secret history. No repository was deleted or created.
- Browser downloads: the resume action requests a viewer and dated download, but browser settings may suppress or change one of these behaviours. It cannot guarantee both across every browser.
- Publication metadata and external links can age. Their historical check dates must remain visible; local site validation does not verify current citation counts or publisher availability.

## Follow-through and resolution paths

Completed in the follow-through review:

- Checked all 16 public repository records and labelled eight upstream forks in the repository map. This resolves the attribution/navigation gap, not a full security or code audit.
- Updated the profile README to link the lab and brief, remove repeated previous-resume links, and identify template forks. Updated portfolio/NammaOpen descriptions and portfolio/NammaOpen/DLEVS homepage links.
- Ran the DLEVS equation baseline on the existing local MAC CSV after adding direct CSV support. Five exporter/integration tests passed. The output stays local; it is not a newly reproduced deep-learning result.

Resolve the remaining items in this order, only where they serve a reader need:

1. **Profile website field:** open GitHub profile settings and set Website to `https://rasheedhaq.github.io/`. The API credential permitted repository updates but rejected the profile-field update with HTTP 404. The README already supplies the link, so this is cosmetic rather than a broken visitor path.
2. **Reusable research code:** establish which code is solely authored versus institutional/coauthored, then apply an authorized licence and document dataset access separately. Public API metadata currently detects no licence for DLEVS, NammaOpen or the time-series prediction repository. An open-source licence must not silently include patents, restricted data or third-party code.
3. **Full research reproduction:** the baseline entry point has now completed against the local MAC CSV. The separate training harness has concrete blockers: default `DO`/`DO_org` mismatch, scaler fit before splitting, one optimizer reused across models, and no complete attention/bidirectional architecture comparison in its model builders. TensorFlow is absent from the checked runtime. See [DLEVS verification findings](https://github.com/rasheedhaq/DLEVS/blob/main/docs/verification.md). The next step is to reconcile the authoritative attention-GRU notebook/configuration, then implement a tested training-only preprocessing split and independent model optimizers. Running the current scaffold would not verify the paper.
4. **Full-text patent edition:** obtain one authoritative granted specification with its claims and drawings per grant/application pair; verify identifiers and page completeness against the official record. Only then replace or supplement the brief within the three-document limit. Do not use a similarly named draft as a verified legal record.
5. **Private archive:** defer it for this portfolio goal. If a complete personal reading room is separately needed, resume the checkpoint, reconcile new files, retry failed formats and validate every generated page before calling it complete. This is a separate large deliverable, not a website defect.

The repo descriptions, attribution map, export code and documentation were changed; no repository, research original or historical patent source was deleted. Browser double-action download restrictions remain platform behaviour rather than a fixable guarantee.

## Maintenance rule

Update the canonical resume pair and its two HTML representations together. Keep one evidence-backed story per selected project and one canonical link per resource. Run tests and inspect mobile layout before pushing. Avoid further archive expansion unless it fills a specific reader need.
