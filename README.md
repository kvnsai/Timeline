## Historical Events Timeline

This project creates a timeline of historical events and presents it on a webpage deployed using AWS Lambda. The event details are stored in a DynamoDB table, and images related to the events are stored in an S3 bucket.

### Deployment

1. **DynamoDB **: Store event details in a DynamoDB table named `TimelineTable`.

2. **S3 Bucket**: Upload images related to historical events to an S3 bucket. Ensure the bucket is configured for public access if displaying images on a public webpage. Users load static content from here. Web pages with further details are also hosted from here.

3. **Lambda **: Write a Python Lambda function that retrieves data from DynamoDB and generates HTML content for the timeline. Insert image URLs dynamically from S3 into the HTML. Another lambda Function to insert html file corresponding to each war into S3 bucket  

4. **API Gateway**: Attach an API Gateway function to AWS Lambda for fetching timelines. 

### HTML & CSS Credits

The HTML and CSS templates for the timeline layout are sourced from [Slider Revolution](https://www.sliderrevolution.com/resources/css-timeline/).

### Example Usage

To view the timeline, visit [Webpage URL](https://f29c23hkj0.execute-api.us-east-1.amazonaws.com/TimelineLambda).


  ![Image Description](https://github.com/kvnsai/Timeline/blob/main/TimelineDeployment.png?raw=true)
