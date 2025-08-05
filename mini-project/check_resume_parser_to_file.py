import sys
import logging
import fitz  # PyMuPDF
from pathlib import Path

# Configure logging to write to a file
log_file = Path("d:\\tmp\\mini-project\\resume_parser_log.txt")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Output file
output_file = Path("d:\\tmp\\mini-project\\resume_parser_output.txt")

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
    # Open the output file
    with open(output_file, 'w') as f:
        # Path to the resume file
        resume_path = Path("D:\\tmp\\mini-project\\10985403.pdf")
        
        # Read the resume content
        try:
            resume_content = read_pdf(resume_path)
            logger.info(f"Successfully read resume: {resume_path}")
            
            # Write first 200 characters of the resume content
            f.write(f"\nResume content (first 200 chars):\n{resume_content[:200]}...\n")
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
            
            # Write the extracted skills
            skills = parsed_resume.get("skills", [])
            f.write(f"\nExtracted skills ({len(skills)}):\n{skills}\n")
            
            # Write other extracted information
            f.write(f"\nName: {parsed_resume.get('name', '')}\n")
            f.write(f"Email: {parsed_resume.get('email', '')}\n")
            f.write(f"Phone: {parsed_resume.get('phone', '')}\n")
            f.write(f"Location: {parsed_resume.get('location', '')}\n")
            
            # Write education information
            education = parsed_resume.get("education", [])
            f.write(f"\nEducation ({len(education)}):\n")
            for edu in education:
                f.write(f"  - {edu}\n")
            
            # Write experience information
            experience = parsed_resume.get("experience", [])
            f.write(f"\nExperience ({len(experience)}):\n")
            for exp in experience:
                f.write(f"  - {exp}\n")
            
        except Exception as e:
            logger.error(f"Error parsing resume: {e}")

if __name__ == "__main__":
    main()
    print(f"Output written to {output_file}")