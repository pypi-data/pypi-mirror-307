# pylint: disable=C0114
from typing import Dict, List
import os
import json
from json import JSONDecodeError
from abc import ABC, abstractmethod
from ..util.exceptions import InputException
from ..util.error import ErrorHandler

from csvpath import CsvPath
from csvpath.util.metadata_parser import MetadataParser


class CsvPathsManager(ABC):
    """holds paths (the path itself, not a file name or reference) in a named set.
    this allows all paths to be run as a unit, with the results manager holding
    the set's outcomes."""

    @abstractmethod
    def add_named_paths_from_dir(self, *, directory: str, name: str = None) -> None:
        """adds named paths found in a directory. files with multiple paths
        will be handled. if name is not None the named paths for all files
        in the directory will be keyed by name.
        """

    @abstractmethod
    def add_named_paths_from_file(self, *, name: str, file_path: str) -> None:
        """adds one or more csvpaths from a single file. the
        contents of the file is straight cvspath, not json."""

    @abstractmethod
    def add_named_paths_from_json(self, file_path: str) -> None:
        """replaces the named paths dict with a dict found in a JSON file. lists
        of paths are keyed by names."""

    @abstractmethod
    def set_named_paths(self, np: Dict[str, List[str]]) -> None:
        """overwrites"""

    @abstractmethod
    def add_named_paths(self, name: str, paths: List[str]) -> None:
        """aggregates the path list under the name. if there is no
        existing list of paths, the name will be added. otherwise,
        the lists will be joined. duplicates are not added.
        """

    @abstractmethod
    def get_named_paths(self, name: str) -> List[str]:  # pylint: disable=C0116
        """returns the csvpaths grouped under the name. remember
        that your csvpaths are in ordered list that determines the
        execution order. when the paths are run serially each csvpath
        completes before the next starts, in the list order. when you
        run the paths breadth-first, line-by-line, the csvpaths are
        applied to each line in the order of the list.
        """

    @abstractmethod
    def remove_named_paths(self, name: str) -> None:  # pylint: disable=C0116
        pass  # pragma: no cover

    @abstractmethod
    def has_named_paths(self, name: str) -> bool:  # pylint: disable=C0116
        pass  # pragma: no cover

    @abstractmethod
    def number_of_named_paths(self) -> bool:  # pylint: disable=C0116
        pass  # pragma: no cover


class PathsManager(CsvPathsManager):  # pylint: disable=C0115, C0116
    MARKER: str = "---- CSVPATH ----"

    def __init__(self, *, csvpaths, named_paths=None):
        if named_paths is None:
            named_paths = {}
        self.named_paths = named_paths
        self.csvpaths = csvpaths

    def set_named_paths(self, np: Dict[str, List[str]]) -> None:
        for name in np:
            if not isinstance(np[name], list):
                ie = InputException("Named-path names must key a list of csvpath")
                ErrorHandler(csvpaths=self.csvpaths).handle_error(ie)
                return
        self.named_paths = np  # pragma: no cover
        self.csvpaths.logger.info(
            "Set named-paths collection to %s groups of csvpaths", len(np)
        )

    def add_named_paths_from_dir(self, *, directory: str, name: str = None) -> None:
        if directory is None:
            ie = InputException("Named paths collection name needed")
            ErrorHandler(csvpaths=self.csvpaths).handle_error(ie)
        if os.path.isdir(directory):
            dlist = os.listdir(directory)
            base = directory
            for p in dlist:
                if p[0] == ".":
                    continue
                if p.find(".") == -1:
                    continue
                ext = p[p.rfind(".") + 1 :].strip().lower()
                if ext not in self.csvpaths.config.csvpath_file_extensions:
                    continue
                path = os.path.join(base, p)
                aname = name
                if aname is None:
                    aname = self._name_from_name_part(p)
                self.add_named_paths_from_file(name=aname, file_path=path)
        else:
            ie = InputException("Dirname must point to a directory")
            ErrorHandler(csvpaths=self.csvpaths).handle_error(ie)

    def add_named_paths_from_file(self, *, name: str, file_path: str) -> None:
        self.csvpaths.logger.debug("Reading csvpaths file at %s", file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            cp = f.read()
            _ = [
                apath.strip()
                for apath in cp.split(PathsManager.MARKER)
                if apath.strip() != ""
            ]
            self.csvpaths.logger.debug("Found %s csvpaths in file", len(_))
            self.add_named_paths(name, _)

    def add_named_paths_from_json(self, file_path: str) -> None:
        try:
            self.csvpaths.logger.debug("Opening JSON file at %s", file_path)
            with open(file_path, encoding="utf-8") as f:
                j = json.load(f)
                self.csvpaths.logger.debug("Found JSON file with %s keys", len(j))
                for k in j:
                    v = j[k]
                    for f in v:
                        self.add_named_paths_from_file(name=k, file_path=f)
        except (OSError, ValueError, TypeError, JSONDecodeError) as ex:
            self.csvpaths.logger.error(f"Error: cannot load {file_path}: {ex}")
            ErrorHandler(csvpaths=self.csvpaths).handle_error(ex)

    def add_named_paths(self, name: str, paths: List[str]) -> None:
        if not isinstance(paths, list):
            ie = InputException(
                """Paths must be a list of csvpaths.
                                 If you want to load a file use add_named_paths_from_file or
                                 set_named_paths_from_json."""
            )
            ErrorHandler(csvpaths=self.csvpaths).handle_error(ie)
        self.csvpaths.logger.debug("Adding csvpaths to named-paths group %s", name)
        if name in self.named_paths:
            for p in paths:
                if p in self.named_paths[name]:
                    self.csvpaths.logger.debug(
                        "csvpaths %s already exists in named-paths group %s", p, name
                    )
                    pass
                else:
                    self.csvpaths.logger.debug("Adding %s to %s", p, name)
                    """
                    if isinstance(self.named_paths[name], str):
                        ps = []
                        ps.append(self.named_paths[name])
                        self.named_paths[name] = ps
                    """
                    self.named_paths[name].append(p)
        else:
            for _ in paths:
                self.csvpaths.logger.debug("Adding %s to %s", _, name)
            self.named_paths[name] = paths

    #
    # changed to not raise IE when not found in order to match
    # files_manager and let csvpaths call the shots.
    #
    def get_named_paths(self, name: str) -> List[str]:
        ret = None
        p2 = self._paths_name_path(name)
        if p2[1] is None and p2[0] in self.named_paths:
            ret = self.named_paths[p2[0]]
        elif p2[1] is not None:
            ret = self._find_one(p2)
        return ret

    def _paths_name_path(self, pathsname) -> tuple[str, str]:
        specificpath = None
        i = pathsname.find("#")
        if i > 0:
            specificpath = pathsname[i + 1 :]
            pathsname = pathsname[0:i]
        return (pathsname, specificpath)

    def _find_one(self, p2: tuple[str]) -> str:
        if p2[1] is not None:
            paths = self.get_named_paths(p2[0])
            for path in paths:
                c = CsvPath()
                MetadataParser(c).extract_metadata(instance=c, csvpath=path)
                if c.identity == p2[1]:
                    return [path]
        raise InputException(
            f"Path identified as '{p2[1]}' must be in the group identitied as '{p2[0]}'"
        )

    def remove_named_paths(self, name: str) -> None:
        if name in self.named_paths:
            del self.named_paths[name]
        else:
            raise InputException("{name} not found")

    def has_named_paths(self, name: str) -> bool:
        return self.get_named_paths(name)

    def number_of_named_paths(self) -> bool:
        return len(self.named_paths)  # pragma: no cover

    def _name_from_name_part(self, name):
        i = name.rfind(".")
        if i == -1:
            pass
        else:
            name = name[0:i]
        return name
