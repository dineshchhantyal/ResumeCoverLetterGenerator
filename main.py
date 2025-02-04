from datetime import datetime
import os
from resume.generator import ResumeGenerator
from coverletter.generator import CoverLetterGenerator

def get_user_choice():
    while True:
        print("\nWhat would you like to generate?")
        print("1. Resume only")
        print("2. Cover Letter only")
        print("3. Both Resume and Cover Letter")
        choice = input("Enter your choice (1-3): ")

        if choice in ['1', '2', '3']:
            return choice

def get_job_description_url():
    return input("\nEnter job description URL (press Enter to skip): ").strip()

def get_company_name():
    return input("\nEnter company name: ").strip()

def get_role_name():
    """Get role name from user"""
    return input("\nEnter role name (e.g. Software Engineer Intern): ").strip()

def create_output_structure(base_dir, company_name, role_name):
    """Create organized output directory structure"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    date_dir = datetime.now().strftime("%Y%m%d")

    structure = {
        'company': company_name.lower().replace(' ', '_'),
        'role': role_name.lower().replace(' ', '_'),
        'date': date_dir,
        'timestamp': timestamp
    }

    output_path = os.path.join(
        base_dir,
        "applications",
        structure['company'],
        structure['role'],
        structure['date'],
        structure['timestamp']
    )

    os.makedirs(output_path, exist_ok=True)
    return output_path

def cli_main():
    base_dir = os.getcwd()
    company_name = get_company_name()
    role_name = get_role_name()
    job_url = get_job_description_url()

    # Create organized output directory
    output_dir = create_output_structure(base_dir, company_name, role_name)

    # Save job description if provided
    if job_url:
        with open(os.path.join(output_dir, 'job_description.txt'), 'w') as f:
            f.write(f"URL: {job_url}\n\n")
            # TODO: Add job description scraping

    choice = get_user_choice()

    # Generate documents based on user choice
    if choice in ['1', '3']:
        resume_file = os.path.join(output_dir, 'resume.pdf')
        resume_generator = ResumeGenerator(os.path.join(base_dir, "resume", "resume.yml"))
        output_file = resume_generator.generate_pdf(resume_file, output_dir)
        print(f"\nResume generated: {output_file}")

    if choice in ['2', '3']:
        cover_letter_file = os.path.join(output_dir, 'cover_letter.pdf')
        coverletter_generator = CoverLetterGenerator(os.path.join(base_dir, "coverletter", "coverletter.yml"))
        output_file = coverletter_generator.generate_pdf(cover_letter_file, output_dir, company_name)
        print(f"\nCover letter generated: {output_file}")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--ui', action='store_true', help='Launch GUI version')
    args = parser.parse_args()

    if args.ui:
        try:
            from ui import main as ui_main
            ui_main()
        except ImportError as e:
            print("\nError: PyQt6 is not properly installed.")
            print("Please run: pip install PyQt6 PyQt6-Qt6 PyQt6-sip")
            print(f"Original error: {str(e)}")
        except Exception as e:
            print(f"\nFailed to start UI: {str(e)}")
    else:
        cli_main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
