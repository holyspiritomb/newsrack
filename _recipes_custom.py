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
            "mobi": ["--output-profile=kindle_pw3", "--mobi-file-type=old", "--authors=newsrack", "--publisher=https://holyspiritomb.github.io/newsrack/"],
        }


@dataclass
class CustomOptionsRecipe(Recipe):
    # Use a different title date format and output profile from default
    def __post_init__(self):
        self.title_date_format = "%Y %b %-d"
        self.conv_options = {
            "mobi": ["--output-profile=kindle_pw3", "--mobi-file-type=old", "--authors=newsrack", "--publisher='https://holyspiritomb.github.io/newsrack/'"],
        }


@dataclass
class CustomCoverOptions(CoverOptions):
    def __post_init__(self):
        self.cover_height = 1448
        self.cover_width = 1072
        self.title_font_path = "static/ReadexPro-SemiBold.ttf"
        self.title_font_size = 96
        self.datestamp_font_path = "static/ReadexPro-Light.ttf"
        self.datestamp_font_size = 80


@dataclass
class CustomMonthlyRecipe(Recipe):
    # Use a different title date format and output profile from default
    def __post_init__(self):
        self.title_date_format = "%b %Y"
        self.conv_options = {
            "mobi": ["--output-profile=kindle_pw3", "--mobi-file-type=old", "--authors=newsrack", "--publisher='https://holyspiritomb.github.io/newsrack/'"],
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
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Ars_Technica_logo_(2016).svg/1024px-Ars_Technica_logo_(2016).svg.png"
        ),
        enable_on=onlyat_hours(list(range(10, 22)), -4),
    ),
    CustomOptionsRecipe(
        recipe="atlantic-custom",
        slug="the-atlantic",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=True,
        category="News",
        tags=["editorial", "commentary"],
        enable_on=onlyon_weekdays([3, 4, 5, 6], -4) and onlyat_hours(list(range(10, 19)), -4),
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/The_Atlantic_Logo_11.2019.svg/1200px-The_Atlantic_Logo_11.2019.svg.png"
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
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://i.imgur.com/ScfaQZb.png"
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
        enable_on=True,
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/The_Forward_logo_2022.svg/1024px-The_Forward_logo_2022.svg.png"
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
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://i.imgur.com/OMxGtzQ.jpg"
        ),
        enable_on=onlyon_weekdays([3, 4, 5, 6], -4) and onlyat_hours(list(range(10, 19)), -4),
    ),
    CustomOptionsRecipe(
        recipe="live-science-custom",
        slug="live-science",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        tags=["science"],
        overwrite_cover=True,
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Live_Science_logo.svg/1024px-Live_Science_logo.svg.png"
        ),
    ),
    CustomOptionsRecipe(
        recipe="mother-jones",
        slug="mother-jones",
        src_ext="mobi",
        target_ext=["epub"],
        category="Politics",
        tags=["politics", "commentary"],
        overwrite_cover=True,
        enable_on=onlyon_weekdays([3, 4, 5, 6], -4) and onlyat_hours(list(range(2, 15)), -4),
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Mother_Jones_Logo_2019.svg/1024px-Mother_Jones_Logo_2019.svg.png"
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
        enable_on=onlyon_weekdays([3, 4, 5, 6], -4) and onlyat_hours(list(range(8, 22)), -4),
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/The_Nation_logo.svg/1024px-The_Nation_logo.svg.png",
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
        enable_on=onlyon_weekdays([3, 4, 5, 6], -4),
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Natgeologo.svg/1024px-Natgeologo.svg.png"
        ),
    ),
    CustomOptionsRecipe(
        recipe="nature-custom",
        slug="nature",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        overwrite_cover=False,
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
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://assets.nautil.us/13891_bb83b72bf545e376f3ff9443bda39421.png"
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
        enable_on=(first_n_days_of_month(7) or last_n_days_of_month(7)),
        tags=["politics", "commentary"],
    ),
    CustomOptionsRecipe(
        recipe="new-scientist",
        slug="new-scientist",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        tags=["weekly", "science"],
        overwrite_cover=True,
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -5),
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/New_Scientist_logo.svg/1024px-New_Scientist_logo.svg.png"
        ),
    ),
    CustomOptionsRecipe(
        recipe="newyorker-custom",
        slug="newyorker",
        src_ext="mobi",
        target_ext=["epub"],
        category="Arts",
        overwrite_cover=False,
        enable_on=onlyon_weekdays([1, 3, 5], -5),
        tags=["editorial", "commentary", "weekly"],
    ),
    CustomOptionsRecipe(
        recipe="nytimes-books-custom",
        slug="nytimes-books",
        src_ext="mobi",
        target_ext=["epub"],
        category="Arts",
        timeout=300,
        retry_attempts=0,
        enable_on=onlyat_hours(list(range(8, 22)),-4),
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://static01.nyt.com/newsgraphics/2015/12/23/masthead-2016/8118277965bda8228105578895f2f4a7aeb22ce2/nyt-logo.png"
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
        enable_on=first_n_days_of_month(7, -6) or last_n_days_of_month(7, -5),
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
        enable_on=first_n_days_of_month(7, -6) or last_n_days_of_month(7, -5),
        tags=["literature", "arts", "monthly"],
    ),
    CustomOptionsRecipe(
        recipe="quanta-magazine-custom",
        slug="quanta-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        enable_on=onlyon_weekdays([0, 2, 4], -5),
        tags=["science", "weekly"],
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Quanta_Magazine_Logo_05.2022.svg/640px-Quanta_Magazine_Logo_05.2022.svg.png",
        ),
    ),
    CustomOptionsRecipe(
        recipe="science-daily",
        slug="science-daily",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        overwrite_cover=True,
        tags=["science", "tech", "daily"],
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://i.imgur.com/nQ1lgZZ.png",
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
        and onlyat_hours(list(range(10, 20)), -4),  # middle of the month?
        tags=["science", "tech", "monthly"],
    ),
    CustomMonthlyRecipe(
        recipe="smithsonian-magazine-custom",
        slug="smithsonian-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        category="Magazines",
        enable_on=onlyon_days(list(range(16, 31)), -5),
        overwrite_cover=False,
        tags=["science", "history", "monthly"],
    ),
    CustomOptionsRecipe(
        recipe="strange-horizons",
        slug="strange-horizons",
        src_ext="mobi",
        target_ext=["epub"],
        enable_on=onlyon_weekdays([5, 6], -5),
        cover_options=CustomCoverOptions(
            logo_path_or_url="http://strangehorizons.com/wordpress/wp-content/themes/strangehorizons/images/sh-logo.jpg"
        ),
        category="Arts",
        tags=["literature", "arts", "weekly"],
    ),
    CustomOptionsRecipe(
        recipe="teen-vogue",
        slug="teen-vogue",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=True,
        category="Magazines",
        # enable_on=False,
        enable_on=onlyon_weekdays([4, 5, 6], -4),
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Teen_Vogue_logo.svg/1024px-Teen_Vogue_logo.svg.png"
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
        enable_on=onlyon_weekdays([3, 4, 5, 6], -4) and onlyat_hours(list(range(6, 22)), -4),
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
        enable_on=(first_n_days_of_month(6) or last_n_days_of_month(6))
        and onlyat_hours(list(range(2, 20)), -4),
        title_date_format="%b %Y",
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Wired_logo.svg/1024px-Wired_logo.svg.png"
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
        # enable_on=lambda recipe: every_x_days(
        #     last_run=recipe.last_run, days=1, drift=0
        # ),
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Wired_logo.svg/1024px-Wired_logo.svg.png"
        ),
    ),
    # Recipe(
    #     recipe="example",
    #     slug="example",
    #     src_ext="epub",
    #     category="example",
    # ),
]
