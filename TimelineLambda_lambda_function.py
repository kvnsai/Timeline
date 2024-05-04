import json, re, boto3
from datetime import datetime

client = boto3.client('dynamodb')

def clean_str(input_string):
    return "?war=" + re.sub(r'[^a-zA-Z0-9]', '', input_string).lower()
    

def html_str(input_string):
    return 'http://timeline-nsai.s3-website-us-east-1.amazonaws.com/war_html/'+re.sub(r'[^a-zA-Z0-9]', '', input_string).lower()+'.html'

def lambda_handler(event, context):

    if 'queryStringParameters' in event and 'timeline' in event['queryStringParameters']:
        timeline_type = event['queryStringParameters']['timeline']
        if timeline_type == 'horizontal':
            data = client.scan(TableName='TimelineTable')
            html_content = ExtractDataHorizontal(data)
        elif timeline_type == 'vertical':
            data = client.scan(TableName='TimelineTable')
            html_content = ExtractDataVertical(data)
        else:
            html_content = "<h1>Invalid timeline type specified</h1>"
            
    elif 'queryStringParameters' in event and 'war' in event['queryStringParameters']:
        war_type = event['queryStringParameters']['war']
        response = {
            'statusCode': 302,  
            'headers': {'Content-Type': 'text/html',
                        'Location': f'https://timeline-nsai.s3.amazonaws.com/war_html/{clean_str1(warName)}.html'
                        }
                    }
      
    else:
        html_content = open('index.html', 'r').read()
        
    response = {
        'statusCode': 200,
        'body': html_content,
        'headers': {
            'Content-Type': 'text/html',
            'Access-Control-Allow-Origin': '*'
        }
    }

    return response

def ExtractDataHorizontal(data):
  
    uns_rows = data["Items"]  # Corrected accessing "Items" key
    
    rows =  sorted(uns_rows, key=lambda x: x.get('duration', {}).get('S', ''), reverse=False)
    
    head_content = open('head.html','r').read()
    
    mid_content = open('mid.html','r').read()
    
    for idx, row in enumerate(rows):
        war = row["war_name"]["S"]
        dur = row["duration"]["S"]
        u = row["url"]["S"]
        desc = row["description"]["S"]
        
        if idx == 0:
            head_content += f"""
            <li><a href="#0" data-date="01/01/{dur.split('-')[0]}" class="cd-h-timeline__date cd-h-timeline__date--selected"> <p>{war}</p> <p>{dur}</p> </a></li>
            """
            mid_content += f"""
            <li class="cd-h-timeline__event cd-h-timeline__event--selected text-component">
              <div class="cd-h-timeline__event-content container">
                <h2 class="cd-h-timeline__event-title"><a href="{html_str(war)}" style="text-decoration: none; color: blue;">{war}</a></h2>
                <em class="cd-h-timeline__event-date">{dur}</em>
                <p class="cd-h-timeline__event-description color-contrast-medium"> 
                  {desc}
                  <img src='{u}' alt='' style='width: 3in; '> 
                </p>
              </div>
            </li>
            """
            
        else:
            head_content += f"""
            <li><a href="#0" data-date="01/01/{dur.split('-')[0]}" class="cd-h-timeline__date"> <p>{war}</p> <p>{dur}</p> </a></li>
            """
            mid_content += f"""
            <li class="cd-h-timeline__event text-component">
              <div class="cd-h-timeline__event-content container">
                <h2 class="cd-h-timeline__event-title"><a href="{html_str(war)}" style="text-decoration: none; color: blue;">{war}</a></h2>
                <em class="cd-h-timeline__event-date">{dur}</em>
                <p class="cd-h-timeline__event-description color-contrast-medium"> 
                  {desc}
                  <img src='{u}' alt='' style='width: 3in; '>  
                </p>
              </div>
            </li>
            """
          
    today_mid_content = f"""
            <li class="cd-h-timeline__event text-component">
              <div class="cd-h-timeline__event-content container">
                <p class="cd-h-timeline__event-description color-contrast-medium"> 
                  These were  some of the infamous wars.   
                </p>
              </div>
            </li>
            """
   
    today_content =  f"""
            <li><a href="#0" data-date="{datetime.today().strftime('%m/%d/%Y')}"  class="cd-h-timeline__date"><p>Today</p></a></li>
            """
    
    html_content =  head_content + today_content + mid_content + today_mid_content + open('tail.html','r').read()
    
    return html_content
    
def ExtractDataVertical(data):
  uns_rows = data["Items"]  
  rows =  sorted(uns_rows, key=lambda x: x.get('duration', {}).get('S', ''), reverse=True)

  html_content = open('head_v.html','r').read()

  for idx,row in enumerate(rows):
      war = row["war_name"]["S"]
      dur = row["duration"]["S"]
      u = row["url"]["S"]
      desc = row["description"]["S"]
     
      html_content += f"""
          <h2 class='timeline__item timeline__item--year'> <a href={html_str(war)}> {war} </a></h2>
          <div class='timeline__item'>
              <div class="container"> <h3 class='timeline__title'>{dur}</h3> <img src='{u}' alt='{war}' style='width: 2in;'> <p> {desc} </p></div>
          </div>
      """
      
  html_content += open('tail.html','r').read()

  return html_content
  
