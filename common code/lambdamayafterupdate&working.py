import json
import socket
import boto3
import os
from boto3.dynamodb.conditions import Key

def send_html_email(loadBalancer, oldIPAddress, newIPAddress):
    ses_client = boto3.client("ses", region_name="us-east-1")
    CHARSET = "UTF-8"

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

    elif "internal-lb-apps-prod-57189173.us-east-1.elb.amazonaws.com" in loadBalancer:
        HTML_EMAIL_CONTENT = f"""
<html>
<head></head>
<body>
    <p style='text-align:left;'>Hi Team,</p>
    <p><strong>Please note that one of the internal Apps PROD application load balancer's IP has changed from {oldIPAddress}</strong> to <strong>{newIPAddress}</strong>. Please make the changes accordingly on the Kemp load balancer.</p>
    <p>The load balancer is accessed as <strong>apps.napierparkglobal.com</strong> externally.</p>
    <p>If we do not make this change on the Kemp side, Odyssey and other apps behind the load balancer will become inaccessible as soon as the other internal IP changes on AWS side for the load balancer.</p>
    <p><strong>NOTE:</strong> You may use ticket NPG-30688  for reference. </p>
    <p>Thanks & Regards</p>
   <head></head>
   <h1 style='text-align:center'>IP Address for {loadBalancer} changed from {oldIPAddress} to {newIPAddress}</h1>
   </body>    
</body>
</html>

        """

    elif "internal-lb-apps-uat-1791296101.us-east-1.elb.amazonaws.com" in loadBalancer:
        HTML_EMAIL_CONTENT = f"""
<html>
<head></head>
<body>
    <p style='text-align:left;'>Hi Team,</p>
    <p><strong>Kindly note that one of the internal Apps UAT application load balancer  IP has changed from {oldIPAddress}</strong> to <strong>{newIPAddress}</strong>. Please make the changes accordingly on the Kemp load balancer.</p>
    <p>If we do not make this change on the Kemp side, Odyssey and other apps behind the load balancer will become inaccessible as soon as the other internal IP changes on AWS side for the load balancer.</p>
    <p><strong>IMP:</strong> Reference Ticket : NPG-26335 FW: IP Changed - Jira (options-it.com).</p>
    <p>Thanks & Regards</p>
   <head></head>
   <h1 style='text-align:center'>IP Address for {loadBalancer} changed from {oldIPAddress} to {newIPAddress}</h1>
  </body>    
</body>
</html>
        """

    elif "internal-lb-apps-dev-tab-1067900310.us-east-1.elb.amazonaws.com" in loadBalancer:
        HTML_EMAIL_CONTENT = f"""
<html>
<head></head>
<body>
    <p style='text-align:left;'> Hi Team,</p>
    <p><strong>Please note that one of the internal Apps dev application load balancer's IP has changed from {oldIPAddress}</strong> to <strong>{newIPAddress}</strong>. Please make the changes accordingly on the Kemp load balancer.</p>
    <p>The load balancer is accessed as <strong>tableaudev.napierparkglobal.com</strong> externally.</p>
    <p>If we do not make this change on the Kemp side, apps behind the load balancer will become inaccessible as soon as the other internal IP changes on AWS side for the load balancer.</p>
    <p><strong>NOTE:</strong> You may use old ticket NPG-26278  for reference. </p>
    <p>Thanks & Regards</p>
   <head></head>
   <h1 style='text-align:center'>IP Address for {loadBalancer} changed from {oldIPAddress} to {newIPAddress}</h1>
   </body>    
</body>
</html>  
        """


    elif "internal-lb-apps-dev-247053080.us-east-1.elb.amazonaws.com" in loadBalancer:
        HTML_EMAIL_CONTENT = f"""
<html>
<head></head>
<body>
    <p style='text-align:left;'>Hi Team,</p>
    <p><strong>Please note that one of the internal Apps DEV application load balancer IP has changed from {oldIPAddress}</strong> to <strong>{newIPAddress}</strong>. Please make the changes accordingly on the Kemp load balancer.</p>
    <p>The load balancer is accessed as <a href='appsdev.napierparkglobal.com' externally.</p>
    <p>If we do not make this change on the Kemp side, Odyssey and other apps behind the load balancer will become inaccessible as soon as the other internal IP changes on AWS side for the load balancer</p>
    <p>Thanks & Regards</p>
   <head></head>
  <h1 style='text-align:center'>IP Address for {loadBalancer} changed from {oldIPAddress} to {newIPAddress}</h1>
  </body></body>
</html>
        """
    else:
        # Default content if no specific load balancer matches
        HTML_EMAIL_CONTENT = f"""
            <html>
                <head></head>
                <h1 style='text-align:center'>IP Address for {loadBalancer} changed from {oldIPAddress} to {newIPAddress}.</h1>
                </body>
            </html>
        """

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "support@options-it.com",
            ],
            "CcAddresses": [
                "nitin.khullar@napierparkglobal.com",
                "napiertechsupportoda@napierparkglobal.com",
                "mukesh.sahu@napierparkglobal.com",
                "rajesh.kumar@napierparkglobal.com",
                "amit.khanna@napierparkglobal.com",
                "mohammed.khan@napierparkglobal.com",
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

    for item in alb_list:
        alb_entry = ((item.replace("[","")).replace("]","")).replace("'","")
        addr1 = socket.gethostbyname_ex(alb_entry)

        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        table = dynamodb.Table('ALBIPStatus')

        response = table.query(KeyConditionExpression=Key('alb_id').eq(alb_entry))
        ip_json = json.dumps(response['Items'])
        ip_dict = json.loads(ip_json)

        storedIPs = [ip_dict[0][key] for key in ip_dict[0].keys() if key != 'alb_id']

        newIPIndexes = [index for index, stored_ip in enumerate(storedIPs) if stored_ip not in addr1[2]]

        keysForUpdates = [key for index in newIPIndexes for key, value in ip_dict[0].items() if value == storedIPs[index]]

        ipforUpdates = [new_ip for new_ip in addr1[2] if new_ip not in storedIPs]

        for counter, ip in enumerate(ipforUpdates):
            try:
                response = table.update_item(
                    Key={"alb_id": alb_entry},
                    UpdateExpression=f"set {keysForUpdates[counter]}=:newIP",
                    ExpressionAttributeValues={":newIP": ip}
                )
                send_html_email(alb_entry, ip_dict[0][keysForUpdates[counter]], ip)
            except Exception as e:
                print("Error updating item in DynamoDB table:", str(e))

    return
