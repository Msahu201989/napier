import json
import socket
import boto3
import os
from boto3.dynamodb.conditions import Key

def send_html_email(loadBalancer, oldIPAddress, newIPAddress):
    ses_client = boto3.client("ses", region_name="us-east-1")
    CHARSET = "UTF-8"

    # Email content based on load balancer
    if "internal-App-Tab-Load-Balancer-947233963.us-east-1.elb.amazonaws.com" in loadBalancer:
        HTML_EMAIL_CONTENT = f"""
<html>
<head></head>
<body>
    <p style='text-align:left;'>Hi Team,</p>
    <p><strong>Please note that one of the internal application’s load balancer IP has changed from {oldIPAddress}</strong> to <strong>{newIPAddress}</strong>. Please make the changes accordingly on the Kemp load balancer.</p>
    <p>The load balancer is accessed as <a href='https://tableauprod.napierparkglobal.com/' target='_blank'>https://tableauprod.napierparkglobal.com/</a> externally.</p>
    <p>If we do not make this change on the Kemp side, Tableau and other apps behind the load balancer will become inaccessible as soon as the other internal IP changes on AWS side for the load balancer.</p>
    <p><strong>IMP:</strong> Please use ticket NPG-30125 for reference.</p>
    <p>Thanks & Regards</p>
    <head></head>
    <h1 style='text-align:center'>IP Address for {loadBalancer} changed from {oldIPAddress} to {newIPAddress}</h1>
    </body>
</body>
</html>
        """

    # Similar email content blocks for other load balancers...

    else:
        # Default content if no specific load balancer matches
        HTML_EMAIL_CONTENT = f"""
            <html>
                <head></head>
                <h1 style='text-align:center'>IP Address for {loadBalancer} changed from {oldIPAddress} to {newIPAddress}.</h1>
                </body>
            </html>
        """

    # Sending email using SES
    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                # Add your ToAddresses
            ],
            "CcAddresses": [
                # Add your CcAddresses
            ],
        },
        Message={
            "Body": {
                "Html": {
                    "Charset": CHARSET,
                    "Data": HTML_EMAIL_CONTENT,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "IP Changed",
            },
        },
        Source="AppsLBIPChangeNotifyList@napierparkglobal.com",
    )
    return

def lambda_handler(event, context):
    alb_list = os.environ['ALBLIST'].split(",")

    for alb_entry in alb_list:
        # Get IP addresses associated with the current load balancer
        addr_info = socket.gethostbyname_ex(alb_entry)
        addr_list = addr_info[2]

        # Connect to DynamoDB
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        table = dynamodb.Table('ALBIPStatus')

        # Query DynamoDB for the current load balancer entry
        response = table.query(KeyConditionExpression=Key('alb_id').eq(alb_entry))
        ip_dict = response['Items'][0]

        # Get stored IP addresses from DynamoDB
        storedIPs = [ip_dict[key] for key in ip_dict if key != 'alb_id']

        # Check for new IP addresses
        newIPs = [ip for ip in addr_list if ip not in storedIPs]

        # Update DynamoDB and send email for each new IP
        for newIP in newIPs:
            # Find the key associated with the new IP
            key_for_newIP = next((key for key, value in ip_dict.items() if value == newIP), None)
            if key_for_newIP:
                # Update DynamoDB with the new IP
                table.update_item(
                    Key={"alb_id": alb_entry},
                    UpdateExpression=f"set {key_for_newIP}=:newIP",
                    ExpressionAttributeValues={":newIP": newIP}
                )
                # Send email notification
                send_html_email(alb_entry, ip_dict[key_for_newIP], newIP)
