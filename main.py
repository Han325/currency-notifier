import requests
import smtplib
from email.mime.text import MIMEText

API_KEY = 'fca_live_R0QuH5Kq1ecVxIFexj2opz3SWQiP9AlmL3rWJnIw'
BASE_URL = f'https://api.freecurrencyapi.com/v1/latest?apikey={API_KEY}&currencies=GBP&base_currency=MYR'
THRESHOLD_RATE = 0.18

def get_exchange_rate():
    response = requests.get(BASE_URL)
    data = response.json()
    if response.status_code == 200 and 'data' in data and 'GBP' in data['data']:
        return data['data']['GBP']
    else:
        print('Error fetching exchange rate:', data)
        return None

def is_good_rate(rate):
    return rate <= THRESHOLD_RATE

def send_notification(rate):
    sender = 'currencyman520@gmail.com'
    receiver = 'yuhan1791@gmail.com'
    subject = 'Good Time to Convert MYR to GBP'

    amount_gbp = 100
    amount_myr = amount_gbp / rate
    
    html = f"""
    <html>
    <head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            color: #333;
            padding: 20px;
        }}
        .container {{
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #4CAF50;
        }}
        p {{
            font-size: 1.1em;
        }}
        .rate {{
            font-size: 1.5em;
            color: #4CAF50;
            font-weight: bold;
        }}
        .footer {{
            margin-top: 20px;
            text-align: center;
            font-size: 0.9em;
            color: #777;
        }}
    </style>
    </head>
    <body>
        <div class="container">
            <h1>Currency Exchange Alert</h1>
            <p>Dear User,</p>
            <p>The current exchange rate for <strong>MYR to GBP</strong> is:</p>
            <p class="rate">{rate}</p>
            <p>It's a good time to convert your Malaysian Ringgit to British Pounds!</p>
            <p>For example, to get <strong>100 GBP</strong>, you would need approximately <strong>{amount_myr:.2f} MYR</strong>.</p>
            <p>Best regards,<br/>Currency Exchange Monitor</p>
            <div class="footer">
                <p>This is an automated message. Please do not reply.</p>
            </div>
        </div>
    </body>
    </html>
    """

    msg = MIMEText(html, 'html')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, 'npkh rnco egzw hukw')
            server.sendmail(sender, receiver, msg.as_string())
            print('Notification sent!')
    except Exception as e:
        print(f'Failed to send email: {e}')


def main(request):
    rate = get_exchange_rate()
    if rate and is_good_rate(rate):
        is_good_rate(rate)
        print('Good rate:', rate)
        send_notification(rate)
    return 'Checked exchange rate.'

if __name__ == '__main__':
    main({})