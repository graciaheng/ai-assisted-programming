import shutil
import subprocess
import sys
from pathlib import Path


CLI = Path(__file__).with_name("cli.py")


def run_cli(folder, *args):
    return subprocess.run(
        [sys.executable, str(folder / "cli.py"), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def isolated_cli(tmp_path):
    shutil.copy(CLI, tmp_path / "cli.py")
    return tmp_path


def test_tasks_persist_between_cli_runs(tmp_path):
    folder = isolated_cli(tmp_path)

    added = run_cli(folder, "add", "Buy milk")
    listed = run_cli(folder, "list")

    assert added.returncode == 0
    assert "Buy milk" in added.stdout
    assert listed.returncode == 0
    assert "[ ] 1: Buy milk" in listed.stdout


def test_can_mark_a_task_done_and_delete_it(tmp_path):
    folder = isolated_cli(tmp_path)
    run_cli(folder, "add", "Buy milk")

    completed = run_cli(folder, "done", "1")
    listed = run_cli(folder, "list")
    deleted = run_cli(folder, "delete", "1")
    empty_list = run_cli(folder, "list")

    assert completed.returncode == 0
    assert "[x] 1: Buy milk" in listed.stdout
    assert deleted.returncode == 0
    assert "No tasks yet." in empty_list.stdout


def test_unknown_task_id_returns_an_error(tmp_path):
    result = run_cli(isolated_cli(tmp_path), "done", "42")

    assert result.returncode == 1
    assert "Task 42 not found." in result.stderr
