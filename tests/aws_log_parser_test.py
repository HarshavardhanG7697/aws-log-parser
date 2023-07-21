from unittest.mock import patch

import pytest

from aws_log_parser.aws_log_parser import (log_dir_exists,
                                           log_file_in_current_dir, parse_logs)


@pytest.mark.parametrize(
    "service, expected",
    [
        ("incorrect_value", False),
        ("ce", True),
        ("drs", True),
        ("mgn", True),
    ],
)
def test_log_dir_exists(service, expected):
    with patch("aws_log_parser.aws_log_parser.os.path.exists", return_value=True):
        assert log_dir_exists(service) == expected


@pytest.mark.parametrize(
    "service, expected",
    [
        ("incorrect_value", False),
        ("ce", True),
        ("drs", True),
        ("mgn", True),
    ],
)
def test_log_file_in_current_dir(service, expected):
    with patch("aws_log_parser.aws_log_parser.os.path.exists", return_value=True):
        assert log_file_in_current_dir(service) == expected


@pytest.mark.skip(reason="TODO")
@pytest.mark.parametrize(
    "raw_log_line, expected",
    [
        ("raw_log_line", "expected"),
    ]
)
def test_parse_logs(raw_log_line, expected):
    assert parse_logs(raw_log_line) == expected
