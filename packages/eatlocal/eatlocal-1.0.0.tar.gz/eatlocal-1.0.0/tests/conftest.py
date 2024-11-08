"""eatlocal specific pytest configuration
"""


from pathlib import Path

import pytest
from dotenv import dotenv_values

from eatlocal.constants import EATLOCAL_HOME


# @pytest.fixture(scope='session')
# def bites_repo_dir(tmp_path_factory) -> Generator[Path, None, None]:
#     cwd = Path.cwd()
#     testing = tmp_path_factory.mktemp('testing_repo')
#     os.chdir(testing)
#
#     yield testing
#
#     os.chdir(cwd)


@pytest.fixture
def testing_config() -> dict[str, str]:
    config = {"PYBITES_USERNAME": "", "PYBITES_PASSWORD": "", "PYBITES_REPO": ""}
    config.update(dotenv_values(dotenv_path=Path(EATLOCAL_HOME / ".env")))
    config["PYBITES_REPO"] = Path("./tests/testing_repo").resolve()
    return config
