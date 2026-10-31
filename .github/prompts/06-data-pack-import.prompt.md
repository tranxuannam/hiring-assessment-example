---
description: Inspect and import the supplied hiring assessment data pack.
---

Inspect the supplied data pack before writing an importer.

1. Identify the actual archive/folder structure and file formats.
2. Read the questions and grading guides.
3. Identify typed answers, audio-only answers, and any reference-score file.
4. Propose a repeatable import format and mapping to the database.
5. Preserve original answer content and source filenames where appropriate.
6. Make importing repeatable and safe to rerun without duplicating candidates, answers, or scoring jobs.
7. Do not invent missing candidate information or scores.
8. Do not treat reference scores as model-generated scores.

Implement the importer only after explaining the mapping. Add tests for repeat imports and malformed/missing files. Report imported counts based on actual execution.
