"""
CO2 emission module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from hub.city_model_structure.building import Building
import hub.helpers.constants as cte


class Co2Emission:
  """
  Cost class
  """

  def __init__(self, building: Building, emissions_factor=None):
    if emissions_factor is None:
      # kgCO2 / J
      emissions_factor = {cte.GAS: 56.25480769E-9,
                          cte.ELECTRICITY: 0.313840909E-9,
                          cte.DIESEL: 74.52882883E-9,
                          cte.RENEWABLE: 0}
    self._emissions_factor = emissions_factor
    self._building = building
    self._year = [0]
    self._month = [0 for _ in range(12)]

  @property
  def building(self) -> Building:
    """
    Get current building.
    """
    return self._building

  @property
  def operational_co2(self) -> dict:
    """
    Get operational_co2
    :return: dict
    """
    results = {}
    for energy_system in self._building.energy_systems:
      for generation_system in energy_system.generation_systems:
        fuel_type = generation_system.fuel_type
        emissions_factor = self._emissions_factor[fuel_type]
        for demand_type in energy_system.demand_types:
          if demand_type == cte.ELECTRICITY:
            continue
          results_by_time_period = {}
          if demand_type == cte.HEATING:
            for time_period in self._building.heating_consumption:
              values = [v * emissions_factor for v in self._building.heating_consumption[time_period]]
              results_by_time_period[time_period] = values
          if demand_type == cte.COOLING:
            for time_period in self._building.cooling_consumption:
              values = [v * emissions_factor for v in self._building.cooling_consumption[time_period]]
              results_by_time_period[time_period] = values
          if demand_type == cte.DOMESTIC_HOT_WATER:
            for time_period in self._building.domestic_hot_water_consumption:
              values = [v * emissions_factor for v in self._building.domestic_hot_water_consumption[time_period]]
              results_by_time_period[time_period] = values
          results[demand_type] = results_by_time_period

    emission_factor = self._emissions_factor[cte.ELECTRICITY]
    results_by_time_period = {}
    for time_period in self._building.lighting_electrical_demand:
      values = [v * emission_factor for v in self._building.lighting_electrical_demand[time_period]]
      results_by_time_period[time_period] = values
    results[cte.LIGHTING] = results_by_time_period
    results_by_time_period = {}
    for time_period in self._building.appliances_electrical_demand:
      values = [v * emission_factor for v in self._building.appliances_electrical_demand[time_period]]
      results_by_time_period[time_period] = values
    results[cte.APPLIANCES] = results_by_time_period

    if cte.HEATING not in results:
      results[cte.HEATING] = {cte.YEAR: self._year, cte.MONTH: self._month}
    if cte.COOLING not in results:
      results[cte.COOLING] = {cte.YEAR: self._year, cte.MONTH: self._month}
    if cte.ELECTRICITY not in results:
      results[cte.ELECTRICITY] = {cte.YEAR: self._year, cte.MONTH: self._month}
    if cte.LIGHTING not in results:
      results[cte.LIGHTING] = {cte.YEAR: self._year, cte.MONTH: self._month}
    if cte.APPLIANCES not in results:
      results[cte.APPLIANCES] = {cte.YEAR: self._year, cte.MONTH: self._month}
    if cte.DOMESTIC_HOT_WATER not in results:
      results[cte.DOMESTIC_HOT_WATER] = {cte.YEAR: self._year, cte.MONTH: self._month}

    return results
