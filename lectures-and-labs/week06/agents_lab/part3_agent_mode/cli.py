import argparse
import json
import sys
from pathlib import Path


TASKS_FILE = Path(__file__).with_name("tasks.json")


def load_tasks():
    if not TASKS_FILE.exists():
        return []

    with TASKS_FILE.open(encoding="utf-8") as tasks_file:
        tasks = json.load(tasks_file)

    if not isinstance(tasks, list) or any(
        not isinstance(task, dict)
        or not isinstance(task.get("id"), int)
        or not isinstance(task.get("title"), str)
        or not isinstance(task.get("done"), bool)
        for task in tasks
    ):
        raise ValueError("tasks.json has an invalid format")
    return tasks


def save_tasks(tasks):
    with TASKS_FILE.open("w", encoding="utf-8") as tasks_file:
        json.dump(tasks, tasks_file, indent=2)
        tasks_file.write("\n")


def build_parser():
    parser = argparse.ArgumentParser(description="Keep a simple to-do list.")
    commands = parser.add_subparsers(dest="command", required=True)

    add_command = commands.add_parser("add", help="Add a task")
    add_command.add_argument("title", help="What you need to do")

    commands.add_parser("list", help="List all tasks")

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
        }
        tasks.append(task)
        save_tasks(tasks)
        print(f"Added task {task['id']}: {task['title']}")
        return 0

    if args.command == "list":
        if not tasks:
            print("No tasks yet.")
        for task in tasks:
            status = "x" if task["done"] else " "
            print(f"[{status}] {task['id']}: {task['title']}")
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
