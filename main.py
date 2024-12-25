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

def main():
    choice = get_user_choice()
    company_name = get_company_name()
    job_url = get_job_description_url()
    
    # Get base directory and create paths using os.path
    base_dir = os.getcwd()
    resume_yml = os.path.join(base_dir, "resume", "resume.yml")
    coverletter_yml = os.path.join(base_dir, "coverletter", "coverletter.yml")
    
    # Initialize generators with YAML files
    resume_generator = ResumeGenerator(resume_yml)
    coverletter_generator = CoverLetterGenerator(coverletter_yml)
    
    # Create output directory with company name
    output_dir = os.path.join(base_dir, "output", company_name, datetime.now().strftime("%b%d%Y").upper())

    os.makedirs(output_dir, exist_ok=True)

    job_description = None
    if job_url:
        # TODO: Implement web scraping and AI processing
        # job_description = scrape_and_process_job(job_url)
        pass

    # Generate documents based on user choice
    if choice in ['1', '3']:
        output_file = resume_generator.generate_pdf(resume_yml, output_dir)
        print(f"\nResume generated: {output_file}")

    if choice in ['2', '3']:
        output_file = coverletter_generator.generate_pdf(coverletter_yml, output_dir, company_name)
        print(f"\nCover letter generated: {output_file}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
