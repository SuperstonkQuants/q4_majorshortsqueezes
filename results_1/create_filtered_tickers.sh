set -eo pipefail

# Store dir of this script since we want to put reports into it
BASEDIR=$(dirname "$0")
TICKER_COUNTS_UNFITLERED_FILE=$BASEDIR/unfiltered_ticker_counts.csv
echo "Replacing ticker file which stores the original unfiltered ticker counts: $TICKER_COUNTS_UNFITLERED_FILE"
echo "Exchange,Min Marketcap,Ticket Count" > $TICKER_COUNTS_UNFITLERED_FILE

for EXCHANGE in nyse nasdaq amex
do
    for MARKETCAP in 1000 100 10
    do
        # Update the unfiltered ticker count file based on the source repos
        SOURCE_DIR=./ticker_data__"$EXCHANGE"_min_"$MARKETCAP"m
        TICKER_COUNT=`ls $SOURCE_DIR | wc -l | tr -d ' '`
        echo "$EXCHANGE,$MARKETCAP,$TICKER_COUNT" >> $TICKER_COUNTS_UNFITLERED_FILE

        for MULTIPLIER in 2 3 5
        do
            for DAYS in 5 10
            do
                # Filter ticker data and keep the historical data of the relevant tickers.
                # This copies the historical price data to a lot of directories, and leaves the core data as-is.
                IDENTIFIER="$EXCHANGE"_min_"$MARKETCAP"_multi_"$MULTIPLIER"_days_"$DAYS"
                echo "Current step: $IDENTIFIER"

                OUTPUT_DIR=./ticker_data__"$IDENTIFIER"
                mkdir -p $OUTPUT_DIR
                poetry run python bin/pull_data.py -v --$EXCHANGE --min-market-cap=$MARKETCAP \
                  --ticker-source-dir $SOURCE_DIR --output-path $OUTPUT_DIR \
                  --filters q4_majorshortsqueezes.filter/price_multi_"$MULTIPLIER"_within_"$DAYS"_days >"$IDENTIFIER".log 2>&1
                # Create summaries/ ticker lists from log data
                grep INFO "$IDENTIFIER".log | grep -Eo '{"Ticker":.*}' | poetry run python $BASEDIR/transform_ljson_to_csv.py > $BASEDIR/"$IDENTIFIER".csv
            done
        done
    done
done
