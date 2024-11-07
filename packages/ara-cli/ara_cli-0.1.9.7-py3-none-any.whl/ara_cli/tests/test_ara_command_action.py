import pytest
from unittest.mock import patch

from ara_cli.ara_command_action import read_action


class MockArgs:
    def __init__(self, classifier, parameter, branch):
        self.classifier = classifier
        self.parameter = parameter
        self.branch = branch


@pytest.fixture
def mock_classifier():
    with patch('ara_cli.classifier.Classifier') as mock:
        yield mock


@pytest.fixture
def mock_artefact_reader():
    with patch('ara_cli.artefact_reader.ArtefactReader') as mock:
        yield mock


@pytest.mark.parametrize("content, file_path, expected_print", [
    ("content", "/path/to/file", True),
    (None, None, False),
])
def test_read_action_no_branch(mock_artefact_reader, mock_classifier, content, file_path, expected_print, capsys):
    mock_artefact_reader.read_artefact.return_value = (content, file_path)
    mock_classifier.get_artefact_title.return_value = "TestTitle"

    args = MockArgs(classifier='test_classifier', parameter='test_parameter', branch=False)

    read_action(args)

    captured = capsys.readouterr()
    if expected_print:
        assert " - TestTitle /path/to/file:\ncontent\n" in captured.out
    else:
        assert captured.out == ""


@pytest.mark.parametrize("content, file_path, name, title, recursive_called", [
    ("content", "/path/to/file", "name", "title", True),
    ("content", "/path/to/file", None, None, False),
])
def test_read_action_with_branch(mock_artefact_reader, mock_classifier, content, file_path, name, title, recursive_called):
    mock_artefact_reader.read_artefact.return_value = (content, file_path)
    mock_classifier.get_artefact_title.return_value = "TestTitle"
    mock_artefact_reader.extract_parent_tree.return_value = (name, title)
    mock_classifier.get_artefact_classifier.return_value = "new_classifier"

    args = MockArgs(classifier='test_classifier', parameter='test_parameter', branch=True)

    with patch('ara_cli.ara_command_action.read_action') as mock_read_action:
        read_action(args)

        if recursive_called:
            assert mock_read_action.call_count == 1
            assert args.parameter == "_".join(name.split())
            assert args.classifier == "new_classifier"
        else:
            assert mock_read_action.call_count == 0
