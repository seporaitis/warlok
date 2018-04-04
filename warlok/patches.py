import types
from github import PullRequest


def _create_review_request_patch(self, reviewers, team_reviewers=None):
    """
    :calls: `POST /repos/:owner/:repo/pulls/:number/reviews <https://developer.github.com/v3/pulls/reviews/>`_
    :param reviewers: list
    :param team_reviewers: list
    :rtype: tuple(headers, data)
    """
    assert isinstance(reviewers, list), reviewers
    post_parameters = {
        'reviewers': reviewers,
        'team_reviewers': team_reviewers or [],
    }
    headers, data = self._requester.requestJsonAndCheck(
        "POST",
        self.url + "/requested_reviewers",
        input=post_parameters,
    )

    return headers, data

def patch_pull_request(pull_request):
    """Add a function to a pull request instance."""

    assert not hasattr(pull_request, 'create_review_request')

    pull_request.create_review_request = _create_review_request_patch.__get__(pull_request)
