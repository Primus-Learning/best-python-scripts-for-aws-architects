import boto3

AWS_ACCESS_KEY_ID = "replace with your keys"
AWS_SECRET_ACCESS_KEY = "replace with your secret access key"
AWS_REGION = 'us-east-1'

def send_email_sns_ses(subject, message, recipient):
    sns = boto3.client('sns', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)
    ses = boto3.client('ses', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)

    topic_response = sns.create_topic(Name='email-topic')
    topic_arn = topic_response['TopicArn']
    
    email_body = "This is a test email sent from Amazon SNS and SES"
    email_subject = "Test Email from SNS and SES"
    email_from = "your email" #replace with your verified email

    ses_response = ses.send_email(
        Source=email_from,
        Destination={
            'ToAddresses': [
                recipient,
            ]
        },
        Message={
            'Subject': {
                'Data': subject
            },
            'Body': {
                'Text': {
                    'Data': message
                }
            }
        }
    )

    sns.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject=subject
    )

    print("Email sent successfully!")

if __name__ == "__main__":
    send_email_sns_ses('Test Email', 'Hello, This is Primuslearning and it is a test email sent using Amazon SNS and SES', 'replace with your verified email')
