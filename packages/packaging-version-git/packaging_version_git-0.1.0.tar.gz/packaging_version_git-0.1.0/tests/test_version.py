from pprint import pp

from packaging_version_git.version import GitVersion


class TestGitVersion(object):
    def test_init(self):
        GitVersion('0.0.0')

    def test_from_tag(self):
        v = GitVersion.from_tag()
        pp(v)
        assert v

    def test_from_commit(self):
        v = GitVersion.from_commit()
        pp(v)
        assert v
