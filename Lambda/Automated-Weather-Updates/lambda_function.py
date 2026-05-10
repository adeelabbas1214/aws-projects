import json
import os
import boto3
import urllib3

def lambda_handler(event, context):
    # 1. Configuration from Environment Variables
    api_key = os.environ['OPENWEATHER_API_KEY']
    city = os.environ['CITY']
    sender_email = os.environ['SENDER_EMAIL']
    receiver_email = os.environ['RECEIVER_EMAIL']
    region = os.environ['AWS_REGION']

    # 2. Fetch Weather Data
    http = urllib3.PoolManager()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = http.request('GET', url)
        data = json.loads(response.data.decode('utf-8'))
        
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        
        weather_report = (
            f"Good morning!\n\n"
            f"Today's weather in {city}:\n"
            f"- Temperature: {temp}°C\n"
            f"- Condition: {description.capitalize()}\n"
            f"- Humidity: {humidity}%\n\n"
            f"Have a great day!"
        )

        # 3. Send Email via SES
        ses = boto3.client('ses', region_name=region)
        ses.send_email(
            Source=sender_email,
            Destination={'ToAddresses': [receiver_email]},
            Message={
                'Subject': {'Data': f"Daily Weather Update: {city}"},
                'Body': {'Text': {'Data': weather_report}}
            }
        )
        
        return {"statusCode": 200, "body": "Email sent successfully!"}

    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": str(e)}
