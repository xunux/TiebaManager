from requester import Requester
from common import config_reader
from constant import *
import urllib
import re


class Lawman(Requester):
    """
    Posts and Users operator unit
    Delete post with post url
    Ban user with post url(Not available now)
    """

    def __init__(self, tieba_name="steam", cookie=None):
        Requester.__init__(self, tieba_name, cookie)
        self.ban_url = TIEBA_BAN_URL
        self.tbs_re = re.compile(r'"tbs": "(\S+)"')
        self.fid_re = re.compile(r"fid:'(\d+)'")

    def delete_post_2(self, post):
        """
        Delete post by generate a url
        :param post:
        :return:
        """
        # parameters
        zid = post.zid
        fid = post.fid
        pid = post.pid

        tbs = self.__get_tbs(post.url)

        operator_url = "http://tieba.baidu.com/mo/m?"

        payload = {'expand': '0',
                   'fid': fid,
                   'nlm': '11',
                   'ntn': 'bdKSW',
                   'pinf': '1_2_0',
                   'pn': '0',
                   'tbs': tbs,
                   'tn': 'baiduManagerSubmit',
                   'word': self.tieba_name,
                   'z': zid}

        delete_url = operator_url + urllib.parse.urlencode(payload)
        response = self.get_content(delete_url)
        return "成功删除" in response.text

    def delete_post(self, delete_page_url):
        """
        Delete given url
        :param delete_page_url:
        :return boolean:
        """
        delete_page_response = self.get_content(delete_page_url)
        delete_confirm_url = delete_page_response.find('a', text='确认删除')
        delete_confirm_url = self.url_base + delete_confirm_url.get('href')

        delete_result = self.get_content(delete_confirm_url)

        return '成功删除' in delete_result.text

    def ban_user(self, post, reason):
        """
        Ban the author of post
        :param post:
        :param reason:
        :return:
        """
        tbs = self.__get_tbs(post.get_url())
        fid = post.fid
        pid = post.pid

        form_data = {'day': 1, 'fid': fid, 'tbs': tbs, 'ie': 'gbk', 'user_name[]': post.get_author(), 'pid[]': pid,
                     'reason': reason}

        response = self.session_worker.post(self.ban_url, data=form_data).json()

        return response['errno'] == 0

    def __get_tbs(self, post_url):
        """
        Get tbs(token)
        :param post_url:
        :return string:
        """
        response = self.get_content(post_url)

        tbs = response.find('input', {'name': 'tbs'}).get('value')

        return tbs


if __name__ == "__main__":
    cookie, _ = config_reader()
    worker = Lawman(cookie=cookie)
    # print(worker.ban_user(
    #     "http://tieba.baidu.com/mo/q---189C1660F1F72884A696954D1ED81373%3AFG%3D1--1-3-0--2--wapp_1457786153016_691/m?kz=4326317739&is_bakan=0&lp=5010&pinf=1_2_0",
    #     'KIDJourney', "Test"))
