from src.model.conexao_banco import Base
from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped


class Viagens(Base):

    __table_name__ = 'Viagens'

    route_id: Mapped[str] = mapped_column(
        String
    )

    service_id: Mapped[str] = mapped_column(
        String
    )

    trip_id: Mapped[str] = mapped_column(
        String
    )

    trip_headsing: Mapped[str] = mapped_column(
        String
    )

    direction_id: Mapped[int] = mapped_column(
        Integer
    )

    shape_id: Mapped[int] = mapped_column(
        Integer
    )

    def __repr__(self):
        return (
            f'Viagens['
            f'route_id={self.route_id},'
            f'service_id={self.service_id},'
            f'trip_id={self.trip_id},'
            f'trip_headsing={self.trip_headsing},'
            f'direction_id={self.direction_id},'
            f'shape_id={self.shape_id}]'

        )
