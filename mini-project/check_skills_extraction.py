import os
import sys
import logging
import json
import re
from pdfminer.high_level import extract_text

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import the ResumeParser class
from resume_parser import ResumeParser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_pdf(file_path):
    """Extract text from a PDF file."""
    try:
        text = extract_text(file_path)
        return text
    except Exception as e:
        logger.error(f"Error reading PDF: {e}")
        return None

def main():
    # Path to the resume PDF file
    resume_path = os.path.join(os.path.dirname(__file__), '10985403.pdf')
    
    # Read the resume PDF
    logger.info(f"Reading resume: {resume_path}")
    resume_text = read_pdf(resume_path)
    
    if resume_text is None:
        logger.error("Failed to read resume")
        return
    
    # Initialize the ResumeParser
    logger.info("Initializing ResumeParser")
    parser = ResumeParser()
    
    # Create a resume dictionary with content
    resume_dict = {"content": resume_text}
    
    # Parse the resume
    logger.info("Parsing resume")
    parsed_resume = parser.parse_resume(resume_dict)
    
    # Write output to a file
    output_file = "skills_detailed_output.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        # Print the extracted skills
        f.write("\nExtracted Skills:\n")
        if 'skills' in parsed_resume and parsed_resume['skills']:
            for skill in parsed_resume['skills']:
                f.write(f"  - {skill}\n")
        else:
            f.write("  No skills extracted\n")
        
        # Print the raw skills section from the resume
        f.write("\nRaw Skills Section:\n")
        skills_section_match = re.search(r'(?i)\bSKILLS\b.*?(?:\n\n|\Z)', resume_text, re.DOTALL)
        if skills_section_match:
            skills_section = skills_section_match.group(0)
            f.write(skills_section + "\n")
        else:
            f.write("  No skills section found\n")
        
        # Print all keys in the parsed resume
        f.write("\nParsed Resume Keys:\n")
        for key in parsed_resume.keys():
            f.write(f"  - {key}\n")
            
        # Print the skills specifically
        f.write("\nSkills from parsed_resume['skills']:\n")
        if 'skills' in parsed_resume:
            f.write(json.dumps(parsed_resume['skills'], indent=2) + "\n")
        else:
            f.write("  No 'skills' key in parsed_resume\n")
    
    print(f"Output written to {output_file}")

if __name__ == "__main__":
    main()