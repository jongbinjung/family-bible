"""Shared paths"""

GCS_BUCKET = "family-bible"

"""Member data with columns

- name: str
- email: str
- lang: str
- role: str
- group: str

"""
MEMBERS_GCS_PATH = f"{GCS_BUCKET}/base/members.parquet"

"""Plan data with columns

- id: int
- date_us: date
- date_kr: date
- plan_en: str
- plan_ko: str

"""
PLAN_GCS_PATH = f"{GCS_BUCKET}/base/plan.parquet"

"""Progress data, one for each user, with columns

- plan_id: int; FK to plan
- completed: bool

"""
PROGRESS_GCS_PATTERN = f"{GCS_BUCKET}/progress/{{}}.parquet"

"""Viewables data indicating what groups each user can view, with columns

- name: str
- group: str; one of the Group enum values

"""
VIEWABLES_GCS_PATH = f"{GCS_BUCKET}/base/viewables.parquet"
