import boto3
from fpdf import FPDF
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def lambda_handler(event, context):
    try:
        # Generate the PDF report
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Daily Report", ln=True, align="C")
        pdf.cell(200, 10, txt="This is your automated report.", ln=True)
        
        # Save the PDF
        report_path = "/tmp/daily_report.pdf"
        pdf.output(report_path)

        # Upload to S3 (Optional)
        s3 = boto3.client('s3')
        bucket_name = "daily-reports-s3-bucket"
        s3.upload_file(report_path, bucket_name, "daily_report.pdf")

        # Send email via SES with attachment using raw email
        ses = boto3.client('ses')
        msg = MIMEMultipart()
        msg['From'] = "adeelabbasad@gmail.com"  # Replace with your SES verified email
        msg['To'] = "contectwithadeel@gmail.com"  # Replace with recipient email
        msg['Subject'] = "Daily Report"

        # Attach the text body
        body = MIMEText("Please find the attached report.", 'plain')
        msg.attach(body)

        # Attach the PDF report
        with open(report_path, 'rb') as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(report_path)}')
            msg.attach(part)

        # Send the email using SES's send_raw_email
        response = ses.send_raw_email(
            Source=msg['From'],
            Destinations=[msg['To']],
            RawMessage={'Data': msg.as_string()}
        )

        return {"status": "success", "response": response}

    except Exception as e:
        return {"status": "error", "message": str(e)}
