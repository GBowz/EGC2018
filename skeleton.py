#import pip
import requests
#import random
#import string
import time
#import EGC2018
from EGC2018 import Line_Names, get_instrument_prices, get_instrument_SMA

#Very simple example to demonstrate usage of the API.

team_name = 'Sexy_Yodellers'.upper()
password = 'abcdef'.upper()

print(f'team_name = Sexy_Yodellers')
print(f'password = abcdef')

#create_res = requests.post('http://egchallenge.tech/team/create', json={'team_name': team_name, 'password': 'password'}).json()
#print(create_res)

login_res = requests.post('http://egchallenge.tech/team/login', json={'team_name': team_name, 'password': 'password'}).json()
print(login_res)

token = login_res['token']
print(f'token = {token}')

last_epoch = None

Sym_List = Line_Names(list(range(500)))

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
            Symbol = Sym_List[ID]
            Price = md['price']
            
            predictions.append({
                'instrument_id': ID,#md['instrument_id'],
                'predicted_return': -0.417795 * md['epoch_return']
            })

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

    next_epoch_in = max(60.0 - (time.time() - timestamp), 0) + 1.0
    print(f'next epoch in {next_epoch_in} sec. Sleeping...')
    time.sleep(next_epoch_in)
