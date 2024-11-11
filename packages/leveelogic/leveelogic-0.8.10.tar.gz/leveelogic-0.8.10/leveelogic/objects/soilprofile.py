from typing import List

from ..models.datamodel import DataModel
from .soillayer import SoilLayer
from .soilpolygon import SoilPolygon
from .crosssection import Crosssection


class SoilProfile(DataModel):
    soillayers: List[SoilLayer] = []

    @property
    def top(self):
        return self.soillayers[0].top

    @property
    def bottom(self):
        return self.soillayers[-1].bottom

    def merge(self):
        """Merge the soillayers if two or more consecutive soillayers are of the same type"""
        result = []
        for i in range(len(self.soillayers)):
            if i == 0:
                result.append(self.soillayers[i])
            else:
                if self.soillayers[i].soilcode == result[-1].soilcode:
                    result[-1].bottom = self.soillayers[i].bottom
                else:
                    result.append(self.soillayers[i])
        self.soillayers = result

    def to_soilpolygons(self, left: float, right: float) -> List[SoilPolygon]:
        result = []
        for layer in self.soillayers:
            result.append(
                SoilPolygon(
                    points=[
                        (left, layer.top),
                        (right, layer.top),
                        (right, layer.bottom),
                        (left, layer.bottom),
                    ],
                    soilcode=layer.soilcode,
                )
            )
        return result

    def set_top(self, top: float):
        self.soillayers[0].top = top

    def set_bottom(self, bottom: float):
        self.soillayers[-1].bottom = bottom
