######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.29                                                                                #
# Generated on 2024-11-07T22:19:34.620126                                                            #
######################################################################################################

from __future__ import annotations

import abc
import metaflow
import typing
if typing.TYPE_CHECKING:
    import abc
    import metaflow.plugins.secrets

from . import SecretsProvider as SecretsProvider

class InlineSecretsProvider(metaflow.plugins.secrets.SecretsProvider, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None):
        """
        Intended to be used for testing purposes only.
        """
        ...
    ...

