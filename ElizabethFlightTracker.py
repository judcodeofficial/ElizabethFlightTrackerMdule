import requests
from bs4 import BeautifulSoup
import argparse
import yagmail

def get_email_html(flights_info):
    email_html = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Email Template</title><style>body, h1, h2, p, table, th, td{margin:0;padding:0;border:0}body{background-color:#f4f4f4;font-family:Arial,sans-serif;line-height:1.6}.container{width:80%;margin:0 auto;background-color:#ffffff;padding:20px;border-radius:8px;box-shadow:0 0 10px rgba(0,0,0,0.1);margin-top:20px}h1{color:#333333}p{color:#666666}.btn{display:inline-block;padding:10px 20px;text-decoration:none;color:#ffffff;background-color:#007BFF;border-radius:5px}table{width:100%;border-collapse:collapse;margin-top:20px}th,td{border:1px solid #dddddd;padding:8px;text-align:left}th{background-color:#f2f2f2}@media screen and (max-width:600px){.container{width:100%;padding:10px}}</style></head><body><div class="container"><h1>Elizabeth flights tracker</h1><p><b>FLIGHT DATE: </b>' + flights_info['date'] + '</p><table><tr><th>Departure time</th><th>Arrival time</th><th>Price</th><th>Stops</th><th>Duration</th><th>Aeroline(s)</th><th>Description</th></tr>'
    for flight in flights_info['flights']:
        email_html += f"<tr><td>{flight['departure_time']}</td><td>{flight['arrival_time']}</td><td>{flight['flight_price']}</td><td>{flight['flight_stops_counter']}</td><td>{flight['flight_total_duration']}</td><td>{flight['flight_aerolines']}</td><td>{flight['flight_description']}</td></tr>"
    email_html += '</table></div></body></html>'
    return email_html

def send_email(subject, to_address, email_html, username, password):
    yag = yagmail.SMTP(username, password)
    email_contents = {'subject': subject, 'to': to_address, 'contents': email_html}
    yag.send(**email_contents)

def flight_crawler(url, username, password, to):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        flight_date = soup.find('input', class_='TP4Lpb eoY5cb j0Ppje').get('value', None)
        flights = soup.find_all('li', class_='pIav2d')

        flights_list = {'date': flight_date, 'flights': []}

        for flight in flights:
            departure_time = flight.find('div', class_='wtdjmc').get('aria-label')
            arrival_time = flight.find('div', class_='XWcVob').get('aria-label')
            flight_description = flight.find('div', class_='JMc5Xc').get('aria-label')
            flight_price = flight.find('div', class_='U3gSDe ETvUZc').find('span').string
            # General flight info
            flight_general_info = flight.find('div', class_='hF6lYb')
            flight_stops_counter = flight_general_info.find('span', class_='VG3hNb').string
            flight_total_duration = flight_general_info.find('span', class_='').string
            flight_aerolines = flight_general_info.find('span', class_='h1fkLb').string

            flights_list['flights'].append({
                "departure_time": departure_time,
                "arrival_time": arrival_time,
                "flight_description": flight_description,
                "flight_price": flight_price,
                "flight_stops_counter": flight_stops_counter,
                "flight_total_duration": flight_total_duration,
                "flight_aerolines": flight_aerolines
            })

        email_html = get_email_html(flights_list)
        send_email("Elizabeth tracker flights", to, email_html, username, password)
    except requests.RequestException as e:
        print(f"Error in requests: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Elizabeth flight tracker')
    parser.add_argument('url', type=str, help='Google flight URL with applied filters')
    parser.add_argument('username', type=str, help='Gmail username')
    parser.add_argument('password', type=str, help='Gmail password')
    parser.add_argument('to', type=str, help='Email that is gonna receive the details')

    args = parser.parse_args()
    flight_crawler(args.url, args.username, args.password, args.to)