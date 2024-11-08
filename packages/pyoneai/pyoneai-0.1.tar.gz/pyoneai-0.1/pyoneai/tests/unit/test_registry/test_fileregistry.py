import os.path as osp

import pytest

from pyoneai.registry import FileRegistry


class TestFileRegistry:

    @pytest.fixture
    def sample_registry_file(self):
        yield osp.join(osp.dirname(__file__), "./data/sample_registry.yaml")

    @pytest.fixture
    def registry(self, sample_registry_file):
        yield FileRegistry(sample_registry_file)

    @pytest.fixture(autouse=True)
    def setup(self, mocker, sample_registry_file):
        with open(sample_registry_file, "r") as file:
            registry = file.read()
        mocker.patch("builtins.open", mocker.mock_open(read_data=registry))

    @pytest.mark.parametrize("path", ["missing.yaml", "missing.json"])
    def test_fail_on_missing_registry_file(self, path):
        with pytest.raises(
            FileNotFoundError, match=r"The registry file .* does not exist"
        ):
            _ = FileRegistry(path)

    def test_update_accessor_class_only(self, onet_utils, registry):
        prev_state = registry["virtualmachine"]["cpu_usage"]["accessor"]
        registry.update_accessor(
            entity="virtualmachine",
            metric="cpu_usage",
            model="some_pkg.DummyAccessor",
        )
        assert (
            registry["virtualmachine"]["cpu_usage"]["accessor"]["class"]
            == "some_pkg.DummyAccessor"
        )
        assert onet_utils.equal_dicts(
            prev_state,
            registry["virtualmachine"]["cpu_usage"]["accessor"],
            ignore_keys="class",
        )

    def test_update_accessor_class_and_args(self, onet_utils, registry):
        prev_state = registry["virtualmachine"]["cpu_usage"]["accessor"]
        registry.update_accessor(
            entity="virtualmachine",
            metric="cpu_usage",
            model="some_pkg.DummyAccessor",
            model_args=[1, 2, 3],
        )
        assert (
            registry["virtualmachine"]["cpu_usage"]["accessor"]["class"]
            == "some_pkg.DummyAccessor"
        )
        assert registry["virtualmachine"]["cpu_usage"]["accessor"]["args"] == [
            1,
            2,
            3,
        ]
        assert onet_utils.equal_dicts(
            prev_state,
            registry["virtualmachine"]["cpu_usage"]["accessor"],
            ignore_keys=["class", "args"],
        )

    def test_update_prediction_class_only(self, onet_utils, registry):
        prev_state = registry["virtualmachine"]["cpu_usage"]["prediction"]
        registry.update_prediction(
            entity="virtualmachine",
            metric="cpu_usage",
            model="some_pkg.DummyPredictor",
        )
        assert (
            registry["virtualmachine"]["cpu_usage"]["prediction"]["class"]
            == "some_pkg.DummyPredictor"
        )
        assert onet_utils.equal_dicts(
            prev_state,
            registry["virtualmachine"]["cpu_usage"]["prediction"],
            ignore_keys="class",
        )

    def test_update_prediction_class_and_args(self, onet_utils, registry):
        prev_state = registry["virtualmachine"]["cpu_usage"]["prediction"]
        registry.update_prediction(
            entity="virtualmachine",
            metric="cpu_usage",
            model="some_pkg.DummyPredictor",
            model_args=[1, 2, 3],
            model_kwargs={"key": "value"},
            path="some_path",
        )
        assert (
            registry["virtualmachine"]["cpu_usage"]["prediction"]["class"]
            == "some_pkg.DummyPredictor"
        )
        assert registry["virtualmachine"]["cpu_usage"]["prediction"][
            "args"
        ] == [1, 2, 3]
        assert registry["virtualmachine"]["cpu_usage"]["prediction"][
            "kwargs"
        ] == {"key": "value"}
        assert (
            registry["virtualmachine"]["cpu_usage"]["prediction"]["path"]
            == "some_path"
        )
        assert (
            prev_state["path"]
            != registry["virtualmachine"]["cpu_usage"]["prediction"]["path"]
        )
        assert (
            prev_state["args"]
            != registry["virtualmachine"]["cpu_usage"]["prediction"]["args"]
        )
        assert (
            prev_state["kwargs"]
            != registry["virtualmachine"]["cpu_usage"]["prediction"]["kwargs"]
        )
        assert (
            prev_state["class"]
            != registry["virtualmachine"]["cpu_usage"]["prediction"]["class"]
        )

    def test_reset(self, onet_utils, registry):
        prev_state = registry["virtualmachine"]["cpu_usage"]
        registry.update_prediction(
            entity="virtualmachine",
            metric="cpu_usage",
            model="some_pkg.DummyPredictor",
            model_args=[1, 2, 3],
            model_kwargs={"key": "value"},
            path="some_path",
        )
        registry.reset()
        assert onet_utils.equal_dicts(
            prev_state, registry["virtualmachine"]["cpu_usage"]
        )

    def test_fail_add_prediction_on_existing_metric(self, registry):
        with pytest.raises(ValueError, match=r"Prediction configuration *"):
            registry.add_prediction(
                entity="virtualmachine",
                metric="cpu_usage",
                model="some_pkg.DummyPredictor",
                model_args=[1, 2, 3],
                model_kwargs={"key": "value"},
                path="some_path",
            )

    def test_fail_add_derived_metric_on_existing_metric(self, registry):
        with pytest.raises(ValueError, match=r"Derived configuration *"):
            registry.add_derived(
                entity="virtualmachine",
                metric="cpu_usage",
                model="some_pkg.DummyPredictor",
                model_args=[1, 2, 3],
                model_kwargs={"key": "value"},
            )

    def test_fail_add_accessor_on_existing_metric(self, registry):
        with pytest.raises(ValueError, match=r"Accessor configuration *"):
            registry.add_accessor(
                entity="virtualmachine",
                metric="cpu_usage",
                model="some_pkg.DummyAccessor",
                model_args=[1, 2, 3],
            )

    def test_add_new_accessor_on_missing_metric(self, onet_utils, registry):
        registry.add_accessor(
            entity="virtualmachine",
            metric="new_metric",
            model="some_pkg.DummyAccessor",
            model_args=[1, 2, 3],
        )
        assert onet_utils.equal_dicts(
            registry["virtualmachine"]["new_metric"]["accessor"],
            {"class": "some_pkg.DummyAccessor", "args": [1, 2, 3]},
            ignore_keys="kwargs",
        )

    def test_add_new_derived_on_present_metric(self, onet_utils, registry):
        registry.add_accessor(
            entity="virtualmachine",
            metric="dummy_metric",
            model="some_pkg.DummyAccessor",
            model_args=[1, 2, 3],
        )
        registry.add_derived(
            entity="virtualmachine",
            metric="dummy_metric",
            model="some_pkg.DummyPredictor",
            model_args=[1, 2, 3],
            model_kwargs={"key": "value"},
        )
        assert onet_utils.equal_dicts(
            registry["virtualmachine"]["dummy_metric"]["derived"],
            {
                "class": "some_pkg.DummyPredictor",
                "args": [1, 2, 3],
                "kwargs": {"key": "value"},
            },
        )

    def test_add_new_prediction_on_present_metric(self, onet_utils, registry):
        registry.add_accessor(
            entity="virtualmachine",
            metric="dummy_metric",
            model="some_pkg.DummyAccessor",
            model_args=[1, 2, 3],
        )
        registry.add_prediction(
            entity="virtualmachine",
            metric="dummy_metric",
            model="some_pkg.DummyPredictor",
            model_args=[1, 2, 3],
            model_kwargs={"key": "value"},
            path="some_path",
        )
        assert onet_utils.equal_dicts(
            registry["virtualmachine"]["dummy_metric"]["prediction"],
            {
                "class": "some_pkg.DummyPredictor",
                "args": [1, 2, 3],
                "kwargs": {"key": "value"},
                "path": "some_path",
                "historical_period": None,
            },
        )
