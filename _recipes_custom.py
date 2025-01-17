from dataclasses import dataclass
from typing import List

from _recipe_utils import Recipe, CoverOptions, onlyon_weekdays, onlyon_days, onlyat_hours, last_n_days_of_month, first_n_days_of_month, every_x_days, every_x_hours, get_local_now

# Define the categories display order, optional
categories_sort: List[str] = ["Science", "Blogs", "Arts & Culture", "News", "Magazines", "Politics", "Podcasts", "Jewish"]

# Define your custom recipes list here
# Example: https://github.com/ping/newsrack-fork-test/blob/custom/_recipes_custom.py


@dataclass
class CustomConvOptions(Recipe):
    def __post_init__(self):
        self.conv_options = {
            "mobi": [
                "--output-profile=kindle_pw3",
                "--mobi-file-type=old",
                "--authors=newsrack",
                "--publisher='https://holyspiritomb.github.io/newsrack/'"
            ],
        }


@dataclass
class CustomOptionsRecipe(Recipe):
    # Use a different title date format and output profile from default
    def __post_init__(self):
        self.title_date_format = "%Y %b %-d"
        self.conv_options = {
            "mobi": [
                "--output-profile=kindle_pw3",
                "--mobi-file-type=old",
                "--authors=newsrack",
                "--publisher='https://holyspiritomb.github.io/newsrack/'",
                "--change-justification=left"
            ],
            "epub": [
                "--output-profile=tablet",
                # to fix the problem of images having a fixed height after conversion
                "--extra-css=img{height:auto !important;}",
            ]
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
            "mobi": ["--output-profile=kindle_pw3", "--mobi-file-type=old", "--authors=newsrack", "--publisher='https://holyspiritomb.github.io/newsrack/'", "--change-justification=left"]
            # "epub": ["--embed-font-family=Lato"]
        }


def bimonthly_odd(offset: float = 0.0):
    if get_local_now(offset).month % 2 != 0:
        return True
    else:
        return False


def bimonthly_even(offset: float = 0.0):
    if get_local_now(offset).month % 2 == 0:
        return True
    else:
        return False


recipes: List[Recipe] = [
    CustomOptionsRecipe(
        recipe="972",
        slug="972",
        src_ext="mobi",
        target_ext=["epub"],
        category="News",
        tags=["news", "jewish", "commentary", "politics", "editorial"],
        overwrite_cover=True,
        cover_options=CustomCoverOptions(logo_path_or_url="recipes_custom/logos/972-logo.png"),
        enable_on=lambda recipe: every_x_days(
            last_run=recipe.last_run, days=1, drift=0
        ),
    ),
    CustomOptionsRecipe(
        recipe="advocate",
        slug="advocate",
        src_ext="mobi",
        target_ext=["epub"],
        category="News",
        tags=["lgbtq", "news"],
        overwrite_cover=True,
        cover_options=CustomCoverOptions(
            logo_path_or_url="recipes_custom/logos/advocate.png"
        ),
        enable_on=False,
        # enable_on=lambda recipe: every_x_hours(
        #     last_run=recipe.last_run, hours=12, drift=0
        # ),
    ),
    CustomOptionsRecipe(
        recipe="aiweirdness",
        slug="aiweirdness",
        src_ext="mobi",
        target_ext=["epub"],
        category="Blogs",
        tags=["science", "tech"],
        overwrite_cover=True,
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://www.aiweirdness.com/content/images/2021/03/ai_weirdness_with_neural_net_box.png"
        ),
        enable_on=lambda recipe: every_x_days(
            last_run=recipe.last_run, days=3, drift=0
        ),
    ),
    # CustomOptionsRecipe(
    #     recipe="archlinux",
    #     slug="archlinux",
    #     src_ext="epub",
    #     target_ext=["mobi"],
    #     category="News",
    #     tags=["tech"],
    #     overwrite_cover=True,
    #     enable_on=False,
    #     cover_options=CustomCoverOptions(
    #         logo_path_or_url="recipes_custom/logos/archlinux.png"
    #     ),
    # ),
    # CustomOptionsRecipe(
    #     recipe="ars-technica",
    #     slug="ars-technica",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="News",
    #     tags=["science", "tech", "commentary"],
    #     overwrite_cover=True,
    #     cover_options=CustomCoverOptions(
    #         logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Ars_Technica_logo_(2016).svg/1024px-Ars_Technica_logo_(2016).svg.png"
    #     ),
    #     enable_on=lambda recipe: every_x_days(
    #         last_run=recipe.last_run, days=1, drift=0
    #     ),
    # ),
    CustomOptionsRecipe(
        recipe="assigned-media",
        slug="assigned-media",
        src_ext="mobi",
        target_ext=["epub"],
        category="News",
        tags=["lgbtq", "trans", "news"],
        overwrite_cover=True,
        cover_options=CustomCoverOptions(
            # logo_path_or_url="recipes_custom/logos/Assigned.jpg"
            logo_path_or_url="https://images.squarespace-cdn.com/content/v1/633303d5ccf756402b93f25c/72772a0c-8d81-4f03-8f39-fed9eebd769a/Assigned+Media+Logo+flat.png"
        ),
        enable_on=True,
    ),
    # CustomOptionsRecipe(
    #     recipe="duolingo-blog",
    #     slug="duolingo-blog",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     overwrite_cover=True,
    #     category="Blogs",
    #     tags=["science", "linguistics"],
    #     enable_on=False,
    #     # enable_on=lambda recipe: every_x_days(
    #         # last_run=recipe.last_run, days=1, drift=0
    #     # ),
    #     cover_options=CustomCoverOptions(
    #         logo_path_or_url="recipes_custom/logos/duolingo-green.png"
    #     ),
    # ),
    CustomOptionsRecipe(
        recipe="erin",
        slug="erin",
        src_ext="mobi",
        target_ext=["epub"],
        category="Blogs",
        overwrite_cover=True,
        tags=["news", "trans", "lgbtq"],
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Transgender_Pride_flag.svg/1024px-Transgender_Pride_flag.svg.png"
        ),
        enable_on=True
    ),
    CustomOptionsRecipe(
        recipe="the-forward",
        slug="the-forward",
        src_ext="mobi",
        target_ext=["epub"],
        category="Jewish",
        tags=["editorial", "commentary", "news", "jewish", "religion"],
        overwrite_cover=True,
        enable_on=lambda recipe: every_x_days(
            last_run=recipe.last_run, days=1, drift=0
        ),
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/The_Forward_logo_2022.svg/1024px-The_Forward_logo_2022.svg.png"
        ),
    ),
    CustomOptionsRecipe(
        recipe="gender-analysis",
        slug="gender-analysis",
        src_ext="mobi",
        target_ext=["epub"],
        category="Blogs",
        overwrite_cover=True,
        tags=["science", "trans", "lgbtq", "news"],
        enable_on=True,
        cover_options=CustomCoverOptions(
            # logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Transgender_Pride_flag.svg/1024px-Transgender_Pride_flag.svg.png"
            logo_path_or_url="https://genderanalysis.net/wp-content/uploads/2017/05/newgabanner.png"
        ),
    ),
    CustomOptionsRecipe(
        recipe="jewish-currents",
        slug="jewish-currents",
        src_ext="mobi",
        target_ext=["epub"],
        category="Jewish",
        tags=["news", "jewish", "commentary", "politics", "editorial"],
        overwrite_cover=True,
        cover_options=CustomCoverOptions(
            logo_path_or_url="recipes_custom/logos/jewish-currents.png"
        ),
        enable_on=lambda recipe: every_x_days(
            last_run=recipe.last_run, days=1, drift=0
        ),
    ),
    # CustomOptionsRecipe(
    #     recipe="jta",
    #     slug="jta",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="Jewish",
    #     tags=["news", "jewish", "politics"],
    #     overwrite_cover=True,
    #     cover_options=CustomCoverOptions(logo_path_or_url="https://www.jta.org/wp-content/uploads/2018/12/cropped-homeicon-square@2x-1-270x270.png"),
    #     enable_on=False
    # ),
    CustomOptionsRecipe(
        recipe="knowable",
        slug="knowable",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        tags=["science"],
        overwrite_cover=True,
        cover_options=CustomCoverOptions(logo_path_or_url="recipes/logos/knowable.png"),
        enable_on=onlyon_weekdays([3, 4, 5, 6], -4),
        # enable_on=False,
    ),
    CustomOptionsRecipe(
        recipe="life-is-a-sacred-text",
        slug="life-is-a-sacred-text",
        src_ext="mobi",
        target_ext=["epub"],
        category="Jewish",
        cover_options=CustomCoverOptions(
            logo_path_or_url="recipes_custom/logos/life.png"
        ),
        # enable_on=True,
        enable_on=lambda recipe: every_x_hours(
            last_run=recipe.last_run, hours=12, drift=0
        ),
        tags=["religion", "jewish"],
    ),
    # CustomOptionsRecipe(
    #     recipe="lithub",
    #     slug="lithub",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="Arts & Culture",
    #     # enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -5)
    #     # and onlyat_hours(list(range(10, 17)), -5),
    #     enable_on=False,
    #     cover_options=CustomCoverOptions(
    #         logo_path_or_url="https://s26162.pcdn.co/wp-content/themes/rigel/images/social_logo.png"
    #     ),
    #     tags=["literature", "books"],
    # ),
    # CustomOptionsRecipe(
    #     recipe="lingthusiasm",
    #     slug="lingthusiasm",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="Podcasts",
    #     tags=["blog", "linguistics"],
    #     overwrite_cover=True,
    #     cover_options=CustomCoverOptions(logo_path_or_url="recipes_custom/logos/ling.png"),
    # ),
    CustomOptionsRecipe(
        recipe="live-science",
        slug="live-science",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        tags=["science"],
        overwrite_cover=True,
        enable_on=lambda recipe: every_x_days(
            last_run=recipe.last_run, days=1, drift=0
        ),
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Live_Science_logo.svg/1024px-Live_Science_logo.svg.png"
        ),
    ),
    # CustomOptionsRecipe(
    #     recipe="maxfun-pods",
    #     slug="maxfun-pods",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="Podcasts",
    #     tags=["science"],
    #     overwrite_cover=True,
    #     cover_options=CustomCoverOptions(
    #         logo_path_or_url="https://maximumfun.org/wp-content/uploads/2019/02/cropped-favicon-512x512.png"
    #     ),
    #     enable_on=lambda recipe: every_x_hours(
    #         last_run=recipe.last_run, hours=12, drift=0
    #     ),
    # ),
    # # CustomOptionsRecipe(
    #     recipe="mother-jones",
    #     slug="mother-jones",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="Politics",
    #     tags=["politics", "commentary"],
    #     overwrite_cover=True,
    #     enable_on=False,
    #     # enable_on=onlyon_weekdays([3, 4, 5, 6], -4) and onlyat_hours(list(range(8, 15)), -4),
    #     cover_options=CustomCoverOptions(
    #         logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Mother_Jones_Logo_2019.svg/1024px-Mother_Jones_Logo_2019.svg.png"
    #     ),
    # ),
    # CustomOptionsRecipe(
    #     recipe="nation",
    #     slug="nation",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="Politics",
    #     tags=["politics", "commentary"],
    #     overwrite_cover=True,
    #     enable_on=False,
    #     # enable_on=onlyon_weekdays([3, 4, 5, 6], -4) and onlyat_hours(list(range(8, 14)), -4),
    #     cover_options=CustomCoverOptions(
    #         logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/The_Nation_logo.svg/1024px-The_Nation_logo.svg.png",
    #     ),
    # ),
    # CustomOptionsRecipe(
    #     recipe="national-geographic",
    #     slug="national-geographic",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="Magazines",
    #     tags=["daily", "history", "science"],
    #     overwrite_cover=True,
    #     # enable_on=lambda recipe: every_x_days(
    #     #     last_run=recipe.last_run, days=1, drift=0
    #     # ),
    #     enable_on=False,
    #     cover_options=CustomCoverOptions(
    #         logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Natgeologo.svg/1024px-Natgeologo.svg.png"
    #     ),
    # ),
    CustomOptionsRecipe(
        recipe="nature",
        slug="nature",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        overwrite_cover=False,
        enable_on=onlyon_weekdays([2, 3, 4], 0),
        tags=["science", "weekly"],
    ),
    CustomOptionsRecipe(
        recipe="nautilus",
        slug="nautilus",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        tags=["science", "weekly"],
        overwrite_cover=True,
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://assets.nautil.us/13891_bb83b72bf545e376f3ff9443bda39421.png"
        ),
        enable_on=lambda recipe: every_x_days(
            last_run=recipe.last_run, days=3, drift=60
        ),
    ),
    # CustomOptionsRecipe(
    #     recipe="new-republic-magazine",
    #     slug="new-republic-magazine",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="Politics",
    #     overwrite_cover=False,
    #     # enable_on=(first_n_days_of_month(4) or last_n_days_of_month(6))
    #     # and onlyat_hours(list(range(8, 16))),
    #     enable_on=False,
    #     tags=["politics", "commentary"],
    # ),
    CustomOptionsRecipe(
        recipe="new-scientist",
        slug="new-scientist",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        tags=["science"],
        overwrite_cover=True,
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -5),
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/New_Scientist_logo.svg/1024px-New_Scientist_logo.svg.png"
        ),
    ),
    CustomOptionsRecipe(
        recipe="newvoices",
        slug="newvoices",
        src_ext="mobi",
        target_ext=["epub"],
        category="Jewish",
        tags=["news", "arts", "jewish", "commentary", "editorial"],
        overwrite_cover=True,
        cover_options=CustomCoverOptions(logo_path_or_url="recipes_custom/logos/newvoices-logo.png"),
        enable_on=lambda recipe: every_x_days(
            last_run=recipe.last_run, days=3, drift=0
        ),
    ),
    CustomOptionsRecipe(
        recipe="npr",
        slug="npr",
        src_ext="mobi",
        target_ext=["epub"],
        category="News",
        overwrite_cover=True,
        tags=["news", "politics", "daily"],
        enable_on=lambda recipe: every_x_days(
            last_run=recipe.last_run, days=1, drift=0
        ),
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/National_Public_Radio_logo.svg/1024px-National_Public_Radio_logo.svg.png"
        ),
    ),
    CustomMonthlyRecipe(
        recipe="philosophy-now",
        slug="philosophy-now",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="Arts & Culture",
        enable_on=lambda recipe: every_x_days(
            last_run=recipe.last_run, days=7, drift=0
        ),
        tags=["philosophy", "commentary", "bimonthly"],
    ),
    CustomMonthlyRecipe(
        recipe="poetry",
        slug="poetry",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="Arts & Culture",
        # enable_on=first_n_days_of_month(7, -6) or last_n_days_of_month(7, -5),
        enable_on=True,
        tags=["literature", "arts", "monthly"],
    ),
    CustomOptionsRecipe(
        recipe="quanta",
        slug="quanta",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -5)
        and onlyat_hours(list(range(8, 14))),
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
            logo_path_or_url="recipes_custom/logos/science-daily.png"
        ),
        enable_on=lambda recipe: every_x_hours(
            last_run=recipe.last_run, hours=6, drift=0
        ),
    ),
    CustomMonthlyRecipe(
        recipe="sci-am",
        slug="sci-am",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        overwrite_cover=False,
        enable_on=onlyon_days(list(range(15, 31)), -5),  # middle of the month?
        tags=["science", "tech", "monthly"],
    ),
    # CustomMonthlyRecipe(
    #     recipe="smithsonian-magazine",
    #     slug="smithsonian-magazine",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="Magazines",
    #     enable_on=False,
    #     # enable_on=onlyon_days(list(range(16, 31)), -5)
    #     # and onlyat_hours(list(range(10, 19)), -5),
    #     overwrite_cover=False,
    #     tags=["science", "history", "monthly"],
    # ),
    # CustomOptionsRecipe(
    #     recipe="strange-horizons",
    #     slug="strange-horizons",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     # enable_on=onlyon_weekdays([5, 6], -4),
    #     enable_on=False,
    #     cover_options=CustomCoverOptions(
    #         logo_path_or_url="http://strangehorizons.com/wordpress/wp-content/themes/strangehorizons/images/sh-logo.jpg"
    #     ),
    #     category="Arts & Culture",
    #     tags=["literature", "arts", "weekly"],
    # ),
    CustomOptionsRecipe(
        recipe="sword-sandwich",
        slug="sword-sandwich",
        src_ext="mobi",
        target_ext=["epub"],
        category="Blogs",
        overwrite_cover=True,
        tags=["politics", "food", "commentary"],
        cover_options=CustomCoverOptions(
            logo_path_or_url="recipes_custom/logos/sword-sandwich-logo.jpeg"
        ),
    ),
    # CustomOptionsRecipe(
    #     recipe="teen-vogue",
    #     slug="teen-vogue",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     overwrite_cover=True,
    #     category="News",
    #     enable_on=lambda recipe: every_x_hours(
    #         last_run=recipe.last_run, hours=24, drift=0
    #     ),
    #     cover_options=CustomCoverOptions(
    #         logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Teen_Vogue_logo.svg/1024px-Teen_Vogue_logo.svg.png"
    #     ),
    #     tags=["news", "politics"],
    # ),
    CustomOptionsRecipe(
        recipe="them",
        slug="them",
        src_ext="mobi",
        target_ext=["epub"],
        category="News",
        overwrite_cover=True,
        tags=["trans", "lgbtq", "news"],
        enable_on=lambda recipe: every_x_hours(
            last_run=recipe.last_run, hours=3, drift=0
        ),
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Them_wordmark.svg/1024px-Them_wordmark.svg.png"
        ),
    ),
    CustomOptionsRecipe(
        recipe="tpwky",
        slug="tpwky",
        src_ext="mobi",
        target_ext=["epub"],
        category="Podcasts",
        overwrite_cover=True,
        tags=["science"],
        enable_on=lambda recipe: every_x_days(
            last_run=recipe.last_run, days=1, drift=0
        ),
        cover_options=CustomCoverOptions(
            logo_path_or_url="recipes_custom/logos/TPWKY.jpg"
        ),
    ),
    # CustomMonthlyRecipe(
    #     recipe="wired",
    #     slug="wired",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     overwrite_cover=True,
    #     category="Magazines",
    #     tags=["science", "tech", "monthly"],
    #     # enable_on=(first_n_days_of_month(7) or last_n_days_of_month(7))
    #     # and onlyat_hours(list(range(10, 18))),
    #     enable_on=False,
    #     cover_options=CustomCoverOptions(
    #         logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Wired_logo.svg/1024px-Wired_logo.svg.png"
    #     ),
    # ),
    CustomOptionsRecipe(
        recipe="wired-daily",
        slug="wired-daily",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=True,
        category="Science",
        tags=["science", "tech", "daily"],
        # enable_on=onlyat_hours(list(range(10, 18))),
        enable_on=lambda recipe: every_x_days(
            last_run=recipe.last_run, days=1, drift=0
        ),
        cover_options=CustomCoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Wired_logo.svg/1024px-Wired_logo.svg.png"
        ),
    ),
    CustomOptionsRecipe(
        recipe="wtfjht",
        slug="wtfjht",
        src_ext="mobi",
        target_ext=["epub"],
        category="News",
        tags=["news", "politics"],
        overwrite_cover=True,
        cover_options=CustomCoverOptions(),
        enable_on=True
    ),
    # Recipe(
    #     recipe="example",
    #     slug="example",
    #     src_ext="epub",
    #     category="example",
    # ),
]
