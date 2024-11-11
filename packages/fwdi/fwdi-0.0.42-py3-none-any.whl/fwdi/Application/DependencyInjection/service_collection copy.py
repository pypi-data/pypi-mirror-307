#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from ...Application.Abstractions.base_di_container import BaseDIConteinerFWDI
from ...Application.Abstractions.base_service_collection import BaseServiceCollectionFWDI
from ...Application.Abstractions.service_descriptor import ServiceDescriptorFWDI
from ...Domain.Enums.service_life import ServiceLifetime
from .dependency_container import DependencyContainerFWDI, TService

class ServiceCollectionFWDI(BaseServiceCollectionFWDI):
    def __init__(self) -> None:        
        self._serviceDescriptor:set[ServiceDescriptorFWDI] = set()

    @property
    def ServiceDescriptor(self)->set:
        return self._serviceDescriptor

    def AddImplementSingleton(self, implementation: TService):
        self._serviceDescriptor.add(ServiceDescriptorFWDI.create_from_instance(implementation, lifetime=ServiceLifetime.Singleton))
	
    def AddSingleton(self, type_service: type[TService], implementation: TService):
        self._serviceDescriptor.add(ServiceDescriptorFWDI.create(type_service, implementation, ServiceLifetime.Singleton))

    def AddImplementTransient(self, implementation: TService):
        self._serviceDescriptor.add(ServiceDescriptorFWDI.create_from_instance(implementation, ServiceLifetime.Transient))

    def AddTransient(self, type_service: type[TService], implementation: TService):
        self._serviceDescriptor.add(ServiceDescriptorFWDI.create(type_service, implementation, ServiceLifetime.Transient))

    def GenerateContainer(self)->BaseDIConteinerFWDI:
        return DependencyContainerFWDI(self._serviceDescriptor)