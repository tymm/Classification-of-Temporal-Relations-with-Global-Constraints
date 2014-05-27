from simplejson import loads
from helper.stanfordnlp import jsonrpc

class StanfordNLP:
    def __init__(self):
        self.server = jsonrpc.ServerProxy(jsonrpc.JsonRpc20(), jsonrpc.TransportTcpIp(addr=("127.0.0.1", 8080)))

    def parse(self, text, position):
        if position:
            try:
                response = loads(self.server.parse(text))
                return response["sentences"][0]["words"][position][1]["PartOfSpeech"]
            except jsonrpc.RPCTransportError:
                print "Error: Please start the StanfordNLP server."
            except IndexError:
                return "None"
        else:
            return "None"
