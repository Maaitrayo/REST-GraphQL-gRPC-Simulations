from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "REST Simulation API"
    app_version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"


settings = Settings()
