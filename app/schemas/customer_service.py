from typing import Any

from pydantic import BaseModel, field_validator


# =========================================================
# MAIN CATEGORY RESPONSE
# =========================================================

class CustomerMainCategoryResponse(BaseModel):
    id: str
    name: str
    icon_url: str | None = None
    sort_order: int | None = None


# =========================================================
# SERVICE RESPONSE
# =========================================================

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

    # Supabase may return:
    # 0
    # 0.0
    # 4
    # 4.0
    # "4"
    # "4.0"
    # ""
    # None
    tax_percent: float | None = None

    work_includes: str | None = None
    work_not_included: str | None = None

    category_icon_url: str | None = None

    how_it_works: Any | None = None

    @field_validator("tax_percent", mode="before")
    @classmethod
    def parse_tax_percent(cls, value):
        # Empty/null value from Supabase
        if value is None or value == "":
            return None

        # Already a number
        if isinstance(value, (int, float)):
            return float(value)

        # String number such as "4" or "4.0"
        if isinstance(value, str):
            value = value.strip()

            if value == "":
                return None

            try:
                return float(value)
            except ValueError:
                return None

        # Anything unexpected
        return None


# =========================================================
# ADD-ON RESPONSE
# =========================================================

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

    # Same handling as services
    tax_percent: float | None = None

    max_quantity: int | None = None

    is_active: bool | None = None

    @field_validator("tax_percent", mode="before")
    @classmethod
    def parse_tax_percent(cls, value):
        # Empty/null value from Supabase
        if value is None or value == "":
            return None

        # Already a number
        if isinstance(value, (int, float)):
            return float(value)

        # String number such as "4" or "4.0"
        if isinstance(value, str):
            value = value.strip()

            if value == "":
                return None

            try:
                return float(value)
            except ValueError:
                return None

        # Anything unexpected
        return None