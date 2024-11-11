import argparse
import asyncio
from openai import AsyncOpenAI

from .chatgpt_logic import main as chatgpt_main  # Relative import for package context

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="supply your prompt, enclosed in quotes")
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    client = AsyncOpenAI()
    asyncio.run(chatgpt_main(args.prompt, client))

if __name__ == "__main__":
    main()