import fs.path
import fs.errors
from nose.tools import eq_, raises
from gitfs2.repo import (
    GitRequire,
    git_clone,
    get_app_home,
    get_repo_name,
    make_sure_git_is_available,
)

try:
    from mock import MagicMock, patch
except ImportError:
    from unittest.mock import MagicMock, patch


@patch("appdirs.user_cache_dir", return_value="root")
@patch("gitfs2.repo.mkdir_p")
@patch("fs.open_fs")
@patch("git.Repo", autospec=True)
class TestGitFunctions:
    def setUp(self):
        self.repo_name = "repoA"
        self.repo = "https://github.com/my/" + self.repo_name
        self.require = GitRequire(git_url=self.repo)
        self.require_with_submodule = GitRequire(
            git_url=self.repo, submodule="True"
        )
        self.require_with_branch = GitRequire(
            git_url=self.repo, branch="ghpages"
        )
        self.require_with_reference = GitRequire(
            git_url=self.repo, reference="a-commit-reference"
        )
        self.expected_local_repo_path = fs.path.join(
            "root", "repos", self.repo_name
        )

    def test_checkout_new(self, fake_repo, local_folder_exists, *_):
        local_folder_exists.side_effect = [fs.errors.CreateFailed]
        git_clone(self.require)
        fake_repo.clone_from.assert_called_with(
            self.repo,
            self.expected_local_repo_path,
            single_branch=True,
            depth=2,
        )
        repo = fake_repo.return_value
        eq_(repo.git.submodule.called, False)

    def test_checkout_new_with_submodules(
        self, fake_repo, local_folder_exists, *_
    ):
        local_folder_exists.side_effect = [fs.errors.CreateFailed]
        git_clone(self.require_with_submodule)
        fake_repo.clone_from.assert_called_with(
            self.repo,
            self.expected_local_repo_path,
            single_branch=True,
            depth=2,
        )
        repo = fake_repo.clone_from.return_value
        repo.git.submodule.assert_called_with("update", "--init")

    def test_git_update(self, fake_repo, local_folder_exists, *_):
        git_clone(self.require)
        fake_repo.assert_called_with(self.expected_local_repo_path)
        repo = fake_repo.return_value
        repo.git.pull.assert_called()

    def test_git_update_with_submodules(
        self, fake_repo, local_folder_exists, *_
    ):
        git_clone(self.require_with_submodule)
        fake_repo.assert_called_with(self.expected_local_repo_path)
        repo = fake_repo.return_value
        repo.git.submodule.assert_called_with("update")

    def test_checkout_new_with_branch(
        self, fake_repo, local_folder_exists, *_
    ):
        local_folder_exists.side_effect = [fs.errors.CreateFailed]
        git_clone(self.require_with_branch)
        fake_repo.clone_from.assert_called_with(
            self.repo,
            self.expected_local_repo_path,
            branch="ghpages",
            single_branch=True,
            depth=2,
        )
        repo = fake_repo.return_value
        eq_(repo.git.submodule.called, False)

    def test_update_existing_with_branch_parameter(
        self, fake_repo, local_folder_exists, *_
    ):
        git_clone(self.require_with_branch)
        repo = fake_repo.return_value
        repo.git.checkout.assert_called_with("ghpages")

    def test_checkout_new_with_reference(
        self, fake_repo, local_folder_exists, *_
    ):
        local_folder_exists.side_effect = [fs.errors.CreateFailed]
        git_clone(self.require_with_reference)
        fake_repo.clone_from.assert_called_with(
            self.repo,
            self.expected_local_repo_path,
            reference="a-commit-reference",
            single_branch=True,
            depth=2,
        )
        repo = fake_repo.return_value
        eq_(repo.git.submodule.called, False)

    def test_update_existing_with_reference_parameter(
        self, fake_repo, local_folder_exists, *_
    ):
        git_clone(self.require_with_reference)
        repo = fake_repo.return_value
        repo.git.checkout.assert_called_with("a-commit-reference")

    @patch("gitfs2.repo.reporter.warn")
    def test_update_failed_because_offline(
        self, fake_warn, fake_repo, local_folder_exists, *_
    ):
        from git.exc import GitCommandError

        repo = MagicMock(autospec=True)
        fake_repo.return_value = repo

        repo.git.pull.side_effect = [GitCommandError("a", "b")]
        git_clone(self.require_with_reference)

        fake_warn.assert_called_with("Unable to run git commands. Offline?")


def test_get_repo_name():
    repos = [
        "https://github.com/repo-abc-def/repo",
        "https://github.com/abc/repo",
        "https://github.com/abc/repo.git",
        "https://github.com/abc/repo/",
        "git@github.com:abc/repo.git",
        "git@bitbucket.org:abc/repo.git",
        "git://github.com/abc/repo.git",
    ]
    actual = [get_repo_name(repo) for repo in repos]
    expected = ["repo"] * len(repos)
    eq_(expected, actual)


@patch("gitfs2.reporter.error")
def test_get_repo_name_can_handle_invalid_url(fake_reporter):
    invalid_repo = "invalid"
    try:
        get_repo_name(invalid_repo)
    except Exception:
        fake_reporter.assert_called_with(
            'An invalid git url: "invalid" in mobanfile'
        )


@patch("appdirs.user_cache_dir", return_value="root")
def test_get_app_home(_):
    actual = get_app_home()
    eq_(fs.path.join("root", "repos"), actual)


@raises(Exception)
@patch("subprocess.check_output", side_effect=Exception)
def test_make_git_is_available(_):
    make_sure_git_is_available()
