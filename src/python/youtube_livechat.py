from googleapiclient.discovery import build,Resource

class YoutubeLiveChat:
    youtube : Resource
    def __init__(self,api_key : str):
        self.youtube = build('youtube','v3',developerKey=api_key)
        pass
    
    def fetch_live_chat(self,livechat_id,page_token = None):
        response = self.youtube.liveChatMessages().list(
        liveChatId=livechat_id,
        part='id,snippet,authorDetails',
        maxResults=100,
        pageToken=page_token  # None なら先頭から
    ).execute()
        return response