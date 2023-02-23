from typing import List

from _recipe_utils import Recipe, CoverOptions

# Define the categories display order, optional
categories_sort: List[str] = []

# Define your custom recipes list here
# Example: https://github.com/ping/newsrack-fork-test/blob/custom/_recipes_custom.py

recipes: List[Recipe] = [
    Recipe(
        recipe="atlantic",
        slug="the-atlantic",
        src_ext="mobi",
        target_ext=[],
        category="Online Magazines",
        tags=["The Atlantic","Periodical","editorial", "commentary"],
        cover_options=CoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/The_Atlantic_Logo_11.2019.svg/1200px-The_Atlantic_Logo_11.2019.svg.png"
        ),
    ),
    Recipe(
        recipe="atlantic-magazine",
        slug="atlantic-magazine",
        src_ext="mobi",
        target_ext=[],
        overwrite_cover=False,
        category="Magazines",
        tags=["The Atlantic","Periodical"],
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -4) and last_n_days_of_month(14, -4),
    ),
    Recipe(
        recipe="knowable-magazine",
        slug="knowable-magazine",
        src_ext="mobi",
        target_ext=[],
        category="Magazines",
        tags=["Science","Periodical"],
        cover_options=CoverOptions(logo_path_or_url="https://i.imgur.com/OMxGtzQ.jpg"),
    ),
    Recipe(
        recipe="nature",
        slug="nature",
        src_ext="mobi",
        target_ext=[],
        category="Magazines",
        overwrite_cover=False,
        enable_on=onlyon_weekdays([2, 3, 4], 0),
        tags=["Science","Periodical"],
    ),
    Recipe(
        recipe="nautilus",
        slug="nautilus",
        src_ext="mobi",
        target_ext=[],
        category="Online Magazines",
        tags=["Science","Periodical"],
        cover_options=CoverOptions(
            logo_path_or_url="https://assets.nautil.us/13891_bb83b72bf545e376f3ff9443bda39421.png"
        ),
    ),
    Recipe(
        recipe="new-republic-magazine",
        slug="new-republic-magazine",
        src_ext="mobi",
        target_ext=[],
        category="Magazines",
        overwrite_cover=False,
        enable_on=(first_n_days_of_month(7) or last_n_days_of_month(7))
        and onlyat_hours(list(range(8, 16))),
    ),
    Recipe(
        recipe="newyorker",
        slug="newyorker",
        src_ext="mobi",
        target_ext=[],
        category="Magazines",
        overwrite_cover=False,
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -5),
        tags=["editorial", "commentary"],
    ),
    Recipe(
        recipe="nytimes-books",
        slug="nytimes-books",
        src_ext="mobi",
        target_ext=[],
        category="Books",
        timeout=300,
        retry_attempts=0,
        enable_on=onlyat_hours(list(range(18, 22))),
        cover_options=CoverOptions(
            logo_path_or_url="https://static01.nyt.com/newsgraphics/2015/12/23/masthead-2016/8118277965bda8228105578895f2f4a7aeb22ce2/nyt-logo.png"
        ),
    ),
    Recipe(
        recipe="poetry",
        slug="poetry-magazine",
        src_ext="mobi",
        target_ext=[],
        overwrite_cover=False,
        category="Books",
        enable_on=first_n_days_of_month(7, -6) or last_n_days_of_month(7, -5),
        tags=["literature", "arts"],
    ),
    Recipe(
        recipe="quanta-magazine",
        slug="quanta-magazine",
        src_ext="mobi",
        target_ext=[],
        category="Online Magazines",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -5)
        and onlyat_hours(list(range(8, 14))),
        tags=["Science","Periodical"],
        cover_options=CoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Quanta_Magazine_Logo_05.2022.svg/640px-Quanta_Magazine_Logo_05.2022.svg.png"
        ),
    ),
    Recipe(
        recipe="scientific-american",
        slug="scientific-american",
        src_ext="mobi",
        target_ext=[],
        category="Magazines",
        overwrite_cover=False,
        enable_on=onlyon_days(list(range(15, 31)), -5),  # middle of the month?
        tags=["Science","Periodical"],
    ),
    Recipe(
        recipe="smithsonian-magazine",
        slug="smithsonian-magazine",
        src_ext="mobi",
        target_ext=[],
        category="Magazines",
        enable_on=onlyon_days(list(range(16, 31)), -5)
        and onlyat_hours(list(range(10, 19)), -5),
        overwrite_cover=False,
    ),
    Recipe(
        recipe="wired",
        slug="wired",
        src_ext="mobi",
        target_ext=[],
        overwrite_cover=True,
        category="Online Magazines",
        tags=["Science","Periodical"],
        enable_on=(first_n_days_of_month(7) or last_n_days_of_month(7))
        and onlyat_hours(list(range(10, 18))),
        cover_options=CoverOptions(
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
