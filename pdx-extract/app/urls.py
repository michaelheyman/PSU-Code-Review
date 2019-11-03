from urllib.parse import urljoin

BASE_URL = "https://app.banner.pdx.edu/StudentRegistrationSsb/ssb/"
INIT_URL = urljoin(BASE_URL, "term/termSelection?mode=search")
CLASS_URL = urljoin(BASE_URL, "classSearch/classSearch")
TERMS_URL = urljoin(BASE_URL, "classSearch/getTerms")
SEARCH_URL = urljoin(BASE_URL, "term/search?mode=search")
SCHEDULE_URL = urljoin(BASE_URL, "searchResults/searchResults")
SUBJECTS_URL = urljoin(BASE_URL, "classSearch/get_subject")
