import glob
import pandas as pd


def merge_csv(
    source_directory: str,
    target_file: str,
    pattern: str = "**",
    extension: str = "csv",
):
    """Combine files in a given `source_directory`, into a `target_file`.
    Only files matching `pattern` and with the `extension` will be included"""
    all_filenames = [i for i in glob.glob(f"{source_directory}/{pattern}.{extension}")]

    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])

    combined_csv.to_csv(target_file, index=False, encoding="utf-8-sig")
