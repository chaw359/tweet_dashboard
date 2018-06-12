from models.SentimentAnalyzer import SentimentAnalyzer


class LinkCreator:
    """
    The purpose of this class is to analyze a tweet's text and find tag. We suppose that a tag in a text is a link
    between the user that tags and the tagged user.
    """
    def __init__(self):
        self.text=""
        self.linked_users=[]


    def __clean_text(self, text):
        """
        Clean the text of a tweet removing all possible special chars
        :param text: text to clean
        :return: cleaned text
        """
        return text.replace(".", "").replace(":", "").replace(";", "").replace(",", "").replace("!", "").replace("#","").replace("@", "").replace(" ","")


    def find_link(self, text):
        """
        Given the text, this method find a link within it. A link is represented by tag (@)
        :param text: text in which to find a link
        :return: a list of links. If no link is found empty list is returned
        """
        toReturn = []
        self.text = text
        s = SentimentAnalyzer()

        for tag in text.split():
            if tag.startswith('@'):
                self.linked_users.append(self.__clean_text(tag))
                toReturn.append(tag)
               # print("TAG CHIAVE: ",tagChiave )

        return toReturn


    def get_all_links(self):
        """
        Get all links of this user
        :return: a list of all tweet user tagged by the monitored user
        """
        return self.linked_users





