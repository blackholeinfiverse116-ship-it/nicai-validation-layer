import traceback
import time


def handle_error(error, context=None):

    return {
        "success": False,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "traceback": traceback.format_exc(),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "context": context or {},
        "message": "NICAI pipeline error occurred"
    }
