from typing import Any
from dynaconf import Dynaconf, settings
from my_app.home_app.views import home_app
from quart import Quart


def init_config(app: Quart, **config_overrides: Any) -> None:
    """Initialize configuration"""
    settings.configure(
        settings_files=["settings.toml"],
        environments=True,
        env_switcher="ENV_FOR_DYNACONF",
    )
    app.config.from_object(settings)
    app.config.update(config_overrides)


async def create_app(**config_overrides: Any) -> Quart:
    """
    Factory application creator
    args: config_overrides = testing overrides
    """
    app = Quart(__name__)
    init_config(app, **config_overrides)

    # register blueprints
    app.register_blueprint(home_app)

    return app
