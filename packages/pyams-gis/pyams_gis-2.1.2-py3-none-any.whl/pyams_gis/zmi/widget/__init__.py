# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

__docformat__ = 'restructuredtext'

from zope.interface import Interface

from pyams_form.interfaces import IObjectFactory
from pyams_form.interfaces.form import IForm
from pyams_form.interfaces.widget import IObjectWidget
from pyams_gis.interfaces.configuration import IMapConfiguration
from pyams_gis.zmi.interfaces import IMapHeaderViewletManager
from pyams_layer.interfaces import IFormLayer
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import get_interface_name, get_object_factory
from pyams_viewlet.manager import WeightOrderedViewletManager, viewletmanager_config


@adapter_config(name=get_interface_name(IMapConfiguration),
                required=(Interface, IFormLayer, IForm, IObjectWidget),
                provides=IObjectFactory)
def map_configuration_factory(*args):
    """Map configuration object factory"""
    return get_object_factory(IMapConfiguration)


@viewletmanager_config(name='pyams_gis.map.header',
                       layer=IFormLayer, view=Interface,
                       provides=IMapHeaderViewletManager)
class MapHeaderViewletManager(WeightOrderedViewletManager):
    """Map header viewlet manager"""
