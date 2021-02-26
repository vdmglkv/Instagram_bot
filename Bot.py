from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from admin.aut_date import username, password
import time
import random
from selenium.common.exceptions import NoSuchElementException
import requests
import os


class InstagramBot:

    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.browser = webdriver.Chrome("../Instagram_Bot/Chromedriver/chromedriver.exe")

    # метод для закрытия браузера
    def close_browser(self):

        self.browser.close()
        self.browser.quit()

    # метод логина
    def login(self):

        browser = self.browser
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(3, 5))

        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(2)

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)
        time.sleep(10)

    # метод ставит лайки по hashtag
    def like_photo_by_hashtag(self, hashtag):

        browser = self.browser
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)

        for i in range(1, 4):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))

        hrefs = browser.find_elements_by_tag_name('a')
        posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

        for url in posts_urls:
            try:
                browser.get(url)
                time.sleep(3)
                like_button = browser.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button')
                like_button.click()
                time.sleep(random.randrange(80, 100))
            except Exception as ex:
                print(ex)
                self.close_browser()

    # метод проверяет по xpath существует ли элемент на странице
    def xpath_exists(self, url):

        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # метод ставит лайк на пост по прямой ссылке
    def like_by_direct_link(self, userpost):

        browser = self.browser
        browser.get(userpost)
        time.sleep(4)

        if not self.xpath_exists(userpost):
            print("Пост успешно найден, ставим лайк!")
            time.sleep(2)

            like_button = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
            browser.find_element_by_xpath(like_button).click()
            time.sleep(2)

            print(f"Лайк на пост: {userpost} поставлен!")
            self.close_browser()

        else:
            print("Такого поста не существует, проверьте URL")
            self.close_browser()

    # метод собирает ссылки на все посты пользователя
    def collect_post_url(self, userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(10)

        if not self.xpath_exists(userpage):
            print("Пользователь успешно найден, ставим лайки!")
            time.sleep(2)

            posts_count = int(browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text)
            loops_count = int(posts_count)
            # print(loops_count)

            posts_urls = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

                for href in hrefs:
                    posts_urls.append(href)

                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # time.sleep(random.randrange(5, 10))
                print(f"Итерация #{i}")

            file_name = userpage.split("/")[-2]

            with open(f'{file_name}.txt', 'a') as file:
                for post_url in posts_urls:
                    file.write(post_url + "\n")

            set_posts_urls = set(posts_urls)
            set_posts_urls = list(set_posts_urls)

            with open(f'{file_name}_set.txt', 'a') as file:
                for post_url in set_posts_urls:
                    file.write(post_url + '\n')

        else:
            print("Такого пользователя не существует, проверьте URL")
            self.close_browser()

    # метод ставит лайки по ссылке на аккаунт пользователя
    def put_many_likes(self, userpage):

        browser = self.browser
        self.collect_post_url(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(5)
        browser.get(userpage)
        time.sleep(5)

        with open(f'{file_name}_set.txt') as file:
            urls_list = file.readlines()

            for post_url in urls_list:
                try:
                    browser.get(post_url)
                    time.sleep(2)

                    like_button = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
                    browser.find_element_by_xpath(like_button).click()
                    # time.sleep(random.randrange(80, 100))
                    time.sleep(2)

                    print(f"Лайк на пост: {post_url} успешно поставлен!")
                except Exception as ex:
                    print(ex)
                    self.close_browser()

        self.close_browser()

    # метод скачивает контент со страницы пользователя
    def download_content(self, userpage):

        browser = self.browser
        self.collect_post_url(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(5)
        browser.get(userpage)
        time.sleep(5)

        # Создание папки пользователя
        if os.path.exists(f"{file_name}"):
            print("Папка уже существует!")
        else:
            print(f"Создаём папку пользователя {file_name}.")
            os.mkdir(file_name)

        img_and_video_src_urls = []
        with open(f'{file_name}_set.txt') as file:
            urls_list = file.readlines()

            for post_url in urls_list:
                try:
                    browser.get(post_url)
                    time.sleep(5)

                    img_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/img"
                    video_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div/div/video"
                    post_id = post_url.split("/")[-2]

                    if self.xpath_exists(img_src):
                        img_src_url = browser.find_element_by_xpath(img_src).get_attribute("src")
                        img_and_video_src_urls.append(img_src_url)

                        # сохраняем изображение
                        get_img = requests.get(img_src_url)
                        with open(f"{file_name}/{file_name}_{post_id}_img.jpg", "wb") as img_file:
                            img_file.write(get_img.content)

                    elif self.xpath_exists(video_src):
                        video_src_url = browser.find_element_by_xpath(video_src).get_attribute("src")
                        img_and_video_src_urls.append(video_src_url)

                        # сохраняем видео
                        get_video = requests.get(video_src_url, stream=True)
                        with open(f"{file_name}/{file_name}_{post_id}_video.mp4", "wb") as video_file:
                            for chunk in get_video.iter_content(chunk_size=1024 * 1024):
                                if chunk:
                                    video_file.write(chunk)
                    else:
                        print("Упс! Что-то пошло не так!")
                        img_and_video_src_urls.append(f"{post_url}, нет ссылки!")
                    print(f"Контент из поста {post_url} успешно скачан!")

                except Exception as ex:
                    print(ex)
                    self.close_browser()

            self.close_browser()

        with open(f'{file_name}/{file_name}_img_and_video_src_urls.txt', 'a') as file:
            for i in img_and_video_src_urls:
                file.write(i + "\n")

    def all_followers(self, userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)
        file_name = userpage.split("/")[-2]

        # Cоздание папки пользователя
        if os.path.exists(f"{file_name}"):
            print(f"Папка {file_name} уже существует!")
        else:
            print(f"Создаём папку пользователя {file_name}.")
            os.mkdir(file_name)

        if not self.xpath_exists(userpage):
            print(f"Пользователь {file_name} успешно найден, начинаем скачивать ссылки на подписчиков!")
            time.sleep(3)

            follow_button = browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a")
            follow_count = follow_button.text
            follow_count = int(follow_count.split(" ")[0])
            time.sleep(5)
            # print(follow_count)

            # Уменьшение кол-ва подписок для обхода блокировки
            loops_count = int(follow_count / 20)
            print(f"Кол-во скачиваемых ссылок: {loops_count}")
            time.sleep(5)

            follow_button.click()
            time.sleep(5)

            followers_ul = browser.find_element_by_css_selector("body > div.RnEpo.Yx5HN > div > div > div.isgrP")

            try:
                followers_urls = []
                for i in range(1, loops_count + 1):
                    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                    time.sleep(random.randint(3, 5))
                    print(f"Итерация #{i}")

                all_followers_urls = followers_ul.find_elements_by_tag_name("li")
                # print(all_followers_urls)

                for url in all_followers_urls:
                    url = url.find_element_by_tag_name("a").get_attribute("href")
                    followers_urls.append(url)

                with open(f"{file_name}/{file_name}.txt", "a") as text_file:
                    for link in followers_urls:
                        text_file.write(link + "\n")

                with open(f"{file_name}/{file_name}.txt") as text_file:
                    users_link = text_file.readlines()

                    for user in users_link:
                        try:
                            try:
                                with open(f'{file_name}/{file_name}_subscribe_list.txt', 'r') as subscribe_list_file:
                                    lines = subscribe_list_file.readlines()
                                    if user in lines:
                                        print(f'Мы уже подписаны на {user}, переходим к следующему пользователю!')
                                        continue

                            except Exception as ex:
                                print('Файл со ссылками ещё не создан!')
                                print(ex)

                            browser = self.browser
                            browser.get(user)
                            owner = user.split("/")[-2]

                            if self.xpath_exists("/html/body/div[1]/section/main/div/header/section/div[1]/div/a"):
                                print("Это наш профиль!")
                            elif self.xpath_exists(
                                    "/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/span/span["
                                    "1]/button/div/span"):
                                print(f"Уже подписаны, на {owner} пропускаем итерацию!")
                            else:
                                time.sleep(random.randint(5, 10))

                                if self.xpath_exists("/html/body/div[1]/section/main/div/div/article/"
                                                     "div[1]/div/h2"):
                                    try:
                                        follow_button = browser.find_element_by_css_selector(
                                            "#react-root > section > main > div > header > section > div.nZSzR > "
                                            "div.Igw0E.IwRSH.eGOV_.ybXk5._4EzTm > div > div > button")
                                        follow_button.click()
                                        print(f"Запросили подписку на закрытый аккаунт пользователя {owner}!")

                                    except Exception as ex:
                                        print(ex)
                                else:
                                    try:
                                        if self.xpath_exists(
                                                "/html/body/div[1]/section/main/div/header/section/div[1]"
                                                "/div[1]/button"):
                                            print(f"Подписались на аккаунт пользователя {owner}!")

                                    except Exception as ex:
                                        print(ex)

                                with open(f'{file_name}/{file_name}_subscribe_list.txt',
                                          'a') as subscribe_list_file:
                                    subscribe_list_file.write(user)

                                time.sleep(random.randint(5, 10))

                        except Exception as ex:
                            print(ex)
                            self.close_browser()

            except Exception as ex:
                print(ex)
                self.close_browser()

        else:
            print("Такого пользователя не существует, проверьте URL")
            self.close_browser()

        self.close_browser()


# my_bot = InstagramBot(username, password)
# my_bot.login()
# my_bot.all_followers("https://www.instagram.com/gulakovvadim/")
