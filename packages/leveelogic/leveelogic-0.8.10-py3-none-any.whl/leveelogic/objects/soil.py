from ..models.datamodel import DataModel


class Soil(DataModel):
    code: str
    yd: float
    ys: float
    c: float
    phi: float
    color: str
