def slack_create_channel(client,channel_name ):

    return client.conversations_create(name = channel_name).data['channel']['id']


def slack_invite_to_channel(client, channel_id, users = ['U016TSW4MSB', 'U018F0DLENQ']):

    return client.conversations_invite(channel=channel_id, users=users).data['ok']


def slack_upload_image(client,channel_id, path_to_file, message):

    return client.files_upload(file=path_to_file,initial_comment=message, channel = channel_id).data['ok']


def slack_post_message(client,channel_id, text):

    return client.chat_postMessage(channel=channel_id,text = text).data['ok']


