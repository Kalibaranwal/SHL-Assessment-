# SHL-Assessment-
This is an interactive Streamlit web application that allows users to receive personalized SHL assessment recommendations based on either:  A natural language job description, or  A URL link to a job listing.

 1.	Input Handling
o	Accepts free-text input or URL to a job posting.
o	If a URL is provided, uses requests and BeautifulSoup to scrape and clean the content.
2.	Text Parsing & Information Extraction
o	Extracts skills using keyword-based regex (e.g., Python, .NET, React).
o	Extracts time constraints (e.g., "20 minutes") using regex patterns.
3.	Assessment Dataset
o	Uses a predefined subset of SHL assessments (stored in pandas.DataFrame).
o	Each record includes: Name, URL, Duration, Test Type, Remote Support, Adaptive Support.
4.	Matching Logic
o	Filters assessments by:
	Skill relevance: Match input skills with assessment title/type.
	Duration: Skips tests exceeding the user-specified max time.
5.	Recommendation Output
o	Displays top 10 matching SHL assessments with:
	Name (hyperlinked)
	Remote & Adaptive support flags
	Duration
	Test type
🖥️ How to Use:
bash
CopyEdit
streamlit run app.py
•	Enter your job description or paste a job URL.
•	Click "Recommend Assessments" to view personalized SHL test recommendations.
________________________________________
✅ Output:
•	User sees a structured list of SHL assessments tailored to their input.
•	Easy for recruiters or hiring managers to identify relevant assessments
