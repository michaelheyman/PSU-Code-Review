import html


def get_courses(subjects_json):
    courses = []
    for discipline in subjects_json:
        for course in discipline:
            courses.append(get_course_data(course))
    return courses


def get_course_data(course):
    course_data = dict()

    course_data["number"] = f"{course['subject']} {course['courseNumber']}"
    course_data["name"] = html.unescape(course["courseTitle"])
    course_data["crn"] = int(course["courseReferenceNumber"])
    course_data["discipline"] = html.unescape(course["subjectDescription"])
    course_data["days"] = get_days(course)
    course_data["credits"] = int(course["creditHours"]) if course["creditHours"] else 0
    course_data["time"] = get_time(course)
    course_data["instructor"] = get_instructor(course)
    course_data["term_description"] = get_term_description(course)
    course_data["term_date"] = int(course["term"])

    return course_data


def get_time(record):
    try:
        meeting_time = record["meetingsFaculty"][0]["meetingTime"]
        begin_time = meeting_time["beginTime"]
        end_time = meeting_time["endTime"]
    except (KeyError, IndexError):
        return None

    if None in (begin_time, end_time):
        return None

    begin_time = begin_time[0:2] + ":" + begin_time[2:]
    end_time = end_time[0:2] + ":" + end_time[2:]
    return f"{begin_time} - {end_time}"


def get_days(record):
    try:
        meeting_time = record["meetingsFaculty"][0]["meetingTime"]
    except (KeyError, IndexError):
        return None

    days = ""

    if meeting_time["monday"]:
        days += "M"
    if meeting_time["tuesday"]:
        days += "T"
    if meeting_time["wednesday"]:
        days += "W"
    if meeting_time["thursday"]:
        days += "R"
    if meeting_time["friday"]:
        days += "F"
    if meeting_time["saturday"]:
        days += "S"
    if meeting_time["sunday"]:
        days += "SU"

    return days


def get_term_description(record):
    term = record["termDesc"]

    return " ".join(term.split(" ")[0:2])


def get_instructor(rec):
    # TODO: consider returning None instead of "TBD"
    try:
        instructor_name = rec["faculty"][0]["displayName"]
    except (KeyError, IndexError):
        return "TBD"

    instructor_name = instructor_name.split(", ", maxsplit=1)
    if len(instructor_name) > 1:
        return f"{instructor_name[1]} {instructor_name[0]}"
    else:
        # TODO: add a test for this scenario. why is this returning an 'Instructor: ' prefix?
        return f"Instructor: {instructor_name}"
