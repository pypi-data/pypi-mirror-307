from packaging.version import Version
from packaging_version_increment import update_version

from packaging_version_git.collector import GitVersionCollector  # noqa: F401


class GitVersion(Version):
    @classmethod
    def from_tag(cls):
        collector = GitVersionCollector()

        status = collector.get_status()

        if status.tag is not None and status.tag.tag_name:
            return cls(status.tag.tag_name)

        return cls('0.0.0')

    @classmethod
    def from_commit(
        cls,
        as_alpha: bool = False,
        as_beta: bool = False,
        as_rc: bool = False,
        as_post: bool = False,
        as_dev: bool = True,
    ) -> Version:
        collector = GitVersionCollector()
        status = collector.get_status()

        assert any([as_alpha, as_beta, as_rc, as_post, as_dev])

        if status.tag is None or status.tag.tag_name is None:
            return cls('0.0.0')

        version = cls(status.tag.tag_name)

        if as_alpha:
            return update_version(version, alpha=status.distance, local=status.commit.short_hash)

        if as_beta:
            return update_version(version, beta=status.distance, local=status.commit.short_hash)

        if as_rc:
            return update_version(version, rc=status.distance, local=status.commit.short_hash)

        if as_post:
            return update_version(version, post=status.distance, local=status.commit.short_hash)

        if as_dev:
            return update_version(version, dev=status.distance, local=status.commit.short_hash)

        return version
