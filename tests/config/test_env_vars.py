import pytest
import allure
from pathlib import Path


ENV_FILES = ['.env']


def _parse_env_file(path):
    result = {}
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        key, _, value = line.partition('=')
        result[key.strip()] = value.strip()
    return result


def _required_keys():
    example = _parse_env_file('.env.example')
    return [k for k, v in example.items() if v]


_required = _required_keys()


@allure.feature('Environment Config')
@allure.story('Env file values match .env.example')
@pytest.mark.smoke
@pytest.mark.parametrize('env_file', ENV_FILES)
@pytest.mark.parametrize('key', _required)
def test_env_file_matches_example(env_file, key):
    assert Path(env_file).exists(), f'{env_file} does not exist'
    expected = _parse_env_file('.env.example')[key]
    actual = _parse_env_file(env_file).get(key, '')
    assert actual.lower() == expected.lower(), (
        f'{key} in {env_file} does not match .env.example '
        f'(expected {expected!r}, got {actual!r})'
    )
