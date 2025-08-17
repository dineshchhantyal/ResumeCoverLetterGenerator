from datetime import datetime
import os
import subprocess
import yaml
from generators.base import DocumentGenerator


class CoverLetterGenerator(DocumentGenerator):
    def __init__(self, yaml_file):
        super().__init__(yaml_file)

    def generate_cover_letter(self):
        personal = self.data["personal_information"]
        recipient = self.data["recipient"]
        letter = self.data["letter"]

        cover_letter = f"""
        {personal['name']}
        {personal.get('title', '')}
        {personal['address']['line']}, {personal['address']['postal_code']}, {personal['address']['country']}
        Mobile: {personal['phone']['mobile']}
        Fixed: {personal['phone'].get('fixed','')}
        Fax: {personal['phone'].get('fax','')}
        Email: {personal['email']}
        Homepage: {personal['homepage']}
        Extra Info: {personal.get('extra_info','')}
        Quote: {personal.get('quote','')}

        To: {recipient['name']}
        Address: {recipient['address']}

        Date: {letter['date']}
        {letter['opening']}

        {letter['body']}

        {letter['closing']}
        Enclosure: {letter['enclosure']}
        """
        return cover_letter.strip()

    def replace_placeholders(self, company_name):
        """
        Interactively ask user for missing placeholder values in the YAML data.
        Only prompts for values that contain placeholder text.
        """
        data = self.data.copy()
        data["letter"]["body"] = data["letter"]["body"].replace("%", "\\%")
        if "[Hiring Manager's Name]" in data["recipient"]["name"]:
            manager_name = input("Enter hiring manager's name: ").strip()
            data["recipient"]["name"] = data["recipient"]["name"].replace(
                "[Hiring Manager's Name]", manager_name
            )
        if "[Company Address]" in data["recipient"]["address"]:
            company_address = input("Enter company address: ").strip()
            data["recipient"]["address"] = data["recipient"]["address"].replace(
                "[Company Address]", company_address
            )
        if "[Company Name]" in data["recipient"]["address"]:
            data["recipient"]["address"] = data["recipient"]["address"].replace(
                "[Company Name]", company_name
            )
        data["letter"]["date"] = datetime.now().strftime("%Y-%m-%d")
        data["letter"]["opening"] = data["letter"]["opening"].replace(
            "[Company Name]", company_name
        )
        data["letter"]["body"] = data["letter"]["body"].replace(
            "[Company Name]", company_name
        )
        self.data = data
        return data

    def generate_tex(self, company_name):
        self.replace_placeholders(company_name)
        personal = self.data["personal_information"]
        recipient = self.data["recipient"]
        letter = self.data["letter"]

        content = [
            r"""
\documentclass[11pt, letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=1in]{geometry}
\usepackage{charter}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{setspace}
\usepackage{parskip}
\usepackage{enumitem}

% Custom colors
\definecolor{primary}{RGB}{45, 55, 72}
\definecolor{accent}{RGB}{49, 130, 206}

% Remove page numbers
\pagenumbering{gobble}

% Hyperlink styling
\hypersetup{
    colorlinks=true,
    urlcolor=accent,
    linkcolor=accent
}

% Set paragraph spacing
\setlength{\parindent}{0pt}
\setlength{\parskip}{1em}

% Compact list style
\setlist[itemize]{leftmargin=*, topsep=2pt, itemsep=2pt, parsep=0pt, partopsep=0pt}

\begin{document}""",
            f"""
\\begin{{flushright}}
\\textcolor{{primary}}{{
\\Large\\bfseries {personal['name']}\\\\[4pt]
\\normalsize {personal['address']['line']}\\\\
{personal['address']['postal_code']}, {personal['address']['country']}\\\\[4pt]
{personal['phone']['mobile']} $|$ \\href{{mailto:{personal['email']}}}{{{personal['email']}}} $|$ \\href{{{personal['homepage']}}}{{{personal['homepage']}}}
}}
\\end{{flushright}}

\\vspace{{1em}}
\\noindent{{\\today}}

\\vspace{{1em}}
\\noindent{{
{recipient['name']}\\\\
{recipient.get('title', '')}\\\\
{recipient['company']}\\\\
{recipient['address']}
}}

\\vspace{{1.5em}}
\\noindent {letter['opening']}

{letter['body']}

\\vspace{{1em}}
\\noindent {letter.get('closing', 'Sincerely,')}

\\vspace{{1.5em}}
\\noindent {personal['name']}

\\vspace{{0.5em}}
\\noindent{{\\textcolor{{accent}}{{\\small{{{letter['enclosure']}}}}}}}
""",
            r"\end{document}",
        ]

        return "\n".join(content)

    def save_cover_letter(self, yaml_file, output_dir, company_name):
        os.makedirs(output_dir, exist_ok=True)
        tex_content = self.generate_tex(company_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tex_file = os.path.join(output_dir, f"cover_letter_{timestamp}.tex")
        with open(tex_file, "w", encoding="utf-8") as tex:
            tex.write(tex_content)
        return tex_file

    def generate_pdf(self, yaml_file, output_dir, company_name):
        try:
            tex_file = self.save_cover_letter(yaml_file, output_dir, company_name)
            pdf_file = self.compile_pdf(tex_file, output_dir)
            os.remove(tex_file)
            return pdf_file
        except Exception as e:
            print(f"Failed to generate PDF: {str(e)}")
            raise

    def compile_pdf(self, tex_file, output_dir):
        try:
            output_dir = os.path.dirname(tex_file)
            for _ in range(2):
                result = subprocess.run(
                    [
                        "pdflatex",
                        "-interaction=nonstopmode",
                        "-output-directory=" + output_dir,
                        tex_file,
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                if result.returncode != 0:
                    print(result.stdout)
                    print(result.stderr)
            base_name = os.path.splitext(tex_file)[0]
            for ext in [".aux", ".log", ".out"]:
                aux_file = base_name + ext
                if os.path.exists(aux_file):
                    os.remove(aux_file)
            pdf_file = base_name + ".pdf"
            if os.path.exists(pdf_file):
                return pdf_file
            raise Exception("PDF file was not generated")
        except Exception as e:
            raise Exception(f"Failed to generate PDF: {str(e)}")


# Example Usage
# generator = CoverLetterGenerator('cover_letter.yml')
# print(generator.generate_cover_letter())
