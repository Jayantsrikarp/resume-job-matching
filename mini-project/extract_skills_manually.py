import os
import re
import json
from pdfminer.high_level import extract_text

def read_pdf(file_path):
    """Extract text from a PDF file."""
    try:
        text = extract_text(file_path)
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def extract_skills_section(text):
    """Extract the skills section from the resume text."""
    # Look for the skills section which starts with 'Skills' and continues until multiple newlines
    skills_section_match = re.search(r'(?i)\bSkills\b[^\n]*(?:\n[^\n]+)*', text)
    if skills_section_match:
        return skills_section_match.group(0)
    return None

def extract_skills_from_section(skills_section):
    """Extract individual skills from the skills section."""
    if not skills_section:
        return []
    
    # Remove the 'SKILLS' header
    skills_text = re.sub(r'(?i)^\s*Skills\s*', '', skills_section).strip()
    
    # Split by commas
    skills = re.split(r',', skills_text)
    
    # Clean up each skill
    cleaned_skills = []
    for skill in skills:
        skill = skill.strip()
        if skill and len(skill) > 1:  # Ignore single characters or empty strings
            cleaned_skills.append(skill)
    
    return cleaned_skills

def main():
    # Path to the resume PDF file
    resume_path = os.path.join(os.path.dirname(__file__), '10985403.pdf')
    
    # Read the resume PDF
    print(f"Reading resume: {resume_path}")
    resume_text = read_pdf(resume_path)
    
    if resume_text is None:
        print("Failed to read resume")
        return
    
    # Print a portion of the resume text to see its structure
    print("\nPortion of resume text:")
    print(resume_text[resume_text.lower().find("skills"):resume_text.lower().find("skills")+500])
    
    # Extract the skills section
    skills_section = extract_skills_section(resume_text)
    
    # Extract skills from the section
    skills = extract_skills_from_section(skills_section)
    
    # Write output to a file
    output_file = "manual_skills_extraction.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Raw Skills Section:\n")
        if skills_section:
            f.write(skills_section + "\n\n")
        else:
            f.write("No skills section found\n\n")
        
        f.write("Extracted Skills:\n")
        if skills:
            for skill in skills:
                f.write(f"  - {skill}\n")
        else:
            f.write("No skills extracted\n")
        
        f.write("\nTotal Skills Extracted: " + str(len(skills)))
    
    print(f"\nOutput written to {output_file}")
    
    # Also print the first 10 skills to console
    print("\nFirst 10 extracted skills:")
    for skill in skills[:10]:
        print(f"  - {skill}")

if __name__ == "__main__":
    main()