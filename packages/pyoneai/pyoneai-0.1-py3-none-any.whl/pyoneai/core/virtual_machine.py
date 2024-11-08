from __future__ import annotations

__all__ = [
    "VirtualMachineState",
    "VirtualMachineLCMState",
    "VirtualMachineMigration",
    "VirtualMachine",
    "VirtualMachinePool",
]

import enum
import inspect
import xml.etree.ElementTree as ET
from typing import Any, SupportsInt

# TODO: # We need to make this error public.
from pyoneai.drivers.xmlrpc import _OneXMLRPCError

from ..session import Session
from . import host
from .bases import Entity, LatestMetricValue, Pool
from .errors import VMMethodError
from .group import Group
from .user import User


@enum.unique
class VirtualMachineState(enum.IntEnum):
    # For more information, see:
    # https://docs.opennebula.io/6.8/integration_and_development/references/vm_states.html
    INIT = 0
    PENDING = 1
    HOLD = 2
    ACTIVE = 3
    STOPPED = 4
    SUSPENDED = 5
    DONE = 6
    POWEROFF = 8
    UNDEPLOYED = 9
    CLONING = 10
    CLONING_FAILURE = 11


@enum.unique
class VirtualMachineLCMState(enum.IntEnum):
    # For more information, see:
    # https://docs.opennebula.io/6.8/integration_and_development/references/vm_states.html
    LCM_INIT = 0
    PROLOG = 1
    BOOT = 2
    RUNNING = 3
    MIGRATE = 4
    SAVE_STOP = 5
    SAVE_SUSPEND = 6
    SAVE_MIGRATE = 7
    PROLOG_MIGRATE = 8
    PROLOG_RESUME = 9
    EPILOG_STOP = 10
    EPILOG = 11
    SHUTDOWN = 12
    CLEANUP_RESUBMIT = 15
    UNKNOWN = 16
    HOTPLUG = 17
    SHUTDOWN_POWEROFF = 18
    BOOT_UNKNOWN = 19
    BOOT_POWEROFF = 20
    BOOT_SUSPENDED = 21
    BOOT_STOPPED = 22
    CLEANUP_DELETE = 23
    HOTPLUG_SNAPSHOT = 24
    HOTPLUG_NIC = 25
    HOTPLUG_SAVEAS = 26
    HOTPLUG_SAVEAS_POWEROFF = 27
    HOTPLUG_SAVEAS_SUSPENDED = 28
    SHUTDOWN_UNDEPLOY = 29
    EPILOG_UNDEPLOY = 30
    PROLOG_UNDEPLOY = 31
    BOOT_UNDEPLOY = 32
    HOTPLUG_PROLOG_POWEROFF = 33
    HOTPLUG_EPILOG_POWEROFF = 34
    BOOT_MIGRATE = 35
    BOOT_FAILURE = 36
    BOOT_MIGRATE_FAILURE = 37
    PROLOG_MIGRATE_FAILURE = 38
    PROLOG_FAILURE = 39
    EPILOG_FAILURE = 40
    EPILOG_STOP_FAILURE = 41
    EPILOG_UNDEPLOY_FAILURE = 42
    PROLOG_MIGRATE_POWEROFF = 43
    PROLOG_MIGRATE_POWEROFF_FAILURE = 44
    PROLOG_MIGRATE_SUSPEND = 45
    PROLOG_MIGRATE_SUSPEND_FAILURE = 46
    BOOT_UNDEPLOY_FAILURE = 47
    BOOT_STOPPED_FAILURE = 48
    PROLOG_RESUME_FAILURE = 49
    PROLOG_UNDEPLOY_FAILURE = 50
    DISK_SNAPSHOT_POWEROFF = 51
    DISK_SNAPSHOT_REVERT_POWEROFF = 52
    DISK_SNAPSHOT_DELETE_POWEROFF = 53
    DISK_SNAPSHOT_SUSPENDED = 54
    DISK_SNAPSHOT_REVERT_SUSPENDED = 55
    DISK_SNAPSHOT_DELETE_SUSPENDED = 56
    DISK_SNAPSHOT = 57
    DISK_SNAPSHOT_DELETE = 59
    PROLOG_MIGRATE_UNKNOWN = 60
    PROLOG_MIGRATE_UNKNOWN_FAILURE = 61
    DISK_RESIZE = 62
    DISK_RESIZE_POWEROFF = 63
    DISK_RESIZE_UNDEPLOYED = 64
    HOTPLUG_NIC_POWEROFF = 65
    HOTPLUG_RESIZE = 66
    HOTPLUG_SAVEAS_UNDEPLOYED = 67
    HOTPLUG_SAVEAS_STOPPED = 68
    BACKUP = 69
    BACKUP_POWEROFF = 70


@enum.unique
class VirtualMachineMigration(enum.IntEnum):
    SAVE = 0
    POWEROFF = 1
    POWEROFF_HARD = 2


class VirtualMachine(Entity):
    __slots__ = ("_pci_devices", "_scheduling")

    def __init__(self, session: Session, id: int) -> None:
        super().__init__(session=session, id=id)
        self._pci_devices: list[dict[str, str]] | None = None
        self._scheduling: host.HostPool | None = None

    @property
    def pci_devices(self) -> list[dict[str, str]]:
        if self._pci_devices is None:
            if data := self.get_data()["TEMPLATE"].get("PCI"):
                self._pci_devices = data if isinstance(data, list) else [data]
            else:
                self._pci_devices = []
        return self._pci_devices

    @property
    def scheduling_requirements(self) -> host.HostPool:
        if self._scheduling is None:
            if (user_template := self.get_data().get("USER_TEMPLATE")) and (
                sched_reqs := user_template.get("SCHED_REQUIREMENTS")
            ):
                reqs = sched_reqs.split("|")
                ids = {int(req.strip().split("=")[1][1:-1]) for req in reqs}
            else:
                # TODO: Add support for `AUTOMATIC_REQUIREMENTS`.
                ids = set()
            self._scheduling = host.HostPool(owner=self, ids=ids)
        return self._scheduling

    cpu_ratio = LatestMetricValue(float)
    cpu_seconds_total = LatestMetricValue(float)
    cpu_usage = LatestMetricValue(float)
    cpu_vcpus = LatestMetricValue(float)
    mem_total_bytes = LatestMetricValue(float)
    disk_size_bytes = LatestMetricValue(float)
    # disks = LatestMetricValue()
    # nics = LatestMetricValue()
    host_id = LatestMetricValue(int)
    state = LatestMetricValue(VirtualMachineState)
    lcm_state = LatestMetricValue(VirtualMachineLCMState)

    @property
    def user(self) -> User:
        uid = int(self.get_data(decrypt_secrets=False)["UID"])
        return User(id=uid, session=self.session)

    @property
    def group(self) -> Group:
        guid = int(self.get_data(decrypt_secrets=False)["GID"])
        return Group(id=guid, session=self.session)

    def get_info(self, decrypt_secrets: bool = False) -> str:
        client = self.session.oned_client
        response = client.request("one.vm.info", self.id, decrypt_secrets)
        return response

    def get_data(self, decrypt_secrets: bool = False) -> dict[str, Any]:
        client = self.session.oned_client
        data = client("one.vm.info", self.id, decrypt_secrets)
        return data["VM"]

    # TODO: Reconsider the names of the parameters and decide on their
    # default values.
    def migrate(
        self,
        host: host.Host | SupportsInt,
        live: bool = False,
        data_store: SupportsInt = -1,
        kind: VirtualMachineMigration = VirtualMachineMigration.SAVE,
        overcommit: bool = False,
    ) -> int:
        """Migrate a virtual machine.

        Migrates the running virtual machine to a new host. The VM's
        storage can also be migrated to a different datastore.

        Parameters
        ----------
        host : Host or SupportsInt
            The target host where the VM will be migrated.
        live : bool, default=False
            Allows live migration (without downtime). If not, the VM
            will be powered off and resumed on the new host.
        data_store : SupportsInt, default=-1
            The datastore ID where the VM's storage will be migrated.
            It is optional, can let OpenNebula choose the datastore.
        kind : VirtualMachineMigration, default=SAVE
            Migration type: SAVE (0), POWEROFF (1), POWEROFF_HARD (2).
        overcommit : bool, default=False
            Allows overcommitting the resources even if the host does
            not have enough capacity.

        Returns
        -------
        int
            The result of the migration operation.

        Raises
        ------
        VMMethodError
            If the migration action fails when calling the OneD client.
        """
        from pyoneai.core.host import Host

        return self._handle_vm_action(
            "one.vm.migrate",
            self.id,
            host.id if isinstance(host, Host) else int(host),
            bool(live),
            not bool(overcommit),
            int(data_store),
            VirtualMachineMigration(kind).value,
        )

    def terminate(self, hard: bool = False) -> None:
        """Terminate a virtual machine.

        Terminates the given virtual machine, ending its lifecycle.

        Parameters
        ----------
        hard : bool, default=False
            A hard option immediately terminates the virtual machine,
            without sending the ACPI signal.

        Raises
        ------
        VMMethodError
            If the action fails when calling the OneD client.
        """
        action = "terminate-hard" if hard else "terminate"
        self._handle_vm_action("one.vm.action", action, self.id)

    def undeploy(self, hard: bool = False) -> None:
        """Undeploy a virtual machine.

        Shuts down the given virtual machine and saves it in the
        system datastore.

        Parameters
        ----------
        hard : bool, default=False
            A hard option immediately destroys the virtual machine,
            without sending the ACPI signal.

        Raises
        ------
        VMMethodError
            If the action fails when calling the OneD client.
        """

        action = "undeploy-hard" if hard else "undeploy"
        self._handle_vm_action("one.vm.action", action, self.id)

    def poweroff(self, hard: bool = False) -> None:
        """Power off a virtual machine.

        Powers off the given virtual machine, without saving the VM
        state.

        Parameters
        ----------
        hard : bool, default=False
            A hard option immediately power offs the virtual machine,
            without sending the ACPI signal.

        Raises
        ------
        VMMethodError
            If the action fails when calling the OneD client.
        """

        action = "poweroff-hard" if hard else "poweroff"
        self._handle_vm_action("one.vm.action", action, self.id)

    def reboot(self, hard: bool = False) -> None:
        """Reboot a virtual machine.

        Reboots the given virtual machine sending the ACPI signal.

        Parameters
        ----------
        hard : bool, default=False
            A hard option immediately restarts the virtual machine,
            without sending the ACPI signal.

        Raises
        ------
        VMMethodError
            If the action fails when calling the OneD client.
        """
        action = "reboot-hard" if hard else "reboot"
        self._handle_vm_action("one.vm.action", action, self.id)

    def hold(self) -> None:
        """Hold a virtual machine.

        Sets the given virtual machine on hold, preventing it from
        being scheduled until it is released.

        Raises
        ------
        VMMethodError
            If the action fails when calling the OneD client.
        """
        self._handle_vm_action("one.vm.action", "hold", self.id)

    def release(self) -> None:
        """Release a virtual machine from hold.

        Releases the virtual machine from the hold state, allowing
        the virtual machine to be scheduled.

        Raises
        ------
        VMMethodError
            If the action fails when calling the OneD client.
        """
        self._handle_vm_action("one.vm.action", "release", self.id)

    def stop(self) -> None:
        """Stop a virtual machine.

        Stops a running virtual machine and transfers its state and
        disk fles back to the system datastore.

        Raises
        ------
        VMMethodError
            If the action fails when calling the OneD client.
        """
        self._handle_vm_action("one.vm.action", "stop", self.id)

    def suspend(self) -> None:
        """Suspend a virtual machine.

        Saves the state of a running virtual machine on the remote host
        for later resumption without freeing resources.

        Raises
        ------
        VMMethodError
            If the action fails when calling the OneD client.
        """
        self._handle_vm_action("one.vm.action", "suspend", self.id)

    def resume(self) -> None:
        """Resume a virtual machine.

        Resumes the execution of a saved virtual machine (undeploy,
        suspend, stop and poweroff), returning it to a running state.

        Raises
        ------
        VMMethodError
            If the action fails when calling the OneD client.
        """
        self._handle_vm_action("one.vm.action", "resume", self.id)

    def resched(self) -> None:
        """Reschedule a virtual machine.

        Sets the rescheduling flag for the virtual machine.

        Raises
        ------
        VMMethodError
            If the action fails when calling the OneD client.
        """
        self._handle_vm_action("one.vm.action", "resched", self.id)

    def unresched(self) -> None:
        """Clear the rescheduling flag for a virtual machine.

        Clears the rescheduling flag, preventing future rescheduling.

        Raises
        ------
        VMMethodError
            If the action fails when calling the OneD client.
        """
        self._handle_vm_action("one.vm.action", "unresched", self.id)

    def rename(self, name: str) -> None:
        """Rename a virtual machine.

        Changes the name of the virtual machine.

        Parameters
        ----------
        name : str
            The new name of the virtual machine.

        Raises
        ------
        VMMethodError
            If the action fails when calling the OneD client.
        """
        self._handle_vm_action("one.vm.rename", self.id, str(name))

    def recover(self, operation: SupportsInt) -> None:
        """Recover a virtual machine.

        Recovers a virtual machine stuck in an operation, either by
        retrying, failing, or succeeding the current operation.

        Parameters
        ----------
        operation : SupportsInt
            Recovery operation: 0 (failure), 1 (success), 2 (retry),
            3 (delete), 4 (delete and recreate), 5 (delete from DB).

        Raises
        ------
        VMMethodError
            If the action fails when calling the OneD client.
        """
        self._handle_vm_action("one.vm.recover", self.id, int(operation))

    def lock(self, level: SupportsInt) -> None:
        """Lock a virtual machine.

        Locks a virtual machine to prevent certain actions.
        The level of the lock determines the actions that are blocked.

        Parameters
        ----------
        level : SupportsInt
            Lock level: 1 (use), 2 (manage), 3 (admin), 4 (all).

        Raises
        ------
        VMMethodError
            If the action fails when calling the OneD client.
        """
        self._handle_vm_action("one.vm.lock", self.id, int(level))

    def unlock(self) -> None:
        """Unlock a virtual machine.

        Unlocks the given virtual machine, allowing previously
        restricted actions.

        Raises
        ------
        VMMethodError
            If the action fails when calling the OneD client.
        """
        self._handle_vm_action("one.vm.unlock", self.id)

    def resize(
        self,
        cpu: SupportsInt,
        vcpu: SupportsInt,
        memory: SupportsInt,
        overcommit: bool = False,
    ) -> None:
        """Resize a virtual machine.

        Resizes the virtual machine's CPU, VCPU and memory resources.

        Parameters
        ----------
        cpu : SupportsInt
            The amount of CPU resources to allocate.
        vcpu : SupportsInt
            The number of virtual CPUs (VCPU) to allocate.
        memory : SupportsInt
            The amount of memory (in MB) to allocate.
        overcommit : bool, default=False
            Allows overcommitting the resources even if the host does
            not have enough capacity.

        Raises
        ------
        VMMethodError
            If the resize action fails when calling the OneD client.
        """
        # TODO: change it with VM Template Data Model
        root = ET.Element("TEMPLATE")
        ET.SubElement(root, "CPU").text = str(int(cpu))
        ET.SubElement(root, "VCPU").text = str(int(vcpu))
        ET.SubElement(root, "MEMORY").text = str(int(memory))
        template = ET.tostring(root, encoding="unicode")
        self._handle_vm_action(
            "one.vm.resize", self.id, template, not bool(overcommit)
        )

    def _handle_vm_action(self, action: str, *args):
        try:
            return self.session.oned_client(action, *args)
        except _OneXMLRPCError as error:
            # Get the name of the method that failed
            method = inspect.currentframe().f_back.f_code.co_name
            raise VMMethodError(
                f"Virtual Machine method '{method}' failed.\nMessage: {error}"
            ) from error


class VirtualMachinePool(Pool):
    __slots__ = ()

    def _get_system_ids(self) -> set[int]:
        from pyoneai.core.host import Host

        client = self.session.oned_client
        # Get VMs from the owner host
        if isinstance(self.owner, Host):
            data = client("one.host.info", self.owner_id)["HOST"]["VMS"]
            if data is None:
                return set()
            return {int(id_) for id_ in data["ID"]}
        # Get all system VMs
        else:
            data = client("one.vmpool.info", -2, -1, -1, -2)["VM_POOL"]["VM"]
            if not isinstance(data, list):
                return {int(data["ID"])}
            return {int(entity_data["ID"]) for entity_data in data}

    def _get_entity(self, id: int) -> VirtualMachine:
        return VirtualMachine(session=self.session, id=id)
