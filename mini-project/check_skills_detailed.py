import pandas as pd
import re
import numpy as np

# Load job listings
job_df = pd.read_csv('C:\\Users\\ASUS\\Downloads\\job_listings.csv')

# Resume skills from the PDF
resume_skills = [
    '3D', 'ANSYS', 'AutoCAD', 'automation', 'Automotive', 'CAD/CAM', 'CAD', 'CATIA', 
    'Engineering Analysis', 'lathe', 'Manufacturing process', 'Materials', 
    'material selection', 'Oil', 'Optimization', 'prototyping', 'Robotic', 
    'safety', 'simulation', 'SolidWorks', 'SPC', 'statistical analysis', 'welding'
]

print(f'Resume skills ({len(resume_skills)}): {resume_skills}')

# Check the matcher implementation
def calculate_skill_match_score(resume_skills, job_skills):
    """Calculate skill match score between resume and job skills."""
    # Convert to lowercase for case-insensitive matching
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
        return jaccard_similarity, matching_skills
    else:
        return 0.0, set()

# Check all jobs
results = []
for i, row in job_df.iterrows():
    # Convert required_skills to list if it's a string
    if isinstance(row['required_skills'], str):
        job_skills = [s.strip() for s in row['required_skills'].split(',')]
    else:
        job_skills = []
    
    # Calculate skill match score
    score, matching = calculate_skill_match_score(resume_skills, job_skills)
    
    results.append({
        'job_id': row.get('job_id', i),
        'title': row['title'],
        'required_skills': job_skills,
        'matching_skills': list(matching),
        'skill_score': score
    })

# Sort by skill score
results.sort(key=lambda x: x['skill_score'], reverse=True)

# Print top 5 matches
print("\nTop 5 job matches by skill score:")
for i, result in enumerate(results[:5]):
    print(f"\nRank {i+1}: {result['title']} (Score: {result['skill_score']:.4f})")
    print(f"Required skills ({len(result['required_skills'])}): {result['required_skills']}")
    print(f"Matching skills ({len(result['matching_skills'])}): {result['matching_skills']}")

# Print statistics
scores = [r['skill_score'] for r in results]
print("\nSkill Score Statistics:")
print(f"Average: {np.mean(scores):.4f}")
print(f"Median: {np.median(scores):.4f}")
print(f"Min: {min(scores):.4f}")
print(f"Max: {max(scores):.4f}")

# Check if there are any jobs with zero skill match
zero_matches = [r for r in results if r['skill_score'] == 0]
print(f"\nJobs with zero skill match: {len(zero_matches)} out of {len(results)}")

# Print a few examples of zero matches
if zero_matches:
    print("\nExamples of jobs with zero skill match:")
    for i, result in enumerate(zero_matches[:3]):
        print(f"\n{i+1}. {result['title']}")
        print(f"Required skills: {result['required_skills']}")