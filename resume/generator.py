import yaml
import os
import subprocess
from datetime import datetime
from generators.base import DocumentGenerator


class ResumeGenerator(DocumentGenerator):
    def __init__(self, yaml_file):
        super().__init__(yaml_file)
        self.latex_preamble = self.get_latex_preamble()
        with open(yaml_file, "r", encoding="utf-8") as f:
            self.data = yaml.safe_load(f)

    def get_latex_preamble(self):
        """Returns the LaTeX preamble with all package imports and custom commands"""
        return r"""\documentclass[letterpaper,10pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\usepackage{setspace}
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault}
% ATS-friendly packages
\usepackage{accsupp}
\usepackage[hidelinks,pdfusetitle]{hyperref}
\hypersetup{
  pdftitle={Resume},
  pdflang={en-US},
  pdfcreator={pdfLaTeX},
  pdfduplex={Simplex},
  pdftoolbar=false,
  pdffitwindow=true,
  pdfnewwindow=true,
  colorlinks=false,
  linktoc=all,
  pdfpagemode=UseNone
}

% Page setup
\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Margins
\usepackage[margin=0.25in]{geometry}  % Set all margins to 0.25 inches

\urlstyle{same}
\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Section formatting
\titleformat{\section}{
  \vspace{-5pt}\scshape\raggedright\small
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

% Custom commands
\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{\small#1} & \small#2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}
"""

    def escape_latex(self, text):
        """Escape special LaTeX characters"""
        if not isinstance(text, str):
            text = str(text)

        # Define replacements in order of precedence
        replacements = [
            ("#", "\\#"),  # Escape the # character
            ("&", "\\&"),
            ("%", "\\%"),
            # ('$', '\\$'),
            ("_", "\\_"),
            # ('{', '\\{'),
            # ('}', '\\}'),
            ("~", "\\textasciitilde{}"),
            # ('^', '\\textasciicircum{}'),
            ("<", "\\textless{}"),
            (">", "\\textgreater{}"),
            ("|", "\\textbar{}"),
            ('"', "''"),
            ("...", "\\ldots{}"),
            ("−", "-"),  # Replace en-dash with hyphen
            ("–", "-"),  # Replace em-dash with hyphen
        ]

        # Apply replacements
        for old, new in replacements:
            text = text.replace(old, new)

        return text

    def generate_header(self, personal):
        """Generate the header section with personal information"""
        return f"""\\begin{{center}}
        \\textbf{{\\LARGE {self.escape_latex(personal['name'])}}} \\\\ \\vspace{{0.2pt}}
        \\small {self.escape_latex(personal['phone'])} $|$
        \\href{{mailto:{self.escape_latex(personal['email'])}}}{{{self.escape_latex(personal['email'])}}} $|$
        \\href{{{self.escape_latex(personal['website'])}}}{{{self.escape_latex(personal['website'].replace('https://www.', ''))}}} $|$
        \\href{{{self.escape_latex(personal['linkedin'])}}}{{{self.escape_latex(personal['linkedin'].replace('https://', ''))}}}
        $|$
        {self.escape_latex(personal['location'])}
    \\end{{center}}
    """

    def generate_education(self, education):
        """Generate the education section"""
        content = []
        content.append("\\section*{\\textbf{Education}}")
        content.append("\\resumeSubHeadingListStart")

        for school in education:
            content.append("\\resumeSubheading")
            content.append(f"{{{school['name']}}}{{{school['location']}}}")
            content.append(
                f"{{{school['degree']}, {{GPA: {school['GPA']}}}}}{{{school['date']}}}"
            )

            if "courses" in school:
                content.append("\\resumeItemListStart")
                content.append(f"\\resumeItem{{{school['courses']}}}")
                content.append("\\resumeItemListEnd")

        content.append("\\resumeSubHeadingListEnd")
        return "\n".join(content)

    def generate_experience(self, experience):
        """Generate the experience section"""
        content = []
        content.append("\\section*{\\textbf{Experience}}")
        content.append("\\resumeSubHeadingListStart")

        for job in experience:
            content.append("\\resumeSubheading")
            content.append(f"{{{self.escape_latex(job['title'])}}}{{{job['date']}}}")
            content.append(
                f"{{{self.escape_latex(job['company'])}}}{{{self.escape_latex(job['location'])}}}"
            )

            content.append("\\resumeItemListStart")
            for achievement in job["achievements"]:
                # Remove any leading dash and whitespace for clean bulleting
                achievement_clean = achievement.lstrip("- ").strip()
                escaped_achievement = self.escape_latex(achievement_clean)
                content.append(f"\\resumeItem{{{escaped_achievement}}}")
            content.append("\\resumeItemListEnd")

            # Add extra spacing between jobs
            content.append("\\vspace{6pt}")

        content.append("\\resumeSubHeadingListEnd")
        return "\n".join(content)

    def generate_projects(self, projects):
        """Generate the projects section"""
        content = []
        content.append("\\section*{\\textbf{Projects}}")
        content.append("\\resumeItemListStart{}")
        for project in projects:
            name = self.escape_latex(project.get("name", ""))
            description = self.escape_latex(project.get("description", ""))
            link = project.get("link")
            if link:
                # Make the project name itself a hyperlink (no visual indication in PDF)
                item = f"\\resumeItem{{\\href{{{link}}}{{\\textbf{{{name}}}}} | {description}}}"
            else:
                item = f"\\resumeItem{{\\textbf{{{name}}} | {description}}}"
            content.append(item)
        content.append("\\resumeItemListEnd")
        return "\n".join(content)

    def generate_skills(self, skills):
        """Generate the skills section"""
        content = []
        content.append(
            "\\section*{\\textbf{Skills}}"
        )  # Changed to standard ATS-friendly heading
        content.append("\\begin{itemize}[leftmargin=0.15in, label={}]")
        content.append("\\small{\\item{")

        for category in skills:
            content.append(
                f"\\textbf{{{category['name']}}}{{: {category['items']}}} \\\\"
            )

        content.append("}}")
        content.append("\\end{itemize}")
        return "\n".join(content)

    def extract_keywords(self):
        """Extract potential keywords from skills and experience for ATS optimization"""
        keywords = set()

        # Extract from skills
        for skill_category in self.data.get("skills", []):
            # Split by commas and clean up
            skills = [s.strip() for s in skill_category["items"].split(",")]
            keywords.update(skills)

        # Extract job titles and company names
        for job in self.data.get("experience", []):
            keywords.add(job["title"])
            keywords.add(job["company"])

            # Extract technical terms from achievements
            for achievement in job["achievements"]:
                # Find words in textbf that are likely technical terms
                import re

                tech_terms = re.findall(r"\\textbf\{([^}]+)\}", achievement)
                keywords.update(tech_terms)

                # Also extract important tech and numerical metrics
                tech_matches = re.findall(
                    r"\b(?:[A-Z][A-Za-z0-9./+_-]+|[0-9]+[xX]|\d+%|\d+[KkMmGgTt][Bb])\b",
                    achievement,
                )
                keywords.update(tech_matches)

        # Add project technologies
        for project in self.data.get("projects", []):
            description = project.get("description", "")
            tech_terms = re.findall(r"\\textbf\{([^}]+)\}", description)
            keywords.update(tech_terms)

            # Extract other tech terms and metrics from projects
            tech_matches = re.findall(
                r"\b(?:[A-Z][A-Za-z0-9./+_-]+|[0-9]+[xX]|\d+%|\d+[KkMmGgTt][Bb])\b",
                description,
            )
            keywords.update(tech_matches)

        # Filter out common non-technical terms and short terms
        filtered_keywords = [
            k
            for k in keywords
            if len(k) > 2
            and not k.lower() in {"the", "and", "with", "for", "from", "that", "this"}
        ]

        return sorted(filtered_keywords)

    def generate_keywords_section(self):
        """Generate a hidden keywords section for ATS optimization"""
        keywords = self.extract_keywords()
        if not keywords:
            return ""

        content = []
        # Hidden section not visible in the PDF but readable by ATS
        content.append("\\begin{comment}")
        content.append("Keywords for ATS Optimization:")
        # Join keywords with commas for better ATS parsing
        keywords_text = ", ".join([self.escape_latex(k) for k in keywords])
        content.append(keywords_text)
        content.append("\\end{comment}")
        return "\n".join(content)

    def generate_activities(self, activities):
        """Generate the activities section"""
        content = []
        content.append("\\section*{\\textbf{Activities \\& Club Involvement}}")
        content.append("\\resumeItemListStart{}")
        for activity in activities:
            name = self.escape_latex(activity["name"])
            description = (
                self.escape_latex(activity["description"])
                if "description" in activity
                else ""
            )
            date = self.escape_latex(activity["date"])

            formatted_activity = (
                f"\\resumeItem{{"
                f"\\textbf{{{name}}} "  # Bold name
                f"\\hfill {date}\\\\"  # Right-aligned date
                f"{description}"  # Description on new line
                f"}}"
            )

            content.append(formatted_activity)
        content.append("\\resumeItemListEnd")
        return "\n".join(content)

    def generate_resume(self, yaml_file):
        """Generate the complete LaTeX resume from YAML"""
        # Optional sections
        summary_text = self.data.get("summary")
        activities = self.data.get("activities", []) or self.data.get("leadership", [])

        content = [
            self.latex_preamble,
            "\\begin{document}",
            self.generate_header(self.data.get("personal", {})),
        ]

        if summary_text:
            content.append("\\section*{\\textbf{Summary}}")
            content.append("\\small{" + self.escape_latex(summary_text.strip()) + "}")

        content.extend(
            [
                self.generate_experience(self.data.get("experience", [])),
                self.generate_projects(self.data.get("projects", [])),
                self.generate_skills(self.data.get("skills", [])),
                self.generate_education(self.data.get("education", [])),
            ]
        )

        if activities:
            content.append(self.generate_activities(activities))

        # Add keywords section for ATS optimization (invisible in rendered PDF)
        content.append(self.generate_keywords_section())

        content.append("\\end{document}")

        return "\n\n".join(content)

    def save_resume(self, yaml_file, output_dir="output"):
        """Save the generated LaTeX resume to a file"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        latex_content = self.generate_resume(yaml_file)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"resume_{timestamp}.tex")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(latex_content)

        return output_file

    def compile_pdf(self, tex_file):
        """Compile LaTeX file to PDF using pdflatex with ATS-friendly settings"""
        try:
            # Get the directory containing the tex file
            output_dir = os.path.dirname(tex_file)

            # Run pdflatex twice to ensure proper generation of references
            for _ in range(2):
                subprocess.run(
                    [
                        "pdflatex",
                        "-interaction=nonstopmode",
                        "-output-directory=" + output_dir,
                        # ATS-friendly settings - remove -dPDFA flag since it's causing issues
                        tex_file,
                    ],
                    check=True,
                    capture_output=True,
                )

            # Clean up auxiliary files
            base_name = os.path.splitext(tex_file)[0]
            for ext in [".aux", ".log", ".out"]:
                aux_file = base_name + ext
                if os.path.exists(aux_file):
                    os.remove(aux_file)

            pdf_file = base_name + ".pdf"
            if os.path.exists(pdf_file):
                return pdf_file
            else:
                raise Exception("PDF file was not generated")

        except subprocess.CalledProcessError as e:
            print(f"Error during PDF compilation: {e}")
            print(f"LaTeX output: {e.output.decode()}")
            raise
        except Exception as e:
            print(f"Error: {str(e)}")
            raise

    def generate_pdf(self, yaml_file, output_dir="output"):
        """Generate both LaTeX and PDF files from YAML"""
        try:
            # First generate the tex file
            tex_file = self.save_resume(yaml_file, output_dir)

            # Then compile it to PDF
            pdf_file = self.compile_pdf(tex_file)

            # delete the tex file
            if os.path.exists(tex_file):
                os.remove(tex_file)

            return pdf_file

        except Exception as e:
            print(f"Failed to generate PDF: {str(e)}")
            raise

    def generate_tex(self):
        """
        Implement the abstract method from DocumentGenerator.
        This method generates the complete text content of the resume.
        """
        return self.generate_resume(self.yaml_file)


if __name__ == "__main__":
    try:
        generator = ResumeGenerator()
        tex_file, pdf_file = generator.generate_pdf("resume.yml")
    except Exception as e:
        print(f"Failed to generate resume: {str(e)}")
