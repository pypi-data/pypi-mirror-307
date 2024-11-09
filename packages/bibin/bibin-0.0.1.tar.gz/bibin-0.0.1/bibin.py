#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

import argparse
from configparser import ConfigParser, Error as ConfigError
from dataclasses import dataclass
import datetime
import errno
import json
import locale
import os
from pathlib import Path
import stat as stat_module
import shutil
from urllib.parse import quote, unquote
import uuid


__version__ = "0.0.1"


DELETION_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"


def get_home_trash():
    xdg_data_home = Path(
        os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share"
    )
    return xdg_data_home / "Trash"


@dataclass
class TrashedFile:
    info: Path
    file: Path
    original_path: Path
    deletion_date: datetime.datetime


class TrashDirectory:
    def __init__(self, root):
        self.rootdir = root
        self.infodir = root / "info"
        self.filesdir = root / "files"
        self.stat = self.rootdir.stat()

    def __repr__(self):
        return f"<{type(self).__name__} root={self.rootdir!r}>"

    def _get_file_from_info(self, infopath):
        return self.filesdir / infopath.stem

    def _get_info_from_file(self, filepath):
        return self.infodir / f"{filepath.name}.trashinfo"

    def iter_trashed(self):
        for info in self._iter_info():
            file = self._parse_info(info)
            if not file:
                continue

            try:
                file.file.lstat()
            except FileNotFoundError:
                continue

            yield file

    def _iter_info(self):
        return self.infodir.glob("*.trashinfo")

    def get_info(self, infopath):
        file = self._parse_info(infopath)
        if not file:
            return None

        try:
            file.file.lstat()
        except FileNotFoundError:
            return None
        return file

    def _parse_info(self, infopath):
        parser = ConfigParser(interpolation=None)
        try:
            with infopath.open() as fp:
                parser.read_file(fp)
        except IOError:
            # TODO catch more exceptions
            # TODO raise specific exception
            return None

        original_path = Path(unquote(parser["Trash Info"]["Path"]))
        try:
            deletion_date = datetime.datetime.strptime(
                parser["Trash Info"]["DeletionDate"], DELETION_DATE_FORMAT,
            )
        except (KeyError, ValueError):
            deletion_date = None

        return TrashedFile(
            info=infopath,
            file=self._get_file_from_info(infopath),
            original_path=original_path,
            deletion_date=deletion_date,
        )

    def erase(self, trashed):
        stat = trashed.file.lstat()
        if stat_module.S_ISDIR(stat.st_mode):
            shutil.rmtree(trashed.file)
        else:
            trashed.file.unlink(missing_ok=True)
        trashed.info.unlink(missing_ok=True)

    def iter_orphans(self):
        # TODO files without info
        for file in self.filesdir.iterdir():
            info = self._get_info_from_file(file)
            try:
                info.lstat()
            except FileNotFoundError:
                yield file

    def clean_spurious(self):
        # TODO info without file or invalid info
        for info in self._iter_info():
            file = self._get_file_from_info(info)
            try:
                file.lstat()
            except FileNotFoundError:
                print(f"would remove {info}")
                # info.unlink()
                yield
                continue

            # what if only original_path is missing or invalid? it's not that serious
            try:
                trashed = self._parse_info(info)
            except ConfigError:
                print(f"would remove {info}")
                #info.unlink()
                yield
                continue

    def _create_info(self, original_name, deletion_date):
        def _or_none(fn):
            try:
                return (self.infodir / f"{fn}.trashinfo").open("x")
            except FileExistsError:
                return None

        return (
            _or_none(original_name)
            or _or_none(f"{deletion_date:%Y%m%d-%H%M%S%}-{original_name}")
            or _or_none(str(uuid.uuid4()))
        )

    def is_eligible(self, original):
        original_stat = original.lstat()
        if original_stat.st_dev != self.stat.st_dev:
            return False

        return True

    def trash_file(self, original):
        if not self.is_eligible(original):
            raise IOError(errno.EXDEV)

        deletion_date = datetime.datetime.now()
        deletion_date_str = deletion_date.strftime(DELETION_DATE_FORMAT)
        infodata = f"[Trash Info]\nPath={quote(str(original))}\nDeletionDate={deletion_date_str}\n"

        with self._create_info(original.name, deletion_date) as fp:
            info_path = Path(fp.name)
            fp.write(infodata)

        target_file = self._get_file_from_info(info_path)
        try:
            original.rename(target_file)
        except FileNotFoundError:
            info_path.unlink(missing_ok=True)
            raise


class TrashDetector:
    @classmethod
    def _iter_top_dirs(cls):
        for line in Path("/proc/mounts").read_text().strip().split("\n"):
            yield Path(line.split()[1])

    @classmethod
    def iter_trashes(cls):
        home_trash = get_home_trash()
        if home_trash.is_dir():
            yield TrashDirectory(home_trash)

        uid = os.getuid()
        for top_dir in cls._iter_top_dirs():
            trash = top_dir / ".Trash"
            try:
                stat = trash.lstat()
            except OSError:
                pass
            else:
                if (
                    stat_module.S_ISDIR(stat.st_mode)
                    and stat.st_mode & stat_module.S_ISVTX
                ):
                    trash = trash / str(uid)
                    if trash.is_dir():
                        yield TrashDirectory(trash)
                        continue

            trash = top_dir / f".Trash-{uid}"
            try:
                trash.lstat()
            except OSError:
                pass
            else:
                if trash.is_dir():
                    yield TrashDirectory(trash)
                    continue

    @classmethod
    def create_home_trash(cls):
        path = get_home_trash()
        path.mkdir(mode=0o700, parents=True, exist_ok=True)
        cls._sub_mkdir(path)
        # check W_OK?
        return TrashDirectory(path)

    @classmethod
    def create_top_trash_at(cls, top_dir):
        uid = os.getuid()
        trash = top_dir / ".Trash"
        if trash.is_dir() and not trash.is_symlink():
            stat = trash.lstat()
            if stat.st_mode & stat_module.S_ISVTX:
                trash = trash / str(uid)
                try:
                    trash.mkdir(mode=0o700, exist_ok=True)
                    cls._sub_mkdir(trash)
                except OSError:
                    pass
                else:
                    if os.access(trash, os.W_OK):
                        return TrashDirectory(trash)

        trash = top_dir / f".Trash-{uid}"
        try:
            trash.mkdir(mode=0o700, exist_ok=True)
            cls._sub_mkdir(trash)
        except OSError:
            pass
        else:
            if os.access(trash, os.W_OK):
                return TrashDirectory(trash)

    @classmethod
    def _sub_mkdir(cls, trash):
        (trash / "files").mkdir(exist_ok=True)
        (trash / "info").mkdir(exist_ok=True)

    @classmethod
    def find_top_dir(cls, path):
        # don't resolve path, caller may want to delete a symlink
        # and Path.absolute doesn't normalize path, which is a problem for .parent
        path = Path(os.path.abspath(path))
        while not path.is_mount():
            path = path.parent
        return path

    @classmethod
    def get_trash_of(cls, info_path):
        trash_root = info_path.parent.parent

        home_trash = get_home_trash()
        if trash_root == home_trash:
            return TrashDirectory(home_trash)

        top = cls.find_top_dir(info_path)
        if trash_root.parent == top:
            return TrashDirectory(trash_root)

    @classmethod
    def create_trash_for(cls, to_delete):
        home_trash = get_home_trash()
        home_top = cls.find_top_dir(home_trash)
        if to_delete.lstat().st_dev == home_top.lstat().st_dev:
            cls.create_home_trash()
            return TrashDirectory(home_trash)

        top_dir = cls.find_top_dir(to_delete)
        return cls.create_top_trash_at(top_dir)


MODE_TYPES = {
    stat_module.S_ISREG: "-",
    stat_module.S_ISDIR: "d",
    stat_module.S_ISLNK: "l",
    stat_module.S_ISBLK: "b",
    stat_module.S_ISCHR: "c",
    stat_module.S_ISSOCK: "s",
    stat_module.S_ISFIFO: "p",
}

MODE_PERMS = {
    0o400: "r",
    0o200: "w",
    0o100: "x",
    0o40: "r",
    0o20: "w",
    0o10: "x",
    0o4: "r",
    0o2: "w",
    0o1: "x",
}


def mode_to_string(mode):
    result = list("?---------")
    perms = stat_module.S_IMODE(mode)
    for func in MODE_TYPES:
        if func(mode):
            result[0] = MODE_TYPES[func]
            break

    if perms & 0o400:
        result[1] = "r"
    if perms & 0o200:
        result[2] = "w"
    if perms & 0o4000:
        if perms & 0o100:
            result[3] = "s"
        else:
            result[3] = "S"
    elif perms & 0o100:
        result[3] = "x"

    if perms & 0o40:
        result[4] = "r"
    if perms & 0o20:
        result[5] = "w"
    if perms & 0o2000:
        if perms & 0o10:
            result[6] = "s"
        else:
            result[6] = "S"
    elif perms & 0o10:
        result[6] = "x"

    if perms & 0o4:
        result[7] = "r"
    if perms & 0o2:
        result[8] = "w"
    if perms & 0o1000:
        if perms & 0o1:
            result[9] = "t"
        else:
            result[9] = "T"
    elif perms & 0o1:
        result[9] = "x"

    return "".join(result)


def trashed_to_json_entry(trashed):
    # roughly the same columns as nushell's ls
    stat = trashed.file.lstat()
    result = {
        "name": trashed.original_path.name,
        "type": "dir" if stat_module.S_ISDIR(stat.st_mode) else "file", # FIXME
        "size": stat.st_size,
        "accessed": datetime.datetime.fromtimestamp(stat.st_atime).astimezone(),
        "modified": datetime.datetime.fromtimestamp(stat.st_mtime).astimezone(),
        "inode": stat.st_ino,
        "mode": mode_to_string(stat.st_mode),
        "readonly": stat.st_mode & stat_module.S_IWUSR,
        "target": None,
        "deleted_at": trashed.deletion_date.astimezone(),
        "original_path": str(trashed.original_path),
        "trashed_path": str(trashed.file),
        "info_path": str(trashed.info),
    }
    try:
        result["user"] = trashed.file.owner()
        result["group"] = trashed.file.group()
    except (KeyError, FileNotFoundError):
        # FIXME use lstat
        pass

    return result


def json_convert(value):
    if isinstance(value, Path):
        return str(value)
    elif isinstance(value, datetime.datetime):
        return value.strftime("%F %T %z")
    raise TypeError(f"{type(value)} object can't be serialized")


def main():
    locale.setlocale(locale.LC_ALL, "")

    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--list-trashes", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--clean-spurious", action="store_true")
    parser.add_argument("--list-orphans", action="store_true")
    parser.add_argument("--put")
    parser.add_argument("--erase", type=Path)
    parser.add_argument("--trash-dir", type=Path)
    args = parser.parse_args()

    if args.trash_dir:
        trash = TrashDirectory(args.trash_dir)
    else:
        trash = TrashDirectory(get_home_trash())
    if args.list:
        items = list(trash.iter_trashed())
        if args.json:
            items = [
                trashed_to_json_entry(item) for item in items
            ]
            print(json.dumps(items, default=json_convert))
        else:
            print(items)
    elif args.list_orphans:
        print(list(trash.iter_orphans()))
    elif args.list_trashes:
        print(list(TrashDetector.iter_trashes()))
    elif args.clean_spurious:
        for _ in trash.clean_spurious():
            pass
    elif args.put:
        to_delete = Path(os.path.abspath(args.put))
        trash = TrashDetector.create_trash_for(to_delete)
        trash.trash_file(to_delete)
    elif args.erase:
        trash = TrashDetector.get_trash_of(args.erase)
        info = trash.get_info(args.erase)
        if not info:
            raise FileNotFoundError(f"no trashed file at {args.erase}")
        trash.erase(info)
    else:
        raise NotImplementedError()


if __name__ == "__main__":
    main()
