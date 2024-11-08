import os
import pytest
from redminelib import Redmine
from redminelib.resources import Issue as RedmineIssue
from dotenv import load_dotenv

from main import Fiscaliza, Issue

load_dotenv(override=True)


class TestIssue:
    @pytest.fixture
    def username(self):
        return os.environ["USERNAME"]

    @pytest.fixture
    def password(self):
        return os.environ["PASSWORD"]

    @pytest.fixture
    def key(self):
        return os.environ["KEY"]

    @pytest.fixture
    def fiscaliza(self, username, password):
        return Fiscaliza(username, password)

    @pytest.mark.parametrize("issue_id", [124144, 84047])
    def test_auth_sucess(self, fiscaliza, issue_id):
        assert isinstance(fiscaliza.client, Redmine)
        issue = Issue(fiscaliza.client, issue_id)
        assert isinstance(issue._issue, RedmineIssue)

    @pytest.mark.parametrize("issue_id", [124144, 84047, 79078, 77719])
    def test_attrs(self, fiscaliza, issue_id):
        issue = Issue(fiscaliza.client, issue_id)
        assert isinstance(issue.details, dict)
        assert isinstance(issue.attachments, dict)
        assert isinstance(issue.custom_fields, dict)
        assert isinstance(issue.relations, dict)
