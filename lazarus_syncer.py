# lazarus_syncer.py
# Author: Jordan Peters (Rollersteaam)
# Purpose: Bot that constantly synchronises a text file with information
# about the stock market.
#
# Should be used in conjunction with a bot that will read it and store the
# values as the history of stock market prices so far (most likely on
# initialization).

import requests
import pandas
import datetime
import os
import time
import timeit

def get_symbol_map():
    """
    Constructs a dictionary mapping instrument ID to instrument symbol.

    Returns:
        (dict) Maps instrument ID to instrument symbol.
    """
    package = {}
    all_instruments = requests.get(
        "http://egchallenge.tech/instruments").json()

    for instrument in all_instruments:
        package[instrument["id"]] = instrument["symbol"]

    return package


def get_all_prices(symbol_map):
    """
    Gets all prices from the stock market.

    Args:
        symbol_map (dict): A dictionary mapping instrument ID to symbol.

    Returns:
        (DataFrame) Column: Symbol, Row: {Epoch : Price}
        (float) Average execution time of json requests.
    """
    constructed_data_frame = []
    average_execution_time = 0

    for instrument_id in range(1, 501):
        before_execution_time = time.clock()
        id_data = requests.get(
            f"http://egchallenge.tech/marketdata/instrument/{instrument_id}").json()
        execution_time = time.clock() - before_execution_time
        average_execution_time += execution_time

        instrument_symbol = symbol_map[instrument_id]

        id_prices = pandas.DataFrame(
            {instrument_symbol: pandas.DataFrame(id_data)["price"]})

        constructed_data_frame.append(id_prices)

    average_execution_time /= 500
    return pandas.DataFrame(constructed_data_frame), average_execution_time


def synchronise():
    """
    Synchronises lazarus.txt with all data from every single instrument.

    Returns:
        (float) Average execution time of JSON requests.
    """
    price_database, average_execution_time = get_all_prices(get_symbol_map())
    price_database.to_pickle("lazarus.txt")
    return average_execution_time


def countdown_synchronisation(time_until_sync, last_sync_timestamp:datetime.datetime, time_taken_sync, average_execution_time):
    """
    Performs the countdown operation.

    Args:
        time_until_sync (int): The amount of seconds until it should synchronise.
            Will take away 1 every call, returning the final value.
        last_sync_timestamp (datetime): The date time of the last sync timestamp.
        time_taken_sync (float): The amount of seconds taken to synchronise last time.
        average_execution_time (float): The average execution time of JSON requests.

    Returns:
        (int) The amount of seconds until it should synchronise.
    """
    os.system("cls")
    print("\033[1;32;40mLazarus Syncer")
    print("\033[3;33;40mTo be engulfed in fear is to be unconscious of the past.")
    print("\033[0;37;40m")
    print(f"Lazarus last synchronised at \033[0;34;40m{last_sync_timestamp}\033[0;37;40m")
    if time_until_sync <= 0:
        estimated_additional_seconds = last_sync_timestamp + datetime.timedelta(seconds=time_taken_sync) if last_sync_timestamp != None else datetime.datetime.now() + datetime.timedelta(seconds=150)
        print(f"Lazarus is likely to synchronise at \033[0;32;40m{estimated_additional_seconds}")
        print("\033[0;32;40mSynchronising...\033[0;37;40m")
    else:
        print(f"Time until next synchronisation... \033[0;34;40m{time_until_sync}s\033[0;37;40m")
    print(f"Time taken for last synchronisation... \033[0;34;40m{time_taken_sync}s\033[0;37;40m")
    print(f"Time taken on average for one JSON request... \033[0;34;40m{average_execution_time}s\033[0;37;40m")
    time.sleep(1)
    time_until_sync -= 1
    return time_until_sync


if __name__ == "__main__":
    # Flag
    should_synchronise = False

    default_time_until_sync = 3
    time_until_sync = 3
    last_sync_timestamp = None
    before_sync_timestamp = None
    average_execution_time = None

    time_taken_sync = None
    while True:
        try:
            if should_synchronise:
                before_sync_timestamp = datetime.datetime.now()
                average_execution_time = synchronise()
                should_synchronise = False
                time_until_sync = default_time_until_sync
                last_sync_timestamp = datetime.datetime.now()
                time_taken_sync = (last_sync_timestamp - before_sync_timestamp).total_seconds()
            else:
                time_until_sync = countdown_synchronisation(time_until_sync, last_sync_timestamp, time_taken_sync, average_execution_time)
                if time_until_sync < 0:
                    should_synchronise = True
        except Exception as ex:
            print(f"\033[0;37;40mException raised: {ex}")
            print(f"Exception raised: {ex}")
            print(f"Exception raised: {ex}")
            print("\033[1;31;40mRestarting Lazarus after 5 seconds...\033[0;37;40m")
            time.sleep(5)