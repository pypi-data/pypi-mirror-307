import tests
import pytest
from pydantic import ValidationError
from agenteasy.models import *


def test_api_key_format():
    with pytest.raises(ValidationError):
        Moonshot(api_key="abcd123")
