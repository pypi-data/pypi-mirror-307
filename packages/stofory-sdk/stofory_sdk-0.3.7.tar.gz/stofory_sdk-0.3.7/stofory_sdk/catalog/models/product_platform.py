from __future__ import annotations

from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import BIGINT, BOOLEAN
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .decorator.jsonb_dict import JSONBDict

if TYPE_CHECKING:
    from .product import Product
    from .platform import Platform

    from .product_platform_pricing import ProductPlatformPricing
    from .product_platform_bonus import ProductPlatformBonus
    from .product_platform_category import ProductPlatformCategory
    from .product_platform_description import ProductPlatformDescription
    from .product_platform_name import ProductPlatformName
    from .product_platform_discount import ProductPlatformDiscount
    from .product_platform_guarantee import ProductPlatformGuarantee

    from .product_platform_parameter import ProductPlatformParameter
    from .product_platform_image import ProductPlatformImage
    from .product_platform_video import ProductPlatformVideo

    from .product_platform_sync_task import ProductPlatformSyncTask
    from .product_platform_versioning import ProductPlatformVersioning
    from .product_platform_external_connection import ProductPlatformExternalConnection


class ProductPlatform(BigIntAuditBase):
    __table_args__ = (
        Index("idx_product_platform_product_id", "product_id"),
        Index("idx_product_platform_platform_id", "platform_id"),
        UniqueConstraint("product_id", "platform_id", name="uq_product_platform_product_id_platform_id"),
    )

    product_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    platform_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("platform.id", ondelete="CASCADE"), nullable=False)
    version: Mapped[int] = mapped_column(BIGINT, default=1)
    is_enabled: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    custom_fields: Mapped[dict] = mapped_column(JSONBDict, default={})

    product: Mapped[Product] = relationship(
        back_populates="product_platforms",
        foreign_keys="ProductPlatform.product_id",
        innerjoin=True,
        uselist=False,
        lazy="noload",   # select/noload?
    )

    platform: Mapped[Platform] = relationship(
        back_populates="product_platforms",
        foreign_keys="ProductPlatform.platform_id",
        innerjoin=True,
        uselist=False,
        lazy="noload",
    )

    names: Mapped[list[ProductPlatformName]] = relationship(
        back_populates="product_platform",
        lazy="noload",
        uselist=True,
        passive_deletes=True,
        cascade="all, delete-orphan",
        order_by="asc(ProductPlatformName.id)"
    )

    descriptions: Mapped[list[ProductPlatformDescription]] = relationship(
        back_populates="product_platform",
        lazy="noload",
        uselist=True,
        passive_deletes=True,
        cascade="all, delete-orphan",
        order_by="asc(ProductPlatformDescription.id)"
    )

    categories: Mapped[list[ProductPlatformCategory]] = relationship(
        back_populates="product_platform",
        lazy="noload",
        uselist=True,
        passive_deletes=True,
        cascade="all, delete-orphan",
        order_by="asc(ProductPlatformCategory.id)"
    )

    parameters: Mapped[list[ProductPlatformParameter]] = relationship(
        back_populates="product_platform",
        lazy="noload",
        uselist=True,
        passive_deletes=True,
        cascade="all, delete-orphan",
        order_by="asc(ProductPlatformParameter.id)"
    )

    images: Mapped[list[ProductPlatformImage]] = relationship(
        back_populates="product_platform",
        lazy="noload",
        uselist=True,
        passive_deletes=True,
        cascade="all, delete-orphan",
        order_by="asc(ProductPlatformImage.id)"
    )

    videos: Mapped[list[ProductPlatformVideo]] = relationship(
        back_populates="product_platform",
        lazy="noload",
        uselist=True,
        passive_deletes=True,
        cascade="all, delete-orphan",
        order_by="asc(ProductPlatformVideo.id)"
    )

    price: Mapped[ProductPlatformPricing] = relationship(
        back_populates="product_platform",
        lazy="noload",
        uselist=False,
        passive_deletes=True,
        cascade="all, delete-orphan"
    )

    bonus: Mapped[ProductPlatformBonus] = relationship(
        back_populates="product_platform",
        lazy="noload",
        uselist=False,
        passive_deletes=True,
        cascade="all, delete-orphan"
    )

    discount: Mapped[ProductPlatformDiscount] = relationship(
        back_populates="product_platform",
        lazy="noload",
        uselist=False,
        passive_deletes=True,
        cascade="all, delete-orphan"
    )

    guarantee: Mapped[ProductPlatformGuarantee] = relationship(
        back_populates="product_platform",
        lazy="noload",
        uselist=False,
        passive_deletes=True,
        cascade="all, delete-orphan"
    )

    sync_tasks: Mapped[list[ProductPlatformSyncTask]] = relationship(
        back_populates="product_platform",
        lazy="noload",
        uselist=True,
        passive_deletes=True,
        cascade="all, delete-orphan",
        order_by="asc(ProductPlatformSyncTask.id)"
    )

    versions: Mapped[ProductPlatformVersioning] = relationship(
        back_populates="product_platform",
        lazy="noload",
        uselist=False,
        passive_deletes=True,
        cascade="all, delete-orphan",
    )

    external_connections: Mapped[ProductPlatformExternalConnection] = relationship(
        back_populates="product_platform",
        lazy="noload",
        uselist=False,
        passive_deletes=True,
        cascade="all, delete-orphan",
    )
