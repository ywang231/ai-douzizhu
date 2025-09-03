# ai-douzizhu
Use various ai models to play douzizhu (A popular Chinese poker card game).

## Quick Setup
1. Install `uv` [here](https://docs.astral.sh/uv/guides/install-python/) if it is not installed.
2. Open terminal under the project path, run `uv sync` to set up the python environment
3. Create a `.env` file in the project root.  
4. Add environment variables:  
DEV_MODE=debug  
LOG_PATH=game.log  
FILE_LOG_SWITCH=true  
OPEN_ROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxx
5. Set up an OpenRouter account [here](https://openrouter.ai/)
6. Obtain API key from OpenRouter and replace the `OPEN_ROUTER_API_KEY` in `.env `.
