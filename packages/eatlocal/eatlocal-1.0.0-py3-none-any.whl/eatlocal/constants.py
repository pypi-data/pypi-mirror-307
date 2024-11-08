from pathlib import Path
from enum import Enum


class ConsoleStyle(Enum):
    SUCCESS = "green"
    SUGGESTION = "yellow"
    WARNING = "red"


BITE_URL = "https://pybitesplatform.com{bite_name}"
EATLOCAL_HOME = Path().home() / ".eatlocal"
EXERCISES_URL = "https://pybitesplatform.com/bites/regular/"
FZF_DEFAULT_OPTS = "--height 13 --layout=reverse --border rounded --margin=2%,5%,10%,2%"
LOGIN_URL = "https://pybitesplatform.com/accounts/auth/login/"
PROFILE_URL = "https://pybitesplatform.com/accounts/profile/"
TIMEOUT_LENGTH = 30000
