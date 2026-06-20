from datetime import datetime
import os
import sys
import shutil
from resume.generator import ResumeGenerator
from resume.tailor import tailor_resume, classify_role
from coverletter.generator import CoverLetterGenerator


def create_output_structure(base_dir, company_name):
    """Create output directory: applications/COMPANY/"""
    company_dir = company_name.replace(' ', '_').replace('/', '_').replace('\\', '_')
    output_path = os.path.join(base_dir, "applications", company_dir)
    os.makedirs(output_path, exist_ok=True)
    return output_path


def generate_filename(role_name, file_type, candidate_name="Candidate"):
    """Generate filename: CandidateName_Resume_PositionTitle.pdf"""
    position_title = role_name.replace(' ', '').replace('/', '').replace('\\', '').replace('&', 'and')
    name = candidate_name.replace(' ', '_').replace('/', '_').replace('\\', '_')
    return f"{name}_{file_type.capitalize()}_{position_title}"


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Generate tailored resume and cover letter PDFs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Workflow:
  Step 1 - Tailor YAML:   python main.py --company X --role Y --type resume --step tailor
  Step 2 - Edit YAML:     Edit applications/X/resume.yml as needed
  Step 3 - Generate PDF:  python main.py --company X --role Y --type resume --step generate

  Or do both at once:     python main.py --company X --role Y --type resume
        """
    )
    parser.add_argument('--ui', action='store_true', help='Launch GUI version')
    parser.add_argument('--company', type=str, required=False, help='Company name (REQUIRED)')
    parser.add_argument('--role', type=str, required=False, help='Role name (REQUIRED)')
    parser.add_argument('--type', type=str, choices=['resume', 'coverletter', 'both'],
                        required=False, help='What to generate (REQUIRED)')
    parser.add_argument('--url', type=str, default='', help='Job description URL (optional)')
    parser.add_argument('--step', type=str, choices=['tailor', 'generate', 'all'], default='all',
                        help='tailor = create tailored YAML only, generate = PDF from existing YAML, all = both (default)')
    args = parser.parse_args()

    if args.ui:
        try:
            from ui import main as ui_main
            ui_main()
        except ImportError as e:
            print(f"\nError: PyQt6 is not properly installed. {e}")
        return

    # Validate required args
    if not args.company:
        parser.error("--company is required. Example: --company 'Google'")
    if not args.role:
        parser.error("--role is required. Example: --role 'Software Engineer New Grad'")
    if not args.type:
        parser.error("--type is required. Choices: resume, coverletter, both")

    base_dir = os.getcwd()
    output_dir = create_output_structure(base_dir, args.company)

    # Save job description URL if provided
    if args.url:
        with open(os.path.join(output_dir, 'job_description.txt'), 'w') as f:
            f.write(f"URL: {args.url}\n\n")

    # --- RESUME ---
    if args.type in ['resume', 'both']:
        base_resume = os.path.join(base_dir, "resume", "resume.yml")
        tailored_yaml = os.path.join(output_dir, "resume.yml")
        base_name = generate_filename(args.role, 'Resume')
        pdf_file = os.path.join(output_dir, base_name + ".pdf")
        tex_file = os.path.join(output_dir, base_name + ".tex")

        # STEP 1: Tailor YAML
        if args.step in ['tailor', 'all']:
            if not os.path.exists(base_resume):
                print(f"Error: Base resume not found at {base_resume}")
                sys.exit(1)

            shutil.copy2(base_resume, tailored_yaml)
            tailor_resume(tailored_yaml, args.role, args.company)
            role_type = classify_role(args.role, args.company)
            print(f"\n  [Tailored for: {role_type}]")
            print(f"  YAML saved: {tailored_yaml}")

            if args.step == 'tailor':
                print(f"\n  >> Edit the YAML above, then run:")
                print(f"     python main.py --company '{args.company}' --role '{args.role}' --type resume --step generate")
                return

        # STEP 2: Generate PDF from YAML
        if args.step in ['generate', 'all']:
            if not os.path.exists(tailored_yaml):
                print(f"Error: Tailored YAML not found at {tailored_yaml}")
                print(f"  Run with --step tailor first to create it.")
                sys.exit(1)

            resume_generator = ResumeGenerator(tailored_yaml)
            output_file = resume_generator.generate_pdf(tex_file, output_dir)
            print(f"\nResume generated: {output_file}")

    # --- COVER LETTER ---
    if args.type in ['coverletter', 'both']:
        base_name = generate_filename(args.role, 'CoverLetter')
        cover_letter_file = os.path.join(output_dir, base_name + ".tex")
        coverletter_generator = CoverLetterGenerator(os.path.join(base_dir, "coverletter", "coverletter.yml"))
        output_file = coverletter_generator.generate_pdf(cover_letter_file, output_dir, args.company)
        print(f"\nCover letter generated: {output_file}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
