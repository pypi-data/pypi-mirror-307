"""Paper management and processing logic."""

import subprocess
import tempfile
import shutil
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from contextlib import contextmanager
from loguru import logger

from .quarto_project import QuartoProject
from .logging_config import stage, substage
from .exceptions import (
    GitError,
    GitTimeoutError,
    GitAuthenticationError,
    ConfigurationError,
)


@dataclass
class Paper:
    """Paper source configuration."""

    repo_url: str
    target_folder: str
    branch: Optional[str] = None
    commit: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> Optional["Paper"]:
        """Create a Paper instance from a dictionary."""
        try:
            return (
                cls(
                    **{k: data[k] for k in ["repo_url", "target_folder"] if k in data},
                    **{k: data[k] for k in ["branch", "commit"] if k in data},
                )
                if all(k in data for k in ["repo_url", "target_folder"])
                else None
            )
        except (KeyError, TypeError) as e:
            logger.error(f"Invalid paper configuration: {e}")
            return None


class PaperManager:
    """Manages paper fetching and processing."""

    def __init__(self, force_update: bool = False, timeout: int = 300):
        self.force_update = force_update
        self.timeout = timeout

    @contextmanager
    def _temporary_directory(self):
        """Safely manage temporary directory with proper cleanup."""
        temp_dir = tempfile.mkdtemp(prefix="quarto_paper_")
        try:
            yield Path(temp_dir)
        finally:
            try:
                shutil.rmtree(temp_dir)
            except Exception as e:
                logger.warning(
                    f"Failed to clean up temporary directory {temp_dir}: {e}"
                )

    @stage("Paper Processing")
    def process(self, paper: Paper) -> bool:
        """Process a single paper."""
        try:
            logger.info("📑 Processing paper: {}", paper.target_folder)
            self._validate_paper(paper)

            paper_dir = Path("research/papers") / paper.target_folder
            commit_file = paper_dir / "last_commit.txt"

            latest_commit = self._get_commit(paper.repo_url, self._get_ref(paper))

            if self._check_if_updated(commit_file, latest_commit):
                return True

            with self._temporary_directory() as temp_dir:
                self._clone_repo(paper, temp_dir)
                self._copy_files(temp_dir, paper_dir, paper.target_folder)
                self._save_commit(commit_file, latest_commit)

            logger.success("✨ Successfully processed paper {}", paper.target_folder)
            return True

        except GitError as e:
            logger.error(f"Git operation failed for {paper.target_folder}: {e}")
            self._cleanup(paper_dir)
            return False
        except Exception as e:
            logger.exception(f"Failed to process paper {paper.target_folder}: {e}")
            self._cleanup(paper_dir)
            return False

    @substage("Paper Validation")
    def _validate_paper(self, paper: Paper) -> None:
        """Validate paper configuration."""
        if not paper.repo_url.strip():
            raise ConfigurationError("Empty repository URL")
        if not paper.target_folder.strip():
            raise ConfigurationError("Empty target folder")
        if ".." in paper.target_folder or not paper.target_folder.isascii():
            raise ConfigurationError("Invalid target folder path")
        try:
            Path(paper.target_folder).resolve().relative_to(Path.cwd())
        except ValueError:
            raise ConfigurationError(
                "Target folder path must be relative to current directory"
            )

    def _get_ref(self, paper: Paper) -> str:
        """Get git reference based on paper configuration."""
        if paper.commit:
            return paper.commit
        if paper.branch:
            return f"refs/heads/{paper.branch}"
        return "HEAD"

    @substage("Repository Status Check")
    def _check_if_updated(self, commit_file: Path, latest_commit: str) -> bool:
        """Check if paper needs updating."""
        if not self.force_update and commit_file.exists():
            current_commit = commit_file.read_text().strip()
            if current_commit == latest_commit:
                logger.success("✓ Paper is up to date (commit: {})", current_commit)
                return True
            logger.info(
                "⟳ Update needed: current={}, latest={}", current_commit, latest_commit
            )
        return False

    @substage("Repository Status Check")
    def _get_commit(self, repo_url: str, ref: str) -> str:
        """Get commit hash with proper error handling."""
        try:
            result = subprocess.run(
                ["git", "ls-remote", repo_url, ref],
                capture_output=True,
                text=True,
                check=True,
                timeout=30,
                env={"GIT_SSL_NO_VERIFY": "false"},
            )
            if not result.stdout:
                raise GitError(f"No commit found for ref: {ref}")
            return result.stdout.split()[0]

        except subprocess.TimeoutExpired:
            raise GitTimeoutError(f"Timeout accessing repository: {repo_url}")
        except subprocess.CalledProcessError as e:
            if "Authentication failed" in e.stderr:
                raise GitAuthenticationError(f"Authentication failed for: {repo_url}")
            raise GitError(f"Git error: {e.stderr.strip()}")

    @substage("Repository Clone")
    def _clone_repo(self, paper: Paper, path: Path) -> None:
        """Clone repository with proper error handling."""
        logger.info("📥 Cloning: {}", paper.repo_url)
        try:
            cmd = ["git", "clone", "--quiet", "--depth", "1"]
            if paper.branch:
                cmd.extend(["--branch", paper.branch])
            cmd.extend([paper.repo_url, str(path)])

            subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                timeout=self.timeout,
                env={"GIT_SSL_NO_VERIFY": "false"},
            )

            if paper.commit:
                logger.info(f"Checking out commit: {paper.commit}")
                subprocess.run(
                    ["git", "checkout", "-q", paper.commit],
                    check=True,
                    capture_output=True,
                    cwd=path,
                    timeout=30,
                )

        except subprocess.TimeoutExpired:
            raise GitTimeoutError(f"Timeout cloning repository: {paper.repo_url}")
        except subprocess.CalledProcessError as e:
            raise GitError(f"Clone failed: {e.stderr.strip()}")

    @substage("Copying files")
    def _copy_files(self, source: Path, target: Path, folder: str) -> None:
        """Copy files to target directory."""
        logger.info("📋 Starting file copy")

        try:
            # Create QuartoProject instance once
            project = QuartoProject(source)
            files = project.get_files()

            # Copy standard files
            logger.info("Copying standard files:")
            target.mkdir(parents=True, exist_ok=True)
            for item in files["standard"]:
                src = source / item
                dst = target / item
                if src.exists():
                    if src.is_file():
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src, dst)
                        logger.info("  └── Copied file: {}", item)
                    else:
                        shutil.copytree(src, dst, dirs_exist_ok=True)
                        logger.info("  └── Copied directory: {}", item)
                else:
                    logger.warning("Source file not found: {}", src)

            # Copy freeze files to special location
            if files["freeze"]:
                logger.info("Copying freeze files:")
                for freeze_dir in files["freeze"]:
                    src = source / freeze_dir
                    dst = Path("_freeze/research/papers") / folder / freeze_dir.name
                    if src.exists():
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copytree(src, dst, dirs_exist_ok=True)
                        logger.info(
                            "  └── Copied freeze directory: {} to {}", freeze_dir, dst
                        )
                    else:
                        logger.warning("Source freeze directory not found: {}", src)

        except Exception as e:
            logger.error("Failed to copy files: {}", str(e))
            raise

    @substage("Saving Commit Information")
    def _save_commit(self, commit_file: Path, commit_hash: str) -> None:
        """Save the current commit hash to the commit file."""
        try:
            logger.info("💾 Saving commit hash: {}", commit_hash)
            commit_file.parent.mkdir(parents=True, exist_ok=True)
            commit_file.write_text(commit_hash)
            logger.debug("Commit hash saved to: {}", commit_file)
        except OSError as e:
            raise GitError(f"Failed to save commit hash: {e}")

    def _cleanup(self, path: Path) -> None:
        """Clean up on failure."""
        if path.exists():
            logger.warning(f"Cleaning up failed paper directory: {path}")
            try:
                shutil.rmtree(path)
                logger.debug(f"Removed directory: {path}")
            except Exception as e:
                logger.error(f"Failed to clean up directory {path}: {e}")
