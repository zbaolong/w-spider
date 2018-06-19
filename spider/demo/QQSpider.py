#encoding:utf-8
import requests,re,time,pymongo
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class SimulateLogin:
    def __init__(self):
        """
        对Chrome浏览器进行配置：1.设置为headless无头浏览器 2.设置网页默认不加载图片。
        """
        self.chrome_opt = webdriver.ChromeOptions()
        # self.chrome_opt.add_argument('--headless')
        # self.chrome_opt.add_argument('--disable-gpu')
        self.prefs = {"profile.managed_default_content_settings.images": 2}
        self.chrome_opt.add_experimental_option("prefs", self.prefs)

    def do_scroll(self):
        """
        实际上模拟下拉滚动条，通过driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")的方法就可以简单的实现;
        但是这里比较特殊，因为在点击下一页加载到的新网页锚定义在顶端，在返回顶部后，使用上边的方法，直接定位到顶端的锚，中间的内容不再显示.
        """
        a,b = 0,1500
        for each in range(15):
            print('正在进行第{}次下拉'.format(each))
            self.driver.execute_script("window.scrollTo({}, {});".format(a,b))
            time.sleep(2)
            a += 1500
            b += 1500

    def goto_top(self):
        #切换到默认的框架，点击返回顶部：
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath('//*[@id="goto_top_btn"]').click()
        # self.driver.switch_to.frame("app_canvas_frame")

    def login(self,target_num):
        try:
            self.driver = webdriver.Chrome(chrome_options=self.chrome_opt)
            self.driver.get('https://user.qzone.qq.com/{}/311'.format(target_num))
            print('成功打开网页，开始模拟登录')
            time.sleep(3)
            # 切换到登陆的iframe框架:
            self.driver.switch_to.frame("login_frame")
            try:
                #通过快速登录：
                self.driver.find_element_by_xpath('//*[@id="qlogin_list"]/a[1]').click()
            except:
                # 通过提交表单的方式登录：查找到用户名和密码的表单，并填入账号和密码：
                self.driver.find_element_by_xpath('//*[@id="switcher_plogin"]').click()
                time.sleep(1)
                self.driver.find_element_by_xpath('//*[@id="u"]').send_keys('1437876073')
                self.driver.find_element_by_xpath('//*[@id="p"]').send_keys('zhengzuqin110.')
                self.driver.find_element_by_xpath('//*[@id="login_button"]').send_keys(Keys.ENTER)
            return True
        except:
            return False

    def get_pn_and_first_html(self):
        """
        这个函数中第一次模拟下拉滚动条，得到返回的变量，并且进行第一次翻页操作；
        :return:第一页的网页源代码和说说的页数
        """
        self.do_scroll()
        self.driver.switch_to.frame("app_canvas_frame")
        self.last_pagenum = etree.HTML(self.driver.page_source).xpath('//*[@id="_pager_content_0"]/p[1]/a[last()-1]/span/text()')
        time.sleep(3)
        first_page_source = self.driver.page_source
        #点击下一页
        self.driver.find_element_by_xpath('//*[@id="pager_next_0"]').click()
        self.driver.switch_to_default_content()
        return first_page_source,self.last_pagenum

    def run(self,target):
        target_num = target
        login_result = self.login(target_num)
        print('登陆成功') if login_result else print('登陆失败')
        time.sleep(4)
        page_source_list = []
        first_page_source,last_pagenum = self.get_pn_and_first_html()
        print(last_pagenum)
        page_source_list.append(first_page_source)
        # 对翻页进行循环:
        if int(last_pagenum[0]) > 15:
            pagenum = 15
        else:
            pagenum = int(self.last_pagenum[0])
        for each in range(1,pagenum):
            # 模拟下拉滚动条：
            self.do_scroll()
            time.sleep(2)
            self.driver.switch_to.frame("app_canvas_frame")
            time.sleep(2)
            #获得说说页面的源代码：
            self.driver.page_source
            page_source_list.append(self.driver.page_source)
            print('成功获取网页的第{}份源代码'.format(each+1))
            if len(last_pagenum) == 0:
                break
            # 点击下一页的按钮:
            try:
                self.driver.find_element_by_xpath('//*[@id="pager_next_{}"]'.format(each)).click()
            except:
                pass
            time.sleep(5)
            self.goto_top()
            time.sleep(2)
            print('返回顶部')
            # break
        self.driver.close()
        return page_source_list

class SpaceSpider:
    def __init__(self):
        self.simulate = SimulateLogin()
        with open('target.txt', encoding='utf-8') as f:
            ids = [re.findall('\d+', each)[0] for each in f.readlines()]
            self.target_list = list(set(ids))
        # self.target_list = ['1033213911']
        self.conn = pymongo.MongoClient('localhost',27017)
        self.db = self.conn['data']
        self.users_table = self.db['users']
        self.cln = self.db['all']

    def get_personal_space(self,html):
        """
        通过传入的html参数，利用xpath获取源码中每一条说说的信息,说说的信息包括：
        :param html:app_canvas_frame框架的源码;
        :return:mood_list代表该html源码（说说的每一页）所有的说说信息.
        """
        html = etree.HTML(html)
        #得到一页中说说的数量：
        li_count = len(html.xpath('//*[@id="msgList"]/li'))
        mood_list = []
        # 对每一条说说进行循环：
        for mood_n in range(1, li_count+1):
            mood = {}
            #优先从从div[3]获取转发的说说内容，如果出现IndexError则再从div[2]中获取本人发表的说说内容：
            try:
                mood_cont = '【转】' +[each.xpath('string(.)') for each in
                             html.xpath('//*[@id="msgList"]/li[{}]/div[3]/div[3]//pre'.format(mood_n))][0]
            except IndexError:
                try:
                    mood_cont = [each.xpath('string(.)') for each in
                                 html.xpath('//*[@id="msgList"]/li[{}]/div[3]/div[2]/pre'.format(mood_n))][0]
                except:
                    mood_cont = ''
            # try:
            #     mood_cont = \
            #     [each.xpath('string(.)') for each in html.xpath('//*[@id="msgList"]/li[{}]/div[3]/div[2]/pre'
            #                                                     .format(mood_n))][0]
            # except IndexError:
            #     try:
            #         mood_cont = \
            #             [each.xpath('string(.)') for each in html.xpath('//*[@id="msgList"]/li[{}]/div[3]/div[3]//pre'
            #                                                             .format(mood_n))][0]
            #     except IndexError:
            if len(mood_cont) == 0:
                mood['mood_cont'] = 'No text.My be only picture'
            else:
                mood['mood_cont'] = mood_cont
            try:
                mood['publish_time'] = \
                    html.xpath('//*[@id="msgList"]/li[{}]/div[3]/div[@class="ft"]/div[1]/span/a/@title'.format(mood_n))
            except IndexError:
                mood['publish_time'] = 'Unknown'
            # ----爬取每一条评论的用户信息和评论内容----：
            # 获取评论者的网名（备注）：
            comtors_name = html.xpath(
                '//ol[@id="msgList"]/li[{}]/div[last()-1]/div[last()]//div[@class="mod_comments"]/div/ul/li/div/div[1]//div[@class="comments_content"]/a/text()'.format(
                    mood_n))
            comments_cont = [each.xpath('string(.)') for each in
                             html.xpath('//ol[@id="msgList"]/li[{}]/div[last()-1]/div[last()]//'
                                        'div[@class="mod_comments"]/div/ul/li/div/div[1]//div[@class="comments_content"]/span[last()]'.format(
                                 mood_n))]
            # 获取评论者的QQ号：
            comtors_num_xpath = '//ol[@id="msgList"]/li[{}]/div[last()-1]/div[last()]//div[@class="mod_comments"]/div/ul/li/div/div[1]//div[@class="comments_content"]/a/@href'.format(
                mood_n)
            comtors_num = [re.findall('\d+', each, re.S)[0] for each in html.xpath(comtors_num_xpath)]
            # 创建字典列表，用来存放每一个评论信息组成的字典：
            comments_list = []
            # 对每一条评论的信息循环：
            comment_index = 1
            for num, name, content in zip(comtors_num, comtors_name, comments_cont):
                comments_dict = {}
                comments_dict['comtors_name'] = name
                comments_dict['content'] = content
                comments_dict['comtors_num'] = num
                # 爬取评论者和房主的回复信息:
                reply_cont = [each.xpath('string(.)') for each in
                              html.xpath(
                                  '//ol[@id="msgList"]/li[{}]/div[last()-1]/div[last()]//div[@class="mod_comments"]'
                                  '/div/ul/li[{}]/div/div[2]//div[@class="comments_content"]/span[last()]'.format(
                                      mood_n, comment_index))]
                reply_er_name = html.xpath(
                    '//ol[@id="msgList"]/li[{}]/div[last()-1]/div[last()]//div[@class="mod_comments"]'
                    '/div/ul/li[{}]/div/div[2]//div[@class="comments_content"]/a/text()'.format(mood_n, comment_index))
                reply_er_num = [re.findall('\d+', each, re.S)[0] for each in
                                html.xpath('//ol[@id="msgList"]/li[{}]/div[last()-1]/'
                                           'div[last()]//div[@class="mod_comments"]/div/ul/li[{}]/div/div[2]//div[@class="comments_content"]/a/@href'.format(
                                    mood_n, comment_index))]
                reply_list = []
                for r_num, r_name, r_cont in zip(reply_er_num, reply_er_name, reply_cont):
                    reply_dict = {}
                    if r_cont == ' ' or len(r_cont) == 0:
                        reply_dict['r_content'] = 'No text'
                    else:
                        reply_dict['r_content'] = r_cont
                    reply_dict['r_num'] = r_num
                    reply_dict['r_name'] = r_name
                    reply_list.append(reply_dict)
                if len(reply_list) == 0:
                    comments_dict['reply'] = 'No reply'
                else:
                    comments_dict['reply'] = reply_list
                comments_list.append(comments_dict)
                comment_index += 1
            # 判断评论的字典列表是否为空，为空则赋值没有评论：
            if len(comments_list) == 0:
                mood['comments'] = 'No Comments'
            else:
                mood['comments'] = comments_list
            mood_list.append(mood)
        return mood_list

    def insert_mongo(self,user_mood_list,target):
        for each in user_mood_list:
            for ent in each:
                ent['own_qqNum'] = target
                self.cln.insert_one(ent)

    def get_everyone_space(self):
        """
        对目标的QQ循环进行爬取
        """
        for target in self.target_list:
            if target in [each['qq_num'] for each in self.users_table.find()]:
                print('{} 空间已经爬取！开始下一个目标空间的爬取...'.format(target))
                continue
            try:
                print('正在爬取{} 的空间...'.format(target))
                pagesource_list = self.simulate.run(target)
                user_moods_list = []
                for each in pagesource_list:
                    mood_list = self.get_personal_space(each)
                    user_moods_list.append(mood_list)
                print(user_moods_list)
                print('源码爬取成功，开始插入数据库...')
                self.insert_mongo(user_moods_list, target)
                self.users_table.insert_one({'qq_num': target})
                print('成功插入数据库！{} 空间爬取成功，开始下一个目标的空间爬取...'.format(target))
            except BaseException as e:
                print('{} 空间爬取失败！'.format(target))
                print('错误信息为：{}'.format(e))
                continue
            break

if __name__ == '__main__':
    spider = SpaceSpider()
    spider.get_everyone_space()
    # spider.test()