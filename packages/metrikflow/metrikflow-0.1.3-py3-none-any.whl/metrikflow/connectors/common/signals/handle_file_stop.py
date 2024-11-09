from typing import Union, BinaryIO, TextIO


def handle_file_stop(
    signame, 
    metrics_file: Union[BinaryIO, TextIO]
): 
    try:
        metrics_file.close()
    except Exception:
        pass