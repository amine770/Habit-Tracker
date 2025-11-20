from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname : str
    database_password : str
    database_port : str
    database_username : str
    database_name : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int

    model_config = {
        "env_file" : ".env"
    }

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.database_username}:{self.database_password}"
            f"@{self.database_hostname}:{self.database_port}/{self.database_name}"
        )