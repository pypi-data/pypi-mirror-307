import yae.common.cli as cli


def run(args):
    pass


@cli.subparser(entry=run, name="install", description="install_desp", help="install_help")
def add_update_parser(parser=None):
    parser.add_argument('-e', "--extra-url", type=str, required=False, help="extra target url")


def cli_main(argv=None):
    cli.run(argv, "install")


if __name__ == "__main__":
    cli_main()