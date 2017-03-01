from scraper.Helper import Helper
import time
import requests
from pathos.threading import ThreadPool

class Crawl:
    login_url = 'https://tutsplus.com/sign_in'
    course_data = []

    def __init__(self):
        cached_data = Helper.read_cache()

        if cached_data:
            self.course_data = cached_data
        else:
            self.driver = Helper.setup_webdriver()
            self.steps()
            Helper.store_cache(self.course_data)

        self.build_storage()
        self.begin_processing()

    def steps(self):
        self.login(self.login_url)

        for course in Helper.config('courses'):
            self.course_data.append(
                self.fetch_data(course)
            )

            time.sleep(Helper.config('sleep'))

        self.driver.close()

    # MAIN METHODS
    def login(self, url):
        print('- Logging in...')

        browser = self.driver
        browser.get(url)

        elements = {
            'user': 'session_login',
            'pass': 'session_password',
            'submit': 'sign-in__button'
        }

        browser.find_element_by_id(elements['user']).send_keys(Helper.config('username'))
        browser.find_element_by_id(elements['pass']).send_keys(Helper.config('password'))
        browser.find_element_by_class_name(elements['submit']).click()

    def fetch_data(self, url):
        course = self.get_course_data(url)
        lessons = map(self.get_lesson_data, course['lessons_links'])

        del course['lessons_links']
        course['lessons'] = list(lessons)

        return course

    def get_course_data(self, url):
        print('- Fetching course data...')

        browser = self.driver
        browser.get(url)

        elements = {
            'breadcrumb': 'content-banner__content-breadcrumb',
            'title': 'content-banner__title',
            'lessons': 'lesson-index__lesson-link'
        }

        breadcrumb_data = browser.find_element_by_class_name(elements['breadcrumb']).find_elements_by_tag_name('a')
        title = browser.find_element_by_class_name(elements['title'])
        lessons = browser.find_elements_by_class_name(elements['lessons'])

        lessons_links = []
        for lesson in lessons:
            lessons_links.append(
                lesson.get_attribute('href')
            )

        return {
            'category': breadcrumb_data[0].text.lower(),
            'sub_category': breadcrumb_data[1].text.lower(),
            'title': title.text,
            'lessons_links': lessons_links
        }

    def get_lesson_data(self, url):
        print('- Fetching lesson data...')

        browser = self.driver
        browser.get(url)

        elements = {
            'current_lesson': 'lesson-index__lesson--current',
            'title': 'lesson-index__lesson-title',
            'video': 'source',
            'number': 'lesson-index__lesson-number',
            'quality_list': 'w-menu__list-item--Quality',
            'quality_items': 'w-menu__list-link'
        }

        # Select best possible quality
        browser.execute_script("var quality = document.querySelectorAll('.w-menu__list-item--Quality .w-menu__list-link'); quality[quality.length - 1].click();")

        current_lesson = browser.find_element_by_class_name(elements['current_lesson'])
        title = current_lesson.find_element_by_class_name(elements['title'])
        video = browser.find_element_by_tag_name(elements['video'])
        number = current_lesson.find_element_by_class_name(elements['number'])

        return {
            'title': title.text,
            'number': number.text,
            'link': video.get_attribute('src')
        }

    def build_storage(self):
        print('- Building storage...')

        courses = self.course_data

        for course in courses:
            base_dir = Helper.config('storage')
            if not Helper.dir_exists(base_dir):
                Helper.make_dir(base_dir)

            category_dir = base_dir + '/' + course['category']
            if not Helper.dir_exists(category_dir):
                Helper.make_dir(category_dir)

            sub_category_dir = category_dir + '/' + course['sub_category']
            if not Helper.dir_exists(sub_category_dir):
                Helper.make_dir(sub_category_dir)

            course_dir = sub_category_dir + '/' + course['title']
            if not Helper.dir_exists(course_dir):
                Helper.make_dir(course_dir)

            for lesson in course['lessons']:
                file = course_dir + '/' + lesson['number'] + ' - ' + lesson['title'] + '.mp4'
                lesson['file'] = file

    def download_lesson(self, lesson):
        print(
            '- Preparing to download lesson "{lesson_title}"'.format(
                lesson_title=lesson['title']
            )
        )

        response = requests.get(lesson['link'], stream=True)
        chunk_size = 1024

        if Helper.file_exists(lesson['file']) and (Helper.get_file_size(lesson['file']) == int(response.headers['Content-Length'])):
            print(
                '-- Skipping... Lesson "{lesson_title}" has already been downloaded.'.format(
                    lesson_title=lesson['title']
                )
            )
        else:
            with open(lesson['file'], 'wb') as file:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    file.write(chunk)

            print(
                '-- Success... Lesson "{lesson_title}" has been downloaded.'.format(
                    lesson_title=lesson['title']
                )
            )

    def begin_processing(self):
        pool = ThreadPool(nodes=Helper.config('threads'))

        for course in self.course_data:
            pool.map(self.download_lesson, course['lessons'])
            print(
                '--- Course "{course_title}" has been downloaded, with total of {lessons_amount} lessons.'.format(
                    course_title=course['title'],
                    lessons_amount=len(course['lessons'])
                )
            )
            time.sleep(Helper.config('sleep'))
