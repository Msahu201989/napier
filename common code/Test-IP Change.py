import json
import socket
import boto3
import json
import os
from boto3.dynamodb.conditions import Key

def send_html_email(loadBalancer,oldIPAddress,newIPAddress):

    ses_client = boto3.client("ses", region_name="us-east-1")
    CHARSET = "UTF-8"
    HTML_EMAIL_CONTENT = f"""
        <html>
            <head></head>
            <h1 style='text-align:center'>IP Address for {loadBalancer} changed from {oldIPAddress} to {newIPAddress}</h1>
            </body>
        </html>
    """

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "mukesh.sahu@napierparkglobal.com",
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

#def updateIPAddress(ipList,keyList)



#   return

def lambda_handler(event, context):
    # TODO implement

    alb_list = os.environ['ALBLIST'].split(",")

    for item in alb_list:
        alb_entry = ((item.replace("[","")).replace("]","")).replace("'","")
        addr1 = socket.gethostbyname_ex(alb_entry)

        #print(addr1[2][0])
        ##print(addr1[2][1])
        #print (len(addr1[2]))

        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        table = dynamodb.Table('ALBIPStatus')

        response = table.query(KeyConditionExpression=Key('alb_id').eq(alb_entry))
        ip_json = json.dumps(response['Items'])
        ip_dict = json.loads(ip_json)
        #print (addr1[2])

        # Find the ips to be replaced in the DynamoDB table

        storedIPs = []
        storedIPs = list(ip_dict[0].values())

        del storedIPs[0]
        print("############# Load Balancer - " + alb_entry + " #############")
        print (storedIPs)

        counter = 0
        for counter in range(len(storedIPs)):
            if storedIPs[counter] in addr1[2]:
                storedIPs[counter]=storedIPs[counter] + " - exists"
            counter = counter + 1
        print (storedIPs)

        newIPIndexes = []
        counter = 0

        for counter in range(len(storedIPs)):
            if not "exists" in storedIPs[counter]:
                newIPIndexes.append(storedIPs[counter])
            counter = counter + 1
        print(newIPIndexes)

        dictkeys = []
        dictkeys = list(ip_dict[0].keys())

        print(dictkeys)

        #Find the keys in the DynamoDB table for which values are to be replaced

        keysForUpdates = []
        for index in newIPIndexes:
            for item in dictkeys:
                if index == ip_dict[0][item]:
                    keysForUpdates.append(item)
        print ("### Keys where update needs to be made ###")
        print (keysForUpdates)


        # Find the IPs to be replaced
        ipforUpdates = []
        for item in list(addr1[2]):
            if not item in list(ip_dict[0].values()):
                ipforUpdates.append(item)

        print ("###IPs to be replaced###")


        ## Updates changed IPs and send mails
        counter = 0
        for counter in range(len(ipforUpdates)):
            response = table.update_item(
                Key={
                    "alb_id": alb_entry
                },

                UpdateExpression="set "+keysForUpdates[counter]+"=:newIP",
                ExpressionAttributeValues={
                    ":newIP": ipforUpdates[counter]
                })
            send_html_email(alb_entry,ip_dict[0][keysForUpdates[counter]],ipforUpdates[counter])
            counter = counter + 1
    #    updateIPAddress()

    #counter = 0
    #for counter in range(len(addr1[2])):
    #    if addr1[2][counter] in storedIPs:
    #        addr1[2][counter]=addr1[2][counter] + " - exists"
    #    counter = counter + 1
    #print (addr1[2])


    #print (addr1[2] )
    #print (temparray)

    ##ipstobeadded = set(addr1[2])-set(temparray)
    #print(ipstobeadded)

    #for item in ipstobeadded:




    #print (set(addr1)-set(ip_dict[0]))
    #storedIPs = []
    #counter = 0

    #for counter in range(len[ip_dict[0]]):
    #    storedIPs[index] = ip_dict[0]['ip_address' + counter+1]
    #    counter = counter + 1

    #if ( len(ip_dict[0]) - len(addr1[2]) > 1 ):
    #    for ipaddress in ip_dict[0]:
    #    print (ip_dict[0][ipaddress] + " in dynamodb")





    #if addr1[2][0] == ip_dict[0]['ip_address2'] or addr1[2][0] == ip_dict[0]['ip_address1']:
    ##    print(addr1[2][0] + " is same")
    #else:
    #try:
    #table = dynamodb.Table('ALBIPStatus')
    #response = table.update_item(
    #    Key={
    #            "alb_id": "prod"
    #    },
    #    UpdateExpression="set ip_address2=:newIP",
    #    ExpressionAttributeValues={
    #        ":newIP": addr1[2][0]
    #    })
    #
    #send_html_email(ip_dict[0]['ip_address2'],addr1[2][0])
    # ReturnValues=("UPDATED_NEW" )
    #except Exception as msg:
    #    print("Oops, could not update: {msg}")

    #if addr1[2][1] == ip_dict[0]['ip_address2'] or addr1[2][1] == ip_dict[0]['ip_address1']:
    #    print(addr1[2][1] + " is same")
    #else:
    #try:
    #print("Changing ip address 1")
    #table = dynamodb.Table('ALBIPStatus')
    #response = table.update_item(
    #    Key={
    #            "alb_id": "prod"
    #    },
    #
    #    UpdateExpression="set ip_address1=:newIP",
    #    ExpressionAttributeValues={
    #        ":newIP": addr1[2][1]
    #    })
    #
    # print("Change ip address 1 successfully")

    #send_html_email(ip_dict[0]['ip_address1'],addr1[2][1])
    # ReturnValues=("UPDATED_NEW" )
    #except Exception as msg:
    #    print("Oops, could not update: {msg}")

# response = table.query(KeyConditionExpression=Key('alb_id').eq('test.json'))
# print(response['Items'])

#Items['ip_address2'] = "updated"
#table.put_item(Items=Items)