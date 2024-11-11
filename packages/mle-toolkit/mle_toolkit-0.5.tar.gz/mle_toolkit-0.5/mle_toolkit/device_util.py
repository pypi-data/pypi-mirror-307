import subprocess


def if_gpu_supported() -> bool:
    try:
        subprocess.check_output("nvidia-smi")
        return True
    except Exception:
        return False
