import typing

import confboy


config = confboy.Config({
    'postgres': {
        'host': '127.0.0.1',
        'port': 5432,
        'username': 'toni',
        'password': 'toni',
        'database': 'toni',
        'url': 'callable:postgres_url',
    },
})


def postgres_url() -> str:
    return (
        'postgresql:/'
        f'/{config.postgres.username}:{config.postgres.password}'
        f'@{config.postgres.host}:{config.postgres.port}'
        f'/{config.postgres.database}'
    )


config.register_callable(postgres_url)


def __getattr__(key: str) -> typing.Any:
    return getattr(config, key)
