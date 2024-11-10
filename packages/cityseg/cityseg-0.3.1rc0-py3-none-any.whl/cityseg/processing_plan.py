"""
This module defines a class for creating and managing the processing plan for video segmentation tasks.

It determines which processing steps need to be executed based on the configuration
and the existence of previously generated outputs.

Classes:
    ProcessingPlan: A class to create and manage the processing plan for video segmentation tasks.
"""

from typing import Dict

from loguru import logger

from .config import Config
from .file_handler import FileHandler


class ProcessingPlan:
    """
    A class to create and manage the processing plan for video segmentation tasks.

    This class determines which processing steps need to be executed based on the
    configuration and the existence of previously generated outputs.

    Attributes:
        config (Config): Configuration object containing processing parameters.
        plan (Dict[str, bool]): A dictionary indicating which processing steps to execute.
    """

    def __init__(self, config: Config):
        """
        Initializes the ProcessingPlan with the given configuration.

        Args:
            config (Config): Configuration object for the processing plan.
        """
        self.config = config
        self.plan = self._create_processing_plan()

    def _create_processing_plan(self) -> Dict[str, bool]:
        """
        Creates a processing plan based on the configuration and existing outputs.

        This method checks if force reprocessing is enabled or if existing outputs
        are valid to determine which processing steps should be executed.

        Returns:
            Dict[str, bool]: A dictionary indicating which processing steps to execute.
        """
        if self.config.force_reprocess:
            logger.info("Force reprocessing enabled. All steps will be executed.")
            return {
                "process_video": True,
                "generate_hdf": True,
                "generate_colored_video": self.config.save_colored_segmentation,
                "generate_overlay_video": self.config.save_overlay,
                "analyze_results": self.config.analyze_results,
            }

        existing_outputs = self._check_existing_outputs()

        plan = {
            "process_video": not existing_outputs["hdf_file_valid"],
            "generate_hdf": not existing_outputs["hdf_file_valid"],
            "generate_colored_video": self.config.save_colored_segmentation
            and not existing_outputs["colored_video_valid"],
            "generate_overlay_video": self.config.save_overlay
            and not existing_outputs["overlay_video_valid"],
            "analyze_results": self.config.analyze_results
            and not existing_outputs["analysis_files_valid"],
        }

        logger.debug(f"Created processing plan: {plan}")
        return plan

    def _check_existing_outputs(self) -> Dict[str, bool]:
        """
        Checks the validity of existing output files.

        This method verifies the existence and validity of the HDF file, colored video,
        overlay video, and analysis files.

        Returns:
            Dict[str, bool]: A dictionary indicating the validity of existing outputs.
        """
        output_path = self.config.get_output_path()
        hdf_path = output_path.with_name(f"{output_path.stem}_segmentation.h5")
        colored_video_path = output_path.with_name(f"{output_path.stem}_colored.mp4")
        overlay_video_path = output_path.with_name(f"{output_path.stem}_overlay.mp4")
        counts_file = output_path.with_name(f"{output_path.stem}_category_counts.csv")
        percentages_file = output_path.with_name(
            f"{output_path.stem}_category_percentages.csv"
        )

        results = {
            "hdf_file_valid": False,
            "colored_video_valid": False,
            "overlay_video_valid": False,
            "analysis_files_valid": False,
        }

        if hdf_path.exists():
            results["hdf_file_valid"] = FileHandler.verify_hdf_file(
                hdf_path, self.config
            )

        if colored_video_path.exists():
            results["colored_video_valid"] = FileHandler.verify_video_file(
                colored_video_path
            )

        if overlay_video_path.exists():
            results["overlay_video_valid"] = FileHandler.verify_video_file(
                overlay_video_path
            )

        if counts_file.exists() and percentages_file.exists():
            results["analysis_files_valid"] = FileHandler.verify_analysis_files(
                counts_file, percentages_file
            )

        return results
