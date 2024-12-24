import yaml
import os
import subprocess
from datetime import datetime
from generators.base import DocumentGenerator

class ResumeGenerator(DocumentGenerator):
    def __init__(self, yaml_file):
        super().__init__(yaml_file)
        self.latex_preamble = self.get_latex_preamble()
        self.data = yaml.safe_load(yaml_file)

    def get_latex_preamble(self):
        """Returns the LaTeX preamble with all package imports and custom commands"""
        return r'''\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\usepackage{setspace}
\usepackage{charter}

% Page setup
\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Margins
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-0.9in}
\addtolength{\textheight}{1.25in}

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
'''

    def escape_latex(self, text):
        """Escape special LaTeX characters"""
        if not isinstance(text, str):
            text = str(text)
        
        # Define replacements in order of precedence
        replacements = [
            ('\\', '\\textbackslash{}'),
            ('&', '\\&'),
            ('%', '\\%'),
            ('$', '\\$'),
            ('#', '\\#'),
            ('_', '\\_'),
            ('{', '\\{'),
            ('}', '\\}'),
            ('~', '\\textasciitilde{}'),
            ('^', '\\textasciicircum{}'),
            ('<', '\\textless{}'),
            ('>', '\\textgreater{}'),
            ('|', '\\textbar{}'),
            ('"', "''"),
            ('...', '\\ldots{}'),
            ('−', '-'),  # Replace en-dash with hyphen
            ('–', '-'),  # Replace em-dash with hyphen
        ]
        
        # Apply replacements
        for old, new in replacements:
            text = text.replace(old, new)
        
        return text

    def generate_header(self, personal):
        """Generate the header section with personal information"""
        return f'''\\begin{{center}}
    \\textbf{{\\Huge \\scshape {personal['name']}}} \\\\ \\vspace{{0.2pt}}
    \\small {personal['phone']} $|$ 
    \\href{{mailto:{personal['email']}}}{{{personal['email']}}} $|$
    \\href{{{personal['website']}}}{{{personal['website'].replace('https://', '')}}} $|$
    \\href{{{personal['linkedin']}}}{{{personal['linkedin'].replace('https://', '')}}}
\\end{{center}}'''

    def generate_education(self, education):
        """Generate the education section"""
        content = []
        content.append("\\section*{\\textbf{Education}}")
        content.append("\\resumeSubHeadingListStart")
        
        for school in education:
            content.append("\\resumeSubheading")
            content.append(f"{{{school['name']}}}{{{school['location']}}}")
            content.append(f"{{{school['degree']}}}{{{school['date']}}}")
            
            if 'courses' in school:
                content.append("\\resumeItemListStart")
                content.append(f"\\resumeItem{{Coursework: {school['courses']}}}")
                content.append("\\resumeItemListEnd")
                
        content.append("\\resumeSubHeadingListEnd")
        return '\n'.join(content)

    def generate_experience(self, experience):
        """Generate the experience section"""
        content = []
        content.append("\\section*{\\textbf{Experience}}")
        content.append("\\resumeSubHeadingListStart")
        
        for job in experience:
            content.append("\\resumeSubheading")
            content.append(f"{{{self.escape_latex(job['title'])}}}{{{job['date']}}}")
            content.append(f"{{{self.escape_latex(job['company'])}}}{{{self.escape_latex(job['location'])}}}")
            
            content.append("\\resumeItemListStart")
            for achievement in job['achievements']:
                # Ensure the achievement text is properly escaped and wrapped
                escaped_achievement = self.escape_latex(achievement)
                content.append(f"\\resumeItem{{{escaped_achievement}}}")
            content.append("\\resumeItemListEnd")
            
        content.append("\\resumeSubHeadingListEnd")
        return '\n'.join(content)

    def generate_projects(self, projects):
        """Generate the projects section"""
        content = []
        content.append("\\section*{\\textbf{Projects}}")
        content.append("\\resumeItemListStart{}")
        
        for project in projects:
            content.append(f"\\resumeItem{{\\textbf{{{project['name']}}} | {self.escape_latex(project['description'])}}}")
            
        content.append("\\resumeItemListEnd")
        return '\n'.join(content)

    def generate_skills(self, skills):
        """Generate the skills section"""
        content = []
        content.append("\\section*{\\textbf{Technical Skills}}")
        content.append("\\begin{itemize}[leftmargin=0.15in, label={}]")
        content.append("\\small{\\item{")
        
        for category in skills:
            content.append(f"\\textbf{{{category['name']}}}{{: {category['items']}}} \\\\")
            
        content.append("}}")
        content.append("\\end{itemize}")
        return '\n'.join(content)

    def generate_activities(self, activities):
        """Generate the activities section"""
        content = []
        content.append("\\section*{\\textbf{Activities \\& Club Involvement}}")
        content.append("\\resumeItemListStart")
        
        for activity in activities:
            content.append(f"\\resumeItem{{\\textbf{{{activity['name']}}}, {activity['date']}\\\\")
            content.append(f"     {self.escape_latex(activity['description'])}}}")
            
        content.append("\\resumeItemListEnd")
        return '\n'.join(content)

    def generate_resume(self, yaml_file):
        """Generate the complete LaTeX resume from YAML"""
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        content = [
            self.latex_preamble,
            "\\begin{document}",
            self.generate_header(data['personal']),
            self.generate_education(data['education']),
            self.generate_experience(data['experience']),
            self.generate_projects(data['projects']),
            self.generate_skills(data['skills']),
            self.generate_activities(data['activities']),
            "\\end{document}"
        ]
        
        return '\n\n'.join(content)

    def save_resume(self, yaml_file, output_dir="output"):
        """Save the generated LaTeX resume to a file"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        latex_content = self.generate_resume(yaml_file)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"resume_{timestamp}.tex")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
            
        return output_file
    
    def compile_pdf(self, tex_file):
        """Compile LaTeX file to PDF using pdflatex"""
        try:
            # Get the directory containing the tex file
            output_dir = os.path.dirname(tex_file)
            
            # Run pdflatex twice to ensure proper generation of references
            for _ in range(2):
                subprocess.run([
                    'pdflatex',
                    '-interaction=nonstopmode',
                    '-output-directory=' + output_dir,
                    tex_file
                ], check=True, capture_output=True)
            
            # Clean up auxiliary files
            base_name = os.path.splitext(tex_file)[0]
            for ext in ['.aux', '.log', '.out']:
                aux_file = base_name + ext
                if os.path.exists(aux_file):
                    os.remove(aux_file)
            
            pdf_file = base_name + '.pdf'
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
            
            return tex_file, pdf_file
            
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
        print(f"LaTeX file generated: {tex_file}")
        print(f"PDF file generated: {pdf_file}")
    except Exception as e:
        print(f"Failed to generate resume: {str(e)}")