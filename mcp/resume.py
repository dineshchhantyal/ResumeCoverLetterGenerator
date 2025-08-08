from mcp.server.fastmcp import FastMCP
import xml.etree.ElementTree as ET

app = FastMCP()
resume_path = (
    "/Users/dineshchhantyal/Documents/ResumeCoverLetterGenerator/mcp/resume.xml"
)


# Parse a section from resume.xml
def get_section_from_resume(xml_path: str, section: str) -> str:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    if section.lower() == "all":
        return ET.tostring(root, encoding="unicode")
    section_element = root.find(section)
    if section_element is not None:
        return ET.tostring(section_element, encoding="unicode")
    return ""


# Tool to extract a section (or all) from resume.xml
@app.tool(
    name="get_section",
    description="Extract a specific section from the resume XML file. Options: 'experience', 'projects', 'skills', 'summary', 'involvements', or 'all' to get the full resume.",
)
def get_resume_section(section: str):
    content = get_section_from_resume(resume_path, section.lower())
    return (
        f"{section.capitalize()}:\n{content}"
        if content
        else f"No content found for section: {section}"
    )


# Tool to extract the research section from resume.xml
@app.tool(
    name="get_research_section",
    description="Get the research section from the resume XML file.",
)
def get_research_section():
    content = get_section_from_resume(resume_path, "research")
    return (
        f"Research Section:\n{content}"
        if content
        else "No content found for research section."
    )


# Tool to extract the awards section from resume.xml
@app.tool(
    name="get_awards_section",
    description="Get the awards section from the resume XML file.",
)
def get_awards_section():
    content = get_section_from_resume(resume_path, "awards")
    return (
        f"Awards Section:\n{content}"
        if content
        else "No content found for awards section."
    )


@app.tool(
    name="get_all_sections", description="Get all sections from the resume XML file."
)
def get_all_resume_sections():
    content = get_section_from_resume(resume_path, "all")
    return (
        f"All Sections:\n{content}" if content else "No content found for any section."
    )


@app.tool(
    name="get_experience_section",
    description="Get the experience section from the resume XML file.",
)
def get_experience_section():
    content = get_section_from_resume(resume_path, "experience")
    return (
        f"Experience Section:\n{content}"
        if content
        else "No content found for experience section."
    )


@app.tool(
    name="get_projects_section",
    description="Get the projects section from the resume XML file.",
)
def get_projects_section():
    content = get_section_from_resume(resume_path, "projects")
    return (
        f"Projects Section:\n{content}"
        if content
        else "No content found for projects section."
    )


@app.tool(
    name="get_involvements_section",
    description="Get the involvements section from the resume XML file.",
)
def get_involvements_section():
    content = get_section_from_resume(resume_path, "involvements")
    return (
        f"Involvements Section:\n{content}"
        if content
        else "No content found for involvements section."
    )


@app.tool(
    name="get_skills_section",
    description="Get the skills section from the resume XML file.",
)
def get_skills_section():
    content = get_section_from_resume(resume_path, "skills")
    return (
        f"Skills Section:\n{content}"
        if content
        else "No content found for skills section."
    )


@app.tool(
    name="get_summary_section",
    description="Get the summary section from the resume XML file.",
)
def get_summary_section():
    content = get_section_from_resume(resume_path, "summary")
    return (
        f"Summary Section:\n{content}"
        if content
        else "No content found for summary section."
    )


@app.tool(
    name="get_certifications_section",
    description="Get the certifications section from the resume XML file.",
)
def get_certifications_section():
    content = get_section_from_resume(resume_path, "certifications")
    return (
        f"Certifications Section:\n{content}"
        if content
        else "No content found for certifications section."
    )


@app.tool(
    name="experience_tool",
    description="Refine the experience section to highlight relevant experience, achievements, and skills for a job.",
)
def experience_tool(job_description: str, resume_experience: str) -> str:
    return f"""
    Job Description:
    {job_description}

    Resume Experience:
    {resume_experience}

    Task:
    Rewrite the experience section to better align with the job role.
    Emphasize relevant experience, achievements, and skills.
    Remove unrelated content and highlight transferable experience.
    Return only the rewritten experience section.
    """


@app.tool(
    name="projects_tool",
    description="Select and refine the most relevant projects based on the job description.",
)
def projects_tool(job_description: str, resume_projects: str) -> str:
    return f"""
    Job Description:
    {job_description}

    Resume Projects:
    {resume_projects}

    Task:
    Identify 2–3 projects most relevant to the job.
    Rewrite them to align with responsibilities, required skills, and outcomes.
    Use action verbs and quantify achievements where possible.
    Return only the refined project descriptions.
    """


@app.tool(
    name="involvements_tool",
    description="Refine leadership and involvement activities to emphasize impact and alignment with company values.",
)
def involvements_tool(job_description: str, resume_involvements: str) -> str:
    return f"""
    Job Description:
    {job_description}

    Resume Involvements:
    {resume_involvements}

    Task:
    Highlight leadership/involvements relevant to the company mission, collaboration, or soft skills.
    Rewrite to emphasize impact and alignment with company values.
    Return only the revised involvement section.
    """


@app.tool(
    name="skills_tool",
    description="Match and reorder skills based on the job posting. Emphasize those mentioned in the job.",
)
def skills_tool(job_description: str, resume_skills: str) -> str:
    return f"""
    Job Description:
    {job_description}

    Resume Skills:
    {resume_skills}

    Task:
    Reorder, add, or remove skills to match the technical and soft skill requirements in the job.
    Emphasize skills mentioned in the job posting.
    Return only the revised list of skills.
    """


@app.tool(
    name="summary_tool",
    description="Rewrite the summary section to target a specific job with confidence and relevance.",
)
def summary_tool(job_description: str, resume_summary: str) -> str:
    return f"""
    Job Description:
    {job_description}

    Current Summary:
    {resume_summary}

    Task:
    Rewrite the summary to target this specific job.
    Use a confident and professional tone.
    Focus on relevant experience, achievements, and motivation for the role.
    Return only the revised summary.
    """


@app.tool(
    name="refine_all",
    description="Refine all resume sections ('summary', 'experience', 'projects', 'involvements', 'skills') to align with the job description.",
)
def refine_all(
    job_description: str,
    experience: str,
    projects: str,
    involvements: str,
    skills: str,
    summary: str,
):
    return {
        "summary": summary_tool(job_description, summary),
        "experience": experience_tool(job_description, experience),
        "projects": projects_tool(job_description, projects),
        "involvements": involvements_tool(job_description, involvements),
        "skills": skills_tool(job_description, skills),
    }


if __name__ == "__main__":
    app.run(transport="stdio")
