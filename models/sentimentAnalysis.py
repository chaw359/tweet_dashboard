import json
import urllib.parse,urllib.request

class sentimentAnalysis:

    def analyze(self, stringa):
        data = urllib.parse.urlencode({"text": stringa}).encode("utf-8")
        u = urllib.request.urlopen("http://text-processing.com/api/sentiment/", data)
        the_page = u.read()
        dizionario = json.loads(the_page.decode())
        return dizionario

    def getLabel(self,stringa):
        print("STRINGA OTTENUTA: ",stringa)
        dizionario = sentimentAnalysis.analyze(self, stringa)
        return dizionario["label"]

    def getNegative(self, stringa):
        print("STRINGA OTTENUTA: ", stringa)
        dizionario = sentimentAnalysis.analyze(self, stringa)
        return dizionario["probability"]["neg"]

    def getNeutral(self, stringa):
        print("STRINGA OTTENUTA: ", stringa)
        dizionario = sentimentAnalysis.analyze(self, stringa)
        return dizionario["probability"]["neutral"]

    def getPositive(self, stringa):
        print("STRINGA OTTENUTA: ", stringa)
        dizionario = sentimentAnalysis.analyze(self, stringa)
        return dizionario["probability"]["pos"]



if __name__ == '__main__':
    s = sentimentAnalysis()
    print(s.getLabel("You're a poor jerk!"))
    print(s.getLabel("I love you!"))
