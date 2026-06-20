# Job Application Agent

An autonomous job-application agent built on Claude Code.

It finds roles that match your profile, tailors a one-page ATS-optimized resume and cover letter to each job description, renders them to PDF, and assists with filling out application forms in the browser. You stay in control: you configure your own profile, and you review every document before anything is submitted.

## What it does

- Finds matching roles across job boards and company career pages.
- Tailors a one-page, ATS-friendly resume and cover letter to each specific job description.
- Generates clean, professional PDFs through a LaTeX pipeline.
- Assists with filling ATS application forms in a real browser via the Playwright MCP.

## How it works

A single source-of-truth profile YAML (`profile/about_candidate.yml`) holds your experience, projects, skills, and preferences. Claude Code subagents read that profile to scout jobs, tailor a resume and cover letter to each job description, and help submit applications. The tailored content is written to per-job YAML files, and a LaTeX pipeline (driven by `main.py`) renders them into polished one-page PDFs.

Because every document traces back to your single profile file, the agent stays consistent and grounded in your real history. It never invents experience you did not provide.

## Features

- Single source-of-truth profile that drives every generated document.
- Per-job tailoring of resume and cover letter to the target job description.
- One-page, ATS-optimized output with a clean, recruiter-friendly layout.
- LaTeX-to-PDF rendering for crisp, consistent typography.
- Browser-based form assistance through the Playwright MCP.
- Claude Code subagents for scouting, tailoring, and submitting.
- Configurable preferences, including an optional, generic work-authorization field.

## Repository structure

```
.
├── main.py                       # Entry point: renders resume/cover letter to PDF
├── ui.py                         # Optional interactive interface
├── ui/                           # UI components and assets
├── resume/
│   └── generator.py              # Resume LaTeX generator
├── coverletter/
│   └── generator.py              # Cover letter LaTeX generator
├── generators/
│   └── base.py                   # Shared generation logic
├── jobdescription/
│   └── scraptor.py               # Job description fetching and parsing
├── profile/
│   └── about_candidate.yml       # Your source-of-truth profile (edit this)
├── .claude/
│   └── agents/                   # Claude Code subagent definitions
├── WORKFLOW.md                   # End-to-end workflow guide
├── CLAUDE.md                     # Project instructions for Claude Code
└── docs/                         # Setup and usage documentation
```

## Quick start

1. **Install prerequisites and Claude Code.** Set up Python, a LaTeX distribution, Node.js, and the Claude Code CLI. See [docs/SETUP.md](docs/SETUP.md).
2. **Clone and install dependencies.** Clone the repository and run `pip install -r requirements.txt`. See [docs/SETUP.md](docs/SETUP.md).
3. **Fill in your profile.** Edit `profile/about_candidate.yml` with your real experience, projects, skills, and preferences. See [docs/USAGE.md](docs/USAGE.md).
4. **Generate your first resume.** Run `python main.py` to render a PDF and confirm the pipeline works end to end. See [docs/USAGE.md](docs/USAGE.md).
5. **Run the workflow in Claude Code.** Open the repository in Claude Code, install the Playwright MCP, and ask Claude to run the workflow. See [docs/PLAYWRIGHT_MCP.md](docs/PLAYWRIGHT_MCP.md) and [WORKFLOW.md](WORKFLOW.md).

## Requirements

- Python 3.8 or newer
- A LaTeX distribution (for example, TeX Live or MiKTeX)
- Node.js (required by the Playwright MCP)
- Claude Code

## Responsible use

This tool automates *your own* job applications using *your own* real information after you configure it. It is meant to save time on repetitive tailoring and form-filling, not to misrepresent you.

- Never fabricate experience, education, skills, or credentials. The agent works from the profile you provide, so keep that profile truthful.
- Review every resume, cover letter, and form before it is submitted. You are responsible for what you send.
- Respect the terms of service of the job boards and application systems you use.
- Keep any work-authorization or sponsorship information accurate and current.

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.
