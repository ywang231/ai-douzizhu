# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,
# pylint: disable=missing-module-docstring
# pylint: disable=broad-exception-caught
# pylint: disable=missing-class-docstring
import os
import asyncio
from openai import AsyncOpenAI, DefaultAioHttpClient
from dotenv import load_dotenv

# OpenRouter API settings, models, modify here to choose models you prefer.
OPEN_ROUTER_URL = "https://openrouter.ai/api/v1"
DEEP_SEEK_MODEL = "tngtech/deepseek-r1t-chimera:free"
GEMINI_2_5_FLASH = "google/gemini-2.5-flash-image-preview:free"
LLAMA_3_3_MODEL = "meta-llama/llama-3.3-8b-instruct:free"

__all__ = ['deepseek_r1t_chimera', 'gemini_2_5_flash', 'llama_3_3']


# Create OpenAI client
async def create_client_() -> AsyncOpenAI:
    return AsyncOpenAI(
        base_url=OPEN_ROUTER_URL,
        api_key=os.environ.get("OPEN_ROUTER_API_KEY"),  # Read from .env
        http_client=DefaultAioHttpClient()
    )


# Query OpenAI models
async def query_(model: str, msg: list) -> str:
    client = await create_client_()
    response = await client.chat.completions.create(
        model=model,
        messages=msg
    )
    await client.close()
    return str(response.choices[0].message.content)


# DeepSeek R1T Chimera
async def deepseek_r1t_chimera(msg: list) -> str:
    return await query_(DEEP_SEEK_MODEL, msg)


# GEMINI 2.5 FLASH
async def gemini_2_5_flash(msg: list) -> str:
    return await query_(GEMINI_2_5_FLASH, msg)


# LLaMA 3.3
async def llama_3_3(msg: list) -> str:
    return await query_(LLAMA_3_3_MODEL, msg)


async def _main():
    response = await deepseek_r1t_chimera([
        {
            "role": "user",
            "content": "Explain me the meaning of life, what should we do in this AI era?"
        }
    ])
    print(response)

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(_main())
