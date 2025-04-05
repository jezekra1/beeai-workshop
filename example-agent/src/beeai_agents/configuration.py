from pydantic_settings import BaseSettings


class Configuration(BaseSettings):
    hello_template: str = "Ciao %s!"
