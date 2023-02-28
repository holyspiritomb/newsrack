from typing import List

from _recipe_utils import Recipe, CoverOptions, onlyon_weekdays, onlyon_days, onlyat_hours, last_n_days_of_month, first_n_days_of_month, every_x_days

# Define the categories display order, optional
categories_sort: List[str] = []

# Define your custom recipes list here
# Example: https://github.com/ping/newsrack-fork-test/blob/custom/_recipes_custom.py

recipes: List[Recipe] = [
    Recipe(
        recipe="atlantic",
        slug="the-atlantic",
        src_ext="mobi",
        target_ext=["epub"],
        category="Online Magazines",
        tags=["editorial", "commentary"],
        cover_options=CoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/The_Atlantic_Logo_11.2019.svg/1200px-The_Atlantic_Logo_11.2019.svg.png",
            title_font_path="static/ReadexPro-SemiBold.ttf",
            datestamp_font_path="static/ReadexPro-Light.ttf"
        ),
        enable_on=every_x_days(1, 1, 60),
        title_date_format="%Y %b %-d",
        conv_options={
            "mobi": ["--output-profile=kindle_pw3", "--mobi-file-type=old"],
        }
    ),
    Recipe(
        recipe="atlantic-magazine",
        slug="atlantic-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="Magazines",
        tags=["editorial", "commentary"],
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -4) and last_n_days_of_month(14, -4),
    ),
    Recipe(
        recipe="the-forward",
        slug="the-forward",
        src_ext="mobi",
        target_ext=["epub"],
        category="News",
        tags=["editorial", "commentary", "news"],
        overwrite_cover=True,
        cover_options=CoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/The_Forward_logo_2022.svg/1024px-The_Forward_logo_2022.svg.png",
            title_font_path="static/ReadexPro-SemiBold.ttf",
            datestamp_font_path="static/ReadexPro-Light.ttf"
        ),
    ),
    Recipe(
        recipe="knowable-magazine",
        slug="knowable-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        category="Magazines",
        tags=["science"],
        cover_options=CoverOptions(
            logo_path_or_url="https://i.imgur.com/OMxGtzQ.jpg",
            title_font_path="static/ReadexPro-SemiBold.ttf",
            datestamp_font_path="static/ReadexPro-Light.ttf"
        ),
        # enable_on=False,
        enable_on=every_x_days(1, 1, 60),
        title_date_format="%Y %b %-d",
    ),
    Recipe(
        recipe="mother-jones",
        slug="mother-jones",
        src_ext="mobi",
        target_ext=["epub"],
        category="Magazines",
        tags=["politics", "commentary"],
        overwrite_cover=True,
        title_date_format="%Y %b %-d",
        cover_options=CoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Mother_Jones_Logo_2019.svg/1024px-Mother_Jones_Logo_2019.svg.png",
            title_font_path="static/ReadexPro-SemiBold.ttf",
            datestamp_font_path="static/ReadexPro-Light.ttf"
        ),
    ),
    Recipe(
        recipe="nature",
        slug="nature",
        src_ext="mobi",
        target_ext=["epub"],
        category="Magazines",
        overwrite_cover=False,
        # enable_on=False,
        enable_on=onlyon_weekdays([2, 3, 4], 0),
        tags=["science"],
        title_date_format="%Y %b %-d",
    ),
    Recipe(
        recipe="nautilus",
        slug="nautilus",
        src_ext="mobi",
        target_ext=["epub"],
        category="Online Magazines",
        tags=["science"],
        overwrite_cover=False,
        # cover_options=CoverOptions(
        #    logo_path_or_url="https://assets.nautil.us/13891_bb83b72bf545e376f3ff9443bda39421.png"
        # ),
        enable_on=every_x_days(1, 1, 60),
        title_date_format="%Y %b %-d",
    ),
    Recipe(
        recipe="new-republic-magazine",
        slug="new-republic-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        category="Magazines",
        overwrite_cover=False,
        tags=["politics", "commentary"],
        enable_on=(first_n_days_of_month(7) or last_n_days_of_month(7))
        and onlyat_hours(list(range(8, 16))),
    ),
    Recipe(
        recipe="newyorker",
        slug="newyorker",
        src_ext="mobi",
        target_ext=["epub"],
        category="Magazines",
        overwrite_cover=False,
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -5),
        # enable_on=False,
        tags=["editorial", "commentary", "weekly"],
        title_date_format="%Y %b %-d",
    ),
    Recipe(
        recipe="nytimes-books",
        slug="nytimes-books",
        src_ext="mobi",
        target_ext=["epub"],
        category="Books",
        timeout=300,
        retry_attempts=0,
        enable_on=onlyat_hours(list(range(18, 22))),
        # enable_on=False,
        cover_options=CoverOptions(
            logo_path_or_url="https://static01.nyt.com/newsgraphics/2015/12/23/masthead-2016/8118277965bda8228105578895f2f4a7aeb22ce2/nyt-logo.png",
            title_font_path="static/ReadexPro-SemiBold.ttf",
            datestamp_font_path="static/ReadexPro-Light.ttf"
        ),
        tags=["literature"],
        title_date_format="%Y %b %-d",
    ),
    Recipe(
        recipe="philosophy-now",
        slug="philosophy-now",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="Magazines",
        # enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -4) and last_n_days_of_month(14, -4),
        # enable_on=False,
        tags=["philosophy", "commentary", "bimonthly"],
    ),
    Recipe(
        recipe="poetry",
        slug="poetry-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="Books",
        enable_on=first_n_days_of_month(7, -6) or last_n_days_of_month(7, -5),
        # enable_on=False,
        tags=["literature", "arts", "monthly"],
    ),
    Recipe(
        recipe="quanta-magazine",
        slug="quanta-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        category="Online Magazines",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -5)
        and onlyat_hours(list(range(8, 14)))
        and every_x_days(1, 1, 60),
        # enable_on=False,
        tags=["science"],
        cover_options=CoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Quanta_Magazine_Logo_05.2022.svg/640px-Quanta_Magazine_Logo_05.2022.svg.png",
            title_font_path="static/ReadexPro-SemiBold.ttf",
            datestamp_font_path="static/ReadexPro-Light.ttf"
        ),
        title_date_format="%Y %b %-d",
    ),
    Recipe(
        recipe="scientific-american",
        slug="scientific-american",
        src_ext="mobi",
        target_ext=["epub"],
        category="Magazines",
        overwrite_cover=False,
        enable_on=onlyon_days(list(range(15, 31)), -5),  # middle of the month?
        # enable_on=False,
        tags=["science", "tech", "monthly"],
    ),
    Recipe(
        recipe="smithsonian-magazine",
        slug="smithsonian-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        category="Magazines",
        enable_on=onlyon_days(list(range(16, 31)), -5)
        and onlyat_hours(list(range(10, 19)), -5),
        # enable_on=False,
        overwrite_cover=False,
        tags=["science", "history"],
    ),
    Recipe(
        recipe="time-magazine",
        slug="time-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="Magazines",
        enable_on=onlyon_weekdays([3, 4, 5, 6], -4),
        tags=["news", "politics", "weekly"],
    ),
    Recipe(
        recipe="wired",
        slug="wired",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=True,
        category="Online Magazines",
        tags=["science", "tech", "monthly"],
        enable_on=(first_n_days_of_month(7) or last_n_days_of_month(7))
        and onlyat_hours(list(range(10, 18))),
        title_date_format="%b %Y",
        cover_options=CoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Wired_logo.svg/1024px-Wired_logo.svg.png",
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
