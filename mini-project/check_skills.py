import pandas as pd
import re

# Load job listings
job_df = pd.read_csv('C:\\Users\\ASUS\\Downloads\\job_listings.csv')

# Resume skills from the PDF
resume_skills = [
    '3D', 'ANSYS', 'AutoCAD', 'automation', 'Automotive', 'CAD/CAM', 'CAD', 'CATIA', 
    'Engineering Analysis', 'lathe', 'Manufacturing process', 'Materials', 
    'material selection', 'Oil', 'Optimization', 'prototyping', 'Robotic', 
    'safety', 'simulation', 'SolidWorks', 'SPC', 'statistical analysis', 'welding'
]

print('Resume skills:', resume_skills)
print('\nJob skills:')

# Check first 5 jobs
for i, row in job_df.head(5).iterrows():
    print(f"\nJob {i+1}: {row['title']} - {row['required_skills']}")
    
    # Convert required_skills to list if it's a string
    if isinstance(row['required_skills'], str):
        job_skills = [s.strip() for s in row['required_skills'].split(',')]
    else:
        job_skills = []
    
    print(f"Job skills: {job_skills}")
    
    # Find matching skills (case insensitive)
    matching = []
    for rs in resume_skills:
        for js in job_skills:
            if rs.lower() in js.lower() or js.lower() in rs.lower():
                matching.append(f"{rs} matches {js}")
    
    print(f'Matching skills: {matching}')
    
    # Calculate skill match score using Jaccard similarity
    resume_skills_lower = [s.lower() for s in resume_skills]
    job_skills_lower = [s.lower() for s in job_skills]
    
    # Check for partial matches
    matching_skills = set()
    for rs in resume_skills_lower:
        for js in job_skills_lower:
            if rs in js or js in rs:
                matching_skills.add(rs)
    
    all_skills = set(resume_skills_lower).union(set(job_skills_lower))
    
    if all_skills:
        jaccard_similarity = len(matching_skills) / len(all_skills)
        print(f"Skill match score: {jaccard_similarity:.4f}")
    else:
        print("Skill match score: 0.0000")