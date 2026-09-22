from pathlib import Path

import pytest

from abs_core import update_manager


def test_runtime_artifacts_do_not_block_updates(monkeypatch):
    monkeypatch.setattr(update_manager, "_git", lambda *args: "?? abs.db\n?? abs_core/__pycache__/\n?? .pytest_cache/")
    assert update_manager._blocking_worktree_changes() == []


def test_real_untracked_file_still_blocks_updates(monkeypatch):
    monkeypatch.setattr(update_manager, "_git", lambda *args: "?? unexpected.txt")
    assert update_manager._blocking_worktree_changes() == ["?? unexpected.txt"]


def test_runtime_path_classifier():
    assert update_manager._runtime_only_change("abs.db")
    assert update_manager._runtime_only_change("abs.db-wal")
    assert update_manager._runtime_only_change("abs_core/__pycache__/x.pyc")
    assert update_manager._runtime_only_change(".pytest_cache/v/cache/nodeids")
    assert not update_manager._runtime_only_change("docs/change.md")
