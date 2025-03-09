#!/usr/bin/env python
import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
import os
import yaml
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# Define Pydantic models for structured output with V2 compatibility
class SocialMediaPost(BaseModel):
    platform: str = Field(description="The social media platform (e.g., Twitter, LinkedIn).")
    content: str = Field(description="The content of the social media post, including hashtags or mentions.")

    class Config:
        from_attributes = True

class ContentOutput(BaseModel):
    article: str = Field(description="The article, formatted in markdown.")
    social_media_posts: List[SocialMediaPost] = Field(description="A list of social media posts related to the article.")

    class Config:
        from_attributes = True

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define file paths
files = {
    'agents': os.path.join(current_dir, 'config', 'agents.yaml'),
    'tasks': os.path.join(current_dir, 'config', 'tasks.yaml')
}

# Load YAML configurations
configs = {}
for config_type, file_path in files.items():
    try:
        with open(file_path, 'r') as file:
            configs[config_type] = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {file_path}")
        exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file {file_path}: {e}")
        exit(1)

agents_config = configs['agents']
tasks_config = configs['tasks']

# Setup single LLM model
# Using Gemini 1.5 Flash exclusively

def main():
    # Create Agents with Gemini 1.5 Flash
    market_news_monitor_agent = Agent(
        config=agents_config['market_news_monitor_agent'],
        tools=[SerperDevTool(), ScrapeWebsiteTool()],
    
    )

    data_analyst_agent = Agent(
        config=agents_config['data_analyst_agent'],
        tools=[SerperDevTool(), ScrapeWebsiteTool()],
        
    )

    content_creator_agent = Agent(
        config=agents_config['content_creator_agent'],
        tools=[SerperDevTool(), ScrapeWebsiteTool()],

    )

    quality_assurance_agent = Agent(
        config=agents_config['quality_assurance_agent'],
    
    )

    # Create Tasks
    monitor_financial_news_task = Task(
        config=tasks_config['monitor_financial_news'],
        agent=market_news_monitor_agent
    )

    analyze_market_data_task = Task(
        config=tasks_config['analyze_market_data'],
        agent=data_analyst_agent
    )

    create_content_task = Task(
        config=tasks_config['create_content'],
        agent=content_creator_agent,
        context=[monitor_financial_news_task, analyze_market_data_task]
    )

    quality_assurance_task = Task(
        config=tasks_config['quality_assurance'],
        agent=quality_assurance_agent,
        output_pydantic=ContentOutput,
        output_file='content_output.md'
    )

    # Create and configure Crew
    content_creation_crew = Crew(
        agents=[
            market_news_monitor_agent,
            data_analyst_agent,
            content_creator_agent,
            quality_assurance_agent
        ],
        tasks=[
            monitor_financial_news_task,
            analyze_market_data_task,
            create_content_task,
            quality_assurance_task
        ],
        verbose=True
    )

    # Execute the crew with input
    print("Starting Crew execution...")
    result = content_creation_crew.kickoff(inputs={
        'subject': 'Inflation in the US and the impact on the stock market in 2024'
    })

    # Print confirmation
    output_path = os.path.join(current_dir, 'content_output.md')
    print(f"Content saved to {output_path}")

    # Optional: Display results in console
    posts = result.pydantic.dict()['social_media_posts']
    print("\n=== Social Media Posts ===")
    for post in posts:
        print(f"{post['platform']}:\n{post['content']}\n{'-' * 50}")

    print("\n=== Article Preview ===")
    print(result.pydantic.dict()['article'][:500] + "...")

if __name__ == "__main__":
    main()