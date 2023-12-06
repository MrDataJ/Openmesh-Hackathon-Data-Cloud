# Data Cloud Project

## Overview
This project implements a system for real-time data processing and broadcasting using Python and WebSocket. It supports data ingestion from multiple sources, processes this data, and transmits it to all connected WebSocket clients. The system is designed to be scalable and supports REST API and WebSocket sources.

## Configuration
The application requires two main configuration files located in the `config/` directory:

1. `connectors.json`: This file contains configurations for various data sources, including REST APIs and WebSocket sources. Each connector configuration includes details like the endpoint, headers, and polling intervals for REST APIs.

2. `app.json`: This file includes general application settings, database configurations, logging settings, and WebSocket server settings.

Ensure these files are properly set up before running the application.

## Backend

All connection sources must be started before starting backend node.

### Requirements
- Python 3.8+
- Required Python libraries: `websockets`, `asyncio`, `aiohttp` (Install using `pip install -r requirements.txt`)

### Starting the Server
To start the backend server, navigate to the root directory of the project and run:

```bash python main.py```

This will start the React development server, and the frontend should be accessible at http://localhost:3000.

## Frontend

The frontend is a separate application built using React.js.

### Requirements
- Node.js and npm

### Starting the Frontend
Navigate to the frontend directory and run:

```bash
npm install
npm start
```

This will start the React development server, and the frontend should be accessible at `http://localhost:3000`.

## Contributing
Contributions to the project are welcome. Please ensure to follow the existing code structure and style. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT


### Notes for README:

- Adjust the paths, commands, and URLs as necessary based on your actual project structure and setup.
- Add any additional instructions or descriptions that are specific to your project.
- You might also want to include a section on how to run tests if you have them.
- The `License` section should correspond to the actual license of your project; replace `[MIT]` with the appropriate one if different.
- If your frontend requires additional setup steps (like environment variables or specific build instructions), be sure to include them.

This README provides a basic guideline and can be expanded with more details about the project, such as its architecture, features, and screenshots of the application in action.
