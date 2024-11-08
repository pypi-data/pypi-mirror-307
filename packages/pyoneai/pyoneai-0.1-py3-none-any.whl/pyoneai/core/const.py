from .virtual_machine import VirtualMachineLCMState

FAIL_LCM_STATES = {
    VirtualMachineLCMState.BOOT_FAILURE,
    VirtualMachineLCMState.BOOT_MIGRATE_FAILURE,
    VirtualMachineLCMState.PROLOG_MIGRATE_FAILURE,
    VirtualMachineLCMState.PROLOG_FAILURE,
    VirtualMachineLCMState.EPILOG_FAILURE,
    VirtualMachineLCMState.EPILOG_STOP_FAILURE,
    VirtualMachineLCMState.EPILOG_UNDEPLOY_FAILURE,
    VirtualMachineLCMState.PROLOG_MIGRATE_POWEROFF_FAILURE,
    VirtualMachineLCMState.PROLOG_MIGRATE_SUSPEND_FAILURE,
    VirtualMachineLCMState.PROLOG_UNDEPLOY_FAILURE,
    VirtualMachineLCMState.BOOT_STOPPED_FAILURE,
    VirtualMachineLCMState.PROLOG_RESUME_FAILURE,
    VirtualMachineLCMState.PROLOG_UNDEPLOY_FAILURE,
    VirtualMachineLCMState.PROLOG_MIGRATE_UNKNOWN_FAILURE,
}
