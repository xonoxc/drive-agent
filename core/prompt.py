from schemas.files import DriveFile


def build_summery_prompt(msg: str, matching_files: str) -> str:
    return f"""
        User query:
        {msg}

        Matching files:
        {matching_files}

        Summarize the results naturally.
    """
