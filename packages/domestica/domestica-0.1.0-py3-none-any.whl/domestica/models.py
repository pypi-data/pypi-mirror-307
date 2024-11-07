from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Quality(Enum):
    """Video quality"""

    P2160 = "2160"
    P1080 = "1080"
    P720 = "720"
    P540 = "540"
    P360 = "360"
    P224 = "224"


class Video(BaseModel):
    """video model"""

    id: Optional[str] = None
    title: str
    m3u8_url: Optional[str]


class Media(BaseModel):
    """media model"""

    name: str
    url: str


class Section(BaseModel):
    """section model"""

    id: Optional[str] = None
    title: str
    videos: list[Video]
    assets: list[Media] = []


class CourseInfo(BaseModel):
    """course info model"""

    product_id: int
    product_name: str
    teacher_name: str
    category_id: int
    category_name: str
    course_level: str
    course_number_of_lessons: int
    course_total_duration_sec: int
    total_units: int
    subtitles_language: list[str]
    audio_language: list[str]
    original_language: str

    @property
    def slug(self) -> str:
        product_name = self.product_name.strip().lower().replace(" ", "-")
        return f"{self.product_id}-{product_name}"

    @property
    def url(self) -> str:
        return f"https://www.domestika.org/courses/{self.slug}/course"


class Course(BaseModel):
    """course model"""

    id: str
    title: str
    url: str
    sections: list[Section]
    assets: list[Media] = []
    info: Optional[CourseInfo] = None
