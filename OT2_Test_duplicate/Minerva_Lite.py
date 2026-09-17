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
import logging
import OpentronsOT2
import SampleHolder
from enum import Enum
from functools import total_ordering

from abc import ABC, abstractmethod, ABCMeta
from dataclasses import dataclass, field
from typing import NamedTuple, Union, Tuple, List, Dict, TYPE_CHECKING, Optional, Any, TypeVar, Type, Iterator, Callable, Iterable

from HelperClassDefinitions import *

# Create a custom logger and set it to the lowest level
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(filename=os.path.join(PathNames.LOG_DIR.value, 'log.txt'), mode='a')

# Configure the handlers
c_format = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Set the logging levels for the individual handlers
c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.INFO)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)


class AbstractClassIterMeta(ABCMeta):
    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        for k, v in vars(self).items():
            if not k.startswith('_') and not callable(getattr(self, k)):
                yield k, v

class ConfigurationMeta(AbstractClassIterMeta):
    def __str__(self) -> str:
        """Returns a formatted, printable string of the configuration."""
        max_len = 0
        repr_string = f'Configuration:\n==============\n'
        for i, j in self:
            for k in j:
                max_len = max(len(k), max_len)

        for i, j in self:
            if len(j) > 0:
                repr_string += f"{''.join(' ' + char if char.isupper() else char.strip() for char in i).strip()}:\n"
                for k, v in j.items():
                    repr_string += f'\t{k:{max_len}} : {v}\n'


        return repr_string

class Configuration(ABC, metaclass=ConfigurationMeta):
    OpentronsOT2: Dict[str, Any] = {}
    SampleHolder: Dict[str, Any] = {}
    Containers: Dict[str, Any] = {}
    Chemicals: Dict[str, Any] = {}

    @staticmethod
    def register_object(obj: Union[Hardware, Chemical, Container]) -> None:
        """
        Static method to register a new Object with this class. Called from the __post__init__ function of the Hardware superclass

        Parameters
        ----------
        obj: Union[Hardware, Chemical, Container]
            The Object to register in this class

        Returns
        -------
        None

        Raises
        ------
        NotImplementedError
            If it is attempted to register an unknown object type
        """
        if isinstance(obj, OpentronsOT2.OT2) and obj not in Configuration.OpentronsOT2:
            Configuration.OpentronsOT2[f'{_get_instance_name_from_object(obj)}'] = obj
        elif isinstance(obj, SampleHolderHardware) and obj not in Configuration.SampleHolder:
            Configuration.SampleHolder[f'{_get_instance_name_from_object(obj)}'] = obj
        elif isinstance(obj, Container) and obj not in Configuration.Containers:
            Configuration.Containers[f'{_get_instance_name_from_object(obj)}'] = obj
        elif isinstance(obj, Chemical) and obj not in Configuration.Chemicals:
            Configuration.Chemicals[f'{_get_instance_name_from_object(obj)}'] = obj
        else:
            raise NotImplementedError

    @staticmethod
    def unregister_object(obj: Union[Hardware, Chemical, Container]) -> None:
        """
        Static method to remove a registered object from the configuration

        Parameters
        ----------
        obj: Union[Hardware, Chemical, Container]
            The Object to register in this class

        Returns
        -------
        None
        """
        for i, j in Configuration:
            for key, val in j.items():
                if obj is val:
                    del j[key]

    @staticmethod
    def update_name_mappings(name_dict: Optional[Dict[str, str]] = None, rename_all: bool = False) -> None:
        """
        Method for updating the names of the objects in the configuration.

        Parameters
        ----------
        name_dict: Optional[Dict[str, str]] = None
            Mapping dictionary in the form {oldname: newname}. If None, current variable names will be used as new names.
        rename_all: bool = False
            If True, all names will be replaced with their variable names, if False, only "generic" names will be replaced. Only has an effect if name_dict is None.

        Returns
        -------
        None
        """
        for _, j in Configuration:
            for k, v in list(j.items()):
                if name_dict is None:
                    if rename_all or k == f'{type(v)}-{id(v)}':
                        j.update({f'{_get_instance_name_from_object(v)}': j.pop(k)})
                elif k in name_dict:
                    j.update({name_dict[k]: j.pop(k)})

    @staticmethod
    @atexit.register
    def save_configuration(configuration_file_path: str = os.path.join(PathNames.CONFIG_DIR.value, 'last_config.json'), update_name_mappings: bool = False) -> Dict[str, Any]:
        """
        Method for serializing the current configuration and saving it to a json file.

        Parameters
        ----------
        configuration_file_path: str = os.path.join(HelperClassDefinitions.PathNames.CONFIG_DIR.value, 'last_config.json')
            The file path to the json file to which the configuration is saved. Default is os.path.join(HelperClassDefinitions.PathNames.CONFIG_DIR.value, 'last_config.json')
        update_name_mappings: bool = False
            If set to True, the names of variables from the global scope will be used as names for the objects in the configuration. Should only be used when remapping variable names to objects.

        Returns
        -------
        Dict[str, Any]
            The json serialization of the current configuration.
        """
        if update_name_mappings:
            Configuration.update_name_mappings()

        config: Dict[str, Any] = {'NameMappings': {}}
        for k, v in Configuration:
            config[k] = {f'{type(i)}-{id(i)}': i.dump_configuration() for _, i in v.items()}
            config['NameMappings'].update({f'{type(j)}-{id(j)}': i for i, j in v.items()})

        with open(configuration_file_path, 'w') as f:
            json.dump(config, fp=f, indent=4)

        return config

    @staticmethod
    def load_configuration(configuration: Union[str, Dict[str, Any]] = os.path.join(PathNames.CONFIG_DIR.value, 'last_config.json')) -> Dict[str, Any]:
        """
        Method for loading a configuration from a json file and deserializing the objects.

        Parameters
        ----------
        configuration: Union[str, Dict[str, Any]] = os.path.join(HelperClassDefinitions.PathNames.CONFIG_DIR.value, 'last_config.json')
            A file path to the configuration file or the json dictionary for deserialization. Default is os.path.join(HelperClassDefinitions.PathNames.CONFIG_DIR.value, 'last_config.json')


        Returns
        -------
        Dict[str, Any]
            The loaded configuration
        """
        # Clear current configuration:
        for _, val in Configuration:
            val.clear()

        # Load new configuration:
        loaded_configuration: Dict[str, Any] = {k: {} for k, _ in Configuration}
        post_load_from_config: List[Tuple[Any, Dict[str, Any]]] = []

        if isinstance(configuration, str):
            with open(configuration, 'r') as f:
                configuration = json.load(f, )

        assert isinstance(configuration, dict)
        name_mappings = configuration.pop('NameMappings')

        error_counter = 0

        # The load order is important here since some components need instances of other components in their constructors. With newer Python versions the order in a dict is preserved, this might be a problem with older python versions, though.
        for k, v in configuration.items():
            for i, j in v.items():
                try:
                    if repr(OpentronsOT2.OT2) in i:
                        tmp_signature = inspect.signature(OpentronsOT2.OT2.__init__).parameters.keys()
                        kwargs = {key.lstrip('_'): val for key, val in j.items()}
                        init_kwargs = {key: kwargs.pop(key) for key in list(kwargs.keys()) if key.lstrip('_') in tmp_signature}
                        loaded_configuration[k][i] = OpentronsOT2.OT2(**init_kwargs)
                        post_load_from_config.append((loaded_configuration[k][i], kwargs.copy()))
                    elif repr(SampleHolder.SampleHolder) in i:
                        tmp_signature = inspect.signature(SampleHolder.SampleHolder.__init__).parameters.keys()
                        kwargs = {key.lstrip('_'): val for key, val in j.items() if key.lstrip('_') in tmp_signature}
                        if kwargs['parent_hardware'] == i:
                            kwargs['parent_hardware'] = None
                        else:
                            for key in configuration.keys():
                                for n in configuration[key].keys():
                                    if kwargs['parent_hardware'] in n:
                                        if kwargs['parent_hardware'] not in loaded_configuration[key].keys():
                                            raise ValueError(f'Parent hardware "{name_mappings[kwargs["parent_hardware"]]}" not found.')
                                        else:
                                            kwargs['parent_hardware'] = loaded_configuration[key][kwargs['parent_hardware']]
                                            break
                                else:
                                    continue
                                break
                        loaded_configuration[k][i] = SampleHolder.SampleHolder(**kwargs)
                    elif repr(Container) in i:
                        tmp_signature = inspect.signature(Container.__init__).parameters.keys()
                        kwargs = {key.lstrip('_'): val for key, val in j.items() if key.lstrip('_') in tmp_signature}
                        for key in configuration.keys():
                            for n in configuration[key].keys():
                                if kwargs['current_hardware'] in n:
                                    if kwargs['current_hardware'] not in loaded_configuration[key].keys():
                                        raise ValueError(f'Current hardware "{name_mappings[kwargs["current_hardware"]]}" not found.')
                                    else:
                                        kwargs['current_hardware'] = loaded_configuration[key][kwargs['current_hardware']]
                                        break
                            else:
                                continue
                            break
                        if 'container_type' in kwargs.keys() and kwargs['container_type'] is not None:
                            kwargs['container_type'] = ContainerTypeCollection.ContainerDescription(*kwargs['container_type'])
                        loaded_configuration[k][i] = Container(**kwargs)
                    elif repr(Chemical) in i:
                        kwargs = {key.lstrip('_'): val for key, val in j.items()}
                        if kwargs['container'] not in loaded_configuration['Containers'].keys():
                            raise ValueError(f'Container "{name_mappings[kwargs["container"]]}" not found.')
                        else:
                            kwargs['container'] = loaded_configuration['Containers'][kwargs['container']]
                            loaded_configuration[k][i] = Chemical(**kwargs)
                    else:
                        pass  # Implement your custom loading routine for other hardware here
                except Exception as ex:
                    logger.error(f'Error while loading configuration. Could not restore object "{k}: {name_mappings[i]}". Error message: {ex}')
                    if i in loaded_configuration.keys():
                        loaded_configuration[k].pop(i)
                    error_counter += 1

        # Do any remaining post_initialization
        for hw, d in post_load_from_config:
            hw.post_load_from_config(kwargs_dict=d, loaded_configuration_dict=loaded_configuration)

        # Restore original names:
        for i in loaded_configuration.values():
            for k, v in i.items():
                name_mappings[f'{type(v)}-{id(v)}'] = name_mappings.pop(k)
        Configuration.update_name_mappings(name_mappings)

        if error_counter == 0:
            logger.info(f'Configuration loaded successfully:\n{Configuration}')
        elif error_counter == 1:
            logger.info(f'Configuration loaded, but there was {error_counter} error:\n{Configuration}')
        else:
            logger.info(f'Configuration loaded, but there were {error_counter} errors:\n{Configuration}')

        return loaded_configuration

    @staticmethod
    def disable_autosave_on_exit() -> None:
        """Disable configuration autosaving on exit"""
        atexit.unregister(Configuration.save_configuration)

    @staticmethod
    def enable_autosave_on_exit() -> None:
        """Enable configuration autosaving on exit (enabled by default, so only needs to be enabled after disabling)"""
        atexit.register(Configuration.save_configuration)


def _get_instance_name_from_object(obj: Any, global_dict: Optional[Any] = None) -> str:
    """
    Function to get the first name of a variable from the global scope dict that points to this object

    Parameters
    ----------
    obj : Any
        The object whose name should be retrieved
    global_dict : Optional[str, Any] = None
        The dictionary in which to look for the Object. If None, the global scope of __main__ will be used

    Returns
    -------
    str
        The first name of a "named" variable from the global scope that points to this object, or obj.__repr__ if no variable is found
    """
    if global_dict is None:
        global_list = [(i, j) for i, j in vars(sys.modules['__main__']).items() if ' object at 0x' in repr(j) and not i.startswith('__')]  # Dictionary with variable name mappings from the main namespace
    else:
        global_list = [(i, j) for i, j in globals().items() if ' object at 0x' in repr(j) and not i.startswith('__')]

    for k, v in global_list:
        if v is obj and k != repr(v):  # try to find "named" objects
            return k

    # return repr(obj)
    return f'{type(obj)}-{id(obj)}'