from crewai import Agent, Task, Crew
import os
from dotenv import load_dotenv,find_dotenv
from typing import List, Dict, Any, Union

from crewai_tools import ScrapeWebsiteTool,SerperDevTool,WebsiteSearchTool
load_dotenv(find_dotenv())
# ---------------agents-------------#
support_agent =Agent(
    role ="senior support Repranstive",
    goal = "Be the most friendly and helpful"
            "support represantive in your team",
    backstory=(
		"You work at crewAI (https://crewai.com) and "
        " are now working on providing "
		"support to {customer}, a super important customer "
        " for your company."
		"You need to make sure that you provide the best support!"
		"Make sure to provide full complete answers, "
        " and make no assumptions."
	),
    llm="gemini/gemini-1.5-flash",
    allow_delegation=False,
	verbose=True

)
support_quality_assurance_agent = Agent(
	role="Support Quality Assurance Specialist",
	goal="Get recognition for providing the "
    "best support quality assurance in your team",
	backstory=(
		"You work at crewAI (https://crewai.com) and "
        "are now working with your team "
		"on a request from {customer} ensuring that "
        "the support representative is "
		"providing the best support possible.\n"
		"You need to make sure that the support representative "
        "is providing full"
		"complete answers, and make no assumptions."
	),
    llm="gemini/gemini-1.5-flash",
	verbose=True
)
#..................Toools .......................#
search_tool = SerperDevTool()
docs_scrape_tool = ScrapeWebsiteTool(
    website_url="https://docs.crewai.com/how-to/Creating-a-Crew-and-kick-it-off/"
)


#..................TASK.........................#
inquiry_resolution = Task(
    description=(
        "{customer} just reached out with a super important ask:\n"
	    "{inquiry}\n\n"
        "{person} from {customer} is the one that reached out. "
		"Make sure to use everything you know "
        "to provide the best support possible."
		"You must strive to provide a complete "
        "and accurate response to the customer's inquiry."
    ),
    expected_output=(
	    "A detailed, informative response to the "
        "customer's inquiry that addresses "
        "all aspects of their question.\n"
        "The response should include references "
        "to everything you used to find the answer, "
        "including external data or solutions. "
        "Ensure the answer is complete, "
		"leaving no questions unanswered, and maintain a helpful and friendly "
		"tone throughout."
    ),
	tools=[docs_scrape_tool],
    agent=support_agent,
)
quality_assurance_review = Task(
    description=(
        "Review the response drafted by the Senior Support Representative for {customer}'s inquiry. "
        "Ensure that the answer is comprehensive, accurate, and adheres to the "
		"high-quality standards expected for customer support.\n"
        "Verify that all parts of the customer's inquiry "
        "have been addressed "
		"thoroughly, with a helpful and friendly tone.\n"
        "Check for references and sources used to "
        " find the information, "
		"ensuring the response is well-supported and "
        "leaves no questions unanswered."
    ),
    expected_output=(
        "A final, detailed, and informative response "
        "ready to be sent to the customer.\n"
        "This response should fully address the "
        "customer's inquiry, incorporating all "
		"relevant feedback and improvements.\n"
		"Don't be too formal, we are a chill and cool company "
	    "but maintain a professional and friendly tone throughout."
    ),
    agent=support_quality_assurance_agent,
)
#### creating and calling crew from uv
def main() -> None:
    try:
        obj = Crew(
            agents=[support_agent, support_quality_assurance_agent],
  			tasks=[inquiry_resolution, quality_assurance_review],
  			verbose=True,
  			
		)
        inputs ={
            "customer" : "PIAIC",
            "person" :"Ajmal Khan",
            "inquiry":"I need help with setting up crew"
						"and kicking it off,specially"
                        "how can i add memory to my crew?"
                        "can you provide guidance?"
            
		}
        result = obj.kickoff(inputs=inputs)
        result_string = str(result)
        with open('customer.md','w',encoding="utf-8") as f:
            f.write(result_string)
    except Exception as e :
        print(f"an error occurd : {e}")
