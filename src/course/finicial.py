import warnings
from crewai import Agent, Task, Crew, Process
import os
from dotenv import load_dotenv, find_dotenv
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
import socket  # For network connectivity check

# Suppress warnings
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv(find_dotenv())
API_KEY = os.getenv("SERPER_API_KEY")

# Tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# Agent Definitions
manager_agent = Agent(
    role="Manager",
    goal="Coordinate and oversee the trading analysis process",
    backstory="Experienced trading manager who orchestrates the workflow between analysis, strategy, execution, and risk teams",
    verbose=True,
    allow_delegation=True
)

data_analyst_agent = Agent(
    role="Data Analyst",
    goal="Monitor and analyze market data in real-time to identify trends and predict market movements.",
    backstory="Specializing in financial markets, this agent uses statistical modeling and machine learning to provide crucial insights. With a knack for data, the Data Analyst Agent is the cornerstone for informing trading decisions.",
    verbose=True,
    allow_delegation=True,
    tools=[scrape_tool, search_tool]
)

trading_strategy_agent = Agent(
    role="Trading Strategy Developer",
    goal="Develop and test various trading strategies based on insights from the Data Analyst Agent.",
    backstory="Equipped with a deep understanding of financial markets and quantitative analysis, this agent devises and refines trading strategies. It evaluates the performance of different approaches to determine the most profitable and risk-averse options.",
    verbose=True,
    allow_delegation=True,
    tools=[scrape_tool, search_tool]
)

execution_agent = Agent(
    role="Trade Advisor",
    goal="Suggest optimal trade execution strategies based on approved trading strategies.",
    backstory="This agent specializes in analyzing the timing, price, and logistical details of potential trades. By evaluating these factors, it provides well-founded suggestions for when and how trades should be executed to maximize efficiency and adherence to strategy.",
    verbose=True,
    allow_delegation=True,
    tools=[scrape_tool, search_tool]
)

risk_management_agent = Agent(
    role="Risk Advisor",
    goal="Evaluate and provide insights on the risks associated with potential trading activities.",
    backstory="Armed with a deep understanding of risk assessment models and market dynamics, this agent scrutinizes the potential risks of proposed trades. It offers a detailed analysis of risk exposure and suggests safeguards to ensure that trading activities align with the firm's risk tolerance.",
    verbose=True,
    allow_delegation=True,
    tools=[scrape_tool, search_tool]
)

# Task Definitions
data_analysis_task = Task(
    description=(
        "Continuously monitor and analyze market data for "
        "the selected stock ({stock_selection}). "
        "Use statistical modeling and machine learning to "
        "identify trends and predict market movements."
    ),
    expected_output=(
        "Insights and alerts about significant market "
        "opportunities or threats for {stock_selection}."
    ),
    agent=data_analyst_agent
)

strategy_development_task = Task(
    description=(
        "Develop and refine trading strategies based on "
        "the insights from the Data Analyst and "
        "user-defined risk tolerance ({risk_tolerance}). "
        "Consider trading preferences ({trading_strategy_preference})."
    ),
    expected_output=(
        "A set of potential trading strategies for {stock_selection} "
        "that align with the user's risk tolerance."
    ),
    agent=trading_strategy_agent
)

execution_planning_task = Task(
    description=(
        "Analyze approved trading strategies to determine the "
        "best execution methods for {stock_selection}, "
        "considering current market conditions and optimal pricing."
    ),
    expected_output=(
        "Detailed execution plans suggesting how and when to "
        "execute trades for {stock_selection}."
    ),
    agent=execution_agent
)

risk_assessment_task = Task(
    description=(
        "Evaluate the risks associated with the proposed trading "
        "strategies and execution plans for {stock_selection}. "
        "Provide a detailed analysis of potential risks "
        "and suggest mitigation strategies."
    ),
    expected_output=(
        "A comprehensive risk analysis report detailing potential "
        "risks and mitigation recommendations for {stock_selection}."
    ),
    agent=risk_management_agent
)

# Function to check internet connectivity
def is_internet_available():
    try:
        socket.create_connection(("www.google.com", 80), timeout=5)
        return True
    except OSError:
        return False

# Main Function
def main():
    try:
        # Define the crew with hierarchical process
        multiAgent = Crew(
            agents=[
                data_analyst_agent,
                trading_strategy_agent,
                execution_agent,
                risk_management_agent
            ],  # Removed manager_agent from this list
            tasks=[
                data_analysis_task,
                strategy_development_task,
                execution_planning_task,
                risk_assessment_task
            ],
            process=Process.hierarchical,
            manager_agent=manager_agent,  # Manager specified separately
            verbose=True
        )
        
        # Input dictionary with trading strategy details
        inputs = {
            'stock_selection': 'AAPL',
            'initial_capital': '100000',
            'risk_tolerance': 'Medium',
            'trading_strategy_preference': 'Day Trading',
            'news_impact_consideration': True,
            'entry_rule': 'Buy when 50-day MA crosses above 200-day MA',
            'exit_rule': 'Sell when 50-day MA crosses below 200-day MA',
            'stop_loss': '5% below entry price',
            'position_size': '1% of initial capital',
            'backtesting_data': {
                'trades': 50,
                'win_rate': 0.55,
                'avg_profit': 2.5,  # Percentage
                'avg_loss': -3.0    # Percentage
            }
        }
        
        # Kick off the process
        result = multiAgent.kickoff(inputs)
        
        # Convert result to string and save to file
        result_string = str(result)
        with open('multi_agent_output.md', 'w', encoding="utf-8") as f:
            f.write(result_string)
        
        print("Execution completed successfully. Output saved to 'multi_agent_output.md'.")
        print(result)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Falling back to manual data fetch...")
        try:
            if not is_internet_available():
                raise Exception("No internet connection available. Please check your network.")
            from crewai_tools import SerperDevTool
            search_tool = SerperDevTool()
            fallback_result = search_tool.run(search_query="AAPL market analysis February 2025")
            print("Fallback result:", fallback_result)
            with open('multi_agent_output_fallback.md', 'w', encoding="utf-8") as f:
                f.write(str(fallback_result))
        except Exception as fallback_e:
            print(f"Fallback failed: {fallback_e}")
            print("Please ensure internet connectivity and a valid SERPER_API_KEY in your .env file.")

if __name__ == "__main__":
    main()