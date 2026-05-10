# 🌤️ Serverless Weather Notifier

Automatically sends you a daily weather email every morning using AWS — no servers, no maintenance, completely free.

---

## How It Works

A scheduled AWS EventBridge rule triggers a Lambda function each morning. The function fetches weather data from the OpenWeatherMap API and emails it to you via Amazon SES.

```
EventBridge (daily schedule) → Lambda (fetch weather) → SES (send email)
```


## Quick Setup

1. **Get an API key** — Sign up free at [openweathermap.org](https://openweathermap.org) and copy your API key. *(Keys take up to 2 hours to activate.)*

2. **Verify emails in SES** — In the AWS console, go to **Simple Email Service → Verified Identities** and verify both your sender and receiver email addresses.

3. **Create a Lambda function** — Runtime: `Python 3.12`. Paste in the code from `lambda_function.py` and deploy.

4. **Add IAM permission** — Attach this policy to the Lambda's execution role:
   ```json
   {
     "Effect": "Allow",
     "Action": "ses:SendEmail",
     "Resource": "*"
   }
   ```

5. **Set environment variables** — In Lambda → Configuration → Environment variables:

   | Key | Example |
   |-----|---------|
   | `OPENWEATHER_API_KEY` | `your_api_key_here` |
   | `CITY` | `Islamabad,PK` |
   | `SENDER_EMAIL` | `me@example.com` |
   | `RECEIVER_EMAIL` | `me@example.com` |

6. **Add a trigger** — Add an EventBridge trigger with schedule `cron(0 3 * * ? *)` *(8:00 AM PKT daily).*

7. **Test it** — Hit the **Test** button in Lambda. Check your inbox.

---

## Sample Email

```
Daily Weather Update for Islamabad,PK
--------------------------------------
Temperature : 28°C
Condition   : Partly cloudy
Humidity    : 55%
```

---
