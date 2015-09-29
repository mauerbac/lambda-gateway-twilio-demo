#Lambda + API Gateway Example  

This example uses [Twilio](https://www.twilio.com/) to send an image from your mobile phone to AWS S3. Users send images using MMS to a Twilio phone number and Twilio processes the image by hitting an API Gateway Endpoint that fires a Lambda function. The app then returns a publicly assessable link to the image in S3. This app uses AWS Lambda, API Gateway, DynamoDB & S3 services. It is also severless!

##AWS Lambda

[Lambda](https://aws.amazon.com/lambda/) is a compute service that runs your code in response to events. Events can be triggered by resources in your AWS environment or via API Gateway. Here our Lambda function is triggered by an API Gateway endpoint that Twilio hits after an MMS is received. The Lambda function is responsible for writing user info to DynamoDB, writing image to S3 with meta data and returning a response to Twilio. 

##AWS API Gateway 
[API Gateway](https://aws.amazon.com/api-gateway/) is a fully managed API as a service where you can create, publish, maintain, monitor, and secure APIs at any scale. In this app, we use API Gateway to create an endpoint for Twilio to make a GET request. API Gateway transforms Twilio's URL encoded request into a JSON object, so that Lambda can accept it. Lastly, API Gateway takes Lambda's response and builds an XML object for Twilio. 

##AWS DynamoDB & S3
[DynamoDB](https://aws.amazon.com/dynamodb/) is Amazon's non-relational database services. This app leverages DynamoDB to store user data. [S3](https://aws.amazon.com/s3/) provides developers with object level storage that is endlessly scalable. We use S3 to store images received via MMS. 

#Usage 

Send an MMS to (650) 200-1944. 

![Example](https://s3-us-west-2.amazonaws.com/mauerbac-hosting/pic.png)

S3 Link: https://s3-us-west-2.amazonaws.com/mauerbac-selfie/ingest-images/19145824224/300007837449609.png


## Building the App

Step-by-step on how to configure, develop & develop this app on AWS.

### Create Credentials


##Troubleshooting
