from playwright.sync_api import Playwright, sync_playwright

import os
from os.path import join, dirname
from dotenv import load_dotenv
import csv


def run(playwright: Playwright, profile_links: list[str]) -> None:
    browser = playwright.chromium.launch(headless=False, timeout=10000)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.linkedin.com/
    page.goto("https://www.linkedin.com/")

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    EMAIL = os.environ.get('EMAIL')
    PASSWORD = os.environ.get('PASSWORD')

    # Click input[name="session_key"]
    page.locator("input[name=\"session_key\"]").click()

    # Fill input[name="session_key"]
    page.locator("input[name=\"session_key\"]").fill(EMAIL)

    # Click text=Senha Exibir >> [placeholder="\ "]
    page.locator("text=Senha Exibir >> [placeholder=\"\\ \"]").click()

    # Fill text=Senha Exibir >> [placeholder="\ "]
    page.locator("text=Senha Exibir >> [placeholder=\"\\ \"]").fill(PASSWORD)

    # Click text=Entrar >> nth=1
    # with page.expect_navigation(url="https://www.linkedin.com/feed/?trk=homepage-basic_signin-form_submit"):
    with page.expect_navigation():
        page.locator("text=Entrar").nth(1).click()
    # assert page.url == "https://www.linkedin.com/feed/?trk=homepage-basic_signin-form_submit"

    for profile in profile_links:
        # Open new page
        newPage = context.new_page()
        # Go to https://www.linkedin.com/in/profile/
        newPage.goto(profile)
        # Close page
        newPage.close()

    # ---------------------
    context.close()
    browser.close()


def read_profiles_file(filename) -> list[str]:
    with open(filename) as file:
        data = csv.reader(file)
        return [profile_line[0] for profile_line in data][1:]


with sync_playwright() as playwright:
    profiles = read_profiles_file('profiles.csv')
    run(playwright, profiles)
