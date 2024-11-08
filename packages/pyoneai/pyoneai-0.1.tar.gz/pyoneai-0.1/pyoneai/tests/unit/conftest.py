import pytest


class OneTestUtils:

    @staticmethod
    def equal_dicts(d1, d2, ignore_keys: str | list | None = None):
        """Evaluate if two dictionaries are equal ignoring some keys."""
        if isinstance(ignore_keys, str):
            ignore_keys = [ignore_keys]
        ignored = set(ignore_keys or [])
        for k1, v1 in d1.items():
            if k1 not in ignored and (k1 not in d2 or d2[k1] != v1):
                return False
        for k2 in d2.keys():
            if k2 not in ignored and k2 not in d1:
                return False
        return True


@pytest.fixture
def onet_utils():
    return OneTestUtils
