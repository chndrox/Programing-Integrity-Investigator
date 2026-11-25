"""
Sample data initialization for demonstration mode.
Creates realistic test data with:
- Students and instructors
- Assignments
- Submissions with actual Python code
- Commit history
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import engine, SessionLocal, Base
from app.models import (
    User, Student, Assignment, Submission, CommitHistory
)
from app.api.auth import hash_password
import random


# Sample Python submissions (varying similarity levels)
SAMPLE_CODE_SUBMISSION_1 = '''
def fibonacci(n):
    """Calculate fibonacci number at position n."""
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b


def prime_check(num):
    """Check if a number is prime."""
    if num < 2:
        return False
    
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    
    return True


if __name__ == "__main__":
    print("Fib(10):", fibonacci(10))
    print("Is 17 prime?", prime_check(17))
'''

SAMPLE_CODE_SUBMISSION_2 = '''
def fib(n):
    """Calculate the nth fibonacci number."""
    if n < 2:
        return n
    
    x, y = 0, 1
    for step in range(2, n + 1):
        x, y = y, x + y
    
    return y


def is_prime(num):
    """Test if number is prime."""
    if num < 2:
        return False
    
    for divisor in range(2, int(num ** 0.5) + 1):
        if num % divisor == 0:
            return False
    
    return True


if __name__ == "__main__":
    print("Fib(10):", fib(10))
    print("Is 17 prime?", is_prime(17))
'''

# Different student code (less similar)
SAMPLE_CODE_SUBMISSION_3 = '''
def merge_sort(arr):
    """Merge sort implementation."""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)


def merge(left, right):
    """Merge two sorted arrays."""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result
'''

SAMPLE_CODE_SUBMISSION_4 = '''
def bubble_sort(items):
    """Sort items using bubble sort algorithm."""
    n = len(items)
    
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
                swapped = True
        
        if not swapped:
            break
    
    return items
'''


def initialize_sample_data(db: Session):
    """Initialize sample data for demonstration."""
    
    # Clear existing data
    db.query(CommitHistory).delete()
    db.query(Submission).delete()
    db.query(Assignment).delete()
    db.query(Student).delete()
    db.query(User).delete()
    db.commit()
    
    # Create instructor
    instructor = User(
        username="instructor1",
        email="instructor@university.edu",
        full_name="Dr. Sarah Johnson",
        hashed_password=hash_password("password123"),
        role="instructor"
    )
    db.add(instructor)
    db.commit()
    
    # Create students
    students_data = [
        ("STU001", "Alice Smith", "alice@university.edu", "Computer Science"),
        ("STU002", "Bob Johnson", "bob@university.edu", "Computer Science"),
        ("STU003", "Charlie Davis", "charlie@university.edu", "Computer Science"),
        ("STU004", "Diana Wilson", "diana@university.edu", "Computer Science"),
    ]
    
    students = []
    for student_id, name, email, dept in students_data:
        student = Student(
            student_id=student_id,
            name=name,
            email=email,
            department=dept
        )
        db.add(student)
        students.append(student)
    
    db.commit()
    
    # Create assignment
    assignment = Assignment(
        name="Assignment 1: Algorithms",
        description="Implement basic algorithms: Fibonacci, Prime Check, Sorting",
        due_date=datetime.now() + timedelta(days=7)
    )
    db.add(assignment)
    db.commit()
    
    # Create submissions
    submissions_data = [
        (students[0].id, SAMPLE_CODE_SUBMISSION_1, "fibonacci_prime.py", "STU001"),
        (students[1].id, SAMPLE_CODE_SUBMISSION_2, "solution.py", "STU002"),
        (students[2].id, SAMPLE_CODE_SUBMISSION_3, "sorting.py", "STU003"),
        (students[3].id, SAMPLE_CODE_SUBMISSION_4, "bubble_sort.py", "STU004"),
    ]
    
    submissions = []
    for student_id, code, filename, student_code in submissions_data:
        submission = Submission(
            student_id=student_id,
            assignment_id=assignment.id,
            file_name=filename,
            file_path=f"/uploads/{filename}",
            source_code=code,
            language="python",
            git_repo_url=None
        )
        db.add(submission)
        submissions.append(submission)
    
    db.commit()
    
    # Create commit history for first two submissions (similar code)
    base_time = datetime.now() - timedelta(days=5)
    
    # Commits for submission 1 (Alice)
    commits_1 = [
        ("abc1234", "alice@university.edu", "Initial project setup", base_time, 15, 0),
        ("abc1235", "alice@university.edu", "Implement fibonacci function", base_time + timedelta(hours=2), 25, 2),
        ("abc1236", "alice@university.edu", "Add prime checking function", base_time + timedelta(hours=4), 20, 1),
        ("abc1237", "alice@university.edu", "Add main block and test", base_time + timedelta(hours=6), 10, 0),
    ]
    
    for hash, author, message, timestamp, adds, dels in commits_1:
        commit = CommitHistory(
            submission_id=submissions[0].id,
            commit_hash=hash,
            author=author,
            message=message,
            timestamp=timestamp,
            additions=adds,
            deletions=dels
        )
        db.add(commit)
    
    # Commits for submission 2 (Bob - similar code)
    commits_2 = [
        ("def2345", "bob@university.edu", "Project start", base_time + timedelta(hours=1), 15, 0),
        ("def2346", "bob@university.edu", "Add fib function", base_time + timedelta(hours=3), 25, 2),
        ("def2347", "bob@university.edu", "Prime number checker", base_time + timedelta(hours=5), 20, 1),
        ("def2348", "bob@university.edu", "Testing and cleanup", base_time + timedelta(hours=7), 10, 0),
    ]
    
    for hash, author, message, timestamp, adds, dels in commits_2:
        commit = CommitHistory(
            submission_id=submissions[1].id,
            commit_hash=hash,
            author=author,
            message=message,
            timestamp=timestamp,
            additions=adds,
            deletions=dels
        )
        db.add(commit)
    
    # Commits for submission 3 (Charlie - merge sort)
    commits_3 = [
        ("ghi3456", "charlie@university.edu", "Start merge sort implementation", base_time + timedelta(hours=1), 10, 0),
        ("ghi3457", "charlie@university.edu", "Implement merge sort algorithm", base_time + timedelta(hours=3), 40, 5),
        ("ghi3458", "charlie@university.edu", "Add merge helper function", base_time + timedelta(hours=5), 20, 2),
        ("ghi3459", "charlie@university.edu", "Testing and documentation", base_time + timedelta(hours=7), 15, 0),
    ]
    
    for hash, author, message, timestamp, adds, dels in commits_3:
        commit = CommitHistory(
            submission_id=submissions[2].id,
            commit_hash=hash,
            author=author,
            message=message,
            timestamp=timestamp,
            additions=adds,
            deletions=dels
        )
        db.add(commit)
    
    # Commits for submission 4 (Diana - single day bulk commit)
    commits_4 = [
        ("jkl4567", "diana@university.edu", "Complete bubble sort implementation", base_time + timedelta(hours=1), 100, 0),
    ]
    
    for hash, author, message, timestamp, adds, dels in commits_4:
        commit = CommitHistory(
            submission_id=submissions[3].id,
            commit_hash=hash,
            author=author,
            message=message,
            timestamp=timestamp,
            additions=adds,
            deletions=dels
        )
        db.add(commit)
    
    db.commit()
    
    print("Sample data initialized successfully!")
    print(f"Created: 1 instructor, 4 students, 1 assignment, 4 submissions with commit history")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    initialize_sample_data(db)
    db.close()
