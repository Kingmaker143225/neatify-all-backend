from pydantic import BaseModel
from typing import Any


class CustomerMainCategoryResponse(BaseModel):
    id: str
    name: str
    icon_url: str | None = None
    sort_order: int | None = None


class CustomerServiceResponse(BaseModel):
    id: str
    slug: str | None = None
    title: str
    service_type: str | None = None
    main_category_id: str | None = None

    category_order: int | None = None
    duration: str | None = None
    price: str | None = None

    image: str | None = None
    gallery_images: list[str] | None = None
    image2: Any | None = None

    description: str | None = None

    sort_order: int | None = None

    original_price: str | None = None
    discount_percent: float | None = None
    discount_label: str | None = None

    tax_percent: float | None = None

    work_includes: str | None = None
    work_not_included: str | None = None

    category_icon_url: str | None = None

    how_it_works: Any | None = None


class CustomerAddOnResponse(BaseModel):
    id: str
    title: str
    duration: int | None = None
    price: str | None = None

    image: str | None = None
    service_type: str | None = None
    description: str | None = None

    sort_order: int | None = None

    original_price: str | None = None
    discount_percent: float | None = None
    discount_label: str | None = None

    work_includes: str | None = None
    work_not_included: str | None = None

    tax_percent: float | None = None
    max_quantity: int | None = None

    is_active: bool | None = None