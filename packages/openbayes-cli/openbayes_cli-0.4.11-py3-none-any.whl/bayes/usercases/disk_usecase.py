import os
import logging
from typing import List, Tuple, Optional

import pathspec


class IgnoreService:
    def __init__(self, ignore_file_name: str, cleanups: List[str]):
        self.ignore_file_name = ignore_file_name
        self.cleanups = cleanups

    def ignored(self, basedir: str) -> Tuple[List[str], List[str], Optional[Exception]]:
        try:
            basedir = os.path.realpath(basedir)

            with open(self.ignore_file_name, 'r') as file:
                ignore_patterns = file.read().splitlines()

            spec = pathspec.PathSpec.from_lines('gitwildmatch', ignore_patterns + self.cleanups)

            matched_files = []
            matched_dirs = []

            for root, dirs, files in os.walk(basedir):
                for name in files:
                    file_path = os.path.relpath(os.path.join(root, name), basedir)
                    if spec.match_file(file_path):
                        matched_files.append(file_path)
                for name in dirs:
                    dir_path = os.path.relpath(os.path.join(root, name), basedir)
                    if spec.match_file(dir_path):
                        matched_dirs.append(dir_path)

            return matched_files, matched_dirs, None
        except Exception as e:
            return [], [], e

    def left(self, basedir: str) -> Tuple[List[str], List[str], Optional[Exception]]:
        try:
            basedir = os.path.realpath(basedir)

            with open(self.ignore_file_name, 'r') as file:
                ignore_patterns = file.read().splitlines()

            spec = pathspec.PathSpec.from_lines('gitwildmatch', ignore_patterns + self.cleanups)

            unmatched_files = []
            unmatched_dirs = []

            for root, dirs, files in os.walk(basedir):
                for name in files:
                    file_path = os.path.relpath(os.path.join(root, name), basedir)
                    if not spec.match_file(file_path):
                        unmatched_files.append(file_path)
                for name in dirs:
                    dir_path = os.path.relpath(os.path.join(root, name), basedir)
                    if not spec.match_file(dir_path):
                        unmatched_dirs.append(dir_path)

            return unmatched_files, unmatched_dirs, None
        except Exception as e:
            return [], [], e


def mbyte_to_byte(mb):
    return mb * (1 << 20)


class DiskService:
    def __init__(self, ignore_service):
        self.ignore_service = ignore_service

    def directory_computing(self, dir, mb_limit):
        try:
            left_files, _, err = self.ignore_service.left(dir)
            if err is not None:
                return 0, 0, err

            files = 0
            total_bytes = 0

            for file in left_files:
                file_path = os.path.join(dir, file)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    total_bytes += stat.st_size
                    files += 1

                if total_bytes >= mbyte_to_byte(mb_limit):
                    return 0, 0, Exception(f"文件总大小超出限制的 {mb_limit} MB")

            logging.debug(f"Get files [{files}] and sizes [{total_bytes}]")


            return files, total_bytes, None
        except Exception as e:
            return 0, 0, e
