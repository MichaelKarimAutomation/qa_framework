import pytest
import allure
from pathlib import Path


ENV_FILES = ['.env']


def _parse_env_file(path):
    """Parse a dotenv-style file into a dict, skipping blank lines and `#` comments and stripping whitespace around keys and values."""
    result = {}
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        key, _, value = line.partition('=')
        result[key.strip()] = value.strip()
    return result


def _required_keys():
    """Return the keys in .env.example that have a non-empty value. These are treated as the contract every other env file must satisfy."""
    example = _parse_env_file('.env.example')
    return [k for k, v in example.items() if v]


_required = _required_keys()


@allure.feature('Environment Config')
@allure.story('Env file values match .env.example')
@pytest.mark.smoke
@pytest.mark.parametrize('env_file', ENV_FILES)
@pytest.mark.parametrize('key', _required)
def test_env_file_matches_example(env_file, key):
    """For every required key in .env.example (those with a non-empty value), verify that the corresponding entry in each real env file (.env, etc.) exists and matches case-insensitively. Catches drift between the committed template and the actual env files used to run the suite."""
    assert Path(env_file).exists(), f'{env_file} does not exist'
    expected = _parse_env_file('.env.example')[key]
    actual = _parse_env_file(env_file).get(key, '')
    assert actual.lower() == expected.lower(), (
        f'{key} in {env_file} does not match .env.example '
        f'(expected {expected!r}, got {actual!r})'
    )
