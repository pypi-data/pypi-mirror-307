import argparse
import os
import shutil
import time
import logging
from distutils.core import setup
from Cython.Build import cythonize


def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)


logger = configure_logging()

ROOT_PATH = os.path.abspath("")
PROJECT_NAME = ROOT_PATH.split("/")[-1]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--ignore", default=[], nargs="+", help="ignore files for compile."
    )
    parser.add_argument("-d", "--dir", default="dist", help="result directory.")
    parser.add_argument("-v", "--version", default=3, help="python version.")
    parser.add_argument("-c", "--copy_py", default=[], nargs="+", help="copy py files.")
    parser.add_argument(
        "-p", "--parallel", type=int, default=os.cpu_count(),
        help="number of parallel workers (default: number of CPU cores)."
    )
    return parser.parse_args()


def list_files(dir=""):
    """Return all relative paths under the current folder."""
    dir_path = os.path.join(ROOT_PATH, dir)
    for filename in os.listdir(dir_path):
        absolute_file_path = os.path.join(dir_path, filename)
        file_path = os.path.join(dir, filename)
        if filename.startswith("."):
            continue
        if os.path.isdir(absolute_file_path) and not filename.startswith("__"):
            for file in list_files(file_path):
                yield file
        else:
            yield file_path


def copy_ignored_files(args):
    """Copy ignored files"""
    files = list_files()
    for file in files:
        file_arr = file.split("/")
        if file_arr[0] == args.dir:
            continue
        suffix = os.path.splitext(file)[1]
        if not suffix:
            continue
        if file_arr[0] not in args.copy_py and file not in args.copy_py:
            if suffix in (".pyc", ".pyx"):
                continue
            elif suffix == ".py":
                continue
        src = os.path.join(ROOT_PATH, file)
        dst = os.path.join(
            ROOT_PATH, os.path.join(args.dir, file.replace(ROOT_PATH, "", 1))
        )
        dir = "/".join(dst.split("/")[:-1])
        if not os.path.exists(dir):
            os.makedirs(dir)
        shutil.copyfile(src, dst)
        logger.debug(f"Copied {src} to {dst}")


def build_project(args):
    """py -> c -> so"""
    start = time.time()
    logger.info("Build started")
    files = list(list_files())
    module_list = [file for file in files if os.path.splitext(file)[1] == ".py" and file.split("/")[
        0] not in args.ignore and file not in args.ignore]

    dist_temp = os.path.join(os.path.join("", args.dir), "temp")

    try:
        setup(
            ext_modules=cythonize(
                module_list,
                exclude=["**/migrations/*.py"],
                nthreads=args.parallel,
                compiler_directives={"language_level": args.version}
            ),
            script_args=[
                "build_ext",
                "-b",
                os.path.join("", args.dir),
                "-t",
                dist_temp,
            ],
        )
    except Exception as e:
        logger.error(f"Error during setup: {e}")

    if os.path.exists(dist_temp):
        shutil.rmtree(dist_temp)
    for file in list_files():
        if file.endswith(".c"):
            os.remove(os.path.join(ROOT_PATH, file))
            logger.debug(f"Removed {file}")

    copy_ignored_files(args)
    end = time.time()
    logger.info(f"Build complete in {end - start:.2f} seconds")


def main():
    args = parse_args()

    args.ignore.append(".venv")
    args.ignore.append("venv")

    logger.info("Starting main function")
    build_project(args)


if __name__ == "__main__":
    main()
