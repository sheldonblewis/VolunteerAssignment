from task import Task
from volunteer import Volunteer


class AssignmentServer:
    tasks: dict[int, Task]
    volunteers: dict[int, Volunteer]
    assignments: dict[Task, Volunteer]

    def __init__(self, tasks: dict[int, Task], volunteers: dict[int, Volunteer]):
        self.tasks = tasks
        self.volunteers = volunteers
        self.assignments = {task: [] for task in tasks.values()}

    def get_interested_volunteers(self, task: Task) -> list[Volunteer]:
        return [
            volunteer for volunteer in self.volunteers.values()
            if volunteer.is_interested(task)
        ]

    def assign_tasks(self):
        for task in self.tasks.values():
            interested_volunteers = self.get_interested_volunteers(task)
            if len(interested_volunteers) >= task.required_volunteers:
                self.assignments[task] = interested_volunteers[:task.required_volunteers]
            else:
                self.assignments[task] = list(self.volunteers.values())[:task.required_volunteers]

    def print_assignments(self):
        for task in self.tasks.values():
            assignees = self.assignments.get(task, [])
            print(task)
            if assignees:
                print(f"    Assigned to {', '.join(str(a) for a in assignees)}")
            else:
                print(f"    Unassigned")
            print()

    def calculate_satisfaction_score(self) -> int:
        score = 0
        max_tasks_per_volunteer = len(self.tasks) // len(self.volunteers) + (len(self.tasks) % len(self.volunteers) > 0)

        task_count = {volunteer: 0 for volunteer in self.volunteers.values()}

        for task, assignees in self.assignments.items():
            for volunteer in assignees:
                task_count[volunteer] += 1
                if volunteer.is_interested(task):
                    rank = volunteer.interested_tasks.index(task) + 1
                    score += max(0, 5 - rank)
                else:
                    score -= 1

        for volunteer, count in task_count.items():
            if count > max_tasks_per_volunteer:
                score -= (count - max_tasks_per_volunteer)

        return score

    def print_satisfaction_score(self):
        score = self.calculate_satisfaction_score()
        print(score)

    def assign_tasks_new_algorithm(self):
        volunteer_task_count = {volunteer: 0 for volunteer in self.volunteers.values()}
        for task in self.tasks.values():
            interested_volunteers = sorted(self.get_interested_volunteers(task), key=lambda v: volunteer_task_count[v])
            if len(interested_volunteers) >= task.required_volunteers:
                self.assignments[task] = interested_volunteers[:task.required_volunteers]
                for volunteer in interested_volunteers[:task.required_volunteers]:
                    volunteer_task_count[volunteer] += 1
            else:
                self.assignments[task] = list(self.volunteers.values())[:task.required_volunteers]
                for volunteer in list(self.volunteers.values())[:task.required_volunteers]:
                    volunteer_task_count[volunteer] += 1

    def compare_algorithms(self):
        original_assignments = self.assignments.copy()
        self.assign_tasks()
        original_score = self.calculate_satisfaction_score()
        self.assignments = original_assignments

        self.assign_tasks_new_algorithm()
        new_score = self.calculate_satisfaction_score()

        print(f"Original Algorithm Satisfaction Score: {original_score}")
        print(f"New Algorithm Satisfaction Score: {new_score}")

