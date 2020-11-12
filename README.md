# sel-discord
Discord API client based on my [sel requests](https://github.com/h0nde/sel-requests) module, primarly focused on evading Discord's TLS fingerprint bot detection.

# Setup
```bash
pip install -U git+https://github.com/h0nde/sel-requests.git
pip install -U git+https://github.com/h0nde/sel-discord-.git
```

# Usage
```python
import seldiscord

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
dsc = seldiscord.Session(user_agent)

# now that TLS fingerprinting has been evaded, Discord is likely
# to present no captchas while creating an account
print(dsc.register(username="234ixcmoas"))
```
