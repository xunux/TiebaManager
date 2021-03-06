from bs4 import BeautifulSoup
from constant import *
from urllib import parse


def get_pid_fid_zid(ban_url):
    """
    Get pid and fid from delete url
    :param ban_url:
    :return:
    """
    query = parse.urlparse(ban_url).query
    query_parse = parse.parse_qs(query)

    pid = query_parse['pid'][0]
    fid = query_parse['fid'][0]
    zid = query_parse['z'][0]

    return pid, fid, zid


class PostBase:
    """
    Base structure to describe element in tieba
    """

    def __init__(self):
        self.MAX_TITLE_DISPLAY = 10
        self.MAX_CONTENT_DISPLAY = 20

        self.title = ''
        self.content = ''
        self.author = ''
        self.time = ''
        self.del_url = ''
        self.ban_url = ''
        self.fid = ''
        self.pid = ''
        self.zid = ''

    def get_pid_sid(self):
        ban_url = self.ban_url

        self.pid, self.fid , self.zid = get_pid_fid_zid(ban_url)

    def __str__(self):
        return """\tContent: {0}\n\tAuthor: {1}\n\tTime: {2}\n\tDel_url: {3}\n\tBan_url: {4}""".format(
            self.content, self.author, self.time, self.del_url, self.ban_url)

    def get_content(self):
        return self.content[:self.MAX_CONTENT_DISPLAY]

    def get_author(self):
        return self.author

    def get_time(self):
        return self.time

    def get_del_url(self):
        return self.del_url

    def get_ban_url(self):
        return self.ban_url

    def get_title(self):
        return "reply"


class Post(PostBase):
    """
    Structure to describe post , provide replay of post info (1 page at present)
    """

    def __init__(self, url, soup=None):

        if soup is None:
            raise Exception("The soup must be provided")
        PostBase.__init__(self)

        self.url = url
        self.reply_list = []
        self.__soup_analyze(soup)

        self.get_pid_sid()

    def get_url(self):
        return self.url

    def get_title(self):
        return self.title[:self.MAX_TITLE_DISPLAY]

    def __str__(self):
        return "\tUrl: {0}\n".format(self.url) + "\tTitle: {0}".format(self.title) + PostBase.__str__(self)

    def __soup_analyze(self, soup):
        reply_list = soup.findAll('div', {'class': 'i'})

        header = soup.find('div', {'class': 'bc'})
        post = reply_list[0]
        self.__soup_analyze_post(header, post)

        reply_list = reply_list[1:]
        self.reply_list = [Reply(tag) for tag in reply_list]

    def __soup_analyze_post(self, header, post):
        self.title = header.find('strong').text

        post_info = list(post.stripped_strings)
        self.content = ''.join(post_info[:-4])
        self.content = self.content[self.content.find('楼') + 2:].strip()
        self.time = post_info[-2]
        self.author = post_info[-3]

        self.del_url = header.find('a', text='删主题').get('href')
        self.del_url = TIEBA_MOBILE_URL + self.del_url

        self.ban_url = post.find('a', {'class': 'banned'}).get('href')
        self.ban_url = TIEBA_MOBILE_URL + self.ban_url


class Reply(PostBase):
    """
    Structure describe reply of Post
    """

    def __init__(self, tag=None):
        if tag is None:
            raise Exception("The tag must be provided")
        PostBase.__init__(self)
        self.__soup_analyze_reply(tag)

        self.get_pid_sid()

    def __soup_analyze_reply(self, tag):
        post_info = list(tag.stripped_strings)
        self.content = ''.join(post_info[:-5])
        self.content = self.content[self.content.find('楼') + 2:].strip()
        self.time = post_info[-4]
        self.author = post_info[-5]

        self.del_url = tag.find('a', {'class': 'delete'}).get('href')
        self.del_url = TIEBA_MOBILE_URL + self.del_url

        self.ban_url = tag.find('a', {'class': 'banned'}).get('href')
        self.ban_url = TIEBA_MOBILE_URL + self.ban_url


if __name__ == "__main__":
    soupDemo = BeautifulSoup("""<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.0//EN" "http://www.wapforum.org/DTD/xhtml-mobile10.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"><!--STATUS OK--><!--STATIC http://static.tieba.baidu.com/tb/mobile/wpb20120222_62344 --><head><meta content="百度贴吧——全球最大的中文社区，为兴趣而生" name="keywords"/><meta content="application/xhtml+xml; charset=utf-8" http-equiv="Content-Type"/><meta content="text/html; charset=utf-8; X-Wap-Proxy-Cookie=none" http-equiv="Content-Type"/><style type="text/css">body{font-size:small;line-height:1.4em;margin:1px;}form{margin:0;padding:0;}a{text-decoration: none;};a img{border:none;}.light{color:#c60a00;}.bc{background-color:#EFF2FA;}.g{color:#AAA;}.b{color:#008000;}.p{padding:1px 0;}.i{border-bottom:1px solid #90B5F4;margin-bottom:3px;padding-bottom:2px;}.d{margin-bottom:6px;}table{width:100%;}.q{width:95%;}.l{text-align:left;}.r{text-align:right;}.h{background-color:#EBF7FE;padding:2px 0;}.fw{font-weight:bold;}#insert_smile{background:none;border:none;font-size:small;color:blue;}.is_bakan,.is_tuce,.outside_post{color:#888;padding:3px 0px;}.advertise{display: block; color: red;}.advertise_top{}.guide{width:100%;}.guide div{font-size: 16px;height:30px;line-height: 30px; font-weight: bold;}.block{width:100%;text-align: center;}.button{font-size: 15px;font-weight:bold;margin-bottom:10px;line-height: 30px;color:#ffffff; display:inline-block; background-color:#3496E9;height:30px;width:100px;border-radius: 3px 3px;}</style><title>话说索尼的z5和6s相比较而言哪个好qaq</title></head><body><div><a name="top"></a><a class="client_spread_text" href="redirect?tbjump=http%3A%2F%2Ftieba.baidu.com%2Fdownload-client%2F&amp;task=%E6%9E%81%E9%80%9F%E7%89%88%E5%AE%A2%E6%88%B7%E7%AB%AF%E9%A1%B6%E9%83%A8%E5%AF%BC%E6%B5%81&amp;locate=pb">客户端继续浏览</a><a class="bc advertise advertise_top" href="http://www.baidu.com/cpro.php?K00000KThn1pz4rMZCv2mtdE3z3vAWPVzhV9D-YtkZQGp9jzp79LtMPDT9-C805kXtRY9AXRKULYzCHebPTaLWwk2PtOb1cy1xN6iwpOC3gfBLjgGv3_4o0qmyU0.DD_j9sTraAG2crqqvaFWI_1e2qMKsoDkEo_LdddvTVxQjWhyAp7W_lIh4f.IgF_5y9YIZ0lQzqYpyNBmi4Bmy-bIi4WUvYE0ZwV5Hcvrjf1rjbvnfKYIHYs0Zwb5H00IvsqP6KWUMw85HbknjbknHDsg17xmLKz0APCUyfqnfK1mv9VujYk0ZPs5HDv0AN3IjYs0A7bmvk9TLnqn0K1uAVxIWYs0Aq15H00mMcqn0KLpywYpjYs0A9-pyICIjYs0ZIG5HD0XA-s5fK1uAVxIhNzTv-EUWY0Uh71IZ0qn0KzT1Ys0APh5H00mLwV5yF9pywdyDdnfh71ufK8mgwd5Hb0pgwGujYs0A-Ypy4hUv-b5H00uLKGujYs0ZF-uMKGujYs0APsThqGujY0mvqVTAk-5HR0mywxT1Y1PH0zmW6zPvDLmvR3nvcs0Ak9UjY0mgwGujY0mgwYXHY0ILPzm1Ys0A7-gLw9TWY0pgPxpLw95fK1UZPzm1Ys0ZP_mv_qn0K1UAVGujYs0AFduAI-I7q-XZKGujYs0A7GTjddr7qQphd-Xb7RTsKdpg0qwYIsiWnLnHFBiDf0mv6q0Zw9TWYz0AwYTjYs0ZP-UAk-T-qGujYk0A-1gv7sTjYs0A7sT7qGujYs0APdTLfq0A-1gLIGThN_ugP15H00Iv7sgLw4TARqnfKsUjYs0AdW5HbYmHw-PWcd0Adv5HD0UMus5H08nj0snj0snj00u1bqn0KhpgF1I7qzuyIGUv3qnWR0TvNWUv4bgLF-uv-EUWYYPjb0TLPs5HD0TLPsnWYz0ZwYTjYk0AwGTLws5H00mycqn0K9uZ6qn0KsuMwzmyw-5Hcvn0KsTLwzmyw-5H00TA-b5H00ILKGujYs0A7bIZ-suHYs0ZPGThN8uANz5H00TLIGujYs0ZPYXgK-5H00mLFW5HR3nWc300" title="境外租车,新春立减818元!">境外租车,新春立减818元!</a><div class="bc p"><strong>话说索尼的z5和6s相比较而言哪个好qaq</strong> 第1页(共178贴)<br/><a href="http://tieba.baidu.com/mo/q---439281407650F15229067DB692A4A231%3AFG%3D1--1-1-0--2--wapp_1453706811037_796/m?kz=4320033252&amp;see_lz=1&amp;lp=6034&amp;regtype=1&amp;pinf=1_2_0">只看楼主</a> <a href="m?kz=4320033252&amp;lp=6003&amp;last=1&amp;r=1&amp;pinf=1_2_0">最新回复</a> <a href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;word=steam&amp;fid=707597&amp;z=4320033252&amp;expand=0&amp;ti=%E8%AF%9D%E8%AF%B4%E7%B4%A2%E5%B0%BC%E7%9A%84z5%E5%92%8C6s%E7%9B%B8%E6%AF%94%E8%BE%83%E8%80%8C%E8%A8%80%E5%93%AA%E4%B8%AA%E5%A5%BDqaq&amp;pinf=1_2_0">删主题</a> <a href="#bottom">去底部</a> <a href="m?kz=4320033252&amp;lp=6000&amp;pn=0&amp;pinf=1_2_0">刷新</a></div><div class="d"> <div class="i">1楼. 嘛。。steam不止谈游戏233333<br/>年底是打算换新手机的。。传家宝4s都快发霉了<img src="http://tb2.bdstatic.com/tb/editor/images/client/image_emoticon19.png"/><img src="http://tb2.bdstatic.com/tb/editor/images/client/image_emoticon19.png"/><br/>预算的话6000左右 现在看下来是索尼的z5和6s。。<br/>lz手机白<img src="http://tb2.bdstatic.com/tb/editor/images/client/image_emoticon9.png"/>求大神明灯<a href="http://m.tiebaimg.com/timg?wapp&amp;quality=80&amp;size=b400_2000&amp;cut_x=0&amp;cut_w=0&amp;cut_y=0&amp;cut_h=0&amp;sec=1369815402&amp;di=e13bc7041139beca8035f9ce95ada3a4&amp;wh_rate=null&amp;src=http%3A%2F%2Fimgsrc.baidu.com%2Fforum%2Fpic%2Fitem%2F7e3c88025aafa40f0a1d68d0ac64034f79f0192b.jpg">图</a><a href="http://m.tiebaimg.com/timg?wapp&amp;quality=80&amp;size=b400_2000&amp;cut_x=0&amp;cut_w=0&amp;cut_y=0&amp;cut_h=0&amp;sec=1369815402&amp;di=734bcf123a83af02ac5abde598184f8e&amp;wh_rate=null&amp;src=http%3A%2F%2Fimgsrc.baidu.com%2Fforum%2Fpic%2Fitem%2F8dc613d8bc3eb135ceec16b6a11ea8d3fc1f44e4.jpg">图</a><br/> <a class="reply_to" href="#reply">回复</a><br/><span class="g"><a href="i?un=%E6%B8%85%E7%BA%AF%E7%9A%84%E5%A5%B6%E8%8C%B6%E5%A9%8A&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">清纯的奶茶婊</a></span> <span class="b">1-24 13:22</span>                      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=%E6%B8%85%E7%BA%AF%E7%9A%84%E5%A5%B6%E8%8C%B6%E5%A9%8A&amp;fid=707597&amp;act=2&amp;pid=82924305985&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a> </div><div class="i">2楼. 感觉z5的机型很有科技感<br/>还能防水<img src="http://tb2.bdstatic.com/tb/editor/images/client/image_emoticon28.png"/><br/>很好看啊www<br/><span class="g"><a href="i?un=%E6%B8%85%E7%BA%AF%E7%9A%84%E5%A5%B6%E8%8C%B6%E5%A9%8A&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">清纯的奶茶婊</a></span> <span class="b">1-24 13:23</span>                     <a class="reply_to" href="flr?pid=82924360620&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复(6)</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=%E6%B8%85%E7%BA%AF%E7%9A%84%E5%A5%B6%E8%8C%B6%E5%A9%8A&amp;fid=707597&amp;act=2&amp;pid=82924360620&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82924360620&amp;lm=707597&amp;sc=82924360620&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">3楼. 嘛。。。最主要的是向索尼大法好一波hhh<br/><span class="g"><a href="i?un=%E6%B8%85%E7%BA%AF%E7%9A%84%E5%A5%B6%E8%8C%B6%E5%A9%8A&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">清纯的奶茶婊</a></span> <span class="b">1-24 13:24</span>                     <a class="reply_to" href="flr?pid=82924383518&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=%E6%B8%85%E7%BA%AF%E7%9A%84%E5%A5%B6%E8%8C%B6%E5%A9%8A&amp;fid=707597&amp;act=2&amp;pid=82924383518&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82924383518&amp;lm=707597&amp;sc=82924383518&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">5楼. <a href="http://m.tiebaimg.com/timg?wapp&amp;quality=80&amp;size=b400_2000&amp;cut_x=0&amp;cut_w=0&amp;cut_y=0&amp;cut_h=0&amp;sec=1369815402&amp;di=6ba2b5f70d5e343fbcf7ec1b11b61faa&amp;wh_rate=null&amp;src=http%3A%2F%2Fimgsrc.baidu.com%2Fforum%2Fpic%2Fitem%2F92f1f2dcd100baa1df27e7b64010b912c9fc2efb.jpg">图</a><br/><span class="g"><a href="i?un=%E6%B8%85%E7%BA%AF%E7%9A%84%E5%A5%B6%E8%8C%B6%E5%A9%8A&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">清纯的奶茶婊</a></span> <span class="b">1-24 13:28</span>                     <a class="reply_to" href="flr?pid=82924574536&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复(3)</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=%E6%B8%85%E7%BA%AF%E7%9A%84%E5%A5%B6%E8%8C%B6%E5%A9%8A&amp;fid=707597&amp;act=2&amp;pid=82924574536&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82924574536&amp;lm=707597&amp;sc=82924574536&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">6楼. 6S，安卓就三星吧，另外我跟你说索移不属于索尼，索移粉不是索粉<br/><span class="g"><a href="i?un=%E8%8F%8A%E4%B9%8B%E5%93%80%E6%AE%87&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">菊之哀殇</a></span> <span class="b">1-24 13:34</span>                     <a class="reply_to" href="flr?pid=82924868892&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复(7)</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=%E8%8F%8A%E4%B9%8B%E5%93%80%E6%AE%87&amp;fid=707597&amp;act=2&amp;pid=82924868892&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82924868892&amp;lm=707597&amp;sc=82924868892&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">8楼. 主要还是看喜欢什么系统了，个人比较喜欢安卓。喜欢ios就买6s喽<br/><span class="g"><a href="i?un=%E5%B0%8F%E5%9C%9F%E8%B4%BCshine&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">小土贼shine</a></span> <span class="b">1-24 13:36</span>                     <a class="reply_to" href="flr?pid=82924956311&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=%E5%B0%8F%E5%9C%9F%E8%B4%BCshine&amp;fid=707597&amp;act=2&amp;pid=82924956311&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82924956311&amp;lm=707597&amp;sc=82924956311&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">9楼. 支持6楼，虽然我是安卓粉，用的也是索尼z3c，但我真心建议楼主，如果你不喜欢刷机啊，美化这类折腾的，买苹果不用考虑了。<br/><span class="g"><a href="i?un=%E6%80%9D%E5%BF%B5%E9%82%A3%E6%98%AF%E9%9D%92%E6%98%A5&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">思念那是青春</a></span> <span class="b">1-24 13:36</span>                     <a class="reply_to" href="flr?pid=82924958484&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复(1)</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=%E6%80%9D%E5%BF%B5%E9%82%A3%E6%98%AF%E9%9D%92%E6%98%A5&amp;fid=707597&amp;act=2&amp;pid=82924958484&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82924958484&amp;lm=707597&amp;sc=82924958484&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">10楼. 虽说喜欢SONY，可惜是安卓。为了流畅和app，还是苹果吧<br/><span class="g"><a href="i?un=edwardrei01&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">edwardrei01</a></span> <span class="b">1-24 13:37</span>                     <a class="reply_to" href="flr?pid=82925010097&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=edwardrei01&amp;fid=707597&amp;act=2&amp;pid=82925010097&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82925010097&amp;lm=707597&amp;sc=82925010097&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">11楼. 要是我就索尼，一直对苹果的设计无感<img src="http://tb2.bdstatic.com/tb/editor/images/client/image_emoticon25.png"/>而且Xperia ui用过我就不习惯其他厂商的ui改的乱七八糟<br/><span class="g"><a href="i?un=cdgeass&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">cdgeass</a></span> <span class="b">1-24 13:39</span>                     <a class="reply_to" href="flr?pid=82925084005&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复(2)</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=cdgeass&amp;fid=707597&amp;act=2&amp;pid=82925084005&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82925084005&amp;lm=707597&amp;sc=82925084005&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">12楼. 虽然我用的索尼，但苹果便宜点吧？捡便宜的买准没错<br/><span class="g"><a href="i?un=waawer&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">waawer</a></span> <span class="b">1-24 13:41</span>                     <a class="reply_to" href="flr?pid=82925198383&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复(10)</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=waawer&amp;fid=707597&amp;act=2&amp;pid=82925198383&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82925198383&amp;lm=707597&amp;sc=82925198383&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">13楼. z5p不解释<img src="http://tb2.bdstatic.com/tb/editor/images/client/image_emoticon3.png"/><br/><span class="g"><a href="i?un=gfgfttt&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">gfgfttt</a></span> <span class="b">1-24 13:43</span>                     <a class="reply_to" href="flr?pid=82925278860&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=gfgfttt&amp;fid=707597&amp;act=2&amp;pid=82925278860&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82925278860&amp;lm=707597&amp;sc=82925278860&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">14楼. 一直用索尼，因为好看，各种方面，不过玩游戏还是iOS方便<br/><span class="g"><a href="i?un=Vortexor&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">Vortexor</a></span> <span class="b">1-24 13:44</span>                     <a class="reply_to" href="flr?pid=82925297276&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复(1)</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=Vortexor&amp;fid=707597&amp;act=2&amp;pid=82925297276&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82925297276&amp;lm=707597&amp;sc=82925297276&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">15楼. <a href="http://m.tiebaimg.com/timg?wapp&amp;quality=80&amp;size=b400_2000&amp;cut_x=0&amp;cut_w=0&amp;cut_y=0&amp;cut_h=0&amp;sec=1369815402&amp;di=1a229a3368c454d4fa46b99834b8edef&amp;wh_rate=null&amp;src=http%3A%2F%2Fimgsrc.baidu.com%2Fforum%2Fpic%2Fitem%2Fb1fd566034a85edf6afd522e4e540923dc547592.jpg">图</a><br/><span class="g"><a href="i?un=%E9%9B%AA%E8%80%BB%E6%99%AF%E9%98%B3%E5%86%88&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">雪耻景阳冈</a></span> <span class="b">1-24 13:44</span>                     <a class="reply_to" href="flr?pid=82925300093&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=%E9%9B%AA%E8%80%BB%E6%99%AF%E9%98%B3%E5%86%88&amp;fid=707597&amp;act=2&amp;pid=82925300093&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82925300093&amp;lm=707597&amp;sc=82925300093&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">16楼. <a href="http://m.tiebaimg.com/timg?wapp&amp;quality=80&amp;size=b400_2000&amp;cut_x=0&amp;cut_w=0&amp;cut_y=0&amp;cut_h=0&amp;sec=1369815402&amp;di=96fb2d9cc4764365dc4824cb7e121a97&amp;wh_rate=null&amp;src=http%3A%2F%2Fimgsrc.baidu.com%2Fforum%2Fpic%2Fitem%2Fdc04ad86c9177f3e6168500077cf3bc79e3d56ae.jpg">图</a><br/><span class="g"><a href="i?un=%E9%9B%AA%E8%80%BB%E6%99%AF%E9%98%B3%E5%86%88&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">雪耻景阳冈</a></span> <span class="b">1-24 13:45</span>                     <a class="reply_to" href="flr?pid=82925353014&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复(6)</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=%E9%9B%AA%E8%80%BB%E6%99%AF%E9%98%B3%E5%86%88&amp;fid=707597&amp;act=2&amp;pid=82925353014&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82925353014&amp;lm=707597&amp;sc=82925353014&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">17楼. 6s，省心<br/><span class="g"><a href="i?un=%E9%A3%9E%E7%81%AB%E8%9B%BE%E5%AD%90&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">飞火蛾子</a></span> <span class="b">1-24 13:46</span>                     <a class="reply_to" href="flr?pid=82925421677&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=%E9%A3%9E%E7%81%AB%E8%9B%BE%E5%AD%90&amp;fid=707597&amp;act=2&amp;pid=82925421677&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82925421677&amp;lm=707597&amp;sc=82925421677&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">18楼. 我喜欢z5p，因为好看<br/><span class="g"><a href="i?un=ZAKU1000&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">ZAKU1000</a></span> <span class="b">1-24 13:47</span>                     <a class="reply_to" href="flr?pid=82925439314&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复(1)</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=ZAKU1000&amp;fid=707597&amp;act=2&amp;pid=82925439314&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82925439314&amp;lm=707597&amp;sc=82925439314&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">19楼. 你可以等等索尼Z6<img src="http://tb2.bdstatic.com/tb/editor/images/face/i_f16.png?t=20140803"/><br/><span class="g"><a href="i?un=%E7%A3%8A%E7%A3%8AKiller&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">磊磊Killer</a></span> <span class="b">1-24 13:47</span>                     <a class="reply_to" href="flr?pid=82925448547&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复(1)</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=%E7%A3%8A%E7%A3%8AKiller&amp;fid=707597&amp;act=2&amp;pid=82925448547&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82925448547&amp;lm=707597&amp;sc=82925448547&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">20楼. 6s<br/><span class="g"><a href="i?un=%E5%97%B7%E5%97%B7ge&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">嗷嗷ge</a></span> <span class="b">1-24 13:48</span>                     <a class="reply_to" href="flr?pid=82925471825&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=%E5%97%B7%E5%97%B7ge&amp;fid=707597&amp;act=2&amp;pid=82925471825&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82925471825&amp;lm=707597&amp;sc=82925471825&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">21楼. 6S<br/><span class="g"><a href="i?un=%E8%8B%A6%E6%B6%A9%E7%9A%84%E6%98%9F%E5%B0%98&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">苦涩的星尘</a></span> <span class="b">1-24 13:49</span>                     <a class="reply_to" href="flr?pid=82925531276&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=%E8%8B%A6%E6%B6%A9%E7%9A%84%E6%98%9F%E5%B0%98&amp;fid=707597&amp;act=2&amp;pid=82925531276&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82925531276&amp;lm=707597&amp;sc=82925531276&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">22楼. <img src="http://tb2.bdstatic.com/tb/editor/images/client/image_emoticon25.png"/>都不买<br/><span class="g"><a href="i?un=Joe__Gv99iccc&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">Joe__Gv99iccc</a></span> <span class="b">1-24 13:51</span>                     <a class="reply_to" href="flr?pid=82925622339&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复(1)</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=Joe__Gv99iccc&amp;fid=707597&amp;act=2&amp;pid=82925622339&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82925622339&amp;lm=707597&amp;sc=82925622339&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">23楼. 索尼好看，系统比较原生，用起来很舒服的<br/><span class="g"><a href="i?un=cingular987&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">cingular987</a></span> <span class="b">1-24 13:52</span>                     <a class="reply_to" href="flr?pid=82925681129&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=cingular987&amp;fid=707597&amp;act=2&amp;pid=82925681129&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82925681129&amp;lm=707597&amp;sc=82925681129&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">24楼. 索尼大法好<img src="http://tb2.bdstatic.com/tb/editor/images/client/image_emoticon16.png"/><br/><span class="g"><a href="i?un=%E5%A4%A9%E8%9D%8E%E9%BB%91%E7%82%8E&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">天蝎黑炎</a></span> <span class="b">1-24 13:52</span>                     <a class="reply_to" href="flr?pid=82925684025&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=%E5%A4%A9%E8%9D%8E%E9%BB%91%E7%82%8E&amp;fid=707597&amp;act=2&amp;pid=82925684025&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82925684025&amp;lm=707597&amp;sc=82925684025&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">25楼. 黑莓priv<br/><span class="g"><a href="i?un=%E7%BE%AFand%E5%B9%B3&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">羯and平</a></span> <span class="b">1-24 13:54</span>                     <a class="reply_to" href="flr?pid=82925763620&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复(1)</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=%E7%BE%AFand%E5%B9%B3&amp;fid=707597&amp;act=2&amp;pid=82925763620&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82925763620&amp;lm=707597&amp;sc=82925763620&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">26楼. 说是Google play国内的服务快恢复了，安卓市场应该会好点吧。反正我是大法<img src="http://tb2.bdstatic.com/tb/editor/images/client/image_emoticon16.png"/><br/><span class="g"><a href="i?un=yoyo%E7%95%AA%E9%95%BF&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">yoyo番长</a></span> <span class="b">1-24 13:59</span>                     <a class="reply_to" href="flr?pid=82925973284&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=yoyo%E7%95%AA%E9%95%BF&amp;fid=707597&amp;act=2&amp;pid=82925973284&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82925973284&amp;lm=707597&amp;sc=82925973284&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">27楼. 喜欢折腾就安卓，不喜欢折腾就安卓<img src="http://tb2.bdstatic.com/tb/editor/images/client/image_emoticon16.png"/><br/><span class="g"><a href="i?un=%E6%B4%9B_%E9%82%A1%E5%9F%8E&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">洛_邡城</a></span> <span class="b">1-24 13:59</span>                     <a class="reply_to" href="flr?pid=82925993877&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=%E6%B4%9B_%E9%82%A1%E5%9F%8E&amp;fid=707597&amp;act=2&amp;pid=82925993877&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82925993877&amp;lm=707597&amp;sc=82925993877&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">28楼. z5p，我是电信不能用索尼<br/><span class="g"><a href="i?un=773021211&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">773021211</a></span> <span class="b">1-24 14:01</span>                     <a class="reply_to" href="flr?pid=82926062471&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=773021211&amp;fid=707597&amp;act=2&amp;pid=82926062471&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82926062471&amp;lm=707597&amp;sc=82926062471&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">29楼. 用过z1z2，表示小毛病一堆夜拍垃圾要命，还是苹果吧，大法党还有一分钟到达战场，我先跑路了<br/><span class="g"><a href="i?un=%E4%BC%9F%E5%A4%A7%E7%9A%84%E7%8C%BF%E9%A6%96&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">伟大的猿首</a></span> <span class="b">1-24 14:01</span>                     <a class="reply_to" href="flr?pid=82926086529&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=%E4%BC%9F%E5%A4%A7%E7%9A%84%E7%8C%BF%E9%A6%96&amp;fid=707597&amp;act=2&amp;pid=82926086529&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82926086529&amp;lm=707597&amp;sc=82926086529&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">30楼. Z5P 不建议买大陆版（核心服务阉割太多），绝对比苹果强<br/><span class="g"><a href="i?un=%E6%8A%95%E5%85%A5%E4%B8%8A%E7%AA%81%E7%84%B6%E7%89%B9&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">投入上突然特</a></span> <span class="b">1-24 14:01</span>                     <a class="reply_to" href="flr?pid=82926091395&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=%E6%8A%95%E5%85%A5%E4%B8%8A%E7%AA%81%E7%84%B6%E7%89%B9&amp;fid=707597&amp;act=2&amp;pid=82926091395&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82926091395&amp;lm=707597&amp;sc=82926091395&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">31楼. 索尼大法好<br/><span class="g"><a href="i?un=%E5%91%A8%E4%B8%89%E4%B8%8B%E5%8D%88%E8%8C%B6&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">周三下午茶</a></span> <span class="b">1-24 14:07</span>                     <a class="reply_to" href="flr?pid=82926350324&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=%E5%91%A8%E4%B8%89%E4%B8%8B%E5%8D%88%E8%8C%B6&amp;fid=707597&amp;act=2&amp;pid=82926350324&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82926350324&amp;lm=707597&amp;sc=82926350324&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><div class="i">32楼. 如果你不是那种带着防水手机去游泳的主。索尼挺好的。true story。我现在这是第二个xperia了<br/>。。。BTW，培育和践行社会主义核心价值观是全社会的共同责任。<br/><span class="g"><a href="i?un=%E9%97%AA%E7%94%B5%E4%BA%9A%E9%BE%99&amp;lp=6033&amp;pinf=1_8_0_2_@steam_@4320033252">闪电亚龙</a></span> <span class="b">1-24 14:10</span>                     <a class="reply_to" href="flr?pid=82926488351&amp;kz=4320033252&amp;pn=0&amp;pinf=1_2_0">回复</a>      <a class="banned" href="m?tn=bdFIL&amp;z=4320033252&amp;word=steam&amp;un=%E9%97%AA%E7%94%B5%E4%BA%9A%E9%BE%99&amp;fid=707597&amp;act=2&amp;pid=82926488351&amp;pn=0&amp;r=0&amp;last=0&amp;pinf=1_2_0">封</a>  <a class="delete" href="m?tn=bdPBC&amp;tbs=76aa0b0c642a25561453709621&amp;z=4320033252&amp;word=steam&amp;pid=82926488351&amp;lm=707597&amp;sc=82926488351&amp;tbs=76aa0b0c642a25561453709621&amp;pn=0&amp;r=0&amp;last=0&amp;templeType=2&amp;pinf=1_2_0">删</a></div><form action="m" method="get"><div class="h"><div></div><a accesskey="6" href="m?kz=4320033252&amp;new_word=&amp;pinf=1_2_0&amp;pn=30&amp;lp=6005">下一页</a><br/>第1/4页<input name="pnum" size="5" type="text" value="4"/><input name="kz" type="hidden" value="4320033252"/><input name="see_lz" type="hidden" value="0"/><input name="tnum" type="hidden" value="178"/><input name="pinf" type="hidden" value="1_2_0"/><input name="pn" type="hidden" value="0"/><input name="r" type="hidden" value="0"/><input name="pd" type="hidden" value="0"/><input name="lp" type="hidden" value="6006"/><input name="sub" type="submit" value="跳页"/></div></form></div><a href="redirect?u=http%3A%2F%2Ftieba.baidu.com%2Fp%2F3397947600">笑话大放送 各种段子都有</a><br/><a href="redirect?u=http%3A%2F%2Ftieba.baidu.com%2Fp%2F2506930060">爱情真的需要门当户对吗？</a><br/><a name="reply"></a><div class="d h">
<form action="submit" method="post">
<div>
<input class="q" maxlength="5000" name="co" type="text"/><br/>
<input name="ti" type="hidden" value="话说索尼的z5和6s相比较而言哪个好qaq"/>
<input name="src" type="hidden" value="1"/>
<input name="word" type="hidden" value="steam"/>
<input name="tbs" type="hidden" value="76aa0b0c642a25561453709621"/>
<input name="ifpost" type="hidden" value="1"/>
<input name="ifposta" type="hidden" value="0"/>
<input name="post_info" type="hidden" value="0"/>
<input name="tn" type="hidden" value="baiduWiseSubmit"/>
<input name="fid" type="hidden" value="707597"/>
<input name="verify" type="hidden" value=""/>
<input name="verify_2" type="hidden" value=""/>
<input name="pinf" type="hidden" value="1_2_0"/>
<input name="pic_info" type="hidden" value=""/>
<input name="z" type="hidden" value="4320033252"/>
<input name="last" type="hidden" value="0"/>
<input name="pn" type="hidden" value="0"/>
<input name="r" type="hidden" value="0"/>
<input name="see_lz" type="hidden" value="0"/>
<input name="no_post_pic" type="hidden" value="0"/>
<input name="floor" type="hidden" value="178"/>
<input name="sub1" type="submit" value="回贴"/>
                                                                                         <input name="insert_smile" type="submit" value="插表情"/>
                             
                                <input name="insert_pic" type="submit" value="插图片"/><br/>
</div>
</form>
</div>
<div class="d h">管理模式|<a href="m?kz=4320033252&amp;r=0&amp;pn=0&amp;pinf=0_2_0&amp;see_lz=0">普通模式</a></div> <div class="d h">KIDJourney <br/><a href="i?un=KIDJourney&amp;lp=5007&amp;pinf=1_8_0_2_@steam_@4320033252">我的i贴吧</a> <a href="m?tn=bdFBW&amp;tab=favorite&amp;lp=6009&amp;pinf=1_2_0">我爱逛的贴吧</a><br/></div> <a href="m?kw=steam&amp;lp=6012&amp;pn=0&amp;pinf=1">steam吧</a> &lt; <a href="m?tn=bdIndex&amp;lp=6013&amp;pinf=1_2_0">贴吧</a> &lt; <a href="http://wap.baidu.com/?lp=6013&amp;pinf=1_2_0&amp;ssid=&amp;from=&amp;uid=439281407650F15229067DB692A4A231%3AFG%3D1&amp;pu=&amp;auth=&amp;originid=2&amp;mo_device=1&amp;bd_page_type=1">百度</a><br/> <a href="urs?src=1&amp;z=4320033252&amp;pinf=1_2_0">阅读设置</a><br/> <div style="text-align:center;"><a href="#top"><img alt="TOP" src="http://wap.baidu.com/r/wise/wapsearchindex/top.gif"/></a></div>    2016-1-25 16:13<a name="bottom"></a></div></body></html>
""")
    post = Post('blabla', soup=soupDemo)
    print(post)
    print(list(map(str, post.reply_list)))
