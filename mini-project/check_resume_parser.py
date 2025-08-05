import sys
import logging
import fitz  # PyMuPDF
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Import the ResumeParser class
sys.path.append('d:\\tmp\\mini-project\\src')
try:
    from resume_parser import ResumeParser
    logger.info("Successfully imported ResumeParser")
except ImportError as e:
    logger.error(f"Error importing ResumeParser: {e}")
    sys.exit(1)

# Function to read PDF content
def read_pdf(file_path):
    """Read text content from a PDF file."""
    try:
        text = ""
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()
        return text
    except Exception as e:
        logger.error(f"Error reading PDF {file_path}: {str(e)}")
        raise

# Main function
def main():
    # Path to the resume file
    resume_path = Path("D:\\tmp\\mini-project\\10985403.pdf")
    
    # Read the resume content
    try:
        resume_content = read_pdf(resume_path)
        logger.info(f"Successfully read resume: {resume_path}")
        
        # Print first 200 characters of the resume content
        print(f"\nResume content (first 200 chars):\n{resume_content[:200]}...")
    except Exception as e:
        logger.error(f"Error reading resume: {e}")
        return
    
    # Create a resume dictionary
    resume = {
        "file_path": str(resume_path),
        "file_name": resume_path.name,
        "content": resume_content,
        "file_type": "pdf"
    }
    
    # Initialize the ResumeParser
    parser = ResumeParser()
    logger.info("Initialized ResumeParser")
    
    # Parse the resume
    try:
        parsed_resume = parser.parse_resume(resume)
        logger.info("Successfully parsed resume")
        
        # Print the extracted skills
        skills = parsed_resume.get("skills", [])
        print(f"\nExtracted skills ({len(skills)}):\n{skills}")
        
        # Print other extracted information
        print(f"\nName: {parsed_resume.get('name', '')}")
        print(f"Email: {parsed_resume.get('email', '')}")
        print(f"Phone: {parsed_resume.get('phone', '')}")
        print(f"Location: {parsed_resume.get('location', '')}")
        
        # Print education information
        education = parsed_resume.get("education", [])
        print(f"\nEducation ({len(education)}):")
        for edu in education:
            print(f"  - {edu}")
        
        # Print experience information
        experience = parsed_resume.get("experience", [])
        print(f"\nExperience ({len(experience)}):")
        for exp in experience:
            print(f"  - {exp}")
        
    except Exception as e:
        logger.error(f"Error parsing resume: {e}")

if __name__ == "__main__":
    main()