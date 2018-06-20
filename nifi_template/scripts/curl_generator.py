from org.apache.nifi.processors.script import ExecuteScript
from org.apache.nifi.processor.io import InputStreamCallback
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import OutputStreamCallback
from java.io import BufferedReader, InputStreamReader
import os

"""This script must be put in the configuration of SendPutOnElasticSearch processor of NiFi"""
class PyOutputStreamCallback(OutputStreamCallback):
    def __init__(self):
        pass
    def setOutput(self, toOutput):
        self.outuput = toOutput

    def process(self, outputStream):
    	outputStream.write(self.outuput.encode('utf-16'))



class ReadFirstLine(InputStreamCallback) :
    __line = None;

    def __init__(self) :
        pass

    def getLine(self) :
        return self.__line

    def process(self, input) :
        try:
            reader = InputStreamReader(input)
            bufferedReader = BufferedReader(reader)
            line = bufferedReader.readLine()

            self.__line = line
        except :
            print("Exception in Reader:")
            print('-' * 60)
            #traceback.print_exc(file=sys.stdout)
            print('-' * 60)
            raise
        finally :
            if bufferedReader is not None :
                bufferedReader.close()
            if reader is not None :
                reader.close()

flowFile = session.get()
if flowFile is not None :

    reader = ReadFirstLine()
    session.read(flowFile, reader)
    text = reader.getLine()

    text = text.replace("[", "").replace("]", "")

    json_commands = text.split("},")
    print("Total entries: ", len(json_commands))
    curl_list = []
    for document in json_commands:
        document = document + "}"
        tweet_id = document.split(":")[1].split(",")[0].replace('"', "")

        curlstring = 'curl -X PUT "localhost:9200/tweet_dataset/tweet/' + tweet_id + '" -H ' + "'Content-Type: application/json' -d '"

        curl_list.append(curlstring + document + "'")

    command_sent = ""
    for command in curl_list:
        command_sent += command + ", "
        os.system(command)

    flowFile = session.putAttribute(flowFile, "curl_command", command_sent)
    session.transfer(flowFile, ExecuteScript.REL_SUCCESS)