import requests
import random
import time
from data_processing_functions import Line_Names, get_instrument_prices, get_instrument_SMA, Prices
import pandas
import pickle
import os

#Very simple example to demonstrate usage of the API.

team_name = 'The_Sexy_Yodellers_Lazarus_Project'
password = 'abcdef'
# team_name = 'The_Sexy_Yodellers_Lazarus_Project'.upper()
# password = 'abcdef'.upper()

print(f'team_name = The_Sexy_Yodellers_Lazarus_Project')
print(f'password = abcdef')

# create_res = requests.post('http://egchallenge.tech/team/create', json={'team_name': team_name, 'password': 'password'}).json()
# print(create_res)

login_res = requests.post('http://egchallenge.tech/team/login', json={'team_name': team_name, 'password': 'password'}).json()
print(login_res)

token = login_res['token']
print(f'token = {token}')

last_epoch = None

all_ids = list(range(1, 501))
Sym_List = Line_Names(all_ids)

# if os.path.exists("prices.txt"):
#     stream = open("prices.txt", "rb")
#     prices = pickle.load(stream)
#     stream.close()
# else:
    # prices = Prices(all_ids, Sym_List)
#     stream = open("prices.txt", "wb+")
#     pickle.dump(prices, stream)
#     stream.close()

# prices = Prices(all_ids, Sym_List)
prices = pandas.read_pickle("lazarus.txt")

amsterdam = 0

while True:
    epoch_res = requests.get('http://egchallenge.tech/epoch').json()
    current_epoch = epoch_res['current_epoch']
    prediction_epoch = epoch_res['prediction_epoch']
    timestamp = epoch_res['unix_timestamp']

    print(f'current_epoch = {current_epoch}, prediction_epoch = {prediction_epoch}')

    # We will just submit prediction of -1 * prev return.
    # In a real submission you would probably use a model that you have pre-trained
    # elsewhere.

    marketdata = requests.get('http://egchallenge.tech/marketdata/latest').json()
    predictions = []
    for md in marketdata:
        if md['is_trading']:
            ID = md['instrument_id']
            zero_based_index = ID - 1
            Symbol = Sym_List[zero_based_index]
            Price = md['price']

            prices[Symbol][current_epoch] = Price
            price_list = prices[Symbol]

            moving_average, standard_deviation, exp_average, exp_std_dev, autocorre = get_instrument_SMA(price_list, (current_epoch % 60) + 1)

            last_moving_average = moving_average[list(moving_average.keys())[-1]]
            # last_moving_average = exp_average
            last_moving_standard_deviation = standard_deviation[list(standard_deviation.keys())[-1]]
            # last_moving_standard_deviation = exp_std_dev

            if last_moving_average == 0:
                last_moving_average = Price
                print("Had to correct LMA...")

            predicted_return = (((last_moving_average + exp_average) / 2) / Price) * md["epoch_return"] * (((exp_std_dev + last_moving_standard_deviation) / 2) / last_moving_average) * ((autocorre + 1) / 2)

            if zero_based_index < 3:
                print(Price)
                print("LMA: " + str(last_moving_average))
                print("LMSD: " + str(last_moving_standard_deviation))
                print(predicted_return)
                print(autocorre)

            predictions.append({
                'instrument_id': ID,#md['instrument_id'],
                'predicted_return': predicted_return
            })

            if zero_based_index == len(md):
                amsterdam = predicted_return

    pred_req = {'token': token, 'epoch': prediction_epoch, 'predictions': predictions}
    pred_res = requests.post('http://egchallenge.tech/predict', json=pred_req)
    print(f'Submitted {len(predictions)} predictions for epoch {prediction_epoch}')

    # Now get our scores for prior predictions
    scores_req = {'token': token}
    scores_res = requests.get('http://egchallenge.tech/scores', json=scores_req).json()
    for score in scores_res:
        epoch = score['epoch']
        sse = score['sse']
        print(f'epoch = {epoch}, sse = {sse}')

        if score == current_epoch - 1:
            print(scores_res[len(scores_res)-1]["sse"] / scores_res[len(scores_res)-2]["sse"])
        

    next_epoch_in = max(60.0 - (time.time() - timestamp), 0) + 1.0
    print(f'next epoch in {next_epoch_in} sec. Sleeping...')
    time.sleep(next_epoch_in)
