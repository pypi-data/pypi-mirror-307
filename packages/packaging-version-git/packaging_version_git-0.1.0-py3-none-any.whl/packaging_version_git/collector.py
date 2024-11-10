import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pygit2
from pygit2.enums import ReferenceFilter
from pygit2.repository import Repository

logger = logging.getLogger('packaging-version-git')


@dataclass()
class GitCommitStatus(object):
    tag_name: Optional[str]
    hash: str

    @property
    def short_hash(self):
        return self.hash[:7]


@dataclass()
class GitStatus(object):
    is_dirty: bool
    tag: Optional[GitCommitStatus]
    commit: GitCommitStatus
    distance: int


class GitVersionCollector(object):
    repo: Repository

    def __init__(self) -> None:
        path = Path.cwd()
        self.repo = Repository(str(path.resolve()))

    @property
    def commits(self) -> list[pygit2.Commit]:
        return list(self.repo.walk(self.repo.head.target))

    @property
    def tags(self) -> list[pygit2.Reference]:
        tags: list[pygit2.Reference] = []

        for i in list(
            self.repo.references.iterator(
                ReferenceFilter.TAGS,
            )
        ):
            tags.append(i)

        return tags

    def get_last_tag(self) -> Optional[pygit2.Reference]:
        """Получение последнего тега нынешней ветки."""
        tag_dict = {tag.target: tag for tag in self.tags}

        for commit in self.commits:
            if commit.id in tag_dict:
                return tag_dict[commit.id]

        return None

    def get_distance(self, from_commit: pygit2.Commit, to_commit: pygit2.Commit) -> int:
        walker = self.repo.walk(to_commit.short_id)
        walker.hide(from_commit.short_id)
        return sum(1 for _ in walker)

    def is_dirty(self) -> bool:
        """Проверка, есть ли незафиксированные изменения в репозитории."""
        status = self.repo.status()
        return bool(status)

    def get_status(self) -> GitStatus:
        tag = self.get_last_tag()
        commit = self.repo.head.peel(pygit2.Commit)

        if tag is None:
            return GitStatus(
                self.is_dirty(),
                None,
                GitCommitStatus(
                    None,
                    str(commit.id),
                ),
                0,
            )

        tag_comit = tag.peel(pygit2.Commit)

        is_current_tag = tag_comit.short_id == commit.short_id
        distance = self.get_distance(tag_comit, commit)

        return GitStatus(
            self.is_dirty(),
            GitCommitStatus(tag.shorthand, tag_comit.short_id),
            GitCommitStatus(tag.name if is_current_tag else None, commit.short_id),
            distance,
        )
