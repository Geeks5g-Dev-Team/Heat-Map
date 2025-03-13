import os

class GoogleConfig ():
  
  def get_google_secret_key (self):
    
    return os.getenv("GOOGLE_API_KEY", None)