# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,
# pylint: disable=missing-module-docstring
# pylint: disable=broad-exception-caught
# pylint: disable=missing-class-docstring
import os
import asyncio
from openai import AsyncOpenAI, DefaultAioHttpClient
from dotenv import load_dotenv

load_dotenv()

OPEN_ROUTER_URL = "https://openrouter.ai/api/v1"
DEEP_SEEK_MODEL = "tngtech/deepseek-r1t-chimera:free"
GPT_OSS_MODEL = "openai/gpt-oss-20b:free"
LLAMA_3_3_MODEL = "meta-llama/llama-3.3-8b-instruct:free"


async def create_client_() -> AsyncOpenAI:
    return AsyncOpenAI(
        base_url=OPEN_ROUTER_URL,
        api_key=os.environ.get("OPEN_ROUTER_API_KEY"),  # Read from .env
        http_client=DefaultAioHttpClient()
    )


async def query_(model: str, msg: list) -> str:
    client = await create_client_()
    response = await client.chat.completions.create(
        model=model,
        messages=msg
    )
    await client.close()
    return str(response.choices[0].message.content)


async def deepseek_r1t_chimera(msg: list) -> str:
    return await query_(DEEP_SEEK_MODEL, msg)


async def gpt_oss(msg: list) -> str:
    return await query_(GPT_OSS_MODEL, msg)


async def llama_3_3(msg: list) -> str:
    return await query_(LLAMA_3_3_MODEL, msg)


async def test1():
    response = await deepseek_r1t_chimera([
        {
            "role": "user",
            "content": "Do you know Trump?"
        }
    ])
    print(response)


async def test2():
    response = await gpt_oss([
        {
            "role": "user",
            "content": "Explain me the meaning of life?"
        }
    ])
    print(response)


async def test3():
    response = await llama_3_3([
        {
            "role": "user",
            "content": "Do you know Mark Carney?"
        }
    ])
    print(response)


async def test4():
    print("Test 4 running...")


async def _test_run():
    await asyncio.gather(test1(), test2(), test3(), test4(), test4())


if __name__ == "__main__":
    asyncio.run(_test_run())
