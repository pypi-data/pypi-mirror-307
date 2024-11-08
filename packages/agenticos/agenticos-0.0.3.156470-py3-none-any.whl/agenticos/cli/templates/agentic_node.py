from dotenv import load_dotenv

from agenticos.node.httpnode import create_server

from .agentic_config import config

load_dotenv()

app = create_server(config=config)
