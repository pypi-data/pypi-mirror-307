import os
import pytest
from redminelib import Redmine
from dotenv import load_dotenv

from fiscaliza.main import Fiscaliza

load_dotenv(override=True)


class TestFiscaliza:
    @pytest.fixture
    def username(self):
        return os.environ["USERNAME"]

    @pytest.fixture
    def password(self):
        return os.environ["PASSWORD"]

    @pytest.fixture
    def key(self):
        return os.environ["KEY"]

    @pytest.mark.parametrize("teste", [True, False])
    def test_authenticate_success(self, username, password, teste):
        fiscaliza = Fiscaliza(username, password, teste=teste).authenticate()
        assert isinstance(fiscaliza, Redmine)

    @pytest.mark.parametrize("teste", [True, False])
    def test_key(self, username, password, teste, key):
        fiscaliza = Fiscaliza(username, password, teste, key=key)
        assert fiscaliza.key == os.environ["KEY"]
        assert fiscaliza.username == os.environ["USERAPI"]
        assert isinstance(fiscaliza.client, Redmine)
