import asyncio
import concurrent
import os

from application.datasource.init_data_source import setup_data_source
import application.abilities.async_tasks
import application.abilities.start_deamon

async def main():
    print("Hello, World!")

if __name__ == "__main__":
    asyncio.run(main())
