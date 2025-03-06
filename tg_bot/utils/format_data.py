

def format_tasks(tasks, start_from=1):
    format_tasks = ""
    for i, task in enumerate(tasks, start=start_from):
        format_tasks += f"{i}. Название: {task.title}\n"
        format_tasks += f"Сложность: {task.difficulty.value}\n"
        format_tasks += f"Ссылка на задачу: {task.link}\n"
    return format_tasks
