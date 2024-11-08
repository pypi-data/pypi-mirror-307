"""Command-line interface for quartofetch"""

import sys
import argparse
from pathlib import Path
from typing import List
import yaml
from loguru import logger
import os

from .logging_config import setup_logging, stage, substage
from .paper_manager import Paper, PaperManager
from .exceptions import QuartoFetchError, ConfigurationError


class CLI:
    """CLI handler for quartofetch"""

    def __init__(self):
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and configure argument parser."""
        parser = argparse.ArgumentParser(
            description="Fetch and manage Quarto paper repositories"
        )
        parser.add_argument(
            "--force", "-f", action="store_true", help="Force update of all papers"
        )
        parser.add_argument(
            "--config",
            type=Path,
            default=Path("research/_paper_sources.yml"),
            help="Path to configuration file (default: research/_paper_sources.yml)",
        )
        parser.add_argument(
            "--log-level",
            default="SUCCESS",
            choices=["DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR"],
            help="Set logging level",
        )
        parser.add_argument(
            "--debug",
            "-d",
            action="store_true",
            help="Enable debug logging (overrides --log-level)",
        )
        parser.add_argument("--log-file", type=Path, help="Path to log file")
        return parser

    # def check_environment():
    #     """Check if required environment variables are set."""
    #     if not os.getenv("QUARTO_PROJECT_RENDER_ALL"):
    #         print("QUARTO_PROJECT_RENDER_ALL is not set. Exiting.")
    #         return False
    #     return True

    @stage("Configuration Loading")
    def load_config(self, config_path: Path) -> dict:
        """Load and validate configuration file."""
        try:
            if not config_path.exists():
                raise ConfigurationError(f"Config file not found: {config_path}")

            config = yaml.safe_load(config_path.read_text())
            if not isinstance(config, dict):
                raise ConfigurationError(
                    "Invalid config format: must be a YAML dictionary"
                )

            papers_config = config.get("papers", [])
            if not isinstance(papers_config, list):
                raise ConfigurationError("Invalid papers configuration: must be a list")

            return config

        except yaml.YAMLError as e:
            raise ConfigurationError(f"Invalid YAML in config file: {e}")
        except OSError as e:
            raise ConfigurationError(f"Failed to read config file: {e}")

    @substage("Paper Configuration")
    def _process_paper_configs(self, config: dict) -> List[Paper]:
        """Process paper configurations from config file."""
        papers = []
        for idx, paper_config in enumerate(config.get("papers", []), 1):
            try:
                if paper := Paper.from_dict(paper_config):
                    papers.append(paper)
                else:
                    logger.warning(
                        f"Skipping invalid paper configuration at index {idx}"
                    )
            except Exception as e:
                logger.error(
                    f"Failed to process paper configuration at index {idx}: {e}"
                )
        return papers

    @substage("Paper Processing")
    def _process_papers(self, papers: List[Paper], force_update: bool) -> List[bool]:
        """Process all papers and return results."""
        manager = PaperManager(force_update=force_update)
        results = []

        for paper in papers:
            try:
                results.append(manager.process(paper))
            except Exception as e:
                logger.exception(f"Failed to process paper {paper.target_folder}: {e}")
                results.append(False)

        return results

    @substage("Results Summary")
    def _log_results(self, results: List[bool], papers: List[Paper]) -> None:
        """Log processing results with proper formatting."""
        success_count = sum(results)
        total_count = len(results)

        with logger.contextualize(padding=""):
            logger.info("═" * 80)
            if success_count == total_count:
                logger.success(
                    f"✅ All papers processed successfully ({success_count}/{total_count})"
                )
            else:
                logger.warning(
                    f"⚠️  Processed {success_count}/{total_count} papers successfully"
                )
                failed_papers = [
                    p.target_folder for p, r in zip(papers, results) if not r
                ]
                logger.warning(f"❌ Failed papers: {', '.join(failed_papers)}")
            logger.info("═" * 80)

    def run(self) -> int:
        """Execute the CLI application."""
        try:
            args = self.parser.parse_args()

            # Setup logging
            log_level = "DEBUG" if args.debug else args.log_level
            setup_logging(console_level=log_level, log_file=args.log_file)

            full_render = os.getenv("QUARTO_PROJECT_RENDER_ALL")
            if not args.force and not full_render:
                logger.success("quartofetch skipped due to partial render")
                return 0

            # Log startup banner
            with logger.contextualize(padding=""):
                logger.info("═" * 80)
                logger.success("🚀 Quarto FETCH")
                logger.info("═" * 80)

            # Load and process configuration
            config = self.load_config(args.config)
            papers = self._process_paper_configs(config)

            if not papers:
                logger.warning("No valid papers found in configuration")
                return 1

            # Process papers
            results = self._process_papers(papers, args.force)

            # Log results
            self._log_results(results, papers)

            return 0 if all(results) else 1

        except KeyboardInterrupt:
            logger.warning("Operation interrupted by user")
            return 130
        except QuartoFetchError as e:
            logger.error(f"Configuration error: {e}")
            return 1
        except Exception as e:
            logger.exception(f"Fatal error: {e}")
            return 1


def main() -> int:
    """Entry point for the quartofetch CLI."""
    return CLI().run()


if __name__ == "__main__":
    sys.exit(main())
