# -*- coding: utf-8 -*-
from flybirds_airtest.cli.parser import get_parser


def main(argv=None):
    ap = get_parser()
    args = ap.parse_args(argv)
    if args.action == "info":
        from flybirds_airtest.cli.info import get_script_info
        print(get_script_info(args.script))
    elif args.action == "report":
        from flybirds_airtest.report.report import main as report_main
        report_main(args)
    elif args.action == "run":
        from flybirds_airtest.cli.runner import run_script
        run_script(args)
    elif args.action == "version":
        from flybirds_airtest.utils.version import show_version
        show_version()
    else:
        ap.print_help()


if __name__ == '__main__':
    main()
