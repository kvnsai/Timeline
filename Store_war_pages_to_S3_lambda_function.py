import json
import boto3
import os,re


s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')


def clean_str(input_string):
    return re.sub(r'[^a-zA-Z0-9]', '', input_string).lower()

def lambda_handler(event, context):
    # Fetch data from DynamoDB
    response = dynamodb.scan(TableName='TimelineTable')
    items = response['Items']
    
    # Iterate over each war
    for item in items:
        war_name = item['war_name']['S']
        war_html_content = generate_html_content(item)  # Generate HTML content for the war
        
        # Write HTML content to a file
        file_path = f'/tmp/{clean_str(war_name)}.html'
        with open(file_path, 'w') as file:
            file.write(war_html_content)
        
        # Upload the file to S3
        upload_to_s3(file_path, war_name)
    
    return {
        'statusCode': 200,
        'body': json.dumps('HTML pages created and uploaded to S3')
    }

def generate_html_content(item):
    # Extracting attributes from the item
    war_name = item['war_name']['S']
    duration = item['duration']['S']
    desc = item['description']['S']
    url = item['url']['S']
    video_url = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"

    # Generating HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{war_name}</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          margin: 0;
          padding: 0;
          background-color: #f2f2f2;
        }}
    
        .container {{
          max-width: 800px;
          margin: 0 auto;
          padding: 20px;
          background-color: #fff;
          box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
          border-radius: 8px;
        }}
    
        .header {{
          text-align: center;
          margin-bottom: 20px;
        }}
    
        .header h1 {{
          font-size: 36px;
          margin: 0;
          color: #333;
        }}
    
        .content {{
          display: flex;
          flex-wrap: wrap;
          justify-content: space-between;
          align-items: flex-start;
        }}
    
        img {{
          flex-shrink: 0;
          max-width: 400px; /* Changed to pixels for better responsiveness */
          margin: 0 auto; /* Centered the image */
        }}
    
        .description {{
          flex-grow: 1;
          margin-right: 20px;
        }}
    
        .description p {{
          color: #666;
        }}
    
        video {{
          max-width: 100%;
          height: auto;
          display: block;
          margin-top: 20px;
          border-radius: 8px;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>{war_name}</h1>
        </div>
        <div class="content">
          <div class="description">
            <p><strong>Duration:</strong> {duration}</p>
            <p>{desc}</p>
          </div>
          <img src="{url}" alt="{war_name}">
        </div>
        <video controls autoplay>
          <source src="{video_url}" type="video/mp4">
          Your browser does not support the video tag.
        </video>
      </div>
    </body>
    </html>

    """

    return html_content


def upload_to_s3(file_path, war_name):
    bucket_name = 'timeline-nsai'
    key = f'war_html/{clean_str(war_name)}.html'  # Specify the key (file path)
    s3.upload_file(file_path, bucket_name, key,ExtraArgs={'ContentType': 'text/html'})
    
