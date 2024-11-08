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

class ImageCheckAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_image_check_plan(self, user_prompt):
        """
        Get a plan for image generation based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            all_file_contents (str): The concatenated contents of all files.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Image generation plan or error reason.
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an image request analyzer. Determine if the development plan requires generating ANY new images in PNG, png, JPG, jpg, JPEG, jpeg, or .ico format.\n\n"
                    "Rules:\n"
                    "1. Carefully analyze the user prompt for any mentions of creating, generating, or adding new images.\n"
                    "2. Return '1' if there's any hint of new image creation needed, including vague or implicit requests or even you are unsure.\n"
                    "3. Return '0' ONLY if you are 100% certain there is no need for new images and no images of these types are ever mentioned.\n\n"
                    "Respond in JSON format: {'result': ''}\n\n"
                    "Examples:\n"
                    "1. If Yes: {'result': '1'}\n"
                    "2. If Unsure: {'result': '1'}\n"
                    "3. If 100% No: {'result': '0'}\n\n"
                    "Ensure valid, parseable JSON. No extra text or formatting."
                )
            },
            {
                "role": "user",
                "content": f"Analyze this request for new image (PNG, png, JPG, jpg, JPEG, jpeg, or .ico) creation needs: {user_prompt}"
            }
        ]

        try:
            logger.debug("\n #### The `ImageCheckAgent` is initiating a request to the AI Gateway")
            response = await self.ai.prompt(messages, self.max_tokens, 0, 0)
            res = json.loads(response.choices[0].message.content)
            logger.debug("\n #### The `ImageCheckAgent` has successfully parsed the AI response")
            return res
        except json.JSONDecodeError:
            logger.debug("\n #### The `ImageCheckAgent` encountered a JSON decoding error and is attempting to repair it")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            logger.debug("\n #### The `ImageCheckAgent` has successfully repaired and parsed the JSON")
            return plan_json
        except Exception as e:
            logger.error(f"  The `ImageCheckAgent` encountered an error during the process: `{e}`")
            return {
                "reason": str(e)
            }

    async def get_image_check_plans(self, user_prompt):
        """
        Get image generation plans based on the user prompt.

        Args:
            files (list): List of file paths.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Image generation plan or error reason.
        """
        logger.debug("\n #### The `ImageCheckAgent` is beginning to retrieve image check plans")
        plan = await self.get_image_check_plan(user_prompt)
        logger.debug("\n #### The `ImageCheckAgent` has successfully retrieved image check plans")
        return plan
