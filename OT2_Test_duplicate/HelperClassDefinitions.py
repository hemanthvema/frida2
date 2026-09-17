#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author:      "Bastian Ruehle"
# @copyright:   "Copyright 2022, Bastian Ruehle, Federal Institute for Materials Research and Testing (BAM)"
# @version:     "0.9.1"
# @maintainer:  "Bastian Ruehle"
# @email        "bastian.ruehle@bam.de"

from __future__ import annotations

import inspect
import json
import queue
import sys
import threading
import os.path
import time
import math
import atexit
from enum import Enum
from functools import total_ordering

from abc import ABC, abstractmethod, ABCMeta
from dataclasses import dataclass, field
from typing import NamedTuple, Union, Tuple, List, Dict, TYPE_CHECKING, Optional, Any, TypeVar, Type, Iterator, Callable, Iterable

import Minerva_Lite

class PathNames(Enum):
    """Enum class with Path Names"""
    ROOT_DIR: str = os.path.join('C:\\', 'users', 'Frida-Lab62', 'Desktop', 'electrochemistry_dupmergedfile', 'OT2_Test_duplicate')
    LOG_DIR: str = os.path.join('C:\\', 'users', 'Frida-Lab62', 'Desktop', 'electrochemistry_dupmergedfile', 'OT2_Test_duplicate', 'Logs')
    CONFIG_DIR: str = os.path.join('C:\\', 'users', 'Frida-Lab62', 'Desktop', 'electrochemistry_dupmergedfile', 'OT2_Test_duplicate', 'Configuration')
    OT2_TEMP_DIR: str = os.path.join('C:\\', 'users', 'Frida-Lab62', 'Desktop', 'electrochemistry_dupmergedfile', 'OT2_Test_duplicate', 'OT2_Temp_Protocols')

class HardwareMeta(ABCMeta):
    def __call__(cls: ABCMeta, *args: Any, **kwargs: Any) -> Hardware:
        obj = type.__call__(cls, *args, **kwargs)
        obj.__post__init__()
        return obj


class Hardware(metaclass=HardwareMeta):
    """Abstract base class for all hardware."""
    def __init__(self) -> None:
        self._deck_position: Union[int, None] = None

    def __post__init__(self) -> None:
        """Executed after the __init__ function."""
        Minerva_Lite.Configuration.register_object(self)  # Only register the object if it was successfully created

    def dump_configuration(self) -> Dict[str, Any]:
        """Dump all current instance vars in a json-serializable dict. Override if some of your instance variables need other functionality (see OT2 for an example)."""
        return dict([(k, v) if _is_json_serializable(v) else (k, f'{type(v)}-{id(v)}') for k, v in vars(self).items()])

    def post_load_from_config(self, kwargs_dict: Dict[str, Any], loaded_configuration_dict: Dict[str, Any]) -> bool:
        """
        Function will be called after everything else is initialized when loading from a configuration file (can e.g. be used for setting configurations that depend on other objects being initialized first).

        Parameters
        ----------
        kwargs_dict: Dict[str, Any]
            Dictionary with any remaining kwargs that were not used in the __init__ method of the class
        loaded_configuration_dict: Dict[str, Any]
            Dictionary with all initialized objects

        Returns
        -------
        bool
            True if successful, False otherwise
        """
        pass

    def __str__(self) -> str:
        """Function returning a human-readable string description of the class."""
        tmp = self.__class__.__name__
        if hasattr(self, 'ip_address'):
            return f'{tmp}@{self.ip_address}'
        else:
            if hasattr(self, 'hardware_definition'):
                # tmp += f'("{self.hardware_definition["metadata"]["displayName"]}")'
                tmp = self.hardware_definition["metadata"]["displayName"]
                if tmp == '':
                    tmp = 'SampleHolder'
            if self._deck_position is None:
                return f'{tmp}'
            else:
                return f'{tmp} at deck {self._deck_position}'


class SampleHolderHardware(Hardware, ABC):
    """Abstract base class for sample holder hardware."""

    def __init__(self) -> None:
        self.available_slots: Dict[int, Union[str, None]] = {}
        self._hardware_definition: Any = {}

    @property
    def deck_position(self) -> int:
        return self._deck_position

    @abstractmethod
    def get_coordinates(self, slot_number: int, offset_top_left: Union[Tuple[float, ...], List[float], dict, None] = (0.0, 0.0, 0.0), rotation_angle: float = 0, invert_y: bool = True) -> Union[Tuple[float, float, float], None]:
        """
        Override this method with your own implementation to get the coordinates of a slot number of a sample holder.

        Parameters
        ----------
        slot_number: int
            The number of the slot in the holder (starting at 1, counting from top left)
        offset_top_left:  Union[Tuple[float, ...], List[float, ...], dict, None] = (0.0, 0.0, 0.0)
            Optional offset to be added to all positions. If None, the offset is read from the json file used when creating the instance. If dict, has to have the keys x0, y0, and z0.
        rotation_angle: float = 0
            Optional counterclockwise rotation angle in degrees about the z-Axis of the holder to match the returned coordinates with the robot coordinate system. Typically, the longer side is along the x-Axis. Default is 0.
        invert_y: bool = True
            Optional value indicating to invert the y coordinates (should be used when spacings are positive and slot 1 is in the top left corner)

        Returns
        -------
        Union[Tuple[float, float, float], None]
            A tuple containing the x, y, and z coordinates of the slot in the specified holder, or None if an invalid slot number was given
        """
        pass

    @abstractmethod
    def get_next_free_slot(self) -> Union[int, None]:
        """
        Override this method to implement getting the number of the next free slot in this hardware.

        Returns
        -------
        Union[int, None]
            An integer of the next free slot, or None if no free slots are available in the holder
        """
        pass


@dataclass
class ContainerTypeCollection(ABC):
    """Collection of Container Types."""
    class ContainerDescription(NamedTuple):
        """
        Class derived from Named Tuple for describing containers.

        Parameters
        ----------
        container_name : str
            The name of the container. The container_name string should also be in the metadata tags of the corresponding sample holder hardware definition.
        container_height : float
            The height the container in Millimeter
        container_max_volume : float
            The maximum volume of the container in Milliliter
        """
        container_name: str
        container_height: float
        container_max_volume: float
        container_diameter: float

    FALCON_TUBE_15_ML = ContainerDescription('FALCON_TUBE_15_ML', 120, 15, 16)  # Labsolute Conical Tube
    FALCON_TUBE_50_ML = ContainerDescription('FALCON_TUBE_50_ML', 115, 50, 28)  # Labsolute Conical Tube
    FLASK_10_ML = ContainerDescription('FLASK_10_ML', 70, 10, 35)  # Labsolute Round-Bottom Flask
    FLASK_25_ML = ContainerDescription('FLASK_25_ML', 85, 25, 41)  # Labsolute Round-Bottom Flask
    FLASK_50_ML = ContainerDescription('FLASK_50_ML', 90, 50, 51)  # Labsolute Round-Bottom Flask
    FLASK_100_ML = ContainerDescription('FLASK_100_ML', 105, 100, 64)  # Labsolute Round-Bottom Flask
    FLASK_250_ML = ContainerDescription('FLASK_250_ML', 140, 250, 85)  # Labsolute Round-Bottom Flask
    FLASK_500_ML = ContainerDescription('FLASK_500_ML', 163, 500, 105)  # Labsolute Round-Bottom Flask


class SampleHolderDefinitions(Enum):
    """Enum class with the file paths to the hardware definitions of the individual holders"""
    Isolab_50mL_Foldable_Tube_Rack = './SampleHolder/Isolab_50mL_Foldable_Tube_Rack.json'
    Opentrons_15mL_Tube_Rack = './SampleHolder/Opentrons_15mL_Tube_Rack.json'
    Opentrons_50mL_Tube_Rack = './SampleHolder/Opentrons_50mL_Tube_Rack.json'
    Labsolute_96_Tip_Rack_1000uL = './SampleHolder/Labsolute_96_Tip_Rack_1000uL.json'


class Unit(NamedTuple):
    """
    Class derived from Named Tuple for defining units.

    Parameters
    ----------
    id : int
        An ID value for the units.
    string_representations : Tuple[str, ...]
        The string representations of the units.
    conversion_factor : float
        The factor used for converting the unit to SI base units.
    """
    id: int
    string_representations: Tuple[str, ...]
    conversion_factor: float


@total_ordering
class Quantity(ABC):
    """
    Abstract class from which classes specifying a quantity are derived (density, volume, mass, etc.)

    Parameters
    ----------
    value : float
        The numerical value of the quantity in the given unit (cannot be negative).
    unit : str
        The string representation of the unit used for the quantity. Has to be defined in the units of the class.

    Raises
    ------
    AssertionError
        If a negative value is entered.
    """
    units: list[Unit]

    def __init__(self, value: float, unit: str):
        assert value >= 0, "Value has to be >= 0."
        for u in self.units:
            if unit.lower() in map(str.lower, u.string_representations):
                break
        else:
            raise AssertionError('Invalid unit. Please make sure the unit is defined in the class.')

        self.value = value
        self._unit = unit

    @classmethod
    def from_string(cls: Type[T], quantity_string: str) -> T:
        """
        Alternative constructor working with a single string that contains both the value and the unit

        Parameters
        ----------
        quantity_string: str
            A single string that contains both the value and the unit

        Returns
        -------
        Quantity
            An instance of the class constructed from the string
        """
        quantity_string = quantity_string.replace(' ', '').strip()
        ind = [char.isalpha() for char in quantity_string].index(True)
        return cls(float(quantity_string[:ind]), quantity_string[ind:])

    @property
    def unit(self) -> str:
        return self._unit

    def in_si(self) -> float:
        """
        Returns the value of the quantity in the SI base unit, without changing any values of the instance itself. Use convert_to to change the value and unit of this instance in place.

        Returns
        -------
        float
            The value in the SI base unit, or None if the conversion fails.

        Raises
        ------
        ValueError
            If the conversion fails (usually because of an invalid unit)
        """
        for u in self.units:
            if self._unit.lower() in map(str.lower, u.string_representations):
                return self.value * u.conversion_factor
        raise ValueError

    def in_unit(self, target_unit: str) -> float:
        """
        Returns the value of the quantity in the specified unit, without changing any values of the instance itself. Use convert_to to change the value and unit of this instance in place.

        Parameters
        ----------
        target_unit : str
            The string representation of the target unit (has to be defined in the classes Unit field).

        Returns
        -------
        float
            The value in the target unit, or None if the conversion fails (due to the target value not being defined).

        Raises
        ------
        ValueError
            If the conversion fails (usually because of an invalid target unit)
        """
        for u in self.units:
            if target_unit.lower() in map(str.lower, u.string_representations):
                si_value = self.in_si()
                if si_value is not None:
                    return si_value / u.conversion_factor
        raise ValueError

    def convert_to(self: T, target_unit: str) -> T:
        """
        Converts the value and unit of this instance in place, and returns the instance with updated values. Use in_unit to just returns the value of the quantity in the specified unit without changing any values of the instance itself.

        Parameters
        ----------
        target_unit : str
            The string representation of the target unit (has to be defined in the classes Unit field).

        Returns
        -------
        Quantity
            The same instance with the value and unit changed in place.
        """
        for u in self.units:
            if target_unit.lower() in map(str.lower, u.string_representations):
                self.value = self.in_si()/u.conversion_factor
                self._unit = target_unit
                break
        return self

    def __add__(self, other: Union[Quantity, int, float], keep_original_unit: bool = True) -> float:
        """
        Add method for adding a number or another quantities to this quantity. If two quantities are added and the units are different, the unit for the first value is used by default for the result.
        Parameters
        ----------
        other : Union[Quantity, int, float]
            The number or quantity to be added.
        keep_original_unit: bool = True
            If True, the result will be returned in the unit of the first Quantity, if False and the second value is also a Quantity, the unit of the second Quantity will be used.

        Returns
        -------
        float
            The result of the addition.

        """
        if isinstance(other, Quantity):
            if keep_original_unit:
                return self.value + other.in_unit(self._unit)
            else:
                return self.in_unit(other._unit) + other.value
        else:
            return self.value + other

    def __sub__(self, other: Union[Quantity, int, float], keep_original_unit: bool = True) -> float:
        """
        Subtract method for subtracting a number or another quantities to this quantity. If two quantities are subtracted and the units are different, the unit for the first value is used by default for the result.
        Parameters
        ----------
        other : Union[Quantity, int, float]
            The number or quantity to be subtracted.
        keep_original_unit: bool = True
            If True, the result will be returned in the unit of the first Quantity, if False and the second value is also a Quantity, the unit of the second Quantity will be used.

        Returns
        -------
        float
            The result of the subtraction.

        """
        if isinstance(other, Quantity):
            if keep_original_unit:
                return self.value - other.in_unit(self._unit)
            else:
                return self.in_unit(other._unit) - other.value
        else:
            return self.value - other

    def __mul__(self, other: Union[Quantity, int, float]) -> float:
        """
        Muliplication method for multiplying a number or another quantities with this quantity. If both values are Quantities, they will be converted to SI base units first.

        Parameters
        ----------
        other : Union[Quantity, int, float]
            The number or quantity to be multiplied.

        Returns
        -------
        float
            The result of the multiplication.
        """
        if isinstance(other, Quantity):
            return self.in_si() * other.in_si()
        else:
            return self.value * other

    def __truediv__(self, other: Union[Quantity, int, float]) -> float:
        """
        Division method for dividing this quantity by a number or another quantities. If both values are Quantities, they will be converted to SI base units first.

        Parameters
        ----------
        other : Union[Quantity, int, float]
            The number or quantity by which this quantity is divided.

        Returns
        -------
        float
            The result of the division.
        """
        if isinstance(other, Quantity):
            return self.in_si() / other.in_si()
        else:
            return self.value / other

    def __eq__(self, other: object) -> bool:
        """
        Method for comparing this quantity to a number or another quantities. If both values are Quantities, they will be converted to SI base units first, otherwise it will be assumed that they use the same unit

        Parameters
        ----------
        other : object
            The number or quantity to with which equality should be checked.

        Returns
        -------
        bool
            The result of the equality comparison

        Raises
        ------
        NotImplementedError
            If the other object is not a Quantity, int or float
        """
        if isinstance(other, Quantity):
            return self.in_si() == other.in_si()
        elif isinstance(other, int) or isinstance(other, float):
            return self.value == other
        else:
            raise NotImplementedError

    def __lt__(self, other: object) -> bool:
        """
        Method for comparing this quantity to a number or another quantities. If both values are Quantities, they will be converted to SI base units first, otherwise it will be assumed that they use the same unit

        Parameters
        ----------
        other : Union[Quantity, int, float]
            The number or quantity to with which this quantity should be compared.

        Returns
        -------
        bool
            The result of the comparison

        Raises
        ------
        NotImplementedError
            If the other object is not a Quantity, int or float
        """
        if isinstance(other, Quantity):
            return self.in_si() < other.in_si()
        elif isinstance(other, int) or isinstance(other, float):
            return self.value < other
        else:
            raise NotImplementedError

    def __str__(self) -> str:
        """
        Method for giving a string representation of the class instance

        Returns
        -------
        str
            A human-readable string representation of the object
        """
        return f'{self.value} {self._unit}'


class Volume(Quantity):
    """Quantity class representing a volume. Units are not case sensitive. Conversion factors are for the conversion to SI base units."""
    units: List[Unit] = [
        Unit(id=0, string_representations=('m3', 'm^3', 'cubic meter', 'cubic metre'), conversion_factor=1),
        Unit(id=1, string_representations=('L', 'liter', 'liters', 'litre', 'litres'), conversion_factor=1e-3),
        Unit(id=2, string_representations=('mL', 'ccm', 'mils', 'mills', 'milliliter', 'milliliters', 'millilitre', 'millilitres'), conversion_factor=1e-6),
        Unit(id=3, string_representations=('uL', 'µL', 'microliter', 'microliters', 'microlitre', 'microlitres'), conversion_factor=1e-9),
    ]


class CustomError(Exception):
    """Custom Exception to be used as a guard clause"""
    pass


class Container(Hardware):
    """
    Class specifying a container object that can hold a chemical (can be a flask, tube, etc.)

    Parameters
    ----------
    current_hardware : Hardware
        The hardware where the container is currently located.
    deck_position : int, default = 0
        The deck number of the holder (if the parent hardware has several positions for holders). If current_hardware is a SampleHolder, the deck number of the sample holder will be used. Default is 0.
    slot_number : int, default = 0
        Optional number of the slot of the holder (for holders with several slots) or the valve position (if the hardware is a syringe pump) that can be used to access the container, default is 0
    name : str, default = ''
        Optional name of the container, default = '' (a name will be generated automatically based on the container type or class).
    current_volume : Union[Volume, str, None] = None
        Optional value specifying the volume that is currently in the container and not already assigned to any queued commands, default is None. If None, it is assumed that the container is empty
    max_volume : Volume = Union[Volume, str, None]
        Optional value the maximum volume the container can hold. If not None, it will be checked if an addition exceeds the maximum volume, default is None. If None, no checks if additions will exceed max volume are performed.
    container_type : Union[ContainerTypeCollection.ContainerDescription, None], default = None
        The type and height of the container in mm. Needs to be specified if the container should be picked up and moved by the robotic arm, and if the OT2 should adjust the aspirating/dispensing height of the pipette depending on the fill level of the container.

    Raises
    ------
    AssertionError
        If an invalid value is entered for any of the fields.
    """
    def __init__(self, current_hardware: SampleHolderHardware, deck_position: int = 0, slot_number: int = 0, name: str = '', current_volume: Union[Volume, str, None] = None, max_volume: Union[Volume, str, None] = None, container_type: Union[ContainerTypeCollection.ContainerDescription, None] = None, has_stirbar: bool = False, is_capped: bool = False):
        if isinstance(current_volume, str):
            current_volume = Volume.from_string(current_volume)
        if isinstance(max_volume, str):
            max_volume = Volume.from_string(max_volume)

        # assert isinstance(current_hardware, SampleHolderHardware), 'invalid hardware'
        assert isinstance(deck_position, int) and deck_position >= 0, 'deck_position must be an integer >= 0'
        assert isinstance(slot_number, int) and slot_number >= 0, 'slot_number must be an integer >= 0'
        assert current_volume is None or isinstance(current_volume, Volume), 'invalid value for current_volume'
        assert max_volume is None or isinstance(max_volume, Volume), 'invalid value for max_volume'

        if isinstance(current_hardware, SampleHolderHardware):
            deck_position = current_hardware.deck_position

        self.name = str(name)
        self._current_hardware = current_hardware
        self._deck_position = int(deck_position)
        self._slot_number = int(slot_number)
        self._current_volume = current_volume
        self._max_volume = max_volume
        self._container_type = container_type

        if self.name == '':
            if self.container_type is None:
                self.name = self.__class__.__name__ + str(time.time())
            else:
                self.name = f'{self.container_type.container_name}_{id(self)}'

        if current_volume is None:
            self._current_volume = Volume(0, 'mL')

        if max_volume is not None:
            self._max_volume = max_volume
        elif isinstance(self._container_type, (ContainerTypeCollection, ContainerTypeCollection.ContainerDescription)):
            self._max_volume = Volume(self._container_type.container_max_volume, 'mL')

        if isinstance(self._current_hardware, SampleHolderHardware):
            self._current_hardware.available_slots[slot_number] = self.name

    def __str__(self) -> str:
        """Function returning a human-readable string description of the class with some information."""
        if self.container_type is None:
            tmp_name = self.__class__.__name__
        else:
            tmp_name = self.container_type.container_name

        if self.current_volume is None:
            tmp_vol = ''
        else:
            if self.current_volume.value >= 1e-3 and self.current_volume.value < 1e4:
                tmp_vol = f': {round(self.current_volume.value, 4)} {self.current_volume.unit}'
            else:
                tmp_vol = f': {self.current_volume.value:.3e} {self.current_volume.unit}'

        return f'{tmp_name}{tmp_vol} at {self.deck_position}->slot {self.slot_number}'

    @property
    def current_hardware(self) -> SampleHolderHardware:
        return self._current_hardware

    @property
    def deck_position(self) -> int:
        return self._deck_position

    @property
    def slot_number(self) -> int:
        return self._slot_number

    @property
    def current_volume(self) -> Union[Volume, None]:
        return self._current_volume

    # @current_volume.setter  # Only allow the class itself and addition hardware to change the current volume
    # def current_volume(self, args: Tuple) -> None:
    #     if isinstance(args, Tuple) and isinstance(args[0], Volume) and (args[1] == self or isinstance(args[1], (OpentronsOT2.OT2, SixWayValve.SixWayValve))):
    #         self._current_volume = args[0]
    #     else:
    #         to_str('Illegal call to setter of private variable _current_volume.')
    @current_volume.setter
    def current_volume(self, value: Volume) -> None:
        self._current_volume = value

    @property
    def max_volume(self) -> Union[Volume, None]:
        return self._max_volume

    @property
    def container_type(self) -> Union[ContainerTypeCollection.ContainerDescription, None]:
        return self._container_type

    @property
    def has_stirbar(self) -> bool:
        return self._has_stirbar

    @property
    def is_capped(self) -> bool:
        return self._is_capped

    def dump_configuration(self) -> Dict[str, Any]:
        """Dump all current instance vars in a json-serializable dict."""
        return_dict = {}
        for k, v in vars(self).items():
            if _is_json_serializable(v):
                return_dict[k] = v
            elif isinstance(v, Quantity):
                return_dict[k] = str(v)
            else:
                return_dict[k] = f'{type(v)}-{id(v)}'
        return return_dict
    
    def get_solvent_level_height(self) -> float:
        """
        Method used for calculating the height of the solvent level in mm above the bottom of the container.

        Returns
        -------
        float
            The height in mm if successful, or 0 if the height cannot be calculated
        """
        h = 0.0
        if self.current_volume is not None and self.current_volume.in_unit('uL') > 0 and self.container_type is not None:
            r = self.container_type.container_diameter / 2.0
            v = self.current_volume.in_unit('uL')
            if 'falcon_tube' in self.container_type.container_name.lower():
                # Calculate height of liquid in conical tube above bottom, assume conical part starts at 10 % of the max volume
                h = min(v, self.max_volume.in_unit('uL') * 0.1) / ((math.pi * r ** 2) / 3.0) + max(0.0, v - self.max_volume.in_unit('uL') * 0.1 / ((math.pi * r ** 2) / 3.0)) / (math.pi * r ** 2)
            else:
                raise NotImplemented('Method is currently only implemented for Falcon tubes')
        return h



class Chemical:
    """
    Class specifying a chemical/reagent that can be used in an addition step. It holds the information about the amount
    of the chemical that should be added and the container it can be taken from.

    Parameters
    ----------
    container : Container
        The container the chemical is in
    volume: Union[Volume, str, None] = None
        Volume of the chemical to be used.
    name: str = ''
        Name of the chemical, default is ''. If lookup_missing_values is set to True, it will be attempted to look up the name from the CAS number or SMILES string.
    lot_number: str = ''
        Lot number of the chemical, default is ''
    supplier: str = ''
        Supplier of the chemical, default is ''
    cas: str = ''
        CAS number of the chemical, default is ''. If lookup_missing_values is set to True, it will be attempted to look up the CAS number from the SMILES string or name.
    smiles: str = ''
        SMILES of the chemical, default is ''. If lookup_missing_values is set to True, it will be attempted to look up the SMILES string from the CAS number or name.

    Raises
    ------
    AssertionError
        If an invalid value is entered for any of the fields.
    """
    def __init__(self,
                 container: Container,
                 volume: Union[Volume, str],
                 name: str = '',
                 lot_number: str = '',
                 supplier: str = '',
                 cas: str = '',
                 smiles: str = ''):

        if isinstance(volume, str):
            volume = Volume.from_string(volume)
        self.volume = volume
        assert isinstance(container, Container), 'Invalid COntainer'
        self.container = container
        self.name = name
        self.lot_number = lot_number
        self.supplier = supplier
        self.cas = cas
        self.smiles = smiles

    def __str__(self) -> str:
        """Function returning a human-readable string description of the class with some information."""
        if self.name is not None:
            tmp_name = f'Chemical {self.name}'
        else:
            tmp_name = 'Unknown chemical'

        if self.cas is not None:
            tmp_cas = f' (CAS:{self.cas})'
        else:
            tmp_cas = ''

        if self.volume.value >= 1e-3 and self.volume.value < 1e4:
            tmp_vol = f': {round(self.volume.value, 4)} {self.volume.unit}'
        else:
            tmp_vol = f': {self.volume.value:.3e} {self.volume.unit}'

        return f'{tmp_name}{tmp_cas}{tmp_vol}'

    def dump_configuration(self) -> Dict[str, Any]:
        """Dump all current instance vars in a json-serializable dict."""
        return_dict = {}
        for k, v in vars(self).items():
            if _is_json_serializable(v):
                return_dict[k] = v
            elif isinstance(v, Quantity):
                return_dict[k] = str(v)
            else:
                return_dict[k] = f'{type(v)}-{id(v)}'
        return return_dict

def _is_json_serializable(obj: Any) -> bool:
    """
    Function to check whether an object is serializable as json.

    Parameters
    ----------
    obj : Any
        The object that should be checked

    Returns
    -------
    bool
        True if the object is serializable, False otherwise
    """
    try:
        json.dumps(obj)
        return True
    except (TypeError, OverflowError):
        return False


T = TypeVar('T', bound='Quantity')
