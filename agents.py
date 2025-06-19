
import asyncio
import httpx

class Agent:
    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions

class AsyncOpenAI:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    async def chat(self, prompt, model):
        url = f"{self.base_url}chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        body = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        }
        async with httpx.AsyncClient() as client:
            res = await client.post(url, headers=headers, json=body)
            res.raise_for_status()
            return res.json()["choices"][0]["message"]["content"]

class OpenAIChatCompletionsModel:
    def __init__(self, model, openai_client):
        self.model = model
        self.client = openai_client

    async def generate(self, prompt):
        return await self.client.chat(prompt, self.model)

class RunConfig:
    def __init__(self, model, model_provider, tracing_disabled=True):
        self.model = model
        self.model_provider = model_provider
        self.tracing_disabled = tracing_disabled

class Runner:
    @staticmethod
    def run_sync(agent, input, run_config):
        async def run():
            return await run_config.model.generate(input)
        return asyncio.run(run())
