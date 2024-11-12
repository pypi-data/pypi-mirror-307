from collections.abc import Callable

from bec_lib import messages
from bec_lib.alarm_handler import Alarms
from bec_lib.device import DeviceStatus
from bec_lib.endpoints import MessageEndpoints
from bec_lib.logger import bec_logger

from .errors import ScanAbortion

logger = bec_logger.logger


class DeviceValidation:
    """
    Mixin class for validation methods
    """

    def __init__(self, connector, worker):
        self.connector = connector
        self.worker = worker

    def get_device_status(self, endpoint: MessageEndpoints, devices: list) -> list:
        """
        Get the status of a list of devices

        Args:
            endpoint (MessageEndpoints): Message endpoint to use
            devices (list): List of devices

        Returns:
            list: List of BECMessage objects
        """
        pipe = self.connector.pipeline()
        for dev in devices:
            self.connector.get(endpoint(dev), pipe)
        return self.connector.execute_pipeline(pipe)

    def devices_are_ready(
        self,
        devices,
        endpoint,
        message_cls,
        metadata,
        checks: list[Callable] = None,
        print_status=False,
        **kwargs,
    ) -> bool:
        """Wait for devices to reach a certain state.

        Args:
            devices (list[str]): List of device IDs to wait for.
            endpoint (MessageEndpoints): Endpoint to check for device status.
            message_cls (BECMessage): Class of BECMessage to expect.
            metadata (dict): Metadata of the instruction.
            checks (list[Callable], optional): List of checks to perform on the device status. Defaults to None.

        Returns:
            bool: True if all checks are successful, False otherwise.
        """
        default_checks = [self.matching_scan_id, self.matching_DIID]
        if checks is None:
            checks = []
        checks = checks + default_checks
        if self.devices_returned_successfully in checks:
            checks.remove(self.devices_returned_successfully)
            run_status_checks = True
        else:
            run_status_checks = False

        device_status = self.get_device_status(endpoint, devices)
        self.worker._check_for_interruption()
        device_status = list(device_status)

        if None in device_status:
            return False

        device_msgs_are_correct = all(check(metadata, device_status, **kwargs) for check in checks)
        if not device_msgs_are_correct:
            if print_status:
                missing_devices = [
                    dev.content["device"]
                    for dev in device_status
                    if not all(
                        check(metadata, [dev], **kwargs) for check in checks + default_checks
                    )
                ]
                logger.info(f"Waiting for a status response of: {missing_devices}")
            return False
        if run_status_checks:
            return self.devices_returned_successfully(metadata, device_status, **kwargs)

        return True

    # pylint: disable=invalid-name
    def matching_scan_id(
        self, metadata: dict, response: list[messages.BECMessage], **kwargs
    ) -> bool:
        """
        Check if the scan_id in the response matches the scan_id in the instruction

        Args:
            metadata (dict): Metadata of the instruction
            response (list[messages.BECMessage]): List of BECMessage objects

        Returns:
            bool: True if the scan_id matches, False otherwise
        """
        return all(dev.metadata.get("scan_id") == metadata["scan_id"] for dev in response)

    # pylint: disable=invalid-name
    def matching_DIID(
        self,
        metadata: dict,
        response: list[messages.BECMessage],
        wait_group_devices: list = None,
        **kwargs,
    ) -> bool:
        """Check if the DIID in the response matches the DIID in the instruction

        Args:
            metadata (dict): Metadata of the instruction
            response (list[messages.BECMessage]): List of BECMessage objects

        Returns:
            bool: True if the DIID matches, False otherwise
        """
        if wait_group_devices is None:
            return all(dev.metadata.get("DIID") >= metadata["DIID"] for dev in response)
        return all(
            dev.metadata.get("DIID") >= wait_group_devices[ii][1] for ii, dev in enumerate(response)
        )

    def matching_requestID(
        self, metadata: dict, response: list[messages.BECMessage], **kwargs
    ) -> bool:
        """Check if the RID in the response matches the RID in the instruction

        Args:
            metadata (dict): Metadata of the instruction
            response (list[messages.BECMessage]): List of BECMessage objects

        Returns:
            bool: True if the RID matches, False otherwise
        """
        return all(dev.metadata.get("RID") == metadata["RID"] for dev in response)

    def devices_returned_successfully(
        self,
        metadata: dict,
        response: list[messages.BECMessage],
        wait_group_devices=None,
        instruction=None,
        **kwargs,
    ) -> bool:
        """Check if all devices returned successfully

        Args:
            response (list[messages.BECMessage]): List of BECMessage objects

        Returns:
            bool: True if all devices moved successfully, False otherwise
        """
        moved_successfully = all(dev.content.get("success") for dev in response)
        if moved_successfully:
            return True

        if instruction:
            return self.worker._check_for_failed_movements(
                response, wait_group_devices, instruction
            )

        # get the first device msg that failed
        failed_device = next(dev for dev in response if not dev.content.get("success"))
        self.connector.raise_alarm(
            severity=Alarms.MAJOR,
            source=failed_device.content,
            msg=(
                f"Device {failed_device.device} returned unsuccessfully on {failed_device.metadata.get('action')}."
            ),
            alarm_type="DeviceError",
            metadata=failed_device.metadata,
        )
        raise ScanAbortion

    def devices_are_staged(
        self, metadata: dict, response: list[messages.BECMessage], **kwargs
    ) -> bool:
        """Check if all devices moved successfully

        Args:
            response (list[messages.BECMessage]): List of BECMessage objects

        Returns:
            bool: True if all devices moved successfully, False otherwise
        """
        return all(bool(dev.content.get("status")) == True for dev in response)

    def devices_are_unstaged(
        self, metadata: dict, response: list[messages.BECMessage], **kwargs
    ) -> bool:
        """Check if all devices moved successfully

        Args:
            response (list[messages.BECMessage]): List of BECMessage objects

        Returns:
            bool: True if all devices moved successfully, False otherwise
        """
        return all(bool(dev.content.get("status")) == False for dev in response)

    def devices_are_idle(
        self, metadata: dict, response: list[messages.BECMessage], **kwargs
    ) -> bool:
        """Check if all devices are idle

        Args:
            response (list[messages.BECMessage]): List of BECMessage objects

        Returns:
            bool: True if all devices are idle, False otherwise
        """
        return all(DeviceStatus(dev.content.get("status")) == DeviceStatus.IDLE for dev in response)
