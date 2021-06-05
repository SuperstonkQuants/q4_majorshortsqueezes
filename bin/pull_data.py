# TODO: Setup a python shebang that work with poetry interpreters across users
import argparse
import logging
import os
from typing import Set

from q4_majorshortsqueezes.api import pull_data
from q4_majorshortsqueezes.ticker import retrieve_tickers_with_get_all_tickers_package
from q4_majorshortsqueezes import filter


def dir_path(path):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f"{path} does not exist")

    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"{path} is not a valid dir")

    return path


def create_arg_parser():
    parser = argparse.ArgumentParser(
        description="Pull data for all given tickers and write the price data into files for "
                    "the tickers that satisfy all filter criteria.\n"
                    "There are various options to set the tickers to download. "
                    "All of them can be used together and the script will "
                    "internally create a single set of all determined tickers.",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--tickers", nargs='+', default=[],
                        help="List of tickers to pull and analyze.")
    parser.add_argument("--nyse", action="store_true",
                        help="Pull all nyse tickers.")
    parser.add_argument("--nasdaq", action="store_true",
                        help="Pull all nasdaq tickers.")
    parser.add_argument("--amex", action="store_true",
                        help="Pull all amex tickers.")
    parser.add_argument("--min-market-cap", default="0",
                        help="Minimum market cap of tickers (in million USD). "
                             "This does not apply to tickers set with `--tickers`.")
    parser.add_argument("--ticker-source-dir", type=dir_path, default=None,
                        help="Load tickers from the given dir if it is available. "
                             "The script expects the following naming schema: `<ticker>.csv`.\n"
                             "If a ticker is not found in the directory, it is downloaded "
                             "as fallback.")
    parser.add_argument("--start-date", default=None,
                        help="The start date for analyzing ticker data. "
                             "By default the max available date range is used. "
                             "This has only effect on newly downloaded tickers (,not csv loaded).")
    parser.add_argument("--filters", nargs='+', default=[],
                        help="A list of Python paths to python functions which each adhere to the "
                             "this interface: `List[Callable[[Ticker], bool]`.\n"
                             "The path format for a criterion function is: "
                             "`full.qualified.path.to.module/func_name`.\n\n"
                             "Predefined filters are available under: "
                             f"`{filter.__name__}`.\n\n"
                             "To filter for tickers that have in the past doubled their "
                             "value in 5 consecutive trading dates use this predefined filter:\n"
                             f"`{filter.__name__}.double_price_within_a_week`.")
    parser.add_argument("--output-path", required=True, type=dir_path,
                        help="The script serializes the ticker price history data to this path.\n"
                             "The file are stored as `csv` with the following naming scheme: "
                             "`<ticker_name>.csv`.\n"
                             "Careful! The script will override existing files!")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Activates debug log level.")
    return parser


def determine_tickers(args: argparse.Namespace) -> Set[str]:
    tickers = set()
    if args.nyse or args.nasdaq or args.amex:
        logging.info("Start pulling ticker symbols with `get_all_tickers` package.")
        tickers = retrieve_tickers_with_get_all_tickers_package(nyse=args.nyse,
                                                                nasdaq=args.nasdaq,
                                                                amex=args.amex,
                                                                min_market_cap=int(args.min_market_cap))
        logging.info("Retrieved %s ticker symbols.", len(tickers))
        logging.debug("Retrieved ticker symbols: %s", ", ".join(sorted(tickers)))
    else:
        if args.min_market_cap:
            logging.warning("Option `--min-market-cap` has no effect. "
                            "Need to set at least one of the following options: "
                            "`--nyse`, `--nasdaq`, `--amex`")

    tickers = tickers.union(set(args.tickers))
    logging.info("%s tickers to process.", len(tickers))
    logging.debug("List of tickers to process: %s", ", ".join(sorted(tickers)))
    return tickers


def main():
    # Parse args
    parser = create_arg_parser()
    args = parser.parse_args()
    # Setup logging
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG if args.verbose else logging.INFO)
    # Log important inputs
    logging.info("Tickers: `%s`", ", ".join(args.tickers))
    logging.info("Start date: `%s`", args.start_date)
    logging.info("Filters: `%s`", " ".join(args.filters))
    logging.info("Output path: `%s`", args.output_path)
    # Determine tickers
    tickers = determine_tickers(args)
    # Pull data
    logging.info("Start pulling and filtering tickers.")
    filtered_tickers = pull_data.main(tickers=tickers,
                                      start_date=args.start_date,
                                      criterion_paths=args.filters,
                                      csv_dir_path=args.ticker_source_dir,
                                      csv_output_dir_path=args.output_path)
    logging.info("Finished pulling and filtering tickers.")
    logging.info(f"The following tickers satisfied all filters: `%s`",
                 ", ".join(filtered_tickers.get_tickers()))


if __name__ == "__main__":
    main()
