#!/usr/bin/env python3
from playwright.sync_api import Playwright, sync_playwright

import os
from os.path import join, dirname
from dotenv import load_dotenv
import csv
import sys


def run(playwright: Playwright, profile_links: list[str], timeout=10000):
    browser = playwright.chromium.launch(headless=False, timeout=timeout)
    context = browser.new_context()

    page = context.new_page()
    page.goto("https://www.linkedin.com/")

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    EMAIL = os.environ.get('EMAIL')
    PASSWORD = os.environ.get('PASSWORD')

    page.locator("input[name=\"session_key\"]").click()
    page.locator("input[name=\"session_key\"]").fill(EMAIL)

    page.locator("text=Senha Exibir >> [placeholder=\"\\ \"]").click()
    page.locator("text=Senha Exibir >> [placeholder=\"\\ \"]").fill(PASSWORD)

    with page.expect_navigation():
        page.locator("text=Entrar").nth(1).click()

    for profile in profile_links:
        newPage = context.new_page()
        newPage.goto(profile)
        newPage.close()

    context.close()
    browser.close()


def read_profiles_file(filename) -> list[str]:
    with open(filename) as file:
        file_data = csv.reader(file)
        header, *profiles = file_data
        email_index = header.index('email')
        return [profile[email_index] for profile in profiles]


with sync_playwright() as playwright:
    file_path = sys.argv[-1]

    profiles = read_profiles_file(file_path)

    run(playwright, profiles, 10000)
