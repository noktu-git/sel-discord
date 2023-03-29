# sel-discord
this is an archive of [sel-requests](https://github.com/h0nde/sel-requests), and this repo is years old so you probably won't have much luck.

Discord API client based on my [sel-requests](https://github.com/h0nde/sel-requests) module, primarly focused on evading Discord's TLS fingerprint bot detection.

# Setup
```bash
pip install -U git+https://github.com/h0nde/sel-requests.git
pip install -U git+https://github.com/h0nde/sel-discord.git
```

# Usage
```python
import seldiscord

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"

with seldiscord.Session(user_agent) as dsc:
  dsc.setup()
  # now that TLS fingerprinting has been evaded, Discord is likely
  # to present no captchas while creating an account
  print(dsc.register(
    username="234ixcmoas",
    #email="support@discordapp.com",
    #password="hunter2",
    #invite="fortnite"
  ))
  dsc.gateway()
```

# Documentation
Only some specific API endpoints have methods of their own.

### Session(user_agent, proxy_url=None)
Initialize a new session/client.

### Session.setup()
Grab fingerprints and stuff.

### Session.request(method, url, json=None, headers=None, context=None)
Wrapper for .sel.request, includes all necessary Discord headers.

### Session.register(username, **signup_params)
Attempts to create an account. If successful, the .token attribute is set, and further API requests will be authenticated.

### Session.gateway()
Briefly connects to the gateway to unlock additional functionalities.

### Session.post_analytics(events: List[AnalyticsEvent])

### Session.refresh_client_uuid()

### Session.close()
Closes the sel-requests instance.
