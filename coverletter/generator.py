from datetime import datetime
import os
import subprocess
import yaml
from generators.base import DocumentGenerator
class CoverLetterGenerator(DocumentGenerator):
    def __init__(self, yaml_file):
        super().__init__(yaml_file)
    
    def generate_cover_letter(self):
        personal = self.data['personal_information']
        recipient = self.data['recipient']
        letter = self.data['letter']
        
        cover_letter = f"""
        {personal['name']}
        {personal.get('title', '')}
        {personal['address']['line']}, {personal['address']['postal_code']}, {personal['address']['country']}
        Mobile: {personal['phone']['mobile']}
        Fixed: {personal['phone']['fixed']}
        Fax: {personal['phone']['fax']}
        Email: {personal['email']}
        Homepage: {personal['homepage']}
        Extra Info: {personal['extra_info']}
        Quote: {personal['quote']}
        
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
        # Deep copy the data to avoid modifying the original
        data = self.data.copy()
        
        # Check and prompt only for placeholders that exist in the data
        if '[Hiring Manager\'s Name]' in data['recipient']['name']:
            manager_name = input("Enter hiring manager's name: ").strip()
            data['recipient']['name'] = data['recipient']['name'].replace(
                    '[Hiring Manager\'s Name]', 
                    manager_name
                )
        
        # Only ask for company address if it contains the placeholder
        if '[Company Address]' in data['recipient']['address']:
            company_address = input("Enter company address: ").strip()
            
            data['recipient']['address'] = data['recipient']['address'].replace(
                '[Company Address]', 
                company_address
            )
        
        if '[Company Name]' in data['recipient']['address']:
            data['recipient']['address'] = data['recipient']['address'].replace(
                '[Company Name]', 
                company_name
            )
        
        data['letter']['date'] = datetime.now().strftime("%Y-%m-%d")

        data['letter']['opening'] = data['letter']['opening'].replace(
            '[Company Name]', 
            company_name
        )
        
        data['letter']['body'] = data['letter']['body'].replace(
            '[Company Name]', 
            company_name
        )
        
        # Update the instance data
        self.data = data
        return data

    def generate_tex(self, company_name):
        """Generate a LaTeX file from the YAML data."""
        self.replace_placeholders(company_name)
        personal = self.data['personal_information']
        recipient = self.data['recipient']
        letter = self.data['letter']
        
        content = [
            r"""%% Modern Cover Letter Template
\documentclass{letter}
\usepackage[utf8]{inputenc}
\usepackage[spanish, english]{babel}
\usepackage[dvipsnames]{xcolor}
\usepackage{hyperref}
\usepackage[scale=0.75]{geometry}
\usepackage{graphicx}
\usepackage{titlesec}
\usepackage{setspace}
\usepackage{fancyhdr}

% Define custom colors - using RGB values divided by 255
\definecolor{primaryOrange}{rgb}{0.996, 0.624, 0.169}
\definecolor{primaryBlue}{rgb}{0.039, 0.098, 0.184}

% Configure page geometry
\geometry{
    a4paper,
    margin=1in,
    top=1.5in
}

% Use standard sans-serif font instead of Courier
\renewcommand{\familydefault}{\sfdefault}

% Custom header style
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}

% Customize hyperlinks
\hypersetup{
    colorlinks=true,
    linkcolor=primaryOrange,
    filecolor=primaryOrange,
    urlcolor=primaryOrange,
}

""",
            # Header information with modern styling
            "\\begin{document}\n",
            
            # Contact information block
            "\\begin{flushright}\n"
            f"\\textcolor{{primaryBlue}}{{\\Large {personal['name']}}}\\\\\n"
            f"\\textcolor{{primaryBlue}}{{{personal['address']['line']}}}\\\\\n"
            f"\\textcolor{{primaryBlue}}{{{personal['address']['postal_code']}, {personal['address']['country']}}}\\\\\n"
            f"\\textcolor{{primaryOrange}}{{Phone: {personal['phone']['mobile']}}}\\\\\n"
            f"\\textcolor{{primaryOrange}}{{Email: {personal['email']}}}\\\\\n"
            f"\\textcolor{{primaryOrange}}{{Web: \\href{{{personal['homepage']}}}{{{personal['homepage']}}}}}\n"
            "\\end{flushright}\n\n",
            
            f"\\vspace{{20pt}}\n",
            
            # Date
            f"\\noindent{{\\today}}\\\\[20pt]\n",
            
            # Recipient
            f"\\textcolor{{primaryBlue}}{{{recipient['name']}}}\\\\\n"
            f"\\textcolor{{primaryBlue}}{{{recipient['address']}}}\\\\\n",
            
            f"\\vspace{{20pt}}\n",
            
            # Opening
            f"\\textcolor{{primaryBlue}}{{\\textbf{{{letter['opening']}}}}}\\\\\n",
            
            f"\\vspace{{20pt}}\n",
            
            # Body with better spacing
            "\\onehalfspacing\n"
            f"{letter['body']}\n\n",
            
            f"\\vspace{{20pt}}\n",
            
            # Closing
            f"\\textcolor{{primaryBlue}}{{{letter['closing']}}},\\\\\n"
            f"\\vspace{{30pt}}\n"
            f"\\textcolor{{primaryBlue}}{{{personal['name']}}}\n",
            
            # Enclosures
            f"\\vspace{{20pt}}\n"
            f"\\textcolor{{primaryOrange}}{{\\textbf{{Enclosure:}} {letter['enclosure']}}}\n",
            
            "\\end{document}"
        ]
        
        return '\n\n'.join(content)

    def save_cover_letter(self, yaml_file, output_dir, company_name):
        """Save the cover letter to a tex file"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        tex_content = self.generate_tex(company_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tex_file = os.path.join(output_dir, f"cover_letter_{timestamp}.tex")
        
        with open(tex_file, 'w') as tex:
            tex.write(tex_content)
            
        return tex_file
    
    def generate_pdf(self, yaml_file, output_dir, company_name):
        """Generate PDF from YAML file"""
        # First generate the tex file
        try:
            tex_file = self.save_cover_letter(yaml_file, output_dir, company_name)
            
            # Then compile it to PDF
            pdf_file = self.compile_pdf(tex_file, output_dir)
            
            return tex_file, pdf_file
        except Exception as e:
            print(f"Failed to generate PDF: {str(e)}")
            raise
    

    def compile_pdf(self, tex_file, output_dir):
        """Compile LaTeX file to PDF using pdflatex"""
        try:
            output_dir = os.path.dirname(tex_file)
            
            # More thorough diagnostics
            diagnostic_commands = [
                ('kpsewhich moderncv.cls', 'Checking moderncv location'),
                ('kpsewhich -var-value=TEXMFHOME', 'Checking TEXMFHOME'),
                ('kpsewhich -var-value=TEXMFLOCAL', 'Checking TEXMFLOCAL'),
                ('kpsewhich -var-value=TEXMFSYSVAR', 'Checking TEXMFSYSVAR'),
                ('texhash --verbose', 'Refreshing TeX database'),
            ]
            
            diagnostic_info = []
            for cmd, desc in diagnostic_commands:
                result = subprocess.run(cmd.split(), capture_output=True, text=True)
                diagnostic_info.append(f"{desc}:\n{result.stdout or result.stderr}")
            
            # Check if moderncv is installed
            result = subprocess.run(['kpsewhich', 'moderncv.cls'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(
                    "moderncv LaTeX class not found. Diagnostic information:\n\n" + 
                    "\n".join(diagnostic_info) + 
                    "\n\nTry running:\n" +
                    "1. sudo texhash\n" +
                    "2. mktexlsr\n" +
                    "3. Check if the file exists: find /usr/local/texlive -name 'moderncv.cls'"
                )
            
            # Run pdflatex twice to ensure proper generation of references
            for _ in range(2):
                result = subprocess.run([
                    'pdflatex',
                    '-interaction=nonstopmode',
                    '-output-directory=' + output_dir,
                    tex_file
                ], check=True, capture_output=True, text=True)
                
                # Print LaTeX compilation output if there's an error
                if result.returncode != 0:
                    print("LaTeX Error Output:")
                    print(result.stdout)
                    print(result.stderr)
            
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
        except Exception as e:
            raise Exception(f"Failed to generate PDF: {str(e)}")

# Example Usage
# generator = CoverLetterGenerator('cover_letter.yml')
# print(generator.generate_cover_letter())
