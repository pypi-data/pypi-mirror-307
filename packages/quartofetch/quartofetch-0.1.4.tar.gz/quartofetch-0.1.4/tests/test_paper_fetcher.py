"""Tests for Quarto Paper Fetcher."""

import pytest
from pathlib import Path
import tempfile
import yaml
from unittest.mock import patch
import subprocess

from quartofetch.paper_manager import Paper, PaperManager
from quartofetch.quarto_project import QuartoProject
from quartofetch.exceptions import GitTimeoutError, ConfigurationError


# Fixtures
@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_paper():
    """Create a sample paper configuration."""
    return Paper(
        repo_url="https://github.com/user/repo",
        target_folder="paper1",
        branch="main",
    )


@pytest.fixture
def quarto_yml():
    """Create a sample Quarto configuration."""
    return {
        "project": {"type": "manuscript"},
        "manuscript": {
            "article": "paper.qmd",
            "notebooks": ["./notebook1.ipynb", "./notebook2.ipynb"],
        },
    }


@pytest.fixture
def mock_subprocess():
    """Mock subprocess for git operations."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "abcdef123456\n"
        yield mock_run


# Paper Tests
class TestPaper:
    def test_paper_creation(self):
        """Test paper creation from valid data."""
        data = {
            "repo_url": "https://github.com/user/repo",
            "target_folder": "paper1",
            "branch": "main",
        }
        paper = Paper.from_dict(data)
        assert paper is not None
        assert paper.repo_url == data["repo_url"]
        assert paper.target_folder == data["target_folder"]
        assert paper.branch == data["branch"]

    def test_invalid_paper_data(self):
        """Test paper creation with invalid data."""
        invalid_data = {"repo_url": "https://github.com/user/repo"}
        paper = Paper.from_dict(invalid_data)
        assert paper is None


# PaperManager Tests
class TestPaperManager:
    def test_validate_paper(self, sample_paper):
        """Test paper validation."""
        manager = PaperManager()
        manager._validate_paper(sample_paper)  # Should not raise

    def test_validate_paper_invalid_path(self):
        """Test paper validation with invalid path."""
        manager = PaperManager()
        paper = Paper(
            repo_url="https://github.com/user/repo", target_folder="../invalid"
        )
        with pytest.raises(ConfigurationError):
            manager._validate_paper(paper)

    @patch("subprocess.run")
    def test_get_commit(self, mock_run, sample_paper):
        """Test getting commit hash."""
        mock_run.return_value.stdout = "abcdef123456 HEAD\n"
        manager = PaperManager()
        commit = manager._get_commit(sample_paper.repo_url, "HEAD")
        assert commit == "abcdef123456"

    @patch("subprocess.run")
    def test_get_commit_timeout(self, mock_run, sample_paper):
        """Test commit hash timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired(cmd=[], timeout=30)
        manager = PaperManager()
        with pytest.raises(GitTimeoutError):
            manager._get_commit(sample_paper.repo_url, "HEAD")

    def test_process_paper(self, temp_dir, mock_subprocess, sample_paper):
        """Test processing a paper."""
        manager = PaperManager()
        with patch.object(manager, "_copy_files"):
            assert manager.process(sample_paper) is True


# QuartoProject Tests
class TestQuartoProject:
    def test_load_config(self, temp_dir, quarto_yml):
        """Test loading Quarto config."""
        config_path = temp_dir / "_quarto.yml"
        config_path.write_text(yaml.dump(quarto_yml))

        project = QuartoProject(temp_dir)
        assert project.config == quarto_yml

    def test_find_main_doc(self, temp_dir):
        """Test finding main document."""
        (temp_dir / "paper.qmd").touch()
        project = QuartoProject(temp_dir)
        assert project.main_doc == Path("paper.qmd")

    def test_get_files(self, temp_dir, quarto_yml):
        """Test getting project files."""
        # Setup test files
        config_path = temp_dir / "_quarto.yml"
        config_path.write_text(yaml.dump(quarto_yml))
        (temp_dir / "paper.qmd").touch()
        (temp_dir / "references.bib").touch()

        project = QuartoProject(temp_dir)
        files = project.get_files()

        assert Path("_quarto.yml") in files["standard"]
        assert Path("paper.qmd") in files["standard"]
        assert Path("references.bib") in files["standard"]


# Integration Tests
class TestIntegration:
    def test_full_paper_processing(self, temp_dir, mock_subprocess):
        """Test full paper processing workflow."""
        # Setup test environment
        config_path = "./_paper_sources.yml"

        # Run CLI
        from quartofetch.cli import CLI

        cli = CLI()
        with patch("sys.argv", ["qpf", "--config", str(config_path)]):
            with patch("os.getenv", return_value="TRUE"):
                result = cli.run()
                assert result == 1

    def test_missing_env_var(self, temp_dir):
        """Test exit for partial quarto render."""
        config_path = "./_paper_sources.yml"

        from quartofetch.cli import CLI

        cli = CLI()
        with patch("sys.argv", ["qpf", "--config", str(config_path)]):
            with patch("os.getenv", return_value=None):
                result = cli.run()
                assert result == 0
