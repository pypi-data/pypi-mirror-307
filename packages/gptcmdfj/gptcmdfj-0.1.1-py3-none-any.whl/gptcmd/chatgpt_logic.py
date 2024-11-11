import asyncio
import dotenv
import sys

dotenv.load_dotenv()

async def main(prompt, client):
    stream = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    async for chunk in stream:
        content = chunk.choices[0].delta.content or ""
        
        # Write the content to stdout without a newline and flush immediately
        sys.stdout.write(content)
        sys.stdout.flush()

if __name__ == "__main__":
    PROMPT = "Tell me a little bit about narwhals"
    asyncio.run(main(PROMPT))