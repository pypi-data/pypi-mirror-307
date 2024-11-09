import argparse
import functools


_parser = argparse.ArgumentParser(prog="yae", usage='%(prog)s <command> [options]',
                                  description="The DevOps Toolbox")
_sub_parsers = _parser.add_subparsers(title="Sub Commands", dest="command", prog="action_prog",
                                      metavar="command",
                                      description="use 'dot <command> -h' to show help of sub command")
_command_map = {}
_parser_map = {}


def subparser(entry, name, description=None, prog=None, help=None):

    def decorator(func):
        global _parser, _command_map, _parser_map
        inner_prog = prog if prog is not None else "yae " + name
        inner_help = help if help is not None else description
        subparser_ = _sub_parsers.add_parser(name=name, prog=inner_prog, description=description, help=inner_help)
        func(subparser_)
        parser_ = argparse.ArgumentParser(prog=prog, description=description)
        func(parser_)
        _parser_map[name] = parser_
        _command_map[name] = entry

        @functools.wraps(func)
        def wrapper(parser):
            return func(parser)

        return wrapper

    return decorator


def parse_args(argv=None, command=None):
    global _parser, _parser_map
    parser = _parser if command is None else _parser_map.get(command)
    if parser is None:
        print("Unknown command: " + command)
        _parser.print_help()
    return parser.parse_args(argv)


def run(argv=None, command=None):
    global _command_map, _parser_map, _parser
    args = parse_args(argv, command)
    if args.command is None:
        _parser.print_help()
    else:
        _command_map[args.command](args)
