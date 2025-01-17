from datetime import datetime
from typing import Tuple

from sqlalchemy import String, DateTime, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, composite

from tradeengine.dto import Asset, OrderTypes, QuantityOrder
from tradeengine.dto.position import PositionAdditionMixin


# objects for SQL Alchemy
class OrderBookBase(DeclarativeBase):

    def __repr__(self):
        params = ', '.join(f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith("_"))
        return f'{self.__class__.__name__}({params})'


class OrderBook(OrderBookBase):
    __tablename__ = 'orderbook'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    strategy_id: Mapped[str] = mapped_column(index=True)
    order_type: Mapped[OrderTypes] = mapped_column(Enum(OrderTypes, length=50), index=True)
    asset: Mapped[Asset] = composite(mapped_column(String(255), index=True))
    limit:  Mapped[float] = mapped_column(nullable=True)
    stop_limit: Mapped[float] = mapped_column(nullable=True)
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    valid_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=True)
    qty: Mapped[float] = mapped_column(nullable=True)

    def to_history(self, order: QuantityOrder = None, execute_time: datetime = None, execute_price: float = None, status: int = None):
        return OrderBookHistory(
            strategy_id=self.strategy_id,
            order_type=self.order_type,
            asset=self.asset,
            limit=self.limit,
            stop_limit=self.stop_limit,
            valid_from=self.valid_from,
            valid_until=self.valid_until,
            size=self.qty,
            qty=None if order is None else order.size,
            status=status if status is not None else 0 if order is None else 1,
            execute_price=execute_price,
            execute_time=execute_time,
            execute_value=None if order is None else (execute_price * order.size),
        )


class OrderBookHistory(OrderBookBase):
    __tablename__ = 'orderbook_history'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    strategy_id: Mapped[str] = mapped_column(index=True)
    order_type: Mapped[OrderTypes] = mapped_column(Enum(OrderTypes, length=50), index=True)
    asset: Mapped[Asset] = composite(mapped_column(String(255), index=True))
    limit: Mapped[float] = mapped_column(nullable=True)
    stop_limit: Mapped[float] = mapped_column(nullable=True)
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    valid_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=True)
    size: Mapped[float] = mapped_column(nullable=True)
    qty: Mapped[float] = mapped_column(nullable=True)
    status: Mapped[int] = mapped_column()
    execute_price: Mapped[float] = mapped_column(nullable=True)
    execute_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=True)
    execute_value: Mapped[float] = mapped_column(nullable=True)

    def to_dict(self):
        return dict(
            id=self.id,
            strategy_id=self.strategy_id,
            order_type=self.order_type,
            asset=str(self.asset),
            limit=self.limit,
            stop_limit=self.stop_limit,
            valid_from=self.valid_from,
            valid_until=self.valid_until,
            size=self.size,
            qty=self.qty,
            status=self.status,
            execute_price=self.execute_price,
            execute_time=self.execute_time,
            execute_value=self.execute_value,
        )

    def __str__(self):
        return str(self.to_dict())

class PortfolioBase(DeclarativeBase):

    def __repr__(self):
        params = ', '.join(f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith("_"))
        return f'{self.__class__.__name__}({params})'




class PortfolioPosition(PortfolioBase, PositionAdditionMixin):
    __tablename__ = 'portfolio_position'
    strategy_id: Mapped[str] = mapped_column(primary_key=True)
    asset: Mapped[Asset] = composite(mapped_column(String(255), primary_key=True))
    time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    quantity: Mapped[float] = mapped_column()
    cost_basis: Mapped[float] = mapped_column()
    value: Mapped[float] = mapped_column()

    def __add__(self, other: Tuple[float, float]):
        new_qty, new_cost_basis, new_value, new_pnl = self.add_quantity_and_price(other)
        self.quantity = new_qty
        self.cost_basis = new_cost_basis
        self.value = new_value
        return self

    def __sub__(self, other: Tuple[float, float]):
        return self + (-other[0], other[1])


class PortfolioHistory(PortfolioBase):
    __tablename__ = 'portfolio_history'
    strategy_id: Mapped[str] = mapped_column(primary_key=True)
    asset: Mapped[Asset] = composite(mapped_column(String(255), primary_key=True))
    time: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    quantity: Mapped[float] = mapped_column()
    cost_basis: Mapped[float] = mapped_column()
    value: Mapped[float] = mapped_column()

    def to_dict(self):
        return dict(
            strategy_id=self.strategy_id,
            asset=str(self.asset),
            time=self.time,
            quantity=self.quantity,
            cost_basis=self.cost_basis,
            value=self.value,
        )
