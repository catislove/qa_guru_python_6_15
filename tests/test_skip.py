"""
Параметризуйте фикстуру несколькими вариантами размеров окна
Пропустите мобильный тест, если соотношение сторон десктопное (и наоборот)
"""
import pytest
from selene import browser, have


def is_mobile(width):
    return width < 1012


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


def test_github_desktop():
    if is_mobile(browser.config.window_width):
        pytest.skip('Тесты для desktop')
    browser.open('/')
    browser.element("a[href='/login']").click()
    browser.element('.auth-form-header').should(have.exact_text('Sign in to GitHub'))


def test_github_mobile():
    if not is_mobile(browser.config.window_width):
        pytest.skip('Тесты для mobile')
    browser.open('/')
    browser.element('.flex-1 button').click()
    browser.element("a[href='/login']").click()
    browser.element('.auth-form-header').should(have.exact_text('Sign in to GitHub'))