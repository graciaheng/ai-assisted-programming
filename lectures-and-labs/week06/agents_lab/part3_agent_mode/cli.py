import argparse
import json
import sys
from datetime import date
from pathlib import Path


TASKS_FILE = Path(__file__).with_name("tasks.json")


def parse_due_date(value):
    try:
        due_date = date.fromisoformat(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "due date must be in YYYY-MM-DD format"
        ) from error
    if due_date.isoformat() != value:
        raise argparse.ArgumentTypeError(
            "due date must be in YYYY-MM-DD format"
        )
    return due_date


def load_tasks():
    if not TASKS_FILE.exists():
        return []

    with TASKS_FILE.open(encoding="utf-8") as tasks_file:
        tasks = json.load(tasks_file)

    if not isinstance(tasks, list):
        raise ValueError("tasks.json has an invalid format")
    for task in tasks:
        if (
            not isinstance(task, dict)
            or not isinstance(task.get("id"), int)
            or not isinstance(task.get("title"), str)
            or not isinstance(task.get("done"), bool)
        ):
            raise ValueError("tasks.json has an invalid format")
        due_date = task.get("due_date")
        if due_date is not None:
            try:
                parsed_due_date = date.fromisoformat(due_date)
            except (TypeError, ValueError) as error:
                raise ValueError("tasks.json has an invalid format") from error
            if parsed_due_date.isoformat() != due_date:
                raise ValueError("tasks.json has an invalid format")
    return tasks


def save_tasks(tasks):
    with TASKS_FILE.open("w", encoding="utf-8") as tasks_file:
        json.dump(tasks, tasks_file, indent=2)
        tasks_file.write("\n")


def build_parser():
    parser = argparse.ArgumentParser(description="Keep a simple to-do list.")
    parser.add_argument("--version", action="version", version="1.0")
    commands = parser.add_subparsers(dest="command", required=True)

    add_command = commands.add_parser("add", help="Add a task")
    add_command.add_argument("title", help="What you need to do")
    add_command.add_argument(
        "--due-date",
        type=parse_due_date,
        help="Due date in YYYY-MM-DD format",
    )

    list_command = commands.add_parser("list", help="List tasks")
    list_filters = list_command.add_mutually_exclusive_group()
    list_filters.add_argument(
        "--overdue",
        action="store_true",
        help="List unfinished tasks due before today",
    )
    list_filters.add_argument(
        "--due-today",
        action="store_true",
        help="List unfinished tasks due today",
    )

    done_command = commands.add_parser("done", help="Mark a task as done")
    done_command.add_argument("id", type=int, help="Task ID shown by list")

    delete_command = commands.add_parser("delete", help="Delete a task")
    delete_command.add_argument("id", type=int, help="Task ID shown by list")

    return parser


def run_command(args):
    tasks = load_tasks()

    if args.command == "add":
        task = {
            "id": max((task["id"] for task in tasks), default=0) + 1,
            "title": args.title,
            "done": False,
            "due_date": args.due_date.isoformat() if args.due_date else None,
        }
        tasks.append(task)
        save_tasks(tasks)
        print(f"Added task {task['id']}: {task['title']}")
        return 0

    if args.command == "list":
        today = date.today()
        if args.overdue:
            tasks = [
                task
                for task in tasks
                if not task["done"]
                and task.get("due_date") is not None
                and date.fromisoformat(task["due_date"]) < today
            ]
            empty_message = "No overdue tasks."
        elif args.due_today:
            tasks = [
                task
                for task in tasks
                if not task["done"] and task.get("due_date") == today.isoformat()
            ]
            empty_message = "No tasks due today."
        else:
            empty_message = "No tasks yet."

        if not tasks:
            print(empty_message)
        for task in tasks:
            status = "x" if task["done"] else " "
            due_date = (
                f" (due: {task['due_date']})" if task.get("due_date") else ""
            )
            print(f"[{status}] {task['id']}: {task['title']}{due_date}")
        return 0

    task = next((task for task in tasks if task["id"] == args.id), None)
    if task is None:
        print(f"Task {args.id} not found.", file=sys.stderr)
        return 1

    if args.command == "done":
        task["done"] = True
        save_tasks(tasks)
        print(f"Completed task {task['id']}: {task['title']}")
    elif args.command == "delete":
        tasks.remove(task)
        save_tasks(tasks)
        print(f"Deleted task {task['id']}: {task['title']}")
    return 0


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        return run_command(args)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
