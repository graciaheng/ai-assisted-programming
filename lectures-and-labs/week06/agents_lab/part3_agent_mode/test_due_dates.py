import shutil
import subprocess
import sys
from datetime import date, timedelta
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


def add_task(folder, title, due_date=None):
    command = ["add", title]
    if due_date is not None:
        command.extend(["--due-date", due_date])
    return run_cli(folder, *command)


def test_add_and_list_task_with_due_date(tmp_path):
    folder = isolated_cli(tmp_path)
    due_date = (date.today() + timedelta(days=1)).isoformat()

    added = add_task(folder, "Pay bill", due_date)
    listed = run_cli(folder, "list")

    assert added.returncode == 0
    assert listed.returncode == 0
    assert f"[ ] 1: Pay bill (due: {due_date})" in listed.stdout


def test_overdue_list_shows_only_unfinished_past_due_tasks(tmp_path):
    folder = isolated_cli(tmp_path)
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    today = date.today().isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    add_task(folder, "Overdue", yesterday)
    add_task(folder, "Due today", today)
    add_task(folder, "Due later", tomorrow)
    add_task(folder, "No due date")
    add_task(folder, "Completed overdue", yesterday)
    run_cli(folder, "done", "5")

    result = run_cli(folder, "list", "--overdue")

    assert result.returncode == 0
    assert "[ ] 1: Overdue" in result.stdout
    assert "Due today" not in result.stdout
    assert "Due later" not in result.stdout
    assert "No due date" not in result.stdout
    assert "Completed overdue" not in result.stdout


def test_due_today_list_shows_only_unfinished_tasks_due_today(tmp_path):
    folder = isolated_cli(tmp_path)
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    today = date.today().isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    add_task(folder, "Overdue", yesterday)
    add_task(folder, "Due today", today)
    add_task(folder, "Due tomorrow", tomorrow)
    add_task(folder, "Completed today", today)
    run_cli(folder, "done", "4")

    result = run_cli(folder, "list", "--due-today")

    assert result.returncode == 0
    assert f"[ ] 2: Due today (due: {today})" in result.stdout
    assert "Overdue" not in result.stdout
    assert "Due tomorrow" not in result.stdout
    assert "Completed today" not in result.stdout


def test_invalid_due_date_is_rejected(tmp_path):
    result = run_cli(
        isolated_cli(tmp_path),
        "add",
        "Pay bill",
        "--due-date",
        "tomorrow",
    )

    assert result.returncode == 2
    assert "due date must be in YYYY-MM-DD format" in result.stderr
