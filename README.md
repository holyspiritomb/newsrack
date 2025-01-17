[![Build](https://github.com/holyspiritomb/newsrack/actions/workflows/build.yml/badge.svg)](https://github.com/holyspiritomb/newsrack/actions/workflows/build.yml)

# newsrack

Generate an online "newsrack" of periodicals for your ereader.

Features:
- Download anywhere using your device browser
- Subscribe via OPDS feeds

Uses [calibre](https://calibre-ebook.com/) + [recipes](https://manual.calibre-ebook.com/news_recipe.html), [GitHub Actions](.github/workflows/build.yml), and hosted
on [GitHub Pages](https://pages.github.com/).

![eInk Kindle Screenshot](https://github.com/ping/newsrack/assets/104607/475daa53-f2d5-4469-b88e-7d5463399d73)
![Mobile Screenshot](https://github.com/ping/newsrack/assets/104607/76ec3514-8d89-43bc-a68c-909df42971cb)

[![Buy me a coffee](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20coffee&emoji=&slug=ping&button_colour=FFDD00&font_colour=000000&font_family=Bree&outline_colour=000000&coffee_colour=ffffff)](https://www.buymeacoffee.com/ping)

## Running Your Own Instance

### General Steps

1. Fork this repository.
2. Create a new branch, for example `custom`. Using a new branch makes a few things, like contributing fixes for example, easier.
3. Add your own recipes to the [`recipes_custom/`](recipes_custom) folder and customise [_recipes_custom.py](_recipes_custom.py). Optional.
4. Customise the cron schedule and job run time in [.github/workflows/build.yml](.github/workflows/build.yml). Optional.
5. Set the new branch `custom` as default
   - from Settings > Branches > Default branch
6. Enable Pages in repository settings to deploy from `GitHub Actions`
   - from Settings > Pages > Build and deployment > Source
7. If needed, manually trigger the `Build` workflow from Actions to start your first build.

### What Can Be Customised

`newsrack` supports extensive customisation such as:
- add/remove recipes
- the formats generated
- when recipes are executed
- cover colours and fonts

Review the [wiki](https://github.com/ping/newsrack/wiki#customisation) page to understand what can be changed according to your preference.

You can also refer to the [example fork repo](https://github.com/ping/newsrack-fork-test/) and see the [actual customisations](https://github.com/ping/newsrack-fork-test/compare/main...custom) in action.


## Available Recipes

`newsrack` has its own set of customised recipes. The full list of available recipes can be viewed on the [wiki](https://github.com/ping/newsrack/wiki/Available-Recipes).
