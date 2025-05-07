#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
School Timetable Generator

This program generates an optimal weekly timetable for a school based on 
classes, subjects, teachers, and period requirements.
"""

### DO NOT MODIFY THE CODE BELOW THIS LINE ###

# Define the input constraints
# Classes
classes = ["Class 6A", "Class 6B", "Class 7A", "Class 7B"]

# Subjects
subjects = ["Mathematics", "Science", "English", "Social Studies", "Computer Science", "Physical Education"]

# Weekly period requirements for each class and subject
# {class_name: {subject_name: number_of_periods_per_week}}
class_subject_periods = {
    "Class 6A": {"Mathematics": 6, "Science": 6, "English": 6, "Social Studies": 6, "Computer Science": 3, "Physical Education": 3},
    "Class 6B": {"Mathematics": 6, "Science": 6, "English": 6, "Social Studies": 6, "Computer Science": 3, "Physical Education": 3},
    "Class 7A": {"Mathematics": 6, "Science": 6, "English": 6, "Social Studies": 6, "Computer Science": 4, "Physical Education": 2},
    "Class 7B": {"Mathematics": 6, "Science": 6, "English": 6, "Social Studies": 6, "Computer Science": 4, "Physical Education": 2}
}

# Teachers and their teaching capabilities
# {teacher_name: [list_of_subjects_they_can_teach]}
teachers = {
    "Mr. Kumar": ["Mathematics"],
    "Mrs. Sharma": ["Mathematics"],
    "Ms. Gupta": ["Science"],
    "Mr. Singh": ["Science", "Social Studies"],
    "Mrs. Patel": ["English"],
    "Mr. Joshi": ["English", "Social Studies"],
    "Mr. Malhotra": ["Computer Science"],
    "Mr. Chauhan": ["Physical Education"]
}

# School timing configuration
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
periods_per_day = 6

### DO NOT MODIFY THE CODE ABOVE THIS LINE ###

def generate_timetable():
    """
    Generate a weekly timetable for the school based on the given constraints.
    
    Returns:
        dict: A data structure representing the complete timetable
              Format: {day: {period: {class: (subject, teacher)}}}
    """
    # Initialize an empty timetable
    timetable = {day: {period: {} for period in range(1, periods_per_day + 1)} for day in days_of_week}
    
    # TODO: Implement the timetable generation algorithm
    # 1. Check if a valid timetable is possible with the given constraints
    # 2. Assign subjects and teachers to periods for each class
    # 3. Ensure all constraints are satisfied

    from collections import defaultdict
    import random

    class_subject_periods_remaining = {
        f"{cls}-{subj}": count
        for cls, subj_map in class_subject_periods.items()
        for subj, count in subj_map.items()
    }

    subject_teachers = defaultdict(list)
    for teacher, subs in teachers.items():
        for subj in subs:
            subject_teachers[subj].append(teacher)

    availability = {
        (day, period): set(teachers.keys())
        for day in days_of_week
        for period in range(1, periods_per_day + 1)
    }

    schedule = defaultdict(lambda: defaultdict(list))
    
    def get_available_class_subjects():
        return [k for k, v in class_subject_periods_remaining.items() if v > 0]
    
    for day in days_of_week:
        for period in range(1, periods_per_day + 1):
            used_teachers = set()
            used_classes = set()
            class_subjects_today = get_available_class_subjects()
            random.shuffle(class_subjects_today)
            for cs in class_subjects_today:
                class_name, subject = cs.split("-")
                if class_subject_periods_remaining[cs] <= 0:
                    continue
                if class_name in used_classes:
                    continue
                # Try to assign a teacher
                possible_teachers = [t for t in subject_teachers[subject]
                                    if t in availability[(day, period)] and t not in used_teachers]
                if possible_teachers:
                    teacher = random.choice(possible_teachers)
                    schedule[day][period].append((class_name, subject, teacher))
                    class_subject_periods_remaining[cs] -= 1
                    used_teachers.add(teacher)
                    used_classes.add(class_name)
                    availability[(day, period)].remove(teacher)

    timetable = {
        day: {
            period: {
                class_name: (subject, teacher)
                for (class_name, subject, teacher) in class_list
            }
            for period, class_list in period_map.items()
        }
        for day, period_map in schedule.items()
    }
    
    return timetable


def display_timetable(timetable):
    """
    Display the generated timetable in a readable format.
    
    Args:
        timetable (dict): The generated timetable
    """
    # TODO: Implement timetable display logic
    # Display the timetable for each class
    # Display the timetable for each teacher
    for cls in classes:
        print("\nTimetable for", cls)
        print("-" * 50)
        for day in days_of_week:
            print(day + ":")
            for p in range(1, periods_per_day + 1):
                if cls in timetable[day][p]:
                    sub, teacher = timetable[day][p][cls]
                    print("  Period {}: {} ({})".format(p, sub, teacher))
                else:
                    print("  Period {}: Free".format(p))
        print("-" * 50)

    for teacher in teachers:
        print("\nSchedule for", teacher)
        print("-" * 50)
        for day in days_of_week:
            print(day + ":")
            for p in range(1, periods_per_day + 1):
                found = False
                for cls in classes:
                    if cls in timetable[day][p]:
                        sub, t = timetable[day][p][cls]
                        if t == teacher:
                            print("  Period {}: {} in {}".format(p, sub, cls))
                            found = True
                if not found:
                    print("  Period {}: Free".format(p))
        print("-" * 50)
    


def validate_timetable(timetable):
    """
    Validate that the generated timetable meets all constraints.
    
    Args:
        timetable (dict): The generated timetable
        
    Returns:
        bool: True if timetable is valid, False otherwise
        str: Error message if timetable is invalid
    """
    # TODO: Implement validation logic
    # Check if all classes have their required number of periods for each subject
    # Check if teachers are not double-booked
    # Check if teachers are only teaching subjects they can teach

    teacher_schedule = {}
    class_counter = {}
    for day in days_of_week:
        teacher_schedule[day] = {}
        for p in range(1, periods_per_day + 1):
            teacher_schedule[day][p] = []
    for cls in classes:
        class_counter[cls] = {}
        for sub in class_subject_periods[cls]:
            class_counter[cls][sub] = 0

    for day in timetable:
        for p in timetable[day]:
            seen_teachers = []
            for cls in timetable[day][p]:
                sub, t = timetable[day][p][cls]
                if t in seen_teachers:
                    return False, "Teacher {} double-booked on {} period {}.".format(t, day, p)
                if sub not in teachers[t]:
                    return False, "Teacher {} is not qualified to teach {}.".format(t, sub)
                class_counter[cls][sub] += 1
                seen_teachers.append(t)

    for cls in class_subject_periods:
        for sub in class_subject_periods[cls]:
            if class_counter[cls][sub] != class_subject_periods[cls][sub]:
                return False, "{} has incorrect number of {} classes.".format(cls, sub)
            
    return True, "Timetable is valid."


def main():
    """
    Main function to generate and display the timetable.
    """
    print("Generating school timetable...")
    
    # Generate the timetable
    timetable = generate_timetable()
    
    # Validate the timetable
    is_valid, message = validate_timetable(timetable)
    
    if is_valid:
        # Display the timetable
        display_timetable(timetable)
    else:
        print(f"Failed to generate valid timetable: {message}")


if __name__ == "__main__":
    main()
