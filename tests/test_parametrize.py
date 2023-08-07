"""
Переопределите параметр с помощью indirect параметризации на уровне теста
"""
import pytest
from selene import have
from selene.support.shared import browser


@pytest.fixture(
    scope='function',
    autouse=True,
    params=[(1366, 768), (1920, 1080), (480, 800), (360, 640)]
)
def browser_manager(request):
    browser.config.base_url = 'https://github.com'
    browser.config.window_width = request.param[0]
    browser.config.window_height = request.param[1]
    yield
    browser.quit()


@pytest.mark.parametrize('browser_manager', [(1366, 768), (1920, 1080)], indirect=True)
def test_github_desktop():
    browser.open('/')
    browser.element("a[href='/login']").click()
    browser.element('.auth-form-header').should(have.exact_text('Sign in to GitHub'))


@pytest.mark.parametrize('browser_manager', [(480, 800), (360, 640)], indirect=True)
def test_github_mobile():
    browser.open('/')
    browser.element('.flex-1 button').click()
    browser.element("a[href='/login']").click()
    browser.element('.auth-form-header').should(have.exact_text('Sign in to GitHub'))