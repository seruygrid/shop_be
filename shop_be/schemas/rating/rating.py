from pydantic import BaseModel


class RatingCount(BaseModel):
    rating: int
    total: int
    positive_feedbacks_count: int
    negative_feedbacks_count: int
    my_feedback: str | None = None
    abusive_reports_count: int

    class Config:
        from_attributes = True
