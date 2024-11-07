#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from typing import TypeVar

from ...Domain.Enums.service_life import ServiceLifetime

_CLS_ = TypeVar('T', bound='ServiceDescriptorFWDI')
T = TypeVar('_CLS')

class ServiceDescriptorFWDI():
    def __init__(self) -> None:
        self.ServiceType: type[T] = None
        self.ImplementationType: type[T] = None
        self.Implementation:T = None
        self.Lifetime:ServiceLifetime = None
	
    @classmethod
    def create_from_instance(cls: type[_CLS_], inst:T, lifetime:ServiceLifetime)-> _CLS_:
        new_instance = cls()
        new_instance.ImplementationType = type(inst)
        new_instance.ServiceType = new_instance.ImplementationType
        new_instance.Implementation = inst
        new_instance.Lifetime = lifetime

        return new_instance

    @classmethod
    def create_from_type(cls: type[_CLS_], inst_type:type[T] , lifetime:ServiceLifetime)-> _CLS_:
         new_instance = cls()
         new_instance.ServiceType = inst_type
         new_instance.ImplementationType = inst_type
         new_instance.Lifetime = lifetime

         return new_instance

    @classmethod
    def create(cls: type[_CLS_], base_type:type[T], inst_type:type[T], lifetime: ServiceLifetime)-> _CLS_:
        new_instance = cls()
        new_instance.ServiceType = base_type
        new_instance.ImplementationType = inst_type
        new_instance.Lifetime = lifetime

        return new_instance