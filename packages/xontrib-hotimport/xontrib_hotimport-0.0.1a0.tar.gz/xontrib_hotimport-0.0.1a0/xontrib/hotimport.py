import atexit
from argparse import ArgumentParser

from rich import print
from xonsh.built_ins import XSH, XonshSession

from hotimport_core.watcher import WatchedModule

__all__ = ()


parser = ArgumentParser(
    prog="hotimport", description="Import a python module and automatically reload it"
)
parser.add_argument(
    "module", nargs="*", default=None, type=str, help="the name of the module"
)
parser.add_argument("--stop", default=False, action="store_true")

watched_modules: list[WatchedModule] = []


class Args:
    module: list[str]
    stop: bool


def _main(_args: list[str] = None):
    if _args:
        args: Args = parser.parse_args(_args)
    else:
        args: Args = parser.parse_args()

    module_arg = args.module

    # print(args)

    if len(module_arg) != 0 and args.stop:
        parser.print_help()
        exit(1)

    module_len = len(module_arg)

    if (
        (module_len == 0 and not args.stop)
        or module_len == 2
        or module_len > 3
        or (module_len == 3 and module_arg[1] != "as")
    ):
        print(
            "[red]💢 Incorrect syntax. Usage: [bold]hotimport module[/bold] or [bold]hotimport module as m[/bold]"
        )
        raise SystemExit()

    if args.stop:
        for module in watched_modules:
            module.stop()
            print(f"Stopped watching {module}")

        watched_modules.clear()
    else:
        module = WatchedModule.watch_and_import(
            module_arg[0], None if module_len < 3 else module_arg[2]
        )
        watched_modules.append(module)


def _stop_all():
    for module in watched_modules:
        module.stop()

    watched_modules.clear()


def _load_xontrib_(xsh: XonshSession, **kwargs) -> dict:
    atexit.register(_stop_all)

    XSH.aliases["hi"] = _main
    XSH.aliases["hotimport"] = _main

    return {}


def _unload_xontrib_(xsh: XonshSession, **kwargs) -> dict:
    _stop_all()
    atexit.unregister(_stop_all)

    del XSH.aliases["hotimport"]
    del XSH.aliases["hi"]
    return {}
