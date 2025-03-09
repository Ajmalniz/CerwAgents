#!/usr/bin/env python3
import warnings
warnings.filterwarnings('ignore')
import os
import yaml
import chainlit as cl
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
gemini_llm = "gemini/gemini-1.5-flash"

# Callback to show agent thinking in real-time
async def on_agent_start(agent, task):
    await cl.Message(content=f"🤓 {agent.role} is thinking...").send()

async def on_agent_end(agent, output):
    await cl.Message(content=f"✅ {agent.role} has finished.").send()

# Chainlit entry point
@cl.on_chat_start
async def start():
    await cl.Message(content="Welcome! Please provide a subject to analyze (e.g., 'Inflation in the US and the impact on the stock market in 2024').").send()

@cl.on_message
async def main(message: cl.Message):
    subject = message.content.strip()
    if not subject:
        await cl.Message(content="Please provide a valid subject.").send()
        return

    await cl.Message(content=f"Starting analysis on: {subject}").send()

    # Create Agents with meaningful names
    news_monitor = Agent(
        config=agents_config['market_news_monitor_agent'],
        tools=[SerperDevTool(), ScrapeWebsiteTool()],
        llm=gemini_llm,
        role="NewsMonitor"  # Renamed for clarity
    )

    data_analyzer = Agent(
        config=agents_config['data_analyst_agent'],
        tools=[SerperDevTool(), ScrapeWebsiteTool()],
        llm=gemini_llm,
        role="DataAnalyzer"  # Renamed for clarity
    )

    content_writer = Agent(
        config=agents_config['content_creator_agent'],
        tools=[SerperDevTool(), ScrapeWebsiteTool()],
        llm=gemini_llm,
        role="ContentWriter"  # Renamed for clarity
    )

    quality_checker = Agent(
        config=agents_config['quality_assurance_agent'],
        llm=gemini_llm,
        role="QualityChecker"  # Renamed for clarity
    )

    # Create Tasks
    monitor_task = Task(
        config=tasks_config['monitor_financial_news'],
        agent=news_monitor
    )

    analyze_task = Task(
        config=tasks_config['analyze_market_data'],
        agent=data_analyzer
    )

    write_task = Task(
        config=tasks_config['create_content'],
        agent=content_writer,
        context=[monitor_task, analyze_task]
    )

    quality_task = Task(
        config=tasks_config['quality_assurance'],
        agent=quality_checker,
        output_pydantic=ContentOutput,
        output_file='content_output.md'
    )

    # Create and configure Crew with callbacks
    content_creation_crew = Crew(
        agents=[
            news_monitor,
            data_analyzer,
            content_writer,
            quality_checker
        ],
        tasks=[
            monitor_task,
            analyze_task,
            write_task,
            quality_task
        ],
        verbose=True,
        manager_callbacks=[
            lambda agent, task: on_agent_start(agent, task),
            lambda agent, output: on_agent_end(agent, output)
        ]
    )

    # Execute the crew
    await cl.Message(content="Crew is now working...").send()
    result = await content_creation_crew.kickoff_async(inputs={'subject': subject})

    # Display results
    output_path = os.path.join(current_dir, 'content_output.md')
    await cl.Message(content=f"Content saved to {output_path}").send()

    posts = result.pydantic.dict()['social_media_posts']
    await cl.Message(content="=== Social Media Posts ===").send()
    for post in posts:
        await cl.Message(content=f"**{post['platform']}**\n{post['content']}").send()

    article_preview = result.pydantic.dict()['article'][:500] + "..."
    await cl.Message(content="=== Article Preview ===\n" + article_preview).send()

if __name__ == "__main__":
    cl.run()