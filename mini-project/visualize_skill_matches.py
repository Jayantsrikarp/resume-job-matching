import matplotlib.pyplot as plt
import numpy as np
import os

def read_skill_match_results(file_path):
    """Read the skill match results from the text file."""
    job_matches = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split the content by job entries (each starting with a number followed by a period)
    job_sections = content.split('\n\n')
    
    # Find the section with "Top 5 Job Matches:"
    top_jobs_index = -1
    for i, section in enumerate(job_sections):
        if "Top 5 Job Matches:" in section:
            top_jobs_index = i
            break
    
    if top_jobs_index == -1 or top_jobs_index + 1 >= len(job_sections):
        print("Could not find job matches section in the results file.")
        return []
    
    # Process each job entry
    for section in job_sections[top_jobs_index+1:]:
        if "Skill Score Statistics:" in section:
            break
        
        lines = section.strip().split('\n')
        if not lines or not lines[0][0].isdigit():
            continue
        
        job_info = {}
        
        # Parse the job title and company
        header = lines[0]
        if ". " in header and " at " in header and " (Job ID: " in header:
            title_part = header.split(".", 1)[1].split(" at ", 1)[0].strip()
            company_part = header.split(" at ", 1)[1].split(" (Job ID: ", 1)[0].strip()
            job_info['title'] = title_part
            job_info['company'] = company_part
        
        # Parse the skill match score
        for line in lines[1:]:
            if "Skill Match Score:" in line:
                try:
                    score_text = line.split(":", 1)[1].strip()
                    job_info['score'] = float(score_text)
                except (ValueError, IndexError) as e:
                    print(f"Error parsing score from line: {line}. Error: {e}")
                    job_info['score'] = 0.0
        
        if 'title' in job_info and 'company' in job_info and 'score' in job_info:
            job_matches.append(job_info)
    
    return job_matches

def create_skill_match_chart(job_matches, output_file):
    """Create a bar chart of skill match scores."""
    if not job_matches:
        print("No job matches to visualize.")
        return
    
    # Extract data for plotting
    companies = [f"{job['company']}\n({job['title']})" for job in job_matches]
    scores = [job['score'] for job in job_matches]
    
    # Create the figure and axis
    plt.figure(figsize=(12, 8))
    
    # Create the bar chart
    bars = plt.bar(companies, scores, color='skyblue')
    
    # Add a horizontal line for the average score
    avg_score = sum(scores) / len(scores)
    plt.axhline(y=avg_score, color='red', linestyle='--', label=f'Average Score: {avg_score:.4f}')
    
    # Add data labels on top of each bar
    for bar, score in zip(bars, scores):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{score:.4f}', ha='center', va='bottom', fontweight='bold')
    
    # Customize the chart
    plt.title('Skill Match Scores by Job Position', fontsize=16, fontweight='bold')
    plt.xlabel('Company and Position', fontsize=12)
    plt.ylabel('Skill Match Score', fontsize=12)
    plt.ylim(0, max(scores) + 0.1)  # Add some space for the data labels
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    
    # Save the chart
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Chart saved to {output_file}")
    
    # Close the figure to free memory
    plt.close()

def main():
    # File paths
    results_file = "skill_match_results.txt"
    output_dir = "skill_visualizations"
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Read the skill match results
    job_matches = read_skill_match_results(results_file)
    
    if job_matches:
        print(f"Found {len(job_matches)} job matches to visualize.")
        for job in job_matches:
            print(f"  - {job['company']}: {job['title']} (Score: {job['score']:.4f})")
        
        # Create the skill match chart
        match_chart_file = os.path.join(output_dir, "skill_match_scores.png")
        create_skill_match_chart(job_matches, match_chart_file)
        
        print("Visualization complete!")
    else:
        print("No job matches found in the results file.")

if __name__ == "__main__":
    main()