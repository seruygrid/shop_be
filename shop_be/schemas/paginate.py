from pydantic import BaseModel, AnyHttpUrl


class Paginate(BaseModel):
    data: list
    total: int
    current_page: int
    count: int
    last_page: int
    firstItem: int
    lastItem: int
    per_page: int
    first_page_url: AnyHttpUrl
    last_page_url: AnyHttpUrl
    next_page_url: AnyHttpUrl | None
    prev_page_url: AnyHttpUrl | None
