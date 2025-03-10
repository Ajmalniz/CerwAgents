# Snake Game AI Crew

Welcome to the Snake Game AI Crew project, powered by [crewAI](https://crewai.com). This project demonstrates how multiple AI agents can collaborate to create, test, and optimize a classic snake game implementation. Our agents work together to handle different aspects of the game, from design to implementation and testing.

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling.

First, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

```bash
crewai install
```

### Configuration

1. Add your `OPENAI_API_KEY` to the `.env` file
2. Configure the following files:
   - `src/snake_game/config/agents.yaml`: Define specialized agents for game development
   - `src/snake_game/config/tasks.yaml`: Set up tasks for game design, implementation, and testing
   - `src/snake_game/crew.py`: Customize game logic and agent interactions
   - `src/snake_game/main.py`: Configure game parameters and initialization

## Game Features

Our Snake Game implementation includes:
- Classic snake movement mechanics
- Score tracking and high score system
- Collision detection
- Food spawning mechanics
- Progressive difficulty levels

## Running the Project

To start the Snake Game AI Crew:

```bash
$ crewai run
```

This command will:
1. Initialize the game development agents
2. Execute the defined tasks in sequence
3. Generate the game implementation
4. Run tests and optimizations

## Project Structure

The Snake Game AI Crew consists of specialized agents:
- Game Designer: Plans game mechanics and features
- Developer: Implements core game functionality
- Tester: Ensures game quality and performance
- UI/UX Specialist: Designs user interface elements

Each agent contributes to specific tasks defined in `config/tasks.yaml`, creating a comprehensive game development pipeline.

## Support

Need help with your Snake Game AI Crew?
- Visit [crewAI documentation](https://docs.crewai.com)

Start building your snake game with the power of collaborative AI agents!
## 🔗 Links

[![portfolio](https://img.shields.io/badge/portfolio-000?style=for-the-badge&logo=vercel&logoColor=white)](https://portfolio-woad-sigma-11.vercel.app/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ajmal-ai-engineer/)
[![email](https://img.shields.io/badge/email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:aknizamani@gmail.com)


Maintained by: Ajmal Niz
