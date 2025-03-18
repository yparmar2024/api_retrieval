import requests
import time
from datetime import datetime
import pytz

apiUrl = "https://sit.instructure.com/api/v1/courses"
token = "1030~Ry8whx4cAYmNQPGWn7MMKmAR2YUGD2mRztHnCY2QRct8ayuAfnMu6PJWN6JhZ7aG"
excludeCourses = ["2024 Stevens Overview of Advising and Registration (SOAR)", 
                  "Advising CS", 
                  "Honor System Modules"]

def start():
    getAssignments()

def getAssignments():
    headers = {
        "Authorization": f"Bearer {token}"
    }

    coursesResponse = requests.get(apiUrl, headers=headers)
    if coursesResponse.status_code != 200:
        print("Error fetching courses.")
        return

    courses = coursesResponse.json()
    currentTimeUnix = int(time.time())

    for course in courses:
        courseId = course["id"]
        courseName = course["name"]

        if courseName in excludeCourses:
            continue

        assignmentsUrl = f"{apiUrl}/{courseId}/assignments"
        assignmentsResponse = requests.get(assignmentsUrl, headers=headers)

        if assignmentsResponse.status_code == 200:
            assignments = assignmentsResponse.json()
            assignmentsToShow = []
            for assignment in assignments:
                name = assignment.get("name")
                dueDateStr = assignment.get("due_at")

                if not dueDateStr:
                    continue

                dueDate = datetime.strptime(dueDateStr, "%Y-%m-%dT%H:%M:%SZ")
                localTz = pytz.timezone("America/New_York")
                dueDateLocal = dueDate.replace(tzinfo=pytz.utc).astimezone(localTz)
                dueDateUnix = int(dueDateLocal.timestamp())

                if dueDateUnix > currentTimeUnix:
                    month = dueDateLocal.strftime("%B")
                    day = dueDateLocal.day
                    year = dueDateLocal.year
                    hour = dueDateLocal.strftime("%I").lstrip("0")
                    minute = dueDateLocal.strftime("%M")
                    ampm = dueDateLocal.strftime("%p")

                    if 11 <= day <= 13:
                        ordinal = "th"
                    elif day % 10 == 1:
                        ordinal = "st"
                    elif day % 10 == 2:
                        ordinal = "nd"
                    elif day % 10 == 3:
                        ordinal = "rd"
                    else:
                        ordinal = "th"

                    dueDateFormatted = f"{month} {day}{ordinal}, {year} @ {hour}:{minute} {ampm}"
                    assignmentsToShow.append(f"- {name} (Due: {dueDateFormatted})")

            if assignmentsToShow:
                print(f"Course: {courseName}")
                for assignment in assignmentsToShow:
                    print(assignment)

                print()