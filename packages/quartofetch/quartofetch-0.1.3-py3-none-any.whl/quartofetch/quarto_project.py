"""Analyze and process Quarto projects."""

from pathlib import Path
from typing import Dict, Set
import yaml
from loguru import logger

from .logging_config import stage, substage
from .exceptions import QuartoError


class QuartoProject:
    """Analyzes and processes Quarto projects."""

    def __init__(self, repo_dir: Path):
        self.repo_dir = repo_dir
        self.config = self._load_config()
        self.project_type = self._determine_project_type()
        self.main_doc = self._find_main_doc()
        logger.debug(
            "Initialized QuartoProject: type={}, main_doc={}",
            self.project_type,
            self.main_doc,
        )

    @substage("Loading Quarto Configuration")
    def _load_config(self) -> dict:
        """Load Quarto configuration with error handling."""
        config_path = self.repo_dir / "_quarto.yml"
        try:
            if config_path.exists():
                config = yaml.safe_load(config_path.read_text())
                logger.debug("Loaded config:\n{}", yaml.dump(config, indent=2))
                return config
            logger.warning("No _quarto.yml found, using empty config")
            return {}
        except yaml.YAMLError as e:
            raise QuartoError(f"Invalid YAML in _quarto.yml: {e}")
        except OSError as e:
            raise QuartoError(f"Failed to read _quarto.yml: {e}")

    @substage("Project Type Analysis")
    def _determine_project_type(self) -> str:
        """Determine project type with validation."""
        project_type = "manuscript" if "manuscript" in self.config else "default"
        logger.debug("Determined project type: {}", project_type)
        return project_type

    @stage("Project Analysis")
    def get_files(self) -> Dict[str, Set[Path]]:
        """Get required project files with proper error handling."""
        try:
            standard_files = {
                Path("_quarto.yml"),
                self.main_doc,
                *self._get_bibliography_files(),
                *self._get_notebooks(),
                *self._get_support_directories(),
            }

            freeze_files = self._get_freeze_directories()

            self._log_file_structure(standard_files, freeze_files)

            return {"standard": standard_files, "freeze": freeze_files}
        except Exception as e:
            raise QuartoError(f"Failed to analyze project structure: {e}")

    @substage("Main Document Search")
    def _find_main_doc(self) -> Path:
        """Find main document with comprehensive search."""
        logger.debug("Searching for main document")

        try:
            # Check manuscript configuration
            if self.project_type == "manuscript":
                if article := self.config.get("manuscript", {}).get("article"):
                    logger.success(
                        "Found main document in manuscript config: {}", article
                    )
                    return Path(article)

            # Check common names
            for name in ["index.qmd", "paper.qmd", "manuscript.qmd"]:
                if (self.repo_dir / name).exists():
                    logger.success("Found main document with common name: {}", name)
                    return Path(name)

            # Take first .qmd or .ipynb file
            for ext in ["qmd", "ipynb"]:
                if files := list(self.repo_dir.glob(f"*.{ext}")):
                    main_doc = files[0].relative_to(self.repo_dir)
                    logger.success(
                        "Using first found {} file as main document: {}", ext, main_doc
                    )
                    return main_doc

            raise QuartoError("No main document found")
        except Exception as e:
            raise QuartoError(f"Failed to find main document: {e}")

    def _find_files(self, pattern: str) -> Set[Path]:
        """Find files matching pattern relative to repo directory.

        Args:
            pattern: Glob pattern to match files against

        Returns:
            Set of Path objects relative to repo directory
        """
        try:
            return {
                f.relative_to(self.repo_dir)
                for f in self.repo_dir.glob(pattern)
                if f.is_file()  # Only include files, not directories
            }
        except Exception as e:
            raise QuartoError(f"Failed to find files matching pattern '{pattern}': {e}")

    @substage("Bibliography Collection")
    def _get_bibliography_files(self) -> Set[Path]:
        """Get bibliography files with validation."""
        try:
            bib_files = set()

            # Check config
            if bib_path := self.config.get("bibliography"):
                logger.info("Found bibliography in config: {}", bib_path)
                bib_files.add(Path(bib_path))

            # Find all .bib files
            filesystem_bibs = self._find_files("*.bib")
            if filesystem_bibs:
                logger.info("Found bibliography files in filesystem:")
                for bib in filesystem_bibs:
                    logger.info("  └── {}", bib)
                bib_files.update(filesystem_bibs)

            if not bib_files:
                logger.warning("No bibliography files found")

            return bib_files
        except Exception as e:
            raise QuartoError(f"Failed to collect bibliography files: {e}")

    @substage("Notebook Collection")
    def _get_notebooks(self) -> Set[Path]:
        """Get notebooks based on project type."""
        try:
            logger.debug("Collecting notebooks for {} project", self.project_type)
            notebooks = set()

            if self.project_type == "manuscript":
                # Get notebooks from manuscript config
                config_notebooks = self.config.get("manuscript", {}).get(
                    "notebooks", []
                )
                if config_notebooks:
                    logger.info("Found notebooks in manuscript config:")
                    for nb in config_notebooks:
                        logger.info("  └── {}", nb)
                    notebooks.update(Path(nb) for nb in config_notebooks)

                # Look for embedded notebooks in main document
                main_doc_path = self.repo_dir / self.main_doc
                if main_doc_path.exists():
                    content = main_doc_path.read_text()
                    embedded_notebooks = {
                        line.split("notebooks/")[1].split("#")[0].strip()
                        for line in content.splitlines()
                        if "embed notebooks/" in line
                    }

                    if embedded_notebooks:
                        logger.info("Found embedded notebooks:")
                        for nb in sorted(embedded_notebooks):
                            logger.info("  └── notebooks/{}", nb)
                            notebooks.add(Path("notebooks") / nb)
            else:
                # For default projects, include all notebooks
                found_notebooks = self._find_files("**/*.ipynb")
                if found_notebooks:
                    logger.info("Found notebooks in filesystem:")
                    for nb in sorted(found_notebooks):
                        logger.info("  └── {}", nb)
                    notebooks.update(found_notebooks)

            return notebooks
        except Exception as e:
            raise QuartoError(f"Failed to collect notebooks: {e}")

    @substage("Support Directory Collection")
    def _get_support_directories(self) -> Set[Path]:
        """Get support directories based on project type."""
        try:
            logger.debug("Collecting support directories")
            # Common directories for both types
            dirs = {"figures", "_tex"}

            # Add notebooks directory for manuscript projects
            if self.project_type == "manuscript":
                dirs.add("notebooks")

            found_dirs = {Path(d) for d in dirs if (self.repo_dir / d).exists()}
            if found_dirs:
                logger.info("Found support directories:")
                for d in sorted(found_dirs):
                    logger.info(f"  └── {d}")
            return found_dirs
        except Exception as e:
            raise QuartoError(f"Failed to collect support directories: {e}")

    @substage("Freeze Directory Collection")
    def _get_freeze_directories(self) -> Set[Path]:
        """Get freeze directories based on project type."""
        try:
            logger.debug(
                f"Collecting freeze directories for {self.project_type} project"
            )
            freeze_dirs = set()
            freeze_base = self.repo_dir / "_freeze"

            if self.project_type == "default":
                # For default projects, check main document's freeze directory
                freeze_path = freeze_base / self.main_doc.stem
                if freeze_path.exists():
                    freeze_dir = Path("_freeze") / self.main_doc.stem
                    logger.success(
                        f"Found default project freeze directory: {freeze_dir}"
                    )
                    freeze_dirs.add(freeze_dir)
            else:
                # For manuscript projects, check all potential freeze directories
                if freeze_base.exists():
                    found_dirs = [
                        Path("_freeze") / p.relative_to(freeze_base)
                        for p in freeze_base.glob("**/*")
                        if p.is_dir()
                        and not any(part.startswith("_") for part in p.parts[1:])
                    ]
                    if found_dirs:
                        logger.info("Found manuscript freeze directories:")
                        for d in sorted(found_dirs):
                            logger.info(f"  └── {d}")
                        freeze_dirs.update(found_dirs)

            return freeze_dirs
        except Exception as e:
            raise QuartoError(f"Failed to collect freeze directories: {e}")

    @substage("File Structure Logging")
    def _log_file_structure(
        self, standard_files: Set[Path], freeze_files: Set[Path]
    ) -> None:
        """Log file structure in a tree format."""
        logger.info("📁 Collected files:")
        logger.info("└── 📄 Standard files:")
        for f in sorted(standard_files):
            logger.info("    └── {}", f)
        logger.info("└── 🧊 Freeze files:")
        for f in sorted(freeze_files):
            logger.info("    └── {}", f)
