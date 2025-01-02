import boto3
from PIL import Image, ImageDraw, ImageFont
import os
import io
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    source_bucket = "image-upload-bucket"
    destination_bucket = "processed-images-bucket"

    # Check if triggered by API Gateway
    if 'body' in event:
        body = event['body']
        data = base64.b64decode(body)
        key = "uploaded-image.jpg"
        
        # Upload image to source bucket
        s3.put_object(Bucket=source_bucket, Key=key, Body=data)
        return {"statusCode": 200, "body": "Image uploaded successfully"}

    # Otherwise, triggered by S3 event
    key = event['Records'][0]['s3']['object']['key']
    
    # Download image from source bucket
    response = s3.get_object(Bucket=source_bucket, Key=key)
    image_data = response['Body'].read()
    image = Image.open(io.BytesIO(image_data))
    
    # Process image: Resize and add watermark
    image = image.resize((300, 300))
    
    # Add watermark
    watermark_text = "© MyWatermark"
    watermark = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(watermark)
    
    # Load font (use a default PIL font)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    # Position watermark at the bottom right corner
    text_width, text_height = draw.textsize(watermark_text, font=font)
    position = (image.size[0] - text_width - 10, image.size[1] - text_height - 10)
    draw.text(position, watermark_text, fill=(255, 255, 255, 128), font=font)
    
    # Merge watermark with image
    watermarked_image = Image.alpha_composite(image.convert("RGBA"), watermark)
    
    # Save processed image to a buffer
    buffer = io.BytesIO()
    watermarked_image.convert("RGB").save(buffer, "JPEG")
    buffer.seek(0)
    
    # Upload processed image to destination bucket
    processed_key = f"processed-{key}"
    s3.upload_fileobj(buffer, destination_bucket, processed_key)
    
    return {"statusCode": 200, "body": "Image processed and watermarked successfully"}
