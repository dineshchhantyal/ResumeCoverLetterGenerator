# CLAUDE.md

## Project purpose

This repo turns Claude Code into an autonomous job-application assistant. Claude acts on the user's behalf to find relevant roles, tailor a resume and cover letter into one-page LaTeX PDFs (via `main.py`), and fill out ATS application forms through the Playwright MCP. The goal is an end-to-end pipeline from job discovery to submitted application, with the user staying in the loop for anything sensitive.

## Source of truth

`profile/about_candidate.yml` holds ALL of the user's real facts: work experience, projects, skills, education, contact info, and work-authorization details. Treat it as the single source of truth. `resume/resume.yml` is a tailored one-page subset derived from it. NEVER invent experience, projects, dates, employers, metrics, or skills that are not present in `profile/about_candidate.yml`.

## Key commands

Generate documents with the interactive generator:

```bash
python main.py
```

It prompts for: Company name, Role title, then a choice of `1` (resume), `2` (cover letter), or `3` (both). Output lands in `applications/{Company}/`.

Non-interactive form (Company, Role, blank line, then `3` for both):

```bash
printf "Company Name\nRole Title\n\n3\n" | python main.py
```

## Subagents and when to use them

Definitions live in `.claude/agents/`.

- **job-scout**: find roles that fit the candidate profile.
- **resume-builder**: tailor `resume/resume.yml` to a specific job description.
- **application-submitter**: fill ATS forms via the Playwright MCP.

## Content rules (hard)

- Resume must be one page.
- Summary is at most 2 lines.
- Every resume bullet includes a metric.
- Mirror the job description's keywords.
- Technology substitution is allowed only within the same category, and only if the user genuinely has the related skill in `about_candidate.yml`.
- Never fabricate experience, projects, dates, or employers.
- No em-dashes in generated cover letters.

## Form-filling defaults

- Pull name, email, phone, location, links, and education from `profile/about_candidate.yml`.
- Answer work-authorization and sponsorship questions honestly using the profile's configured fields.
- Always pause and ask the user for CAPTCHAs, OTP codes, and before any final submission.

## Workflow reference

See `WORKFLOW.md` for the full 9-phase pipeline. See `docs/` for setup (`docs/SETUP.md`), usage (`docs/USAGE.md`), Playwright MCP details (`docs/PLAYWRIGHT_MCP.md`), and architecture (`docs/ARCHITECTURE.md`).
