######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.29                                                                                #
# Generated on 2024-11-07T22:19:34.582314                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.runner.click_api
    import metaflow.runner.subprocess_manager
    import tempfile
    import typing


TYPE_CHECKING: bool

def get_current_cell(ipython):
    ...

def format_flowfile(cell):
    """
    Formats the given cell content to create a valid Python script that can be
    executed as a Metaflow flow.
    """
    ...

def check_process_status(command_obj: "metaflow.runner.subprocess_manager.CommandManager"):
    ...

def read_from_file_when_ready(file_path: str, command_obj: "metaflow.runner.subprocess_manager.CommandManager", timeout: float = 5):
    ...

def handle_timeout(tfp_runner_attribute: "tempfile._TemporaryFileWrapper[str]", command_obj: "metaflow.runner.subprocess_manager.CommandManager", file_read_timeout: int):
    """
    Handle the timeout for a running subprocess command that reads a file
    and raises an error with appropriate logs if a TimeoutError occurs.
    
    Parameters
    ----------
    tfp_runner_attribute : NamedTemporaryFile
        Temporary file that stores runner attribute data.
    command_obj : CommandManager
        Command manager object that encapsulates the running command details.
    file_read_timeout : int
        Timeout for reading the file.
    
    Returns
    -------
    str
        Content read from the temporary file.
    
    Raises
    ------
    RuntimeError
        If a TimeoutError occurs, it raises a RuntimeError with the command's
        stdout and stderr logs.
    """
    ...

def get_lower_level_group(api: "metaflow.runner.click_api.MetaflowAPI", top_level_kwargs: typing.Dict[str, typing.Any], sub_command: str, sub_command_kwargs: typing.Dict[str, typing.Any]) -> "metaflow.runner.click_api.MetaflowAPI":
    """
    Retrieve a lower-level group from the API based on the type and provided arguments.
    
    Parameters
    ----------
    api : MetaflowAPI
        Metaflow API instance.
    top_level_kwargs : Dict[str, Any]
        Top-level keyword arguments to pass to the API.
    sub_command : str
        Sub-command of API to get the API for
    sub_command_kwargs : Dict[str, Any]
        Sub-command arguments
    
    Returns
    -------
    MetaflowAPI
        The lower-level group object retrieved from the API.
    
    Raises
    ------
    ValueError
        If the `_type` is None.
    """
    ...

