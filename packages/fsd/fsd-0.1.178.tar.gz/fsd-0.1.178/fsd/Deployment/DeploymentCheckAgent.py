import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util.portkey import AIGateway
from json_repair import repair_json
from log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)

class DeploymentCheckAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_deployment_check_plan(self):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            all_file_contents (str): The concatenated contents of all files.

        Returns:
            dict: Development plan or error reason.
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "Check if the current project is eligible for deployment as either a static HTML/CSS website or a React-based app (including Next.js, React Native, etc.). "
                    "For HTML/CSS, the project is eligible if there's an index.html file directly in the project root. "
                    "For React-based projects, the project is eligible if there's a package.json file directly in the project root. "
                    f"The root path: {self.repo.get_repo_path()}. "
                    "Here's the project structure:\n"
                    f"{self.repo.print_tree()}\n\n"
                    "Example of an eligible HTML/CSS project structure:\n"
                    "project_root/\n"
                    "├── index.html\n"
                    "├── css/\n"
                    "│   └── styles.css\n"
                    "├── js/\n"
                    "│   └── script.js\n"
                    "└── images/\n"
                    "    └── logo.png\n\n"
                    "Example of an HTML/CSS project with package.json (still considered HTML/CSS):\n"
                    "project_root/\n"
                    "├── package.json  # Only used for dev tools like sass/less\n"
                    "├── index.html    # Main entry point\n"
                    "├── css/\n"
                    "│   ├── styles.css\n"
                    "│   └── main.css\n"
                    "├── js/\n"
                    "│   └── script.js # Plain JavaScript\n"
                    "└── assets/\n"
                    "    └── images/\n"
                    "        └── logo.png\n\n"
                    "Examples of eligible React-based project structures:\n"
                    "1. Basic React project:\n"
                    "project_root/\n"
                    "├── package.json\n"
                    "├── src/\n"
                    "│   ├── App.js\n"
                    "│   └── index.js\n"
                    "└── public/\n"
                    "    └── index.html\n\n"
                    "2. Next.js project:\n"
                    "project_root/\n"
                    "├── package.json\n"
                    "├── pages/\n"
                    "│   ├── index.js\n"
                    "│   └── _app.js\n"
                    "└── public/\n"
                    "    └── favicon.ico\n\n"
                    "3. React Native project:\n"
                    "project_root/\n"
                    "├── package.json\n"
                    "├── App.js\n"
                    "├── index.js\n"
                    "└── android/\n"
                    "    └── ...\n"
                    "└── ios/\n"
                    "    └── ...\n\n"
                    "4. TypeScript React project:\n"
                    "project_root/\n"
                    "├── package.json\n"
                    "├── tsconfig.json\n"
                    "└── src/\n"
                    "    ├── App.tsx\n"
                    "    └── index.tsx\n\n"
                    "5. Create React App project:\n"
                    "project_root/\n"
                    "├── package.json\n"
                    "├── src/\n"
                    "│   ├── App.js\n"
                    "│   ├── index.js\n"
                    "│   └── App.css\n"
                    "└── public/\n"
                    "    └── index.html\n\n"
                    "6. Gatsby project:\n"
                    "project_root/\n"
                    "├── package.json\n"
                    "├── gatsby-config.js\n"
                    "└── src/\n"
                    "    └── pages/\n"
                    "        └── index.js\n\n"
                    "7. Expo React Native project:\n"
                    "project_root/\n"
                    "├── package.json\n"
                    "├── App.js\n"
                    "└── app.json\n\n"
                    "8. React with Redux project:\n"
                    "project_root/\n"
                    "├── package.json\n"
                    "└── src/\n"
                    "    ├── actions/\n"
                    "    ├── reducers/\n"
                    "    ├── components/\n"
                    "    └── index.js\n\n"
                    "9. React with Webpack configuration:\n"
                    "project_root/\n"
                    "├── package.json\n"
                    "├── webpack.config.js\n"
                    "└── src/\n"
                    "    └── index.js\n\n"
                    "10. Preact project:\n"
                    "project_root/\n"
                    "├── package.json\n"
                    "└── src/\n"
                    "    ├── index.js\n"
                    "    └── components/\n"
                    "        └── app.js\n\n"
                    "Respond in this exact JSON format:\n"
                    "{\n"
                    '    "result": "0" or "1",\n'
                    '    "project_type": "0" or "1",\n'
                    '    "full_project_path": "full/path/to/project_folder" or null\n'
                    "}\n"
                    "Where 'result' is '1' if eligible, '0' if not. "
                    "'project_type' is '0' for purely static HTML/CSS, '1' for React-based project. "
                    "For HTML/CSS, 'full_project_path' must be the full path to the project root containing index.html, e.g., '/home/user/projects/mysite'. "
                    "For React-based projects, 'full_project_path' must be the full path to the project root containing package.json, e.g., '/home/user/projects/myapp'. "
                    "If you see a project with package.json but the majority of code is HTML/CSS (e.g. only using package.json for dev tools), "
                    "treat it as an HTML/CSS project with project_type '0' and set full_project_path to the folder containing index.html. "
                    "Return null if not found."
                )
            },
            {
                "role": "user",
                "content": "Check if this project is eligible for deployment and return full path for deploy folder."
            }
        ]

        try:
            logger.debug("\n #### The `DeploymentCheckAgent` is initiating a request to the AI Gateway")
            response = await self.ai.arch_prompt(messages, self.max_tokens, 0, 0)
            res = json.loads(response.choices[0].message.content)
            logger.debug("\n #### The `DeploymentCheckAgent` has successfully parsed the AI response")
            return res
        except json.JSONDecodeError:
            logger.debug("\n #### The `DeploymentCheckAgent` encountered a JSON decoding error and is attempting to repair it")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            logger.debug("\n #### The `DeploymentCheckAgent` has successfully repaired and parsed the JSON")
            return plan_json
        except Exception as e:
            logger.error(f"  The `DeploymentCheckAgent` encountered an error during the process: `{e}`")
            return {
                "reason": str(e)
            }

    async def get_deployment_check_plans(self):
        """
        Get development plans for a list of txt files from Azure OpenAI based on the user prompt.

        Args:
            files (list): List of file paths.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### The `DeploymentCheckAgent` is beginning to retrieve deployment check plans")
        plan = await self.get_deployment_check_plan()
        logger.debug("\n #### The `DeploymentCheckAgent` has successfully retrieved deployment check plans")
        return plan
