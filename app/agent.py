from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from app.config import get_settings
from app.prompt import prompt
from app.tools import get_tools

settings = get_settings()


model = init_chat_model(
    model=settings.model_name,
    model_provider=settings.model_provider,
    api_key=settings.google_api_key
)

agent = create_agent(
    model=model,
    tools=get_tools(),
    system_prompt=prompt,
)
