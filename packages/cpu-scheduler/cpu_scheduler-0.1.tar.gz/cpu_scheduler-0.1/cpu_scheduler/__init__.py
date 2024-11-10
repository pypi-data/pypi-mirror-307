# cpu_scheduler/__init__.py

from .algorithms import fcfs, sjf, round_robin, priority_scheduling

# Define what’s available when importing *
__all__ = ["fcfs", "sjf", "round_robin", "priority_scheduling"]
