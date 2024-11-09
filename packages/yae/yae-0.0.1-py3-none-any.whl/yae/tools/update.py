import yae.common.cli as cli


def run(args):
    pass


@cli.subparser(entry=run, name="update", description="update_desp", help="update_help")
def add_update_parser(parser):
    parser.add_argument('-i', "--index-url", type=str, required=False, help="target url")


def cli_main(argv=None):
    cli.run(argv, "update")


if __name__ == "__main__":
    cli_main()
