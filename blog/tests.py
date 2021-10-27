from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post


# Beautirulsoup4 설치하기 #
# pip install beautifulsoap4 #

# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client() # Client 객체를 이용해 사용 # #Client import #
        # setUp함수는 테스트를 실행하기 전에 공통적으로 수행할 어떤 작업의 내용을 넣어줌

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

    def test_post_list(self):
        # 포스트 목록 페이지를 가져온다
        response = self.client.get('/blog/')
        # 정상적으로 페이지가 로드
        self.assertEqual(response.status_code, 200)
        # OK 200/ Not found 404 /bad 400 #

        # 페이지 타이틀 'Blog'가 있는가
        soup = BeautifulSoup(response.content, 'html.parser')
        # 전달받은 html내용(response.content)을 분석해서 blog가 있는가
        # 전달받은 html 파서를 이용해 분석하겠다 분석한 결과 -> soup
        # BeutifulSoup import 하기

        # Blog 내용과 일치한가?
        self.assertEqual(soup.title.text, 'Blog')

        self.navbar_test(soup)

        # 포스트(게시물)이 하나도 없는 경우
        # post의 갯수가 0개 인가?
        self.assertEqual(Post.objects.count(),0)
        # Post import 하기

        # 없는 경우 적정한 안내 문구가 포함되어 있는지
        # main-area인 div 를 찾아라
        main_area = soup.find('div',id='main-area')
        # main-area에 없으면 '아직 게시물이 없습니다'를 포함 하는가?
        self.assertIn('아직 게시물이 없습니다.',main_area.text)

        # 포스트(게시물)이 2개 존재하는 경우
        # 임이의 2개 게시물 만들기
        # 첫번째 포스트
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content = 'Hello World!!! We are the world...'
        )
        # 두번째 포스트
        post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='1등이 전부가 아니잖아요'
        )
        # post의 갯수가 2개인가?
        self.assertEqual(Post.objects.count(), 2)

        # 목록페이지를 새롭게 불러와서
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 그 목록 페이지에 포스트(게시물)의 타이틀이 2개 존재하는가
        main_area = soup.find('div', id='main-area')
        # main_area의 텍스트에 001이 포함되었나?
        self.assertIn(post_001.title, main_area.text)
        # main_area의 텍스트에 002가 포함되었나?
        self.assertIn(post_002.title, main_area.text)
        # main_area의 텍스트에 '아직 게시물이 없습니다'가 존재하지 않는가?
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

    def test_post_detail(self):
        # 포스트 하나가 있다
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World!!! We are the world...'
        )
        # 이 포스트의 url이 /blog/1 이다.
        self.assertEqual(post_001.get_absolute_url(), '/blog/1')
        # url에 의해 정상적으로 상세페이지를 불러오는가
        response = self.client.get('/blog/1/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser') #웹브라우저

        self.navbar_test(soup)

        # 포스터의 title은 웹브라우저 탭 title에 들어있는가
        self.assertIn(post_001.title, soup.title.text)
        # 포스터의 title은 포스터영억에도 있는가
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id="post-area")
        self.assertIn(post_001.title, post_area.text)
        # 포스트 작성자가 있는가
        # 아직 작성중
        # 포스트의 내용이 있는가
        self.assertIn(post_001.content, post_area.text)