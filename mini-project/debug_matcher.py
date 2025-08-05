import pandas as pd
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Resume skills from the PDF
resume_skills = [
    '3D', 'ANSYS', 'AutoCAD', 'automation', 'Automotive', 'CAD/CAM', 'CAD', 'CATIA', 
    'Engineering Analysis', 'lathe', 'Manufacturing process', 'Materials', 
    'material selection', 'Oil', 'Optimization', 'prototyping', 'Robotic', 
    'safety', 'simulation', 'SolidWorks', 'SPC', 'statistical analysis', 'welding'
]

# Create a mock resume dictionary
mock_resume = {
    "file_name": "10985403.pdf",
    "skills": resume_skills,
    "location": ""
}

# Load job listings
job_df = pd.read_csv('C:\\Users\\ASUS\\Downloads\\job_listings.csv')

# Convert DataFrame to list of dictionaries
jobs = job_df.to_dict(orient="records")

# Process required_skills to convert from string to list if needed
for job in jobs:
    if "required_skills" in job and isinstance(job["required_skills"], str):
        job["required_skills"] = [skill.strip() for skill in job["required_skills"].split(",")]
    elif "required_skills" not in job:
        job["required_skills"] = []

# Implement the matcher's skill matching logic
def calculate_skill_match_score(resume, job):
    """Calculate skill match score between resume and job."""
    # Get resume skills
    resume_skills = set()
    if "skills" in resume and resume["skills"]:
        resume_skills = {skill.lower() for skill in resume["skills"]}
    
    # Get job skills
    job_skills = set()
    
    # First try required_skills
    if "required_skills" in job and job["required_skills"]:
        if isinstance(job["required_skills"], list):
            job_skills.update({skill.lower() for skill in job["required_skills"]})
        elif isinstance(job["required_skills"], str):
            job_skills.add(job["required_skills"].lower())
    
    # Then try extracted_skills
    if "extracted_skills" in job and job["extracted_skills"]:
        job_skills.update({skill.lower() for skill in job["extracted_skills"]})
    
    # If no skills found, return 0
    if not resume_skills or not job_skills:
        logger.warning(f"No skills found. Resume skills: {len(resume_skills)}, Job skills: {len(job_skills)}")
        return 0.0, [], []
    
    # Calculate Jaccard similarity
    matching_skills = resume_skills.intersection(job_skills)
    all_skills = resume_skills.union(job_skills)
    
    if not all_skills:
        return 0.0, [], []
    
    # Get missing skills
    missing_skills = job_skills - resume_skills
    
    return len(matching_skills) / len(all_skills), list(matching_skills), list(missing_skills)

# Match the resume with all jobs
print(f"Resume skills ({len(resume_skills)}): {resume_skills}\n")

results = []
for i, job in enumerate(jobs):
    title = job.get('title', f'Job {i+1}')
    required_skills = job.get('required_skills', [])
    
    # Calculate skill match score
    score, matching_skills, missing_skills = calculate_skill_match_score(mock_resume, job)
    
    results.append({
        'job_id': job.get('job_id', i),
        'title': title,
        'required_skills': required_skills,
        'matching_skills': matching_skills,
        'missing_skills': missing_skills,
        'skill_score': score
    })
    
    print(f"Job {i+1}: {title}")
    print(f"  Required skills ({len(required_skills)}): {required_skills}")
    print(f"  Matching skills ({len(matching_skills)}): {matching_skills}")
    print(f"  Missing skills ({len(missing_skills)}): {missing_skills}")
    print(f"  Skill match score: {score:.4f}\n")

# Sort by skill score
results.sort(key=lambda x: x['skill_score'], reverse=True)

# Print top 3 matches
print("Top 3 job matches by skill score:")
for i, result in enumerate(results[:3]):
    print(f"\nRank {i+1}: {result['title']} (Score: {result['skill_score']:.4f})")
    print(f"  Required skills ({len(result['required_skills'])}): {result['required_skills']}")
    print(f"  Matching skills ({len(result['matching_skills'])}): {result['matching_skills']}")
    print(f"  Missing skills ({len(result['missing_skills'])}): {result['missing_skills']}")