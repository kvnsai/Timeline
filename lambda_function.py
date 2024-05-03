import json
import boto3

client = boto3.client('dynamodb')


def lambda_handler(event, context):
    data = client.scan(TableName='TimelineTable')
    
    data1 = ExtractData(data)
    
    
    
    response = {
        'statusCode' : 200,
        'body': data1,
        'headers' : {
            'Content-Type' : 'text/html',
            'Access-Control-Allow-Origin' : '*'
        },
    }
    
    return response
    
def ExtractData(data):
    rows = data["Items"]  
    
    html_content = open('head.html','r').read()
    
    for row in rows:
        war = row["war_name"]["S"]
        dur = row["duration"]["S"]
        u = row["url"]["S"]
        
        html_content += f"""
            <h2 class='timeline__item timeline__item--year'>{war}</h2>
            <div class='timeline__item'>
                <h3 class='timeline__title'>{dur}</h3>
                <p><img src='{u}' alt='{war}' style='width: 3in; '></p>
            </div>
        """
    
    html_content += open('tail.html','r').read()
    
    return html_content
