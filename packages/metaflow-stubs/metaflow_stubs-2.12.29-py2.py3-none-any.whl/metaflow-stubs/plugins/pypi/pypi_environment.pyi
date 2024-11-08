######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.29                                                                                #
# Generated on 2024-11-07T22:19:34.603536                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

