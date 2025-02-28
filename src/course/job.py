import warnings
from crewai import Agent, Task, Crew, Process
import os
from dotenv import load_dotenv, find_dotenv
from crewai_tools import ScrapeWebsiteTool, SerperDevTool, FileReadTool
from langchain_google_genai import ChatGoogleGenerativeAI

# Suppress warnings
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv(find_dotenv())

# Get API keys from .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
MODEL = os.getenv("MODEL")


# Validate API keys
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")
if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY not found in environment variables.")

# Configure Gemini LLM
llm = ChatGoogleGenerativeAI(
    model=MODEL,  # Use "gemini-1.5-pro" if available
    google_api_key=GEMINI_API_KEY,
    temperature=0.7,
    verbose=True
)

# Define Tools (no MDXSearchTool)
search_tool = SerperDevTool(api_key=SERPER_API_KEY)
scrape_tool = ScrapeWebsiteTool()
read_resume = FileReadTool(file_path="./fake_resume.txt")

# Define a simple agent
resume_summary = Agent(
    role="Researcher",
    goal="Analyze the resume and provide insights",
    backstory="You are an expert in resume analysis.",
    tools=[search_tool, scrape_tool, read_resume],  # Only tools we need
    verbose=True
)
researcher = Agent(
    role="Tech Job Researcher",
    goal="Make sure to do amazing analysis on "
         "job posting to help job applicants",
    tools = [scrape_tool, search_tool],
    verbose=True,
    backstory=(
        "As a Job Researcher, your prowess in "
        "navigating and extracting critical "
        "information from job postings is unmatched."
        "Your skills help pinpoint the necessary "
        "qualifications and skills sought "
        "by employers, forming the foundation for "
        "effective application tailoring."
    )
)
profiler = Agent(
    role="Personal Profiler for Engineers",
    goal="Do increditble research on job applicants "
         "to help them stand out in the job market"
         "resume summary is provided by resume_task",
    tools = [scrape_tool, search_tool,
             read_resume,],
    verbose=True,
    backstory=(
        "Equipped with analytical prowess, you dissect "
        "and synthesize information "
        "from diverse sources to craft comprehensive "
        "personal and professional profiles, laying the "
        "groundwork for personalized resume enhancements."
    )
)

resume_strategist = Agent(
    role="Resume Strategist for Engineers",
    goal="Find all the best ways to make a "
         "resume stand out in the job market."
         "resume summary is provided by resume_task",
    tools = [scrape_tool, search_tool,
             read_resume],
    verbose=True,
    backstory=(
        "With a strategic mind and an eye for detail, you "
        "excel at refining resumes to highlight the most "
        "relevant skills and experiences, ensuring they "
        "resonate perfectly with the job's requirements."
    )
)

interview_preparer = Agent(
    role="Engineering Interview Preparer",
    goal="Create interview questions and talking points "
         "based on the resume and job requirements",
    tools = [scrape_tool, search_tool,
             read_resume,],
    verbose=True,
    backstory=(
        "Your role is crucial in anticipating the dynamics of "
        "interviews. With your ability to formulate key questions "
        "and talking points, you prepare candidates for success, "
        "ensuring they can confidently address all aspects of the "
        "job they are applying for."
    )
)
# Define a task
resume_task = Task(
    description="Read the resume from './fake_resume.txt' using the FileReadTool and summarize its key points.",
    agent=resume_summary,
    expected_output="A summary of the resume's key points."
)
research_task = Task(
    description=(
        "Analyze the job posting URL provided ({job_posting_url}) "
        "to extract key skills, experiences, and qualifications "
        "required. Use the tools to gather content and identify "
        "and categorize the requirements."
    ),
    expected_output=(
        "A structured list of job requirements, including necessary "
        "skills, qualifications, and experiences."
    ),
    agent=researcher,
    async_execution=True
)
profile_task = Task(
    description=(
        "Compile a detailed personal and professional profile "
        "using the GitHub ({github_url}) URLs, and personal write-up "
        "({personal_writeup}). Utilize tools to extract and "
        "synthesize information from these sources."
    ),
    expected_output=(
        "A comprehensive profile document that includes skills, "
        "project experiences, contributions, interests, and "
        "communication style."
    ),
    agent=profiler,
    async_execution=True
)
resume_strategy_task = Task(
    description=(
        "Using the profile and job requirements obtained from "
        "previous tasks, tailor the resume to highlight the most "
        "relevant areas. Employ tools to adjust and enhance the "
        "resume content. Make sure this is the best resume even but "
        "don't make up any information. Update every section, "
        "inlcuding the initial summary, work experience, skills, "
        "and education. All to better reflrect the candidates "
        "abilities and how it matches the job posting."
    ),
    expected_output=(
        "An updated resume that effectively highlights the candidate's "
        "qualifications and experiences relevant to the job."
    ),
    output_file="tailored_resume.md",
    context=[research_task, profile_task],
    agent=resume_strategist
)
interview_preparation_task = Task(
    description=(
        "Create a set of potential interview questions and talking "
        "points based on the tailored resume and job requirements. "
        "Utilize tools to generate relevant questions and discussion "
        "points. Make sure to use these question and talking points to "
        "help the candiadte highlight the main points of the resume "
        "and how it matches the job posting."
    ),
    expected_output=(
        "A document containing key questions and talking points "
        "that the candidate should prepare for the initial interview."
    ),
    output_file="interview_materials.md",
    context=[research_task, profile_task, resume_strategy_task],
    agent=interview_preparer
)


# Create a crew
crew = Crew(
    agents=[resume_summary,researcher,profiler,resume_strategist,interview_preparer],
    tasks=[resume_task,research_task,
           profile_task,
           resume_strategy_task,
           interview_preparation_task],
    verbose=True,
     # Optional: enables memory for context
    # No embedder needed since we’re not using semantic search
)

# Main function to run the crew
def main():
    print("Starting the crew...")
    job_application_inputs = {
    'job_posting_url': 'https://jobs.lever.co/AIFund/6c82e23e-d954-4dd8-a734-c0c2c5ee00f1?lever-origin=applied&lever-source%5B%5D=AI+Fund',
    'github_url': 'https://github.com/Ajmalniz',
    'personal_writeup': """Hi, I’m Ajmal Khan, an AI Engineer and Full Stack Developer driven by a passion for building intelligent, scalable solutions. I specialize in Agentic AI, leveraging frameworks like CrewAI, AutoGen, and LangGraph.
I graduated with honors from COMSATS, Abbottabad in 2012 with a BS in Computer Engineering on a full scholarship. I hold certifications in Google Data Analytics and Meta Front-End Development, blending data insights with modern web tech.
My expertise combines AI with Vector and Graph Databases to create impactful applications. I’m excited to push boundaries and solve complex problems with innovative tech."""
    }
    try:
        result = crew.kickoff(job_application_inputs)
        print("Crew finished.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()