import re, urllib, urllib2
import json

class Spreadsheet(object):
    def __init__(self, key):
        super(Spreadsheet, self).__init__()
        self.key = key


class Client(object):
    def __init__(self, email, password):
        super(Client, self).__init__()
        self.email = email
        self.password = password

    def _get_auth_token(self, email, password, source, service):
        url = "https://www.google.com/accounts/ClientLogin"
        params = {
            "Email": email, "Passwd": password,
            "service": service,
            "accountType": "HOSTED_OR_GOOGLE",
            "source": source
        }
        req = urllib2.Request(url, urllib.urlencode(params))
        return re.findall(r"Auth=(.*)", urllib2.urlopen(req).read())[0]

    def get_auth_token(self):
        source = type(self).__name__
        print("source ", source)
        return self._get_auth_token(self.email, self.password, source, service="wise")

    def download(self, spreadsheet, gid=0, format="xlsx"):
        url_format = "https://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=%s&exportFormat=%s&gid=%i"
        print("I'm in ")
        headers = {
            "Authorization": "GoogleLogin auth=" + self.get_auth_token(),
            "GData-Version": "3.0"
        }
        print("I'm")
        req = urllib2.Request(url_format % (spreadsheet.key, format, gid), headers=headers)
        print("I'm too")
        return urllib2.urlopen(req)


class ReadGoogleSheet:

    def get_spreadSheet(self):
        data = json.load(open('../Config/Setting.json'))
        email = data["Google_User"]  # (your email here)
        password = data["Google_Password"]
        spreadsheet_id = data["Google_SpreadSheet"]  # (spreadsheet id here)

        # Create client and spreadsheet objects
        gs = Client(email, password)
        ss = Spreadsheet(spreadsheet_id)
        print("Spread sheet", ss)
        # Request a file-like object containing the spreadsheet's contents
        return gs.download(ss)
