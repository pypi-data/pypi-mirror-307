# coding=utf-8
"""Water Source Heat Pump (WSHP) with DOAS HVAC system."""
from __future__ import division

from ._base import _DOASBase

from honeybee._lockable import lockable


@lockable
class WSHPwithDOAS(_DOASBase):
    """Water Source Heat Pump (WSHP) with DOAS HVAC system.

    All rooms/zones in the system are connected to a Dedicated Outdoor Air System
    (DOAS) that supplies a constant volume of ventilation air at the same temperature
    to all rooms/zones. The ventilation air temperature will vary from 21.1C (70F)
    to 15.5C (60F) depending on the outdoor air temperature (the DOAS supplies cooler air
    when outdoor conditions are warmer). The ventilation air temperature is maintained
    by a chilled water cooling coil and a hot water heating coil except when the
    ground source heat pump (GSHP) option is selected. In this case, the ventilation
    air temperature is maintained by a two-speed direct expansion (DX) cooling coil
    and a single-speed DX heating coil with backup electrical resistance heat.

    Each room/zone also receives its own Water Source Heat Pump (WSHP), which meets
    the heating and cooling loads of the space. All WSHPs are connected to the
    same water condenser loop, which has its temperature maintained by the
    equipment_type (eg. Boiler with Cooling Tower).

    Args:
        identifier: Text string for system identifier. Must be < 100 characters
            and not contain any EnergyPlus special characters. This will be used to
            identify the object across a model and in the exported IDF.
        vintage: Text for the vintage of the template system. This will be used
            to set efficiencies for various pieces of equipment within the system.
            Choose from the following.

            * DOE_Ref_Pre_1980
            * DOE_Ref_1980_2004
            * ASHRAE_2004
            * ASHRAE_2007
            * ASHRAE_2010
            * ASHRAE_2013
            * ASHRAE_2016
            * ASHRAE_2019

        equipment_type: Text for the specific type of the system and equipment. (Default:
            the first option below) Choose from.

            * DOAS_WSHP_FluidCooler_Boiler
            * DOAS_WSHP_CoolingTower_Boiler
            * DOAS_WSHP_GSHP
            * DOAS_WSHP_DCW_DHW

        sensible_heat_recovery: A number between 0 and 1 for the effectiveness
            of sensible heat recovery within the system. (Default: 0).
        latent_heat_recovery: A number between 0 and 1 for the effectiveness
            of latent heat recovery within the system. (Default: 0).
        demand_controlled_ventilation: Boolean to note whether demand controlled
            ventilation should be used on the system, which will vary the amount
            of ventilation air according to the occupancy schedule of the
            Rooms. (Default: False).
        doas_availability_schedule: An optional On/Off discrete schedule to set when
            the dedicated outdoor air system (DOAS) shuts off. This will not only
            prevent any outdoor air from flowing thorough the system but will also
            shut off the fans, which can result in more energy savings when spaces
            served by the DOAS are completely unoccupied. If None, the DOAS will be
            always on. (Default: None).

    Properties:
        * identifier
        * display_name
        * vintage
        * equipment_type
        * sensible_heat_recovery
        * latent_heat_recovery
        * demand_controlled_ventilation
        * doas_availability_schedule
        * schedules
        * has_district_heating
        * has_district_cooling
        * user_data
        * properties
    """
    __slots__ = ()

    EQUIPMENT_TYPES = (
        'DOAS_WSHP_FluidCooler_Boiler',
        'DOAS_WSHP_CoolingTower_Boiler',
        'DOAS_WSHP_GSHP',
        'DOAS_WSHP_DCW_DHW'
    )
