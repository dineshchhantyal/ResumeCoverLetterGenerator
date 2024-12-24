from abc import ABC, abstractmethod
import os
import subprocess
import yaml

class DocumentGenerator(ABC):
    def __init__(self, yaml_file):
        with open(yaml_file, 'r') as file:
            self.data = yaml.safe_load(file)
    
    @abstractmethod
    def generate_tex(self, tex_file):
        """Generate a LaTeX file from the YAML data."""
        pass

    def generate_pdf(self, tex_file, output_dir):
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
        except Exception as e:
            raise Exception(f"Failed to generate PDF: {str(e)}") 