# Space Shooter Game AI Crew

Welcome to the Space Shooter Game AI Crew project, powered by [crewAI](https://docs.crewai.com). This project demonstrates how multiple AI agents collaborate to create, test, and optimize a 2D space shooter game implementation using Pygame. Our agents work together to handle different aspects of the game development process, from implementation to testing.

## Game Features

The Space Shooter game includes:
- Player-controlled spaceship (blue rectangle)
- Enemy ships (red circles)
- Shooting mechanics (green bullets)
- Collision detection
- Score tracking
- Smooth movement controls

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system.

1. Install CrewAI and its tools:
```bash
pip install 'crewai[tools]'
```

2. Install required game dependencies:
```bash
pip install pygame
```

## Project Structure

```
src/snake_demo/
├── config/
│   ├── agents.yaml    # Agent definitions and roles
│   └── tasks.yaml     # Task configurations
├── main.py           # Main execution script
└── generated_game.py  # The generated game code
```

### AI Agents

The project utilizes three specialized AI agents:

1. **Game Developer**
   - Role: Senior Software Engineer
   - Purpose: Creates the initial game implementation
   - Focus: Core game mechanics and functionality

2. **Code Quality Engineer**
   - Role: Software Quality Control Engineer
   - Purpose: Reviews and improves code quality
   - Focus: Syntax, logic errors, and vulnerabilities

3. **Game Tester**
   - Role: Chief Software Quality Control Engineer
   - Purpose: Final validation and testing
   - Focus: Gameplay functionality and requirements

## Running the Project

To generate and run the game:

1. Execute the main script:
```bash
python src/snake_demo/main.py
```

2. Run the generated game:
```bash
python generated_game.py
```

### Game Controls
- Left Arrow: Move spaceship left
- Right Arrow: Move spaceship right
- Spacebar: Shoot bullets

## How It Works

The project follows a sequential process:
1. Game Developer creates the initial game code
2. Code Quality Engineer reviews and improves the code
3. Game Tester validates the final implementation
4. The final game is saved as 'generated_game.py'

## Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a new branch for your feature
3. Submitting a pull request

## License

This project is open-source and available under the MIT License.

## Support

For questions or issues:
- Check the [CrewAI documentation](https://docs.crewai.com)
- Open an issue in the repository
- Contact the maintainers

---
Created with [CrewAI](https://docs.crewai.com) - Empowering AI Agent Collaboration
