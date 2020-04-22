from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import json, requests
from .models import Coins
from .forms import CoinsForm

from django.http import JsonResponse


# Create your views here.
def home_page(request):

    #Grabs Bitcoin values
    price_requests = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,XRP,USDT,BCH,BSV,LTC,BNB,EOS,XTZ&tsyms=INR")
    price = json.loads(price_requests.content)

    coins = ['Bitcoin', 'Ethereum', 'XRP', 'Bitcoin Cash', 'EOS', 'Litecoin', 'Stellar', 'Cardano', 'Tether', 'IOTA']
    table_data = dict()
    sub_dic = dict()

    #Changing the key values in dictionary for the table data
    price['DISPLAY']['Bitcoin'] = price['DISPLAY'].pop('BTC')
    price['DISPLAY']['Ethereum'] = price['DISPLAY'].pop('ETH')
    price['DISPLAY']['XRP'] = price['DISPLAY'].pop('XRP')
    price['DISPLAY']['Tether'] = price['DISPLAY'].pop('USDT')
    price['DISPLAY']['Bitcoin Cash'] = price['DISPLAY'].pop('BCH')
    price['DISPLAY']['Bitcoin SV'] = price['DISPLAY'].pop('BSV')
    price['DISPLAY']['Litecoin'] = price['DISPLAY'].pop('LTC')
    price['DISPLAY']['EOS'] = price['DISPLAY'].pop('EOS')
    price['DISPLAY']['Binance Coin'] = price['DISPLAY'].pop('BNB')
    price['DISPLAY']['Tezos'] = price['DISPLAY'].pop('XTZ')

    #Preparing for charts
    labels, data = [], []   #data = MArket Capital
    for key, value in price['DISPLAY'].items():
        labels.append(key)
        data.append(value['INR']['MKTCAP'])

    #Converting the data(price value) from international to floating numbers
    from re import sub
    from decimal import Decimal

    market_capital = []
    for value in data :
        money = Decimal(sub(r'[^\d.]', '', value))
        market_capital.append(float(money))

    #Grabs News 
    api_requests = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
    api = json.loads(api_requests.content)

    return render( request, 'home.html', { 'api' : api, 'price': price, 'labels' : labels, 'market_capital' : market_capital })


def prices(request):
    if request.method == 'POST':
        search_box =  request.POST['search_box']
        search_box = search_box.upper()
        search_requests = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + search_box + "&tsyms=INR")
        search = json.loads(search_requests.content)

        return render(request, 'prices.html', { 'search_box' : search_box, 'search' : search })

    else :
        not_found = " Enter the string from above......!!!"
        return render(request, 'prices.html', {'not_found' : not_found })

def allCoin(request):
    api_key = '0949e8c49eefb5714246665f93e742f2f673da6db3358863c05814e095a69dc3'
    
    all_data = requests.get("https://min-api.cryptocompare.com/data/all/coinlist")
    all_data = json.loads(all_data.content)


    #print()
    #print()
    #print('--------------------------------------------------------------------')
    #print('Coin_name\tFull_name')


    #Saving all the coins to the db
    #for key, value in all_data['Data'].items():
    #    f_name = value['CoinName']
    #    c_name = value['Symbol']
    #    Coin_obj = Coins(coin_name = c_name, full_name = f_name)
    #    Coin_obj.save()
    #    print(c_name +'\t'+f_name)    
    return render(request, 'all_coins.html', { 'all_data' : all_data })


def search_auto(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    coins = Coins.objects.filter(coin_name__icontains=q)
    results = []
    for cn in coins:
      coins_json = {}
      coins_json = cn.coin_name
      results.append(coins_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)