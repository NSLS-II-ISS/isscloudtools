def slack_create_channel(client,channel_name ):

    return client.conversations_create(name = channel_name).data['channel']['id']


def slack_invite_to_channel(client, channel_id, users = ['U016TSW4MSB', 'U018F0DLENQ']):

    return client.conversations_invite(channel=channel_id, users=users).data['ok']


def slack_upload_image(client,channel_id, path_to_file, message):

    return client.files_upload(file=path_to_file,initial_comment=message, channel = channel_id).data['ok']


def slack_post_message(client,channel_id, text):

    return client.chat_postMessage(channel=channel_id,text = text).data['ok']






# response
# response.keys
# response.keys()
# list(response)service.chat_postMessage(channel=cidresponse,text = 'hello')
# response["id"]
# response
# response.headers
# response.api_url
# response.data
# response = client.users.admin.invite()
# client.conversations_invite?
# client.conversations_invite(channel='G018FBYSP28',users='U018F0DLENQ')
# client.conversations_invite(channel='G018FBYSP28',users='U018F0DLENQ').data
# client.conversations_invite(channel='G0187QETD8D',users='U018F0DLENQ').data
# pwd
# cd Desktop/
# ls
# client.files_upload(file='I9fmWi2QbQg.jpg',initial_comment='Here', channel = 'C017M890NP3')
# token = ''
# client = WebClient(token=token)
# client.files_upload(file='I9fmWi2QbQg.jpg',initial_comment='Here', channel = 'C017M890NP3')
# client.files_upload(file='I9fmWi2QbQg.jpg',initial_comment='Here', channel = 'C017M890NP3')
# client = WebClient(token=token)
# client.files_upload(file='I9fmWi2QbQg.jpg',initial_comment='Here', channel = 'C017M890NP3')