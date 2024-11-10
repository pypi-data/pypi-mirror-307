import importlib
import sys
import threading
from glob import glob
from threading import Thread
from types import ModuleType
from typing import Generator, Set

from rich import print
from watchfiles import watch
from watchfiles.main import FileChange
from xonsh.built_ins import XSH


class WatchedModule:

    @staticmethod
    def watch_and_import(module_name: str, alias: str | None) -> "WatchedModule":
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:

            def cantfind():
                print("[red]💢 Can't find that module")
                exit(1)

            if "" in sys.path:
                cantfind()

            try_names = (f"{module_name}.py", f"{module_name}.xsh")
            files_in_this_dir = glob("*")
            found_it = False

            for file_name in try_names:
                print(file_name)
                if file_name in files_in_this_dir:
                    print(f"[yellow]found {file_name} in this directory")
                    print("[yellow]adding this directory to sys.path")

                    sys.path.insert(0, "")

                    try:
                        module = importlib.import_module(module_name)
                        found_it = True
                    except ModuleNotFoundError as e:
                        print("[red]💢 this module really doesn't want to be imported")
                        print(e)
                        exit(100)

                    break

            if not found_it:
                cantfind()

        XSH.ctx[alias or module_name] = module

        watched_module = WatchedModule(module)
        watched_module.start()

        return watched_module

    def __init__(self, module: ModuleType):
        self._module = module
        self._watcher: None | Generator[Set[FileChange], None, None] = None
        self._stop_token = threading.Event()
        self._thread: None | Thread = None

    def start(self):
        print(self._module.__file__)
        self._thread = Thread(target=self._watch_module)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        self._stop_token.set()
        self._thread.join(200)

    def _watch_module(self):
        for _ in watch(self._module.__file__, stop_event=self._stop_token):
            try:
                importlib.reload(self._module)
            except Exception:
                print("[red]Couldn't reload the module!")
