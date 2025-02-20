from typing import List, Union, Generator, Iterator
from schemas import OpenAIChatMessage
import requests
import base64
import os


class Pipeline:
    def __init__(self):
        # Optionally, you can set the id and name of the pipeline.
        # Best practice is to not specify the id so that it can be automatically inferred from the filename, so that users can install multiple versions of the same pipeline.
        # The identifier must be unique across all pipelines.
        # The identifier must be an alphanumeric string that can include underscores or hyphens. It cannot contain spaces, special characters, slashes, or backslashes.
        # self.id = "ollama_pipeline"
        self.name = "Ollama Pipeline"
        pass

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        print(f"on_shutdown:{__name__}")
        pass

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # This is where you can add your custom pipelines like RAG.
        print(f"pipe:{__name__}")

        OLLAMA_BASE_URL = "http://localhost:11434"
        MODEL = "llama3"

        if "user" in body:
            print("######################################")
            print(f'# User: {body["user"]["name"]} ({body["user"]["id"]})')
            print(f"# Message: {user_message}")
            print("######################################")

        try:
            # return "test"
            sk = os.getenv("SK")
            if not sk:
                raise ValueError("Environment variable 'SK' is not set")

            payload = {
                "pk": sk,
                "module": "github.com/rhochmayr/ollama-deepseek-r1-7b:1.0.0",
                "inputs": f'-i "{user_message}"',
                "format": "json",
                "stream": "true"
            }
            response = requests.post(
                "https://js-cli.arsenum.com",
                headers={"Content-Type": "application/json"},
                json=payload
            )
            response.raise_for_status()
            json_response = response.json()
            print("json", json_response)
            decoded_output = json_response.get("stdout", "")
            decoded_output = decoded_output.encode('ascii')
            decoded_output = base64.b64decode(decoded_output).decode('ascii')
            return decoded_output
            # r = requests.post(
            #     url=f"{OLLAMA_BASE_URL}/v1/chat/completions",
            #     json={**body, "model": MODEL},
            #     stream=True,
            # )

            # r.raise_for_status()

            # if body["stream"]:
            #     return r.iter_lines()
            # else:
            #     return r.json()
        except Exception as e:
            return f"Error: {e}"
