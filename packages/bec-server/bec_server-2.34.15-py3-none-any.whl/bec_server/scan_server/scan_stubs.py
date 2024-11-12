"""
Scan stubs are commands that can be used to control devices during a scan. They typically yield device messages that are
consumed by the scan worker and potentially forwarded to the device server.
"""

from __future__ import annotations

import threading
import time
import uuid
from collections.abc import Callable
from typing import Generator, Literal

import numpy as np

from bec_lib import messages
from bec_lib.connector import ConnectorBase
from bec_lib.device import Status
from bec_lib.endpoints import MessageEndpoints
from bec_lib.logger import bec_logger

from .errors import DeviceMessageError, ScanAbortion

logger = bec_logger.logger


class ScanStubs:
    """
    Scan stubs are commands that can be used to control devices during a scan. They typically yield device messages that are
    consumed by the scan worker and potentially forwarded to the device server.
    """

    def __init__(
        self,
        connector: ConnectorBase,
        device_msg_callback: Callable = None,
        shutdown_event: threading.Event = None,
    ) -> None:
        self.connector = connector
        self.device_msg_metadata = (
            device_msg_callback if device_msg_callback is not None else lambda: {}
        )
        self.shutdown_event = shutdown_event

    @staticmethod
    def _exclude_nones(input_dict: dict):
        for key in list(input_dict.keys()):
            if input_dict[key] is None:
                input_dict.pop(key)

    def _device_msg(self, **kwargs):
        """"""
        msg = messages.DeviceInstructionMessage(**kwargs)
        msg.metadata = {**self.device_msg_metadata(), **msg.metadata}
        return msg

    def send_rpc_and_wait(self, device: str, func_name: str, *args, **kwargs) -> any:
        """Perform an RPC (remote procedure call) on a device and wait for its return value.
        This method can be used to call any function on a device, irrespective of the
        function's USER ACCESS settings. The function will be called with the provided arguments
        and return the return value of the function. If the function returns a status object, the
        status object will be returned instead.

        Args:
            device (str): Name of the device
            func_name (str): Function name. The function name will be appended to the device.
            args (tuple): Arguments to pass on to the RPC function
            kwargs (dict): Keyword arguments to pass on to the RPC function

        Raises:
            ScanAbortion: Raised if the RPC's success is False

        Returns:
            any: Return value of the executed rpc function

        Examples:
            >>> send_rpc_and_wait("samx", "controller.my_custom_function")
        """
        rpc_id = str(uuid.uuid4())
        parameter = {
            "device": device,
            "func": func_name,
            "rpc_id": rpc_id,
            "args": args,
            "kwargs": kwargs,
        }
        yield from self.rpc(
            device=device, parameter=parameter, metadata={"response": True, "RID": rpc_id}
        )
        return self._get_from_rpc(rpc_id)

    def _get_from_rpc(self, rpc_id) -> any:
        """
        Get the return value from an RPC call.

        Args:
            rpc_id (str): RPC ID

        Raises:
            ScanAbortion: Raised if the RPC's success flag is False

        Returns:
            any: Return value of the RPC call
        """

        while not self.shutdown_event.is_set():
            msg = self.connector.get(MessageEndpoints.device_rpc(rpc_id))
            if msg:
                break
            time.sleep(0.001)
        if self.shutdown_event.is_set():
            raise ScanAbortion("The scan was aborted.")
        if not msg.content["success"]:
            error = msg.content["out"]
            if isinstance(error, dict) and {"error", "msg", "traceback"}.issubset(
                set(error.keys())
            ):
                error_msg = f"During an RPC, the following error occured:\n{error['error']}: {error['msg']}.\nTraceback: {error['traceback']}\n The scan will be aborted."
            else:
                error_msg = "During an RPC, an error occured"
            raise ScanAbortion(error_msg)

        logger.debug(msg.content.get("out"))
        return_val = msg.content.get("return_val")
        if not isinstance(return_val, dict):
            return return_val
        if return_val.get("type") == "status" and return_val.get("RID"):
            return Status(self.connector, return_val.get("RID"))
        return return_val

    def set_with_response(
        self, *, device: str, value: float, request_id: str = None, metadata=None
    ) -> Generator[None, None, None]:
        """Set a device to a specific value and return the request ID. Use :func:`request_is_completed` to later check if the request is completed.
        Use this method if you want to wait for the completion of a set operation whilst still being able to perform other operations on the same device.

        On the device server, `set_with_response` will call the `set` method of the device.

        Args:
            device (str): Device name.
            value (float): Target value.

        Returns:
            Generator[None, None, None]: Generator that yields a device message.

        see also: :func:`request_is_completed`

        """
        request_id = str(uuid.uuid4()) if request_id is None else request_id
        metadata = metadata if metadata is not None else {}
        metadata.update({"response": True, "RID": request_id})
        yield from self.set(device=device, value=value, wait_group="set", metadata=metadata)
        return request_id

    def request_is_completed(self, RID: str) -> bool:
        """Check if a request that was initiated with :func:`set_with_response` is completed.

        Args:
            RID (str): Request ID.

        Returns:
            bool: True if the request is completed, False otherwise.

        """
        msg = self.connector.lrange(MessageEndpoints.device_req_status_container(RID), 0, -1)
        if not msg:
            return False
        return True

    def set_and_wait(
        self, *, device: list[str], positions: list | np.ndarray
    ) -> Generator[None, None, None]:
        """Set devices to a specific position and wait completion.

        On the device server, `set_and_wait` will call the `set` method of the device.

        Args:
            device (list[str]): List of device names.
            positions (list | np.ndarray): Target position.

        Returns:
            Generator[None, None, None]: Generator that yields a device message.

        see also: :func:`set`, :func:`wait`, :func:`set_with_response`

        """
        if not isinstance(positions, list) and not isinstance(positions, np.ndarray):
            positions = [positions]
        if len(positions) == 0:
            return
        for ind, val in enumerate(device):
            yield from self.set(device=val, value=positions[ind], wait_group="scan_motor")
        yield from self.wait(device=device, wait_type="move", wait_group="scan_motor")

    def read_and_wait(
        self, *, wait_group: str, device: list = None, group: str = None, point_id: int = None
    ) -> Generator[None, None, None]:
        """Perform a reading and wait for completion.

        On the device server, `read_and_wait` will call the `read` method of the device.

        Args:
            wait_group (str): wait group
            device (list, optional): List of device names. Can be specified instead of group. Defaults to None.
            group (str, optional): Group name of devices. Can be specified instead of device. Defaults to None.
            point_id (int, optional): _description_. Defaults to None.

        Returns:
            Generator[None, None, None]: Generator that yields a device message.

        """
        self._check_device_and_groups(device, group)
        yield from self.read(device=device, group=group, wait_group=wait_group, point_id=point_id)
        yield from self.wait(device=device, wait_type="read", group=group, wait_group=wait_group)

    def open_scan(
        self,
        *,
        scan_motors: list,
        readout_priority: dict,
        num_pos: int,
        scan_name: str,
        scan_type: Literal["step", "fly"],
        positions=None,
        metadata=None,
    ) -> Generator[None, None, None]:
        """Open a new scan.

        Args:
            scan_motors (list): List of scan motors.
            readout_priority (dict): Modification of the readout priority.
            num_pos (int): Number of positions within the scope of this scan.
            positions (list): List of positions for this scan.
            scan_name (str): Scan name.
            scan_type (str): Scan type (e.g. 'step' or 'fly')

        Returns:
            Generator[None, None, None]: Generator that yields a device message.

        """
        yield self._device_msg(
            device=None,
            action="open_scan",
            parameter={
                "scan_motors": scan_motors,
                "readout_priority": readout_priority,
                "num_points": num_pos,
                "positions": positions,
                "scan_name": scan_name,
                "scan_type": scan_type,
            },
            metadata=metadata,
        )

    def kickoff(
        self, *, device: str, parameter: dict = None, wait_group="kickoff", metadata=None
    ) -> Generator[None, None, None]:
        """Kickoff a fly scan device.

        On the device server, `kickoff` will call the `kickoff` method of the device.

        Args:
            device (str): Device name of flyer.
            parameter (dict, optional): Additional parameters that should be forwarded to the device. Defaults to {}.

        Returns:
            Generator[None, None, None]: Generator that yields a device message.
        """
        parameter = parameter if parameter is not None else {}
        parameter = {"configure": parameter, "wait_group": wait_group}
        yield self._device_msg(
            device=device, action="kickoff", parameter=parameter, metadata=metadata
        )

    def complete(self, *, device: str, metadata=None) -> Generator[None, None, None]:
        """Complete a fly scan device.

        On the device server, `complete` will call the `complete` method of the device.

        Args:
            device (str): Device name of flyer.

        Returns:
            Generator[None, None, None]: Generator that yields a device message.
        """
        yield self._device_msg(device=device, action="complete", parameter={}, metadata=metadata)

    def get_req_status(self, device: str, RID: str, DIID: int) -> int:
        """Check if a device request status matches the given RID and DIID

        Args:
            device (str): device under inspection
            RID (str): request ID
            DIID (int): device instruction ID

        Returns:
            int: 1 if the request status matches the RID and DIID, 0 otherwise
        """
        msg = self.connector.get(MessageEndpoints.device_req_status(device))
        if not msg:
            return 0
        matching_RID = msg.metadata.get("RID") == RID
        matching_DIID = msg.metadata.get("DIID") == DIID
        if matching_DIID and matching_RID:
            return 1
        return 0

    def get_device_progress(self, device: str, RID: str) -> float | None:
        """Get reported device progress

        Args:
            device (str): Name of the device
            RID (str): request ID

        Returns:
            float: reported progress value

        """
        msg = self.connector.get(MessageEndpoints.device_progress(device))
        if not msg:
            return None
        matching_RID = msg.metadata.get("RID") == RID
        if not matching_RID:
            return None
        if not isinstance(msg, messages.ProgressMessage):
            raise DeviceMessageError(
                f"Expected to receive a Progressmessage for device {device} but instead received {msg}."
            )
        return msg.content["value"]

    def close_scan(self) -> Generator[None, None, None]:
        """
        Close the scan.

        Returns:
            Generator[None, None, None]: Generator that yields a device message.

        see also: :func:`open_scan`
        """

        yield self._device_msg(device=None, action="close_scan", parameter={})

    def stage(self) -> Generator[None, None, None]:
        """
        Stage all devices.

        On the device server, `stage` will call the `stage` method of the device.

        Returns:
            Generator[None, None, None]: Generator that yields a device message.

        see also: :func:`unstage`
        """
        yield self._device_msg(device=None, action="stage", parameter={})

    def unstage(self) -> Generator[None, None, None]:
        """
        Unstage all devices.

        On the device server, `unstage` will call the `unstage` method of the device.

        Returns:
            Generator[None, None, None]: Generator that yields a device message.

        see also: :func:`stage`
        """
        yield self._device_msg(device=None, action="unstage", parameter={})

    def pre_scan(self) -> Generator[None, None, None]:
        """
        Trigger pre-scan actions on all devices. Typically, pre-scan actions are called directly before the scan core starts and
        are used to perform time-critical actions.
        The event will be sent to all devices that have a pre_scan method implemented.

        On the device server, `pre_scan` will call the `pre_scan` method of the device, if implemented.

        Returns:
            Generator[None, None, None]: Generator that yields a device message.
        """
        yield self._device_msg(device=None, action="pre_scan", parameter={})

    def baseline_reading(self) -> Generator[None, None, None]:
        """
        Run the baseline readings. This will readout all devices that are marked with the readout_priority "baseline".

        On the device server, `baseline_reading` will call the `read` method of the device.

        Returns:
            Generator[None, None, None]: Generator that yields a device message.

        """
        yield self._device_msg(
            device=None,
            action="baseline_reading",
            parameter={},
            metadata={"readout_priority": "baseline"},
        )

    def wait(
        self,
        *,
        wait_type: Literal["move", "read", "trigger"],
        device: list[str] | str | None = None,
        group: Literal["scan_motor", "primary", None] = None,
        wait_group: str = None,
        wait_time: float = None,
    ):
        """Wait for an event.

        Args:
            wait_type (Literal["move", "read", "trigger"]): Type of wait event. Can be "move", "read" or "trigger".
            device (list[str] | str, optional): List of device names. Defaults to None.
            group (Literal["scan_motor", "primary", None]): Device group that can be used instead of device. Defaults to None.
                "scan_motor" is used to select the provided "scan_motors" of the scan. "primary" is used to select all monitored devices.
            wait_group (str, optional): Wait group for this event. Defaults to None. The specified wait group must match the wait group
                that was used in the corresponding trigger, read or set command, cf. :func:`read`, :func:`set`, :func:`trigger`.
            wait_time (float, optional): Wait time (for wait_type="trigger"). Defaults to None. The specified wait time is the minimum time
                the wait event will wait for the completion of the trigger. Additionally, the wait event will wait for the completion of the
                status events of the triggered devices.

        Returns:
            Generator[None, None, None]: Generator that yields a device message.

        Example:
            >>> yield from self.stubs.wait(wait_type="move", group="scan_motor", wait_group="scan_motor")
            >>> yield from self.stubs.wait(wait_type="read", group="scan_motor", wait_group="my_readout_motors")

        """
        self._check_device_and_groups(device, group)
        parameter = {"type": wait_type, "time": wait_time, "group": group, "wait_group": wait_group}
        self._exclude_nones(parameter)
        yield self._device_msg(device=device, action="wait", parameter=parameter)

    def read(
        self,
        *,
        wait_group: str,
        device: list[str] | str | None = None,
        point_id: int | None = None,
        group: Literal["scan_motor", "primary", None] = None,
    ) -> Generator[None, None, None]:
        """
        Perform a reading on a device or device group.

        On the device server, `read` will call the `read` method of the device.

        Args:
            wait_group (str): Wait group for this event. The specified wait group can later be used
                to wait for the completion of this event. Please note that the wait group has to be
                unique. within the scope of the read / wait event.
            device (list, optional): Device name. Can be used instead of group. Defaults to None.
            point_id (int, optional): point_id to assign this reading to point within the scan. Defaults to None.
            group (Literal["scan_motor", "primary", None], optional): Device group. Can be used instead of device. Defaults to None.

        Returns:
            Generator[None, None, None]: Generator that yields a device message.

        Example:
            >>> yield from self.stubs.read(wait_group="readout_primary", group="primary", point_id=self.point_id)
            >>> yield from self.stubs.read(wait_group="sample_stage", device="samx", point_id=self.point_id)

        """
        self._check_device_and_groups(device, group)
        parameter = {"group": group, "wait_group": wait_group}
        metadata = {"point_id": point_id}
        self._exclude_nones(parameter)
        self._exclude_nones(metadata)
        yield self._device_msg(device=device, action="read", parameter=parameter, metadata=metadata)

    def publish_data_as_read(
        self, *, device: str, data: dict, point_id: int
    ) -> Generator[None, None, None]:
        """
        Publish the given data as a read event and assign it to the given point_id.
        This method can be used to customize the assignment of data to a specific point within a scan.

        Args:
            device (str): Device name.
            data (dict): Data that should be published.
            point_id (int): point_id that should be attached to this data.

        Returns:
            Generator[None, None, None]: Generator that yields a device message.
        """
        metadata = {"point_id": point_id}
        yield self._device_msg(
            device=device,
            action="publish_data_as_read",
            parameter={"data": data},
            metadata=metadata,
        )

    def trigger(self, *, group: str, point_id: int) -> Generator[None, None, None]:
        """Trigger a device group. Note that the trigger event is not blocking and does not wait for the completion of the trigger event.
        To wait for the completion of the trigger event, use the :func:`wait` command, specifying the wait_type as "trigger".

        On the device server, `trigger` will call the `trigger` method of the device.

        Args:
            group (str): Device group that should receive the trigger.
            point_id (int): point_id that should be attached to this trigger event.

        Returns:
            Generator[None, None, None]: Generator that yields a device message.

        see also: :func:`wait`
        """
        yield self._device_msg(
            device=None,
            action="trigger",
            parameter={"group": group},
            metadata={"point_id": point_id},
        )

    def set(self, *, device: str, value: float, wait_group: str, metadata=None):
        """Set the device to a specific value. This is similar to the direct set command
        in the command-line interface. The wait_group can be used to wait for the completion of this event.
        For a set operation, this simply means that the device has acknowledged the set command and does not
        necessarily mean that the device has reached the target value.

        On the device server, `set` will call the `set` method of the device.

        Args:
            device (str): Device name
            value (float): Target value.
            wait_group (str): wait group for this event.

        Returns:
            Generator[None, None, None]: Generator that yields a device message.

        .. warning::

            Do not use this command to kickoff a long running operation. Use :func:`kickoff` instead or, if the
            device does not support the kickoff command, use :func:`set_with_response` instead.

        see also: :func:`wait`, :func:`set_and_wait`, :func:`set_with_response`

        """
        yield self._device_msg(
            device=device,
            action="set",
            parameter={"value": value, "wait_group": wait_group},
            metadata=metadata,
        )

    def open_scan_def(self) -> Generator[None, None, None]:
        """
        Open a new scan definition

        Returns:
            Generator[None, None, None]: Generator that yields a device message.
        """
        yield self._device_msg(device=None, action="open_scan_def", parameter={})

    def close_scan_def(self) -> Generator[None, None, None]:
        """
        Close a scan definition

        Returns:
            Generator[None, None, None]: Generator that yields a device message.
        """
        yield self._device_msg(device=None, action="close_scan_def", parameter={})

    def close_scan_group(self) -> Generator[None, None, None]:
        """
        Close a scan group

        Returns:
            Generator[None, None, None]: Generator that yields a device message.
        """
        yield self._device_msg(device=None, action="close_scan_group", parameter={})

    def rpc(self, *, device: str, parameter: dict, metadata=None) -> Generator[None, None, None]:
        """Perfrom an RPC (remote procedure call) on a device.
        Do not use this command directly. Instead, use :func:`send_rpc_and_wait` to perform an RPC and wait for its return value.

        Args:
            device (str): Device name.
            parameter (dict): parameters used for this rpc instructions.

        Returns:
            Generator[None, None, None]: Generator that yields a device message.

        """
        yield self._device_msg(device=device, action="rpc", parameter=parameter, metadata=metadata)

    def scan_report_instruction(self, instructions: dict) -> Generator[None, None, None]:
        """Scan report instructions

        Args:
            instructions (dict): Dict containing the scan report instructions

        Returns:
            Generator[None, None, None]: Generator that yields a device message.
        """
        yield self._device_msg(
            device=None, action="scan_report_instruction", parameter=instructions
        )

    def _check_device_and_groups(self, device, group) -> None:
        if device and group:
            raise DeviceMessageError("Device and device group was specified. Pick one.")
        if device is None and group is None:
            raise DeviceMessageError("Either devices or device groups have to be specified.")
