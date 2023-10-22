import math
from urllib.parse import urlencode, urljoin

from db_models.db_models import Shop
from shop_be.conf.settings import settings
from shop_be.schemas.shop.shop import ShopPaginationRequest, PaginatedShops


def paginate_shops(
        data: list[Shop],
        total_count: int,
        query_params: ShopPaginationRequest,
) -> PaginatedShops:
    def make_url(page: int) -> str:
        query_params.page = page
        path = '/shops?' + urlencode(query_params.model_dump(exclude_none=True))
        return urljoin(str(settings.WEB_URL), path)

    total_pages = math.ceil(total_count / query_params.limit)
    return PaginatedShops(
        data=data,
        total=total_count,
        current_page=query_params.page,
        count=len(data),
        last_page=total_pages,
        firstItem=(query_params.page - 1) * query_params.limit,
        per_page=query_params.limit,
        first_page_url=make_url(1),
        last_page_url=make_url(total_pages),
        next_page_url=make_url(query_params.page + 1) if total_pages > query_params.page else None,
        prev_page_url=make_url(query_params.page - 1) if query_params.page > 1 else None,
    )
