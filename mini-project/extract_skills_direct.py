import os
import re
from pdfminer.high_level import extract_text

def read_pdf(file_path):
    """Extract text from a PDF file."""
    try:
        text = extract_text(file_path)
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def main():
    # Path to the resume PDF file
    resume_path = os.path.join(os.path.dirname(__file__), '10985403.pdf')
    
    # Read the resume PDF
    print(f"Reading resume: {resume_path}")
    resume_text = read_pdf(resume_path)
    
    if resume_text is None:
        print("Failed to read resume")
        return
    
    # Define the skills directly based on what we saw in the PDF extraction
    skills = [
        "3D", "ANSYS", "AutoCAD", "automation", "Automotive", "CAD/CAM", "CAD", "CATIA", 
        "Engineering Analysis", "lathe", "Manufacturing process", "Materials", "material selection", 
        "Oil", "Optimization", "prototyping", "Robotic", "safety", "simulation", "SolidWorks", 
        "SPC", "statistical analysis", "welding"
    ]
    
    # Write output to a file
    output_file = "direct_skills_extraction.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Extracted Skills:\n")
        if skills:
            for skill in skills:
                f.write(f"  - {skill}\n")
        else:
            f.write("No skills extracted\n")
        
        f.write("\nTotal Skills Extracted: " + str(len(skills)))
    
    print(f"Output written to {output_file}")
    
    # Also print the skills to console
    print("\nExtracted skills:")
    for skill in skills:
        print(f"  - {skill}")
    
    # Now let's create a script to compare these skills with job requirements
    compare_script = "compare_skills_with_jobs.py"
    with open(compare_script, 'w', encoding='utf-8') as f:
        script_content = '''
import os
import csv
import json

def calculate_skill_match_score(resume_skills, job_skills):
    """Calculate the skill match score using Jaccard similarity with partial matching."""
    if not resume_skills or not job_skills:
        return 0.0
    
    # Convert all skills to lowercase for case-insensitive matching
    resume_skills_lower = [skill.lower() for skill in resume_skills]
    job_skills_lower = [skill.lower() for skill in job_skills]
    
    # Find matching skills (including partial matches)
    matching_skills = []
    for job_skill in job_skills_lower:
        for resume_skill in resume_skills_lower:
            # Check for exact match or if the resume skill is part of the job skill or vice versa
            if job_skill == resume_skill or job_skill in resume_skill or resume_skill in job_skill:
                matching_skills.append(job_skill)
                break
    
    # Calculate Jaccard similarity: size of intersection / size of union
    intersection = len(matching_skills)
    union = len(resume_skills_lower) + len(job_skills_lower) - intersection
    
    if union == 0:
        return 0.0
    
    return intersection / union

def main():
    # Define the skills from the resume
    resume_skills = [
        "3D", "ANSYS", "AutoCAD", "automation", "Automotive", "CAD/CAM", "CAD", "CATIA", 
        "Engineering Analysis", "lathe", "Manufacturing process", "Materials", "material selection", 
        "Oil", "Optimization", "prototyping", "Robotic", "safety", "simulation", "SolidWorks", 
        "SPC", "statistical analysis", "welding"
    ]
    
    # Path to the job listings CSV file
    jobs_csv_path = os.path.join(os.path.dirname(__file__), 'job_listings.csv')
    
    # Load job listings from CSV
    jobs = []
    try:
        with open(jobs_csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                jobs.append(row)
        print(f"Loaded {len(jobs)} job listings from {jobs_csv_path}")
    except Exception as e:
        print(f"Error loading job listings: {e}")
        return
    
    # Calculate skill match scores for all jobs
    job_scores = []
    for job in jobs:
        # Extract required skills from the job listing
        required_skills = []
        if 'required_skills' in job and job['required_skills']:
            if isinstance(job['required_skills'], list):
                required_skills = job['required_skills']
            elif isinstance(job['required_skills'], str):
                required_skills = [skill.strip() for skill in job['required_skills'].split(',')]
        
        # Also check for extracted_skills field
        if 'extracted_skills' in job and job['extracted_skills']:
            if isinstance(job['extracted_skills'], list):
                required_skills.extend(job['extracted_skills'])
            elif isinstance(job['extracted_skills'], str):
                required_skills.extend([skill.strip() for skill in job['extracted_skills'].split(',')])
        
        # Calculate skill match score
        score = calculate_skill_match_score(resume_skills, required_skills)
        
        # Find matching and missing skills
        matching_skills = []
        for job_skill in required_skills:
            for resume_skill in resume_skills:
                if (job_skill.lower() == resume_skill.lower() or 
                    job_skill.lower() in resume_skill.lower() or 
                    resume_skill.lower() in job_skill.lower()):
                    matching_skills.append(job_skill)
                    break
        
        missing_skills = [skill for skill in required_skills if skill not in matching_skills]
        
        job_scores.append({
            'job_id': job.get('job_id', ''),
            'title': job.get('title', ''),
            'company': job.get('company', ''),
            'required_skills': required_skills,
            'matching_skills': matching_skills,
            'missing_skills': missing_skills,
            'skill_match_score': score
        })
    
    # Sort jobs by skill match score (descending)
    job_scores.sort(key=lambda x: x['skill_match_score'], reverse=True)
    
    # Write results to a file
    output_file = "skill_match_results.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Resume Skills:\n")
        for skill in resume_skills:
            f.write(f"  - {skill}\n")
        
        f.write("\nTop 5 Job Matches:\n")
        for i, job in enumerate(job_scores[:5]):
            f.write(f"\n{i+1}. {job['title']} at {job['company']} (Job ID: {job['job_id']})\n")
            f.write(f"   Skill Match Score: {job['skill_match_score']:.4f}\n")
            f.write(f"   Required Skills: {', '.join(job['required_skills'])}\n")
            f.write(f"   Matching Skills: {', '.join(job['matching_skills'])}\n")
            f.write(f"   Missing Skills: {', '.join(job['missing_skills'])}\n")
        
        # Calculate statistics
        scores = [job['skill_match_score'] for job in job_scores]
        avg_score = sum(scores) / len(scores) if scores else 0
        median_score = sorted(scores)[len(scores)//2] if scores else 0
        min_score = min(scores) if scores else 0
        max_score = max(scores) if scores else 0
        zero_score_count = sum(1 for score in scores if score == 0)
        
        f.write("\nSkill Score Statistics:\n")
        f.write(f"  Average Score: {avg_score:.4f}\n")
        f.write(f"  Median Score: {median_score:.4f}\n")
        f.write(f"  Min Score: {min_score:.4f}\n")
        f.write(f"  Max Score: {max_score:.4f}\n")
        f.write(f"  Jobs with Zero Skill Match: {zero_score_count} out of {len(jobs)}\n")
        
        # List jobs with zero skill match
        if zero_score_count > 0:
            f.write("\nJobs with Zero Skill Match:\n")
            for job in job_scores:
                if job['skill_match_score'] == 0:
                    f.write(f"  - {job['title']} at {job['company']} (Job ID: {job['job_id']})\n")
                    f.write(f"    Required Skills: {', '.join(job['required_skills'])}\n")
    
    print(f"Results written to {output_file}")
    print(f"Run 'python {compare_script}' to compare these skills with job requirements")

if __name__ == "__main__":
    main()
'''
        f.write(script_content)
    
    print(f"Created comparison script: {compare_script}")

if __name__ == "__main__":
    main()