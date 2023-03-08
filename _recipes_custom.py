from dataclasses import dataclass
from typing import List

from _recipe_utils import Recipe, CoverOptions, onlyon_weekdays, onlyon_days, onlyat_hours, last_n_days_of_month, first_n_days_of_month, every_x_days

# Define the categories display order, optional
categories_sort: List[str] = ["News", "Science", "Blogs", "Arts", "Magazines", "Politics"]

# Define your custom recipes list here
# Example: https://github.com/ping/newsrack-fork-test/blob/custom/_recipes_custom.py


@dataclass
class CustomConvOptions(Recipe):
    def __post_init__(self):
        self.conv_options = {
            "mobi": ["--output-profile=kindle_pw3", "--mobi-file-type=old", "--authors=newsrack"],
        }


@dataclass
class CustomOptionsRecipe(Recipe):
    # Use a different title date format and output profile from default
    def __post_init__(self):
        self.title_date_format = "%Y %b %-d"
        self.conv_options = {
            "mobi": ["--output-profile=kindle_pw3", "--mobi-file-type=old", "--authors=newsrack"],
        }


@dataclass
class CustomMonthlyRecipe(Recipe):
    # Use a different title date format and output profile from default
    def __post_init__(self):
        self.title_date_format = "%b %Y"
        self.conv_options = {
            "mobi": ["--output-profile=kindle_pw3", "--mobi-file-type=old", "--authors=newsrack"],
        }


recipes: List[Recipe] = [
    CustomOptionsRecipe(
        recipe="ars-technica",
        slug="ars-technica",
        src_ext="mobi",
        target_ext=["epub"],
        category="News",
        tags=["science", "tech", "commentary"],
        overwrite_cover=True,
        cover_options=CoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Ars_Technica_logo_(2016).svg/1024px-Ars_Technica_logo_(2016).svg.png",
            title_font_path="static/ReadexPro-SemiBold.ttf",
            datestamp_font_path="static/ReadexPro-Light.ttf"
        ),
        enable_on=onlyat_hours(list(range(10, 19)), 0),
    ),
    CustomOptionsRecipe(
        recipe="atlantic-custom",
        slug="the-atlantic",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=True,
        category="News",
        tags=["editorial", "commentary"],
        enable_on=onlyon_weekdays([3, 4, 5, 6], -4) and onlyat_hours(list(range(10, 19)), 0),
        cover_options=CoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/The_Atlantic_Logo_11.2019.svg/1200px-The_Atlantic_Logo_11.2019.svg.png",
            title_font_path="static/ReadexPro-SemiBold.ttf",
            datestamp_font_path="static/ReadexPro-Light.ttf"
        ),
    ),
    CustomMonthlyRecipe(
        recipe="atlantic-magazine-custom",
        slug="atlantic-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="News",
        tags=["editorial", "commentary"],
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -4)
        and onlyon_days(list(range(32 - 14, 32)), -4),
    ),
    CustomOptionsRecipe(
        recipe="duolingo-blog",
        slug="duolingo-blog",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=True,
        category="Blogs",
        tags=["science", "linguistics"],
        cover_options=CoverOptions(
            logo_path_or_url="https://i.imgur.com/ScfaQZb.png",
            title_font_path="static/ReadexPro-SemiBold.ttf",
            datestamp_font_path="static/ReadexPro-Light.ttf"
        ),
    ),
    CustomOptionsRecipe(
        recipe="the-forward",
        slug="the-forward",
        src_ext="mobi",
        target_ext=["epub"],
        category="News",
        tags=["editorial", "commentary", "news"],
        overwrite_cover=True,
        enable_on=False,
        cover_options=CoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/The_Forward_logo_2022.svg/1024px-The_Forward_logo_2022.svg.png",
            title_font_path="static/ReadexPro-SemiBold.ttf",
            datestamp_font_path="static/ReadexPro-Light.ttf"
        ),
    ),
    CustomOptionsRecipe(
        recipe="knowable-magazine-custom",
        slug="knowable-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        tags=["science"],
        overwrite_cover=True,
        cover_options=CoverOptions(
            logo_path_or_url="https://i.imgur.com/OMxGtzQ.jpg",
            title_font_path="static/ReadexPro-SemiBold.ttf",
            datestamp_font_path="static/ReadexPro-Light.ttf"
        ),
        enable_on=onlyon_weekdays([3, 4, 5, 6], -4) and onlyat_hours(list(range(10, 19)), -5),
    ),
    CustomOptionsRecipe(
        recipe="mother-jones",
        slug="mother-jones",
        src_ext="mobi",
        target_ext=["epub"],
        category="Politics",
        tags=["politics", "commentary"],
        overwrite_cover=True,
        enable_on=onlyon_weekdays([3, 4, 5, 6], -4) and onlyat_hours(list(range(10, 19)), -5),
        cover_options=CoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Mother_Jones_Logo_2019.svg/1024px-Mother_Jones_Logo_2019.svg.png",
            title_font_path="static/ReadexPro-SemiBold.ttf",
            datestamp_font_path="static/ReadexPro-Light.ttf"
        ),
    ),
    CustomOptionsRecipe(
        recipe="the-nation",
        slug="the-nation",
        src_ext="mobi",
        target_ext=["epub"],
        category="Politics",
        tags=["politics", "commentary"],
        overwrite_cover=False,
        enable_on=onlyon_weekdays([3, 4, 5, 6], -4) and onlyat_hours(list(range(10, 19)), -5),
        cover_options=CoverOptions(
            logo_path_or_url="",
            title_font_path="static/ReadexPro-SemiBold.ttf",
            datestamp_font_path="static/ReadexPro-Light.ttf"
        ),
    ),
    CustomOptionsRecipe(
        recipe="national-geographic",
        slug="national-geographic",
        src_ext="mobi",
        target_ext=["epub"],
        category="Magazines",
        tags=["daily", "history", "science"],
        overwrite_cover=True,
        enable_on=onlyon_weekdays([3, 4, 5, 6], -4) and onlyat_hours(list(range(10, 19)), -5),
        cover_options=CoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Natgeologo.svg/1024px-Natgeologo.svg.png",
            title_font_path="static/ReadexPro-SemiBold.ttf",
            datestamp_font_path="static/ReadexPro-Light.ttf"
        ),
    ),
    CustomOptionsRecipe(
        recipe="nature-custom",
        slug="nature",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        overwrite_cover=False,
        # enable_on=False,
        enable_on=onlyon_weekdays([2, 3, 4], 0),
        tags=["science", "weekly"],
    ),
    CustomOptionsRecipe(
        recipe="nautilus-custom",
        slug="nautilus",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        tags=["science", "weekly"],
        overwrite_cover=True,
        cover_options=CoverOptions(
            logo_path_or_url="https://assets.nautil.us/13891_bb83b72bf545e376f3ff9443bda39421.png",
            title_font_path="static/ReadexPro-SemiBold.ttf",
            datestamp_font_path="static/ReadexPro-Light.ttf"
        ),
        enable_on=onlyon_weekdays([2, 4, 5], 0),
    ),
    CustomOptionsRecipe(
        recipe="new-republic-magazine",
        slug="new-republic-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        category="Politics",
        overwrite_cover=False,
        tags=["politics", "commentary"],
        enable_on=(first_n_days_of_month(5) or last_n_days_of_month(5))
        and onlyat_hours(list(range(8, 16))),
    ),
    CustomOptionsRecipe(
        recipe="new-scientist",
        slug="new-scientist",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        tags=["weekly", "science"],
        overwrite_cover=False,
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -5),
        # cover_options=CoverOptions(
        #     logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/New_Scientist_logo.svg/1024px-New_Scientist_logo.svg.png",
        #     title_font_path="static/ReadexPro-SemiBold.ttf",
        #     datestamp_font_path="static/ReadexPro-Light.ttf"
        # ),
        conv_options={
            "mobi": ["--output-profile=kindle_pw3", "--mobi-file-type=old", "--tags='Science,News,Periodical'"],
        }
    ),
    CustomOptionsRecipe(
        recipe="newyorker-custom",
        slug="newyorker",
        src_ext="mobi",
        target_ext=["epub"],
        category="Arts",
        overwrite_cover=False,
        enable_on=onlyon_weekdays([1, 3, 5], -5),
        # enable_on=False,
        tags=["editorial", "commentary", "weekly"],
    ),
    CustomOptionsRecipe(
        recipe="nytimes-books-custom",
        slug="nytimes-books",
        src_ext="mobi",
        target_ext=["epub"],
        category="Arts",
        timeout=180,
        retry_attempts=0,
        enable_on=onlyon_weekdays([3, 4, 5, 6], -4) and onlyat_hours(list(range(10, 19)), -5),
        cover_options=CoverOptions(
            logo_path_or_url="https://static01.nyt.com/newsgraphics/2015/12/23/masthead-2016/8118277965bda8228105578895f2f4a7aeb22ce2/nyt-logo.png",
            title_font_path="static/ReadexPro-SemiBold.ttf",
            datestamp_font_path="static/ReadexPro-Light.ttf"
        ),
        tags=["literature"],
    ),
    CustomMonthlyRecipe(
        recipe="philosophy-now",
        slug="philosophy-now",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="Magazines",
        enable_on=first_n_days_of_month(4, -6) or last_n_days_of_month(4, -4),
        tags=["philosophy", "commentary", "bimonthly"],
    ),
    CustomMonthlyRecipe(
        recipe="poetry-custom",
        slug="poetry-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="Arts",
        title_date_format="%b %Y",
        enable_on=first_n_days_of_month(4, -6) or last_n_days_of_month(4, -5),
        tags=["literature", "arts", "monthly"],
    ),
    CustomOptionsRecipe(
        recipe="quanta-magazine-custom",
        slug="quanta-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        enable_on=onlyon_weekdays([0, 2, 4], -5)
        and onlyat_hours(list(range(8, 14)))
        and every_x_days(1, 1, 60),
        # enable_on=False,
        tags=["science"],
        cover_options=CoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Quanta_Magazine_Logo_05.2022.svg/640px-Quanta_Magazine_Logo_05.2022.svg.png",
            title_font_path="static/ReadexPro-SemiBold.ttf",
            datestamp_font_path="static/ReadexPro-Light.ttf"
        ),
    ),
    CustomMonthlyRecipe(
        recipe="scientific-american-custom",
        slug="scientific-american",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        overwrite_cover=False,
        enable_on=onlyon_days(list(range(15, 31)), -5)
        and onlyat_hours(list(range(10, 20))),  # middle of the month?
        # enable_on=False,
        tags=["science", "tech", "monthly"],
    ),
    CustomMonthlyRecipe(
        recipe="smithsonian-magazine-custom",
        slug="smithsonian-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        category="Magazines",
        enable_on=onlyon_days(list(range(16, 31)), -5)
        and onlyat_hours(list(range(10, 19)), -5),
        overwrite_cover=False,
        tags=["science", "history", "monthly"],
    ),
    CustomOptionsRecipe(
        recipe="teen-vogue",
        slug="teen-vogue",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=True,
        category="Magazines",
        enable_on=False,
        cover_options=CoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Teen_Vogue_logo.svg/1024px-Teen_Vogue_logo.svg.png",
            title_font_path="static/ReadexPro-SemiBold.ttf",
            datestamp_font_path="static/ReadexPro-Light.ttf"
        ),
        tags=["news", "politics"],
    ),
    CustomOptionsRecipe(
        recipe="time-magazine-custom",
        slug="time-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="Magazines",
        enable_on=onlyon_weekdays([3, 4, 5, 6], -4) and onlyat_hours(list(range(10, 19)), -5),
        tags=["news", "politics", "weekly"],
    ),
    CustomMonthlyRecipe(
        recipe="wired-custom",
        slug="wired",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=True,
        category="Science",
        tags=["science", "tech", "monthly"],
        enable_on=(first_n_days_of_month(4) or last_n_days_of_month(4))
        and onlyat_hours(list(range(10, 20))),
        title_date_format="%b %Y",
        cover_options=CoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Wired_logo.svg/1024px-Wired_logo.svg.png",
            title_font_path="static/ReadexPro-SemiBold.ttf",
            datestamp_font_path="static/ReadexPro-Light.ttf"
        ),
    ),
    CustomOptionsRecipe(
        recipe="wired-daily",
        slug="wired-daily",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=True,
        category="Science",
        tags=["science", "tech", "daily"],
        enable_on=lambda recipe: every_x_days(
            last_run=recipe.last_run, days=1, drift=0
        ),
        cover_options=CoverOptions(
            logo_path_or_url="https://www.wired.com/images/logos/wired.png",
            title_font_path="static/ReadexPro-SemiBold.ttf",
            datestamp_font_path="static/ReadexPro-Light.ttf"
        ),
    ),
    # Recipe(
    #     recipe="example",
    #     slug="example",
    #     src_ext="epub",
    #     category="example",
    # ),
]
