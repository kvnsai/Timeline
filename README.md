## Historical Events Timeline

This project creates a timeline of historical events and presents it on a webpage deployed using AWS Lambda. The event details are stored in a DynamoDB table, and images related to the events are stored in an S3 bucket.

### Deployment

1. **DynamoDB Setup**: Store event details in a DynamoDB table named `TimelineTable`.

2. **S3 Bucket**: Upload images related to historical events to an S3 bucket. Ensure the bucket is configured for public access if displaying images on a public webpage. Users load static content from here.

3. **Lambda Function**: Write a Python Lambda function that retrieves data from DynamoDB and generates HTML content for the timeline. Insert image URLs dynamically from S3 into the HTML. Another lambda Function to insert html file corresponding to each war into S3 bucket  

4. **Deploy Lambda**: Deploy the Lambda function on AWS Lambda with appropriate permissions to access DynamoDB and S3.

### HTML & CSS Credits

The HTML and CSS templates for the timeline layout are sourced from [Slider Revolution](https://www.sliderrevolution.com/resources/css-timeline/).

### Example Usage

To view the timeline, visit [Webpage URL](https://f29c23hkj0.execute-api.us-east-1.amazonaws.com/TimelineLambda).


  ![Image Description](https://timeline-nsai.s3.amazonaws.com/TimelineDeployment.png)
