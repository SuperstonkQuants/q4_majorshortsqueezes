# TODO: Setup a python shebang that work with poetry interpreters across users
import argparse
import logging
import os

from q4_majorshortsqueezes.api import pull_data
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
                    "the tickers that satisfy all filter criteria.",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--tickers", nargs='+', required=True,
                        help="List of tickers to pull and analyze.")
    parser.add_argument("--start-date", default=None,
                        help="The start date for analyzing ticker data. "
                             f"By default the max available date range is used.")
    parser.add_argument("--filters", nargs='+', default=[],
                        help="A list of Python paths to python functions which each adhere to the "
                             "this interface: `List[Callable[[TickerHistory], bool]`.\n"
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
    return parser


def main():
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    parser = create_arg_parser()
    args = parser.parse_args()

    logging.info("Tickers: `%s`", ", ".join(args.tickers))
    logging.info("Start date: `%s`", args.start_date)
    logging.info("Filters: `%s`", " ".join(args.filters))
    logging.info("Output path: `%s`", args.output_path)

    logging.info("Start pulling and filtering tickers.")
    filtered_tickers = pull_data.main(args.tickers, args.start_date, args.filters)
    logging.info("Finished pulling and filtering tickers.")
    logging.info(f"The following tickers satisfied all filters: `%s`",
                 ", ".join(filtered_tickers.keys()))

    logging.info("Storing their historical price data now under: `%s`", args.output_path)
    for ticker, ticker_history in filtered_tickers.items():
        file_path = os.path.join(args.output_path, f"{ticker}.csv")
        with open(file_path, mode="w") as fd:
            ticker_history.to_csv(fd)


if __name__ == "__main__":
    main()
