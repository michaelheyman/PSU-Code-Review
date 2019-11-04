import html


days_mapping = {
    "monday": "M",
    "tuesday": "T",
    "wednesday": "W",
    "thursday": "R",
    "friday": "F",
    "saturday": "S",
    "sunday": "SU",
}


def get_courses(subjects_json):
    """Gets courses from the subjects JSON response.

    :param subjects_json: Dictionary with subject JSON response
    :returns:             List of courses.
    """
    courses = []
    for discipline in subjects_json:
        for course in discipline:
            courses.append(get_course_data(course))
    return courses


def get_course_data(course):
    """Gets the course data by parsing it from the course record.

    :param record: Dictionary containing the course record.
    :returns:      Simpler dictionary with pruned attributes.
    """
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
    """Gets and formats the time found in the course record.

    :param record: Dictionary containing the course record.
    :returns:      The formatted time in the format 'HH:MM - HH:MM'
    """
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
    """Gets the days encoding of the days found in the course record.

    :param record: Dictionary containing the course record.
    :returns:      Encoded day character (M-T-W-R-F-S-SU)
    """
    try:
        meeting_time = record["meetingsFaculty"][0]["meetingTime"]
    except (KeyError, IndexError):
        return None

    days = ""
    for day in days_mapping.keys():
        if meeting_time[day]:
            days += days_mapping[day]

    return days


def get_term_description(record):
    """Gets the term description from a course record.

    Removes the "Quarter" suffix from a term description, turning
    "Fall 2019 Quarter" into "Fall 2019".

    :param record: Dictionary containing the term description value.
    :returns:      Trimmed term name.
    """
    term = record["termDesc"]

    return " ".join(term.split(" ")[0:2])


def get_instructor(rec):
    """Gets instructor from a course record.

    :param record: Dictionary containing the course record.
    :returns:      TBD if instructor doesn't exist.
                   None if instructor has invalid format.
                   Instructor first name and last name if it exists.
    """
    try:
        instructor_name = rec["faculty"][0]["displayName"]
    except (KeyError, IndexError):
        return "TBD"

    instructor_name = instructor_name.split(", ", maxsplit=1)
    if len(instructor_name) < 1:
        return None

    return f"{instructor_name[1]} {instructor_name[0]}"
