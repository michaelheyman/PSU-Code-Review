from app import sanitize
from tests import data


def test_get_courses():
    subjects_json = data.subjects_json
    courses = sanitize.get_courses(subjects_json)

    assert len(courses) == 2
    assert courses[0]["number"] == "CS 161"
    assert courses[1]["number"] == "CS 457"
    assert courses[0]["instructor"] == "David D Ely"
    assert courses[1]["instructor"] == "Mark P Jones"


def test_get_course_data_returns_sanitized_data():
    # TODO: separate this into smaller tests
    sanitized_course = sanitize.get_course_data(data.original_course)

    assert sanitized_course["number"] == "CS 161"
    assert sanitized_course["name"] == "INTRO PROGRAM & PROB SOLVING"
    assert sanitized_course["crn"] == 10883
    assert sanitized_course["discipline"] == "Computer Science"
    assert sanitized_course["days"] == "TR"
    assert sanitized_course["credits"] == 4
    assert sanitized_course["time"] == "10:00 - 11:50"
    assert sanitized_course["instructor"] == "David D Ely"
    assert sanitized_course["term_description"] == "Fall 2019"
    assert sanitized_course["term_date"] == 201904


def test_get_time_returns_time():
    content = {
        "meetingsFaculty": [{"meetingTime": {"beginTime": "1000", "endTime": "1150"}}]
    }

    time = sanitize.get_time(content)

    assert time == "10:00 - 11:50"


def test_get_time_returns_none_when_missing_meeting_faculty():
    content = {}

    time = sanitize.get_time(content)

    assert time is None


def test_get_time_returns_none_when_missing_meeting_info():
    content = {"meetingsFaculty": []}

    time = sanitize.get_time(content)

    assert time is None


def test_get_time_returns_none_when_missing_meetings_faculty():
    content = {"meetingsFaculty": [{}]}

    time = sanitize.get_time(content)

    assert time is None


def test_get_time_returns_none_when_missing_begin_time():
    content = {"meetingsFaculty": [{"meetingTime": {"endTime": "1150"}}]}

    time = sanitize.get_time(content)

    assert time is None


def test_get_time_returns_none_when_missing_end_time():
    content = {"meetingsFaculty": [{"meetingTime": {"beginTime": "1000"}}]}

    time = sanitize.get_time(content)

    assert time is None


def test_get_time_returns_none_begin_time_is_none():
    content = {
        "meetingsFaculty": [{"meetingTime": {"beginTime": None, "endTime": "1150"}}]
    }

    time = sanitize.get_time(content)

    assert time is None


def test_get_time_returns_none_end_time_is_none():
    content = {
        "meetingsFaculty": [{"meetingTime": {"beginTime": "1000", "endTime": None}}]
    }

    time = sanitize.get_time(content)

    assert time is None


def test_get_time_returns_formatted_time():
    content = {
        "meetingsFaculty": [{"meetingTime": {"beginTime": "1000", "endTime": "1150"}}]
    }

    time = sanitize.get_time(content)

    assert time == "10:00 - 11:50"


def test_get_days_returns_none_when_missing_meeting_faculty():
    content = {}

    days = sanitize.get_days(content)

    assert days is None


def test_get_days_returns_none_when_missing_meeting_info():
    content = {"meetingsFaculty": []}

    days = sanitize.get_days(content)

    assert days is None


def test_get_days_returns_none_when_missing_meetings_faculty():
    content = {"meetingsFaculty": [{}]}

    days = sanitize.get_days(content)

    assert days is None


def test_get_days_returns_string_when_all_days_true():
    content = {
        "meetingsFaculty": [
            {
                "meetingTime": {
                    "friday": True,
                    "monday": True,
                    "saturday": True,
                    "sunday": True,
                    "thursday": True,
                    "tuesday": True,
                    "wednesday": True,
                }
            }
        ]
    }

    days = sanitize.get_days(content)

    assert days == "MTWRFSSU"


def test_get_days_returns_empty_string_when_all_days_false():
    content = {
        "meetingsFaculty": [
            {
                "meetingTime": {
                    "friday": False,
                    "monday": False,
                    "saturday": False,
                    "sunday": False,
                    "thursday": False,
                    "tuesday": False,
                    "wednesday": False,
                }
            }
        ]
    }

    days = sanitize.get_days(content)

    assert days == ""


def test_get_term_description_returns_term_description():
    content = {"termDesc": "Fall 2019 Quarter"}

    term_description = sanitize.get_term_description(content)

    assert term_description == "Fall 2019"


def test_get_instructor_returns_instructor_first_last():
    content = {"faculty": [{"displayName": "Ely, David D"}]}

    term_description = sanitize.get_instructor(content)

    assert term_description == "David D Ely"


def test_get_instructor_returns_tbd_when_empty_faculty():
    content = {"faculty": []}

    term_description = sanitize.get_instructor(content)

    assert term_description == "TBD"


def test_get_instructor_returns_tbd_when_missing_faculty():
    content = {"faculty": [{}]}

    term_description = sanitize.get_instructor(content)

    assert term_description == "TBD"
