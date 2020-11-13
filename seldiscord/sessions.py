from .analytics import AnalyticsEvent
from urllib.parse import urlparse
import user_agents
import selrequests
import websocket
import base64
import json
import typing

DEFAULT_HOST = "discord.com"

class Session:
    host: str
    api: str
    user_agent: str
    proxy_url: str
    build_number: int
    client_uuid: str
    token: str
    fingerprint: str
    _sel: selrequests.Session

    def __init__(self, user_agent: str, proxy_url: str=None,
                 host: str=DEFAULT_HOST):
        self.user_agent = user_agent
        self.proxy_url = proxy_url
        self.host = host
        self.api = "v8"
        self.build_number = 9999

        self.token = None
        self.fingerprint = None
        self.client_uuid = None

        self._sel = selrequests.Session(proxy_url, user_agent)
        self._sel.set_origin(f"https://{self.host}/")

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def close(self):
        self._sel.close()

    """
    Set-up the session
    """
    def setup(self):
        with self.request(
            method="GET",
            url=f"https://{self.host}/api/{self.api}/experiments",
        ) as resp:
            data = resp.json()
            self.fingerprint = data["fingerprint"]

    """
    Briefly connects to the gateway, to unlock additional functionalities (lazy)
    """
    def gateway(self):
        proxy_config = {}
        if self.proxy_url:
            purl = urlparse(self.proxy_url)
            proxy_config = dict(
                http_proxy_host=purl.hostname,
                http_proxy_port=purl.port
            )
        ws = websocket.create_connection(
            f"wss://gateway.discord.gg/?encoding=json&v=8&compress=zlib-stream",
            **proxy_config,
            origin=f"https://{self.host}",
            header={
                "User-Agent": self.user_agent,
                "Pragma": "no-cache",
                "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
                "Sec-WebSocket-Key": "AV9Y5FZyifxt410j9UqTqw==",
                "Sec-WebSocket-Version": "13",
                "Connection": "Upgrade"
            }
        )
        ws.recv()
        ws.send(json.dumps(
            {"op":2,"d":{"token":self.token,"capabilities":61,"properties":self._get_properties(False),"presence":{"status":"online","since":0,"activities":[],"afk":False},"compress":False,"client_state":{"guild_hashes":{},"highest_last_message_id":"0","read_state_version":0,"user_guild_settings_version":-1}}},
            separators=(",", ":")
        ).encode("UTF-8"))
        ws.recv()
        ws.recv()
        ws.close()

    """
    Register an account
    """
    def register(self, username: str, **signup_params) -> dict:
        with self.request(
            method="POST",
            url=f"https://{self.host}/api/{self.api}/auth/register",
            json={"fingerprint": self.fingerprint, "consent": True,
                  "username": username, **signup_params}
        ) as resp:
            data = resp.json()
            self.token = data["token"]
            return data

    """
    Post list of AnalyticsEvent instances
    """
    def post_analytics(self,
                       events: typing.List[AnalyticsEvent],
                       **params) -> bool:
        if not self.client_uuid:
            self.refresh_client_uuid()
        
        with self.request(
            method="POST",
            url=f"https://{self.host}/api/{self.api}/science",
            json={
                "events": list(map(
                    lambda e: e.to_dict(self.client_uuid),
                    events
                )),
                **params
            }
        ) as resp:
            return resp.status_code == 204

    """
    Wrapper for _sel.request
    """
    def request(self, method: str, url: str, json: dict=None,
                headers: dict={},
                context: dict=None) -> selrequests.Response:
        headers = headers or {}
        
        if url.startswith(f"https://{self.host}/api/"):
            if self.token:
                headers["Authorization"] = self.token
            
            if self.fingerprint:
                headers["X-Fingerprint"] = self.fingerprint
            
            if self._use_x_track_header():
                headers["X-Track"] = self._get_properties()
            else:
                headers["X-Super-Properties"] = self._get_properties()

            if context:
                headers["X-Context-Properties"] = base64.b64encode(
                    json.dumps(
                        context, separators=(",",":")).encode("UTF-8")
                ).decode("UTF-8")
        
        resp = self._sel.request(
            method=method,
            url=url,
            json=json,
            headers=headers
        )
        return resp

    """
    Refresh the client uuid used in analytics
    """
    def refresh_client_uuid(self): ## TODO: implement this
        self.client_uuid = "HgAGvytpxgq2VZjvfk2CvHUBAAAAAAAA"

    def _use_x_track_header(self) -> bool:
        return self.build_number == 9999

    def _get_properties(self, encode=True) -> dict:
        pua = user_agents.parse(self.user_agent)
        device = None
        if not pua.device.family in [None, "Other"]:
            device = pua.device.family
        data = {
            "os": pua.os.family,
            "browser": pua.browser.family,
            "device": device,
            "browser_user_agent": self.user_agent,
            "browser_version": pua.browser.version_string,
            "os_version": pua.os.version_string,
            "referrer": "",
            "referring_domain": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": self.build_number,
            "client_event_source": None
        }
        if encode:
            data = json.dumps(data, separators=(",", ":"))
            data = base64.b64encode(data.encode("UTF-8")).decode("UTF-8")
        return data
