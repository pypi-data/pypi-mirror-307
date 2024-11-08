import pytest
import yaml

from pyoneai import One, TimeIndex
from pyoneai.core import VirtualMachineState


class TestSKDIntegration:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.one = One()
        self.entity_dict = {
            "one": lambda **kwargs: self.one,
            "virtualmachine": lambda vm_id=None, **kwargs: self.one.vms[vm_id],
            "host": lambda host_id=None, **kwargs: self.one.hosts[host_id],
            "datastore": lambda ds_id=None, **kwargs: self.one.datastores[
                ds_id
            ],
        }
        self.pool_dict = {
            "virtualmachine": self.one.vms,
            "host": self.one.hosts,
            "datastore": self.one.datastores,
        }
        self.registry_data = self.read_registry()

    def read_registry(self):
        with open("/etc/one/aiops/registry.yaml", "r") as file:
            return yaml.safe_load(file)

    def test_metrics_available(
        self, entity, metric, time_range, expected_data, vm_id, host_id, ds_id
    ):
        parts = time_range.split(":")
        entity_ = self.entity_dict[entity](
            vm_id=vm_id, host_id=host_id, ds_id=ds_id
        )
        if parts.__len__() == 3:
            metrics = entity_.metrics[metric][parts[0] : parts[1] : parts[2]]
        else:
            metrics = entity_.metrics[metric][parts[0]]
        assert len(metrics) == expected_data

    def test_pool_metrics(self, time_range, expected_data):
        parts = time_range.split(":")
        errors = []
        for entity_str, metrics in self.registry_data.items():
            if entity_str in ("default", "one") or metrics is None:
                continue
            pool_ = self.pool_dict[entity_str]
            if entity_str == "virtualmachine":
                pool_ = pool_[
                    (pool_.metrics["state"]["0"] == VirtualMachineState.ACTIVE)
                ]
            for metric in metrics:
                if len(parts) == 3:
                    metric_data = pool_.metrics[metric][
                        parts[0] : parts[1] : parts[2]
                    ]
                else:
                    metric_data = pool_.metrics[metric][parts[0]]
                for k, v in metric_data:
                    if len(v) != expected_data:
                        errors.append(
                            f"Failed {entity_str} - {metric} - {time_range}"
                        )
                if len(metric_data) != len(pool_.ids):
                    errors.append(f"Failed{ entity_str} - {metric}:")
        if errors:
            raise AssertionError("Errors occurred:\n" + "\n".join(errors))

    def test_metrics_values(
        self, one_data, host_data, vm_data, ds_data, vm_id, host_id, ds_id
    ):
        one_metrics = ["oned_state", "scheduler_state", "flow_state"]
        for idx, metric in enumerate(one_metrics):
            metrics = self.one.metrics[metric]["0"].item()
            assert metrics == one_data[idx], f"Failed '{metric}' metric"
        host_metrics = ["cpu_maximum_ratio", "cpu_ratio", "state"]
        for idx, metric in enumerate(host_metrics):
            metrics = self.one.hosts[host_id].metrics[metric]["0"].item()
            assert metrics == host_data[idx], f"Failed '{metric}' metric"
        vm_metrics = ["lcm_state", "cpu_ratio", "cpu_vcpus", "mem_total_bytes"]
        for idx, metric in enumerate(vm_metrics):
            metrics = self.one.vms[vm_id].metrics[metric]["0"].item()
            assert metrics == vm_data[idx], f"Failed '{metric}' metric"
        ds_metrics = ["free_bytes", "used_bytes", "total_bytes"]
        for idx, metric in enumerate(ds_metrics):
            metrics = self.one.datastores[ds_id].metrics[metric]["0"].item()
            metrics = metrics / (1024 * 1024)
            assert metrics == ds_data[idx], f"Failed '{metric}' metric"

    def test_multivariate(self, vm_id, host_id, ds_id):
        time_ranges = [
            TimeIndex(slice("-3m", "0m", "1m")),
            TimeIndex(slice("-3m", "-1m", "1m")),
            TimeIndex(slice("+1m", "+3m", "1m")),
            TimeIndex(slice("0m", "+3m", "1m")),
            TimeIndex("0m"),
            TimeIndex("-1m"),
            TimeIndex("+1m"),
        ]
        for entity, metrics_list in self.registry_data.items():
            if entity == "default" or metrics_list is None:
                continue
            entity_ = self.entity_dict[entity](
                vm_id=vm_id, host_id=host_id, ds_id=ds_id
            )
            for time_range in time_ranges:
                current_metrics = entity_.metrics[metrics_list.keys()][
                    time_range
                ]
                df = current_metrics.to_dataframe()
                assert df.shape[1] == len(
                    metrics_list
                ), f"Failed '{entity}', time range '{time_range.values}'"
                assert (
                    not df.isnull().any().any()
                ), f"Failed entity {entity}, time range {time_range.values}."

    def test_latest_metrics(self, vm_id, host_id, ds_id):
        for entity_str, metrics in self.registry_data.items():
            # TODO: remove "one" when One has LatestMetricValues
            if entity_str in ("default", "one") or metrics is None:
                continue
            entity_ = self.entity_dict[entity_str](
                vm_id=vm_id, host_id=host_id, ds_id=ds_id
            )
            for metric_name in metrics:
                assert entity_.metrics[metric_name]["0"].item() == getattr(
                    entity_, metric_name
                )

    def test_vm_migration(self, vm_id, time_range, expected_data):
        parts = time_range.split(":")
        if parts.__len__() == 3:
            metrics = self.one.vms[vm_id].metrics["cpu_usage"][
                parts[0] : parts[1] : parts[2]
            ]
        else:
            metrics = self.one.vms[vm_id].metrics["cpu_usage"][parts[0]]
        assert expected_data == len(metrics)

    def test_vm_timestamps(self, vm_id):
        metrics = self.one.vms[vm_id].metrics["cpu_usage"]["-5m":"5m":"1m"]
        assert metrics.time_index.is_monotonic_increasing, "Not ordered"

    def test_vm_state(self, vm_id, state, expected_data):
        state_map = {
            "ACTIVE": VirtualMachineState.ACTIVE,
            "STOPPED": VirtualMachineState.STOPPED,
            "PENDING": VirtualMachineState.PENDING,
        }
        vm_list = self.one.vms[
            self.one.vms.metrics["state"]["0"] == state_map[state]
        ]
        assert len(vm_list._ids) == expected_data
        assert vm_id in vm_list._ids
