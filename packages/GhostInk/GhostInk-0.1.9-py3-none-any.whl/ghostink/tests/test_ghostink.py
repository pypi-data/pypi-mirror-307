import pytest
import os
import json
import logging
from ghostink import GhostInk


# Initial setup for testing the GhostInk class
@pytest.fixture
def ghostink_instance():
    return GhostInk(title="TestInstance", project_root="test_project", log_to_file=True)


# Teardown: clean up generated logs after tests
@pytest.fixture(scope="function", autouse=True)
def clean_up_logs():
    yield
    if os.path.exists("test_project/logs"):
        for file in os.listdir("test_project/logs"):
            os.remove(os.path.join("test_project/logs", file))
        os.rmdir("test_project/logs")


def test_initialization():
    ink = GhostInk(title="TestTitle", project_root="test_root")
    assert ink.title == "TestTitle"
    assert ink.project_root == "test_root"
    assert not ink.log_to_file  # default value
    assert ink.etches == set()


def test_haunt(capsys):
    ink = GhostInk()
    ink.haunt("Testing haunt message")
    captured = capsys.readouterr()
    assert "Testing haunt message" in captured.out
    assert "haunt" in captured.out


def test_inkdrop_basic(ghostink_instance):
    ghostink_instance.inkdrop("Simple test etch")
    assert any("Simple test etch" in etch[1] for etch in ghostink_instance.etches)


def test_inkdrop_dict_input(ghostink_instance):
    data = {"key": "value"}
    ghostink_instance.inkdrop(data)
    assert any(
        "key" in etch[1] and "value" in etch[1] for etch in ghostink_instance.etches
    )


def test_inkdrop_error_stacktrace(ghostink_instance):
    ghostink_instance.inkdrop("Error etch", shade=GhostInk.shade.ERROR)
    assert any("Stack Trace" in etch[1] for etch in ghostink_instance.etches)


def test_whisper(capsys, ghostink_instance):
    ghostink_instance.inkdrop("Debug message", shade=GhostInk.shade.DEBUG)
    ghostink_instance.inkdrop("Info message", shade=GhostInk.shade.INFO)
    ghostink_instance.whisper(shade_mask=GhostInk.shade.DEBUG)
    captured = capsys.readouterr()
    assert "Debug message" in captured.out
    assert "Info message" not in captured.out


def test_color_text(ghostink_instance):
    text = "Test"
    for shade in GhostInk.shade:
        colored_text = ghostink_instance._color_text(shade, text)
        assert text in colored_text  # Ensure the text is wrapped with color codes


def test_get_relative_path(ghostink_instance):
    path, line, func = ghostink_instance._get_relative_path()
    assert isinstance(path, str)
    assert isinstance(line, int)
    assert isinstance(func, str)


def test_format_etch_from_object(ghostink_instance):
    # Test with dict
    dict_input = {"key": "value"}
    formatted = ghostink_instance._format_etch_from_object(dict_input)
    assert '"key": "value"' in formatted

    # Test with list
    list_input = [1, 2, 3]
    formatted = ghostink_instance._format_etch_from_object(list_input)
    assert "[\n    1,\n    2,\n    3\n]" in formatted

    # Test with custom object
    class CustomObj:
        def __init__(self):
            self.attr = "test"

    obj_input = CustomObj()
    formatted = ghostink_instance._format_etch_from_object(obj_input)
    assert '"attr": "test"' in formatted


def test_format_echoes(ghostink_instance):
    echoes = ["tag1", " tag2", "#tag3"]
    formatted = ghostink_instance._format_echoes(echoes)
    assert "#tag1" in formatted
    assert "#tag2" in formatted
    assert "#tag3" not in formatted  # Excludes tags with `#`


def test_format_etch(ghostink_instance):
    etch_text = "Sample Etch"
    formatted = ghostink_instance._format_etch(
        GhostInk.shade.INFO, etch_text, "file.py", 10, "test_func", ["tag"]
    )
    assert "Sample Etch" in formatted
    assert "file.py" in formatted
    assert "(Ln:" in formatted
    assert "tag" in formatted


# TODO test for the logger

if __name__ == "__main__":
    pytest.main()
