#
# Copyright (c) 2015-2024 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_*** module

"""

from decimal import Decimal

from persistent import Persistent
from zope.schema.fieldproperty import FieldProperty

from pyams_gis.interfaces import CRS, IGeoArea
from pyams_gis.transform import transform
from pyams_utils.factory import factory_config
from pyams_utils.list import is_not_none

__docformat__ = 'restructuredtext'


@factory_config(IGeoArea)
class GeoArea(Persistent):
    """GeoArea attribute object"""

    x1 = FieldProperty(IGeoArea['x1'])
    y1 = FieldProperty(IGeoArea['y1'])
    x2 = FieldProperty(IGeoArea['x2'])
    y2 = FieldProperty(IGeoArea['y2'])
    projection = FieldProperty(IGeoArea['projection'])

    def __init__(self, data=None, **kwargs):
        super().__init__()
        if 'x1' in kwargs:
            self.x1 = Decimal(kwargs['x1'])
        if 'y1' in kwargs:
            self.y1 = Decimal(kwargs['y1'])
        if 'x2' in kwargs:
            self.x2 = Decimal(kwargs['x2'])
        if 'y2' in kwargs:
            self.y2 = Decimal(kwargs['y2'])
        if 'projection' in kwargs:
            self.projection = kwargs['projection']

    def __bool__(self):
        return len(tuple(filter(is_not_none, (self.x1, self.y1, self.x2, self.y2)))) == 4

    def get_coordinates(self, projection=CRS.WGS84.value):
        if projection == self.projection:
            return (self.x1, self.y1), (self.x2, self.y2)
        point1 = transform({
            'longitude': float(self.x1),
            'latitude': float(self.y1)
        }, self.projection, projection).get('point')
        point2 = transform({
            'longitude': float(self.x2),
            'latitude': float(self.y2)
        }, self.projection, projection).get('point')
        return (
            (point1['longitude'], point1['latitude']),
            (point2['longitude'], point2['latitude'])
        )

    @property
    def wgs_coordinates(self):
        return self.get_coordinates(CRS.WGS84.value)

    def to_json(self):
        if not self:
            return None
        return {
            'x1': float(self.x1),
            'y1': float(self.y1),
            'x2': float(self.x2),
            'y2': float(self.y2),
            'crs': self.projection
        }
