from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category


# Beautirulsoup4 설치하기 #
# pip install beautifulsoap4 #

# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client() # Client 객체를 이용해 사용 # #Client import #
        # setUp함수는 테스트를 실행하기 전에 공통적으로 수행할 어떤 작업의 내용을 넣어줌

        self.user_james = User.objects.create_user(username='James', password='somepassword')
        self.user_trump = User.objects.create_user(username='Trump', password='somepassword')

        self.category_programming = Category.objects.create(name='programming', slug='programming')
        self.category_culture = Category.objects.create(name='culture', slug='culture')

        self.post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World!!! We are the world...',
            author=self.user_james,
            category=self.category_programming
        )
        # 두번째 포스트
        self.post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='1등이 전부가 아니잖아요',
            author=self.user_trump,
            category=self.category_culture
        )
        self.post_003 = Post.objects.create(
            title='세 번째 포스트입니다.',
            content='세 번째 포스트입니다.',
            author=self.user_trump,
        )

    def navbar_test(self, soup):
        # 네비게이션바가 있다
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        logo = navbar.find('a', text='Internet Programming')
        self.assertEqual(logo.attrs['href'], '/')
        home = navbar.find('a', text='Home')
        self.assertEqual(home.attrs['href'], '/')
        blog = navbar.find('a', text='Blog')
        self.assertEqual(blog.attrs['href'], '/blog/')
        about = navbar.find('a', text='About Me')
        self.assertEqual(about.attrs['href'], '/about_me/')

    def category_test(self, soup):
        category=soup.find('div', id='category-card')
        self.assertIn('Categories', category.text)
        self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})', category.text)
        self.assertIn(f'{self.category_culture.name} ({self.category_culture.post_set.count()})', category.text)
        self.assertIn(f'미분류 (1)', category.text)

    def test_post_list(self):
        self.assertEqual(Post.objects.count(), 3)

        # 포스트 목록 페이지를 가져온다
        response = self.client.get('/blog/')
        # 정상적으로 페이지가 로드
        self.assertEqual(response.status_code, 200)
        # OK 200/ Not found 404 /bad 400 #

        # 페이지 타이틀 'Blog'가 있는가
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')

        self.navbar_test(soup)
        self.category_test(soup)

        # 그 목록 페이지에 포스트(게시물)의 타이틀이 3개 존재하는가
        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        post_001_card = main_area.find('div', id="post-1")
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.nmae, post_001_card.text)

        post_002_card = main_area.find('div', id="post-2")
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)

        post_003_card = main_area.find('div', id="post-3")
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn('미분류', post_003_card.text)

        self.assertIn(self.user_james.username.upper(), main_area.text)
        self.assertIn(self.user_trump.username.upper(), main_area.text)

        # 포스트(게시물)이 하나도 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        main_area = soup.find('div',id='main-area')
        self.assertIn('아직 게시물이 없습니다.',main_area.text)

    def test_post_detail(self):
        # 포스트 하나가 있다

        # 이 포스트의 url이 /blog/1 이다.
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1')
        # url에 의해 정상적으로 상세페이지를 불러오는가
        response = self.client.get('/blog/1/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser') #웹브라우저

        self.navbar_test(soup)
        self.category_test(soup)

        # 포스터의 title은 웹브라우저 탭 title에 들어있는가
        self.assertIn(self.post_001.title, soup.title.text)
        # 포스터의 title은 포스터영억에도 있는가
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id="post-area")
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.post_001.category.name, post_area.text)
        # 포스트 작성자가 있는가
        # 아직 작성중
        # 포스트의 내용이 있는가
        self.assertIn(self.post_001.content, post_area.text)
        self.assertIn(self.user_james.username.upper(), post_area.text)