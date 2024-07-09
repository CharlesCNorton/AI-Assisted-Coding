import os
import platform
from pathlib import Path
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def find_cuda_path():
    system = platform.system()
    cuda_path = None

    try:
        if system == 'Windows':
            default_path = 'C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA'
            cuda_path = os.getenv('CUDA_PATH', default_path)
            if not Path(cuda_path).exists():
                logging.warning(f"Default CUDA path {cuda_path} does not exist.")
                possible_versions = [p for p in Path(default_path).iterdir() if p.is_dir()]
                if possible_versions:
                    cuda_path = str(possible_versions[-1])
                    logging.info(f"Using CUDA path {cuda_path}")
                else:
                    raise FileNotFoundError(f"No CUDA versions found in {default_path}.")
        elif system == 'Darwin':  # macOS
            cuda_path = os.getenv('CUDA_PATH', '/usr/local/cuda')
            if not Path(cuda_path).exists():
                raise FileNotFoundError(f"CUDA not found at {cuda_path}.")
        else:
            cuda_path = os.getenv('CUDA_PATH', '/usr/local/cuda')
            if not Path(cuda_path).exists():
                raise FileNotFoundError(f"CUDA not found at {cuda_path}.")

        if not Path(cuda_path).exists():
            raise FileNotFoundError(f"CUDA not found at {cuda_path}. Please set the CUDA_PATH environment variable correctly.")

    except Exception as e:
        logging.error(f"Error finding CUDA path: {e}")
        raise

    return cuda_path

def set_environment_variables():
    try:
        cuda_home = os.getenv('CUDA_HOME')
        if cuda_home:
            logging.info(f"CUDA_HOME is already set to {cuda_home}. Skipping environment variable setup.")
            return

        cuda_path = find_cuda_path()
        os.environ['CUDA_HOME'] = cuda_path
        os.environ['PATH'] = f"{cuda_path}/bin:{os.environ['PATH']}"
        os.environ['LD_LIBRARY_PATH'] = f"{cuda_path}/lib64:{os.environ.get('LD_LIBRARY_PATH', '')}"
        logging.info(f"Environment variables set for {platform.system()}:")
        logging.info(f"CUDA_HOME={cuda_path}")
        logging.info(f"PATH={os.environ['PATH']}")
        logging.info(f"LD_LIBRARY_PATH={os.environ['LD_LIBRARY_PATH']}")

    except FileNotFoundError as e:
        logging.critical(f"Critical error: {e}")
        sys.exit(1)
    except PermissionError as e:
        logging.critical(f"Permission error: {e}")
        sys.exit(1)
    except OSError as e:
        logging.critical(f"OS error: {e}")
        sys.exit(1)
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        sys.exit(1)

def setup_cuda_env():
    try:
        set_environment_variables()
    except Exception as e:
        logging.critical(f"Critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_cuda_env()
