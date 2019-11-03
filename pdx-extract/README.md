# pdx-extract

[pdx-extract](https://github.com/michaelheyman/pdx-extract/) is part of the
[pdx-schedule](https://github.com/michaelheyman/pdx-schedule/) project.

Runs a Cloud Function that scrapes the schedule information from Portland State.
It then stores the JSON representation of the schedule into a Cloud Storage bucket.

## Setup

### Create Virtual Environment

```bash
pyenv virtualenv 3.7.3 pdx-extract-3.7.3
pyenv activate pdx-extract-3.7.3
```

### Install Requirements

```bash
pip -r install requirements.txt
```

### Install Git Hooks

See [.pre-commit-config.yaml](.pre-commit-config.yaml) for information on which hooks are configured.

```bash
pre-commit install
```

```bash
pre-commit install -t pre-push
```

## Running

Run the application by executing

```bash
python -m app
```

## Testing

Ensure that the necessary testing packages are installed:

```bash
pip install pytest pytest-cov pytest-asyncio asynctest
```

Run `pytest` with verbose output:

```bash
pytest -vv
```

Run `pytest` with coverage:

```bash
pytest --cov=app tests/
```

```bash
pytest --cov-report html --cov=app tests/
```


## Deploying Cloud Function

Run the following command from the root of the project to deploy the Cloud Function

```bash
gcloud functions deploy extract --timeout=540 --memory=1024MB --runtime python37 --trigger-http --region us-central1
```

There is the potential to reduce the memory requirements of the Function.

## JSON Fields

The PSU API returns JSON payloads with the following format:

```json
{
    "data": [
        {
            "term": "201904",
            "termDesc": "Fall 2019 Quarter",
            "courseReferenceNumber": "10883",
            "courseNumber": "161",
            "subject": "CS",
            "subjectDescription": "Computer Science",
            "courseTitle": "INTRO PROGRAM &amp; PROB SOLVING",
            "creditHours": 4,
            "faculty": [
                {
                    "displayName": "Ely, David D"
                }
            ],
            "meetingsFaculty": [
                {
                    "meetingTime": {
                        "beginTime": "1000",
                        "endTime": "1150",
                        "monday": true,
                        "tuesday": false,
                        "wednesday": false,
                    },
                }
            ],
        }
    ],
}
```

The goal is to transform them into this:

```json
[
    {
        "number": "CS 161",
        "name": "INTRO PROGRAM &amp; PROB SOLVING",
        "crn": "10883",
        "discipline": "Computer Science",
        "days": "M",
        "credits": 4,
        "time": "10:00 - 11:50",
        "instructor": "David Ely",
        "term_description": "Fall 2019",
        "term_date": "201904",
    }
]
```
