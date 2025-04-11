from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings


class RunModule(BaseModel):
    '''
    Configs for running the project.
    '''
    host: str = "0.0.0.0"
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = "/api/v1"


class DatabaseModule(BaseModel):
    url: PostgresDsn,
    echo: bool = False,
    echo_pool: bool = False,
    pool_size: int = 50,
    max_overflow: int = 10,



class Settings(BaseSettings):
    run: RunModule = RunModule()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseModule


settings = Settings()
