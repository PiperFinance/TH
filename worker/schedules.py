from celery.schedules import crontab


_all_tasks = {
    "save_func_selectors":
        {
            'func_selector':
            {
                'task': 'save_func_selectors',
                'schedule': crontab(hour='*/24')

            }
        }
}


all_schedules = {}

for cat in _all_tasks:
    for task_name, task_det in _all_tasks[cat].items():
        all_schedules.update({task_name: task_det})
