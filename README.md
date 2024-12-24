# Resume & Cover Letter Generator

A Python-based tool that generates professional resumes and cover letters using LaTeX templates. This tool allows you to maintain your professional information in YAML files and generates beautifully formatted PDF documents.

## 🌟 Features

- Generate professional resumes and cover letters from YAML files
- Modern, clean design with customizable colors
- Consistent formatting across documents
- Support for both resume and cover letter generation
- Easy-to-maintain YAML-based content
- Professional LaTeX templates
- Custom color schemes (default: Orange & Navy Blue)

## 🔧 Prerequisites

- Python 3.6+
- LaTeX distribution (TeX Live or MiKTeX)
- Required Python packages:
  ```bash
  pip install pyyaml
  ```

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/resume-cover-letter-generator.git
cd resume-cover-letter-generator
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Run the script:

```bash
python main.py
```

3. Ensure you have a LaTeX distribution installed:
   - For MacOS: Install [MacTeX](https://www.tug.org/mactex/)
   - For Linux: `sudo apt-get install texlive-full`
   - For Windows: Install [MiKTeX](https://miktex.org/)

## 🚀 Usage

1. Update your information in the YAML files:
   - `resume/resume.yml` for resume content
   - `coverletter/coverletter.yml` for cover letter content

2. Run the generator:

```bash
python main.py
```

3. Follow the interactive prompts:
   - Choose to generate resume, cover letter, or both
   - Enter company name
   - Enter job description URL (optional)


4. Find your generated documents in the `output/{company_name}` directory

## 📄 YAML File Structure

### Resume YAML Structure

```yaml
personal:
name: Your Name
email: your.email@example.com
phone: "+1 (123) 456-7890"
website: https://yourwebsite.com
linkedin: https://linkedin.com/in/yourprofile
education:
name: University Name
location: City, State
degree: Degree Name
date: Graduation Date
courses: Relevant Coursework
experience:
title: Job Title
company: Company Name
location: City, State
date: Employment Period
achievements:
Achievement 1
Achievement 2
```

### Cover Letter YAML Structure

```yaml
personal_information:
name: Your Name
title: Your Title
address:
line: Street Address
postal_code: Postal Code
country: Country
phone:
mobile: "+1 (123) 456-7890"
email: your.email@example.com
homepage: https://yourwebsite.com
recipient:
name: Recipient Name
address: Company Address
letter:
date: Application Date
opening: Dear Hiring Manager,
body: Your cover letter content...
closing: Best regards
```


## 🎨 Customization

The templates use two primary colors:
- Orange: rgb(254, 159, 43)
- Navy Blue: rgb(10, 25, 47)

To customize colors, modify the RGB values in the LaTeX templates in `generator.py` files.

## 📝 License

This project is licensed under the Creative Commons Attribution-NonCommercial (CC BY-NC) license - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- LaTeX for beautiful document formatting
- Python YAML for easy data management
- The open-source community for inspiration and resources

## 📞 Support

For support, please open an issue in the GitHub repository or contact [myagdichhantyal@gmail.com](mailto:myagdichhantyal@gmail.com).