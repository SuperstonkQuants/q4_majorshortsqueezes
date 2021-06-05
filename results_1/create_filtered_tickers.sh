for EXCHANGE in nyse nasdaq amex
do
    for MARKETCAP in 1000 100
    do
        for MULTIPLIER in 2 3
        do
            for DAYS in 5 10
            do
                # Filter ticker data and keep the historical data of the relevant tickers.
                # This copies the historical price data to a lot of directories, and leaves the core data as-is.
                IDENTIFIER="$EXCHANGE"_min_"$MARKETCAP"_multi_"$MULTIPLIER"_days_"$DAYS"
                echo $IDENTIFIER
                OUTPUT_DIR=./ticker_data__"$IDENTIFIER"
                mkdir $OUTPUT_DIR
                poetry run python bin/pull_data.py -v --$EXCHANGE --min-market-cap=$MARKETCAP \
                  --ticker-source-dir ./ticker_data__"$EXCHANGE"_min_"$MARKETCAP"m --output-path $OUTPUT_DIR \
                  --filters q4_majorshortsqueezes.filter/price_multi_"$MULTIPLIER"_within_"$DAYS"_days >"$IDENTIFIER".log 2>&1
                # Create summaries/ ticker lists from log data
                BASEDIR=$(dirname "$0")
                grep -Eo '{.*}' "$IDENTIFIER".log | poetry run python $BASEDIR/transform_ljson_to_csv.py > $BASEDIR/"$IDENTIFIER".csv
            done
        done        
    done
done
