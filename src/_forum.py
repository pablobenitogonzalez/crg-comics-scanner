from enum import Enum


class Library(Enum):
    complete = 'complete'
    incomplete = 'incomplete'


class Group(Enum):
    marvel = 'marvel'
    dc = 'dc'
    other_usa_canada = 'other-usa-canada'
    crossovers = 'crossovers'
    manga = 'manga'
    european = 'european'
    iberoamerican = 'iberoamerican'
    infantile_juvenile = 'infantile-juvenile'
    classic = 'classic'
    adult_humor = 'adult-humor'
    artbooks_and_others = 'artbooks-and-others'

    other_usa = 'other-usa'
    image = 'image'
    over_18 = 'over-18'

    finished = 'finished'


class Key(Enum):
    root = 'root'
    classics = 'classics'
    heroes = 'heroes'
    crossovers = 'crossovers'
    other_editions = 'other-editions'

    mutants = 'mutants'
    mutants_wolverine = 'mutants-wolverine'
    mutants_massacre = 'mutants-massacre'
    fantastic_4 = 'fantastic-4'
    daredevil = 'daredevil'
    hulk = 'hulk'
    punisher = 'punisher'
    spiderman = 'spiderman'
    avengers = 'avengers'
    avengers_captain_america = 'avengers-captain-america'
    avengers_iron_man = 'avengers-iron-man'
    avengers_thor = 'avengers-thor'
    ultimate_universe = 'ultimate-universe'
    universe_2099 = 'universe-2099'

    heroes_green_lantern = 'heroes-green-lantern'
    heroes_wonder_woman = 'heroes-wonder-woman'
    jla_jsa = 'jla-jsa'
    batman = 'batman'
    superman = 'superman'
    vertigo = 'vertigo'

    aftershock = 'aftershock'
    aspen = 'aspen'
    avatar = 'avatar'
    boom = 'boom'
    chaos = 'chaos'
    dark_horse = 'dark-horse'
    drawn_quarterly = 'drawn-quarterly'
    dynamite = 'dynamite'
    fantagraphics = 'fantagraphics'
    idw = 'idw'
    image = 'image'
    oni_press = 'oni-press'
    uni_conan = 'universe-conan'
    uni_star_trek = 'universe-star-trek'
    uni_star_wars = 'universe-star-wars'
    valiant = 'valiant'
    wildstorm = 'wildstorm'
    zenescope = 'zenescope'

    spain = 'spain'
    spain_labyrinth = 'spain-labyrinth'
    france_belgium = 'france-belgium'
    italy = 'italy'
    united_kingdom = 'united-kingdom'

    argentina = 'argentina'
    argentina_film_adaptions = 'argentina-film-adaptions'
    chile = 'chile'
    mexico = 'mexico'

    spanish_until_1969 = 'spanish-until-1969'

    finished = 'finished'


class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class Forum(ExtendedEnum):

    def __new__(cls, code: int, library: Library, group: Group, key: Key):
        forum = object.__new__(cls)
        forum._value_ = f'{library.value}-{group.value}-{key.value}'
        forum.code = code
        forum.library = str(library.value)
        forum.group = str(group.value)
        forum.key = str(key.value)
        return forum

    def __int__(self):
        return self.value

    # INCOMPLETE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # >>> incomplete marvel ····························································································

    INCOMPLETE_MARVEL_CLASSICS = 2, Library.incomplete, Group.marvel, Key.classics
    INCOMPLETE_MARVEL_HEROES = 9, Library.incomplete, Group.marvel, Key.heroes
    INCOMPLETE_MARVEL_MUTANTS = 11, Library.incomplete, Group.marvel, Key.mutants
    INCOMPLETE_MARVEL_SPIDERMAN = 10, Library.incomplete, Group.marvel, Key.spiderman
    INCOMPLETE_MARVEL_AVENGERS = 12, Library.incomplete, Group.marvel, Key.avengers

    # >>> incomplete dc ································································································

    INCOMPLETE_DC_BATMAN = 14, Library.incomplete, Group.dc, Key.batman
    INCOMPLETE_DC_SUPERMAN = 49, Library.incomplete, Group.dc, Key.superman
    INCOMPLETE_DC_HEROES = 13, Library.incomplete, Group.dc, Key.heroes
    INCOMPLETE_DC_VERTIGO = 65, Library.incomplete, Group.dc, Key.vertigo

    # >>> incomplete image ·····························································································

    INCOMPLETE_IMAGE_ROOT = 69, Library.incomplete, Group.image, Key.root

    # >>> incomplete other-usa ·························································································

    INCOMPLETE_OTHER_USA_ROOT = 15, Library.incomplete, Group.other_usa, Key.root

    # >>> incomplete crossovers ························································································

    INCOMPLETE_CROSSOVERS_ROOT = 16, Library.incomplete, Group.crossovers, Key.root

    # >>> incomplete manga ·····························································································

    INCOMPLETE_MANGA_ROOT = 17, Library.incomplete, Group.manga, Key.root

    # >>> incomplete european ··························································································

    INCOMPLETE_EUROPEAN_ROOT = 61, Library.incomplete, Group.european, Key.root

    # >>> incomplete iberoamerican ·····················································································

    INCOMPLETE_IBEROAMERICAN_ROOT = 114, Library.incomplete, Group.iberoamerican, Key.root

    # >>> incomplete infantile-juvenile ················································································

    INCOMPLETE_INFANTILE_JUVENILE_ROOT = 139, Library.incomplete, Group.infantile_juvenile, Key.root

    # >>> incomplete classic ···························································································

    INCOMPLETE_CLASSIC_ROOT = 60, Library.incomplete, Group.classic, Key.root

    # >>> incomplete over-18 ···························································································

    INCOMPLETE_OVER_18_ROOT = 50, Library.incomplete, Group.over_18, Key.root
    INCOMPLETE_OVER_18_FINISHED = 128, Library.incomplete, Group.over_18, Key.finished

    # >>> incomplete finished ··························································································

    INCOMPLETE_FINISHED_ROOT = 26, Library.incomplete, Group.finished, Key.root

    # COMPLETE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # >>> complete marvel ······························································································

    COMPLETE_MARVEL_CLASSICS = 35, Library.complete, Group.marvel, Key.classics
    COMPLETE_MARVEL_HEROES = 33, Library.complete, Group.marvel, Key.heroes
    COMPLETE_MARVEL_CROSSOVERS = 41, Library.complete, Group.marvel, Key.crossovers
    COMPLETE_MARVEL_MUTANTS = 31, Library.complete, Group.marvel, Key.mutants
    COMPLETE_MARVEL_MUTANTS_WOLVERINE = 163, Library.complete, Group.marvel, Key.mutants_wolverine
    COMPLETE_MARVEL_MUTANTS_MASSACRE = 202, Library.complete, Group.marvel, Key.mutants_massacre
    COMPLETE_MARVEL_FANTASTIC_4 = 124, Library.complete, Group.marvel, Key.fantastic_4
    COMPLETE_MARVEL_DAREDEVIL = 147, Library.complete, Group.marvel, Key.daredevil
    COMPLETE_MARVEL_HULK = 126, Library.complete, Group.marvel, Key.hulk
    COMPLETE_MARVEL_PUNISHER = 148, Library.complete, Group.marvel, Key.punisher
    COMPLETE_MARVEL_SPIDERMAN = 32, Library.complete, Group.marvel, Key.spiderman
    COMPLETE_MARVEL_AVENGERS = 36, Library.complete, Group.marvel, Key.avengers
    COMPLETE_MARVEL_AVENGERS_CAPTAIN_AMERICA = 160, Library.complete, Group.marvel, Key.avengers_captain_america
    COMPLETE_MARVEL_AVENGERS_IRON_MAN = 161, Library.complete, Group.marvel, Key.avengers_iron_man
    COMPLETE_MARVEL_AVENGERS_THOR = 162, Library.complete, Group.marvel, Key.avengers_thor
    COMPLETE_MARVEL_ULTIMATE_UNIVERSE = 125, Library.complete, Group.marvel, Key.ultimate_universe
    COMPLETE_MARVEL_UNIVERSE_2099 = 123, Library.complete, Group.marvel, Key.universe_2099
    COMPLETE_MARVEL_OTHER_EDITIONS = 120, Library.complete, Group.marvel, Key.other_editions

    # >>> complete dc ··································································································

    COMPLETE_DC_CLASSICS = 105, Library.complete, Group.dc, Key.classics
    COMPLETE_DC_HEROES = 40, Library.complete, Group.dc, Key.heroes
    COMPLETE_DC_HEROES_GREEN_LANTERN = 200, Library.complete, Group.dc, Key.heroes_green_lantern
    COMPLETE_DC_HEROES_WONDER_WOMAN = 201, Library.complete, Group.dc, Key.heroes_wonder_woman
    COMPLETE_DC_JLA_JSA = 91, Library.complete, Group.dc, Key.jla_jsa
    COMPLETE_DC_BATMAN = 39, Library.complete, Group.dc, Key.batman
    COMPLETE_DC_SUPERMAN = 38, Library.complete, Group.dc, Key.superman
    COMPLETE_DC_CROSSOVERS = 42, Library.complete, Group.dc, Key.crossovers
    COMPLETE_DC_VERTIGO = 66, Library.complete, Group.dc, Key.vertigo
    COMPLETE_DC_OTHER_EDITIONS = 185, Library.complete, Group.dc, Key.other_editions

    # >>> complete other-usa-canada ····················································································

    COMPLETE_OTHER_USA_CANADA_ROOT = 43, Library.complete, Group.other_usa_canada, Key.root
    COMPLETE_OTHER_USA_CANADA_AFTERSHOCK = 203, Library.complete, Group.other_usa_canada, Key.aftershock
    COMPLETE_OTHER_USA_CANADA_ASPEN = 168, Library.complete, Group.other_usa_canada, Key.aspen
    COMPLETE_OTHER_USA_CANADA_AVATAR = 121, Library.complete, Group.other_usa_canada, Key.avatar
    COMPLETE_OTHER_USA_CANADA_BOOM = 146, Library.complete, Group.other_usa_canada, Key.boom
    COMPLETE_OTHER_USA_CANADA_CHAOS = 122, Library.complete, Group.other_usa_canada, Key.chaos
    COMPLETE_OTHER_USA_CANADA_DARK_HORSE = 70, Library.complete, Group.other_usa_canada, Key.dark_horse
    COMPLETE_OTHER_USA_CANADA_DRAWN_QUARTERLY = 183, Library.complete, Group.other_usa_canada, Key.drawn_quarterly
    COMPLETE_OTHER_USA_CANADA_DYNAMITE = 143, Library.complete, Group.other_usa_canada, Key.dynamite
    COMPLETE_OTHER_USA_CANADA_FANTAGRAPHICS = 173, Library.complete, Group.other_usa_canada, Key.fantagraphics
    COMPLETE_OTHER_USA_CANADA_IDW = 87, Library.complete, Group.other_usa_canada, Key.idw
    COMPLETE_OTHER_USA_CANADA_IMAGE = 44, Library.complete, Group.other_usa_canada, Key.image
    COMPLETE_OTHER_USA_CANADA_ONI_PRESS = 198, Library.complete, Group.other_usa_canada, Key.oni_press
    COMPLETE_OTHER_USA_CANADA_UNIVERSE_CONAN = 127, Library.complete, Group.other_usa_canada, Key.uni_conan
    COMPLETE_OTHER_USA_CANADA_UNIVERSE_STAR_TREK = 180, Library.complete, Group.other_usa_canada, Key.uni_star_trek
    COMPLETE_OTHER_USA_CANADA_UNIVERSE_STAR_WARS = 86, Library.complete, Group.other_usa_canada, Key.uni_star_wars
    COMPLETE_OTHER_USA_CANADA_VALIANT = 184, Library.complete, Group.other_usa_canada, Key.valiant
    COMPLETE_OTHER_USA_CANADA_WILDSTORM = 73, Library.complete, Group.other_usa_canada, Key.wildstorm
    COMPLETE_OTHER_USA_CANADA_ZENESCOPE = 164, Library.complete, Group.other_usa_canada, Key.zenescope

    # >>> complete crossovers ··························································································

    COMPLETE_CROSSOVERS_ROOT = 45, Library.complete, Group.crossovers, Key.root

    # >>> complete manga ·······························································································

    COMPLETE_MANGA_ROOT = 57, Library.complete, Group.manga, Key.root

    # >>> complete european ····························································································

    COMPLETE_EUROPEAN_ROOT = 55, Library.complete, Group.european, Key.root
    COMPLETE_EUROPEAN_SPAIN = 169, Library.complete, Group.european, Key.spain
    COMPLETE_EUROPEAN_SPAIN_LABYRINTH = 59, Library.complete, Group.european, Key.spain_labyrinth
    COMPLETE_EUROPEAN_FRANCE_BELGIUM = 170, Library.complete, Group.european, Key.france_belgium
    COMPLETE_EUROPEAN_ITALY = 171, Library.complete, Group.european, Key.italy
    COMPLETE_EUROPEAN_UNITED_KINGDOM = 172, Library.complete, Group.european, Key.united_kingdom

    # >>> complete iberoamerican ·······················································································

    COMPLETE_IBEROAMERICAN_ROOT = 113, Library.complete, Group.iberoamerican, Key.root
    COMPLETE_IBEROAMERICAN_ARG = 186, Library.complete, Group.iberoamerican, Key.argentina
    COMPLETE_IBEROAMERICAN_ARG_FILM_ADAP = 189, Library.complete, Group.iberoamerican, Key.argentina_film_adaptions
    COMPLETE_IBEROAMERICAN_CHILE = 187, Library.complete, Group.iberoamerican, Key.chile
    COMPLETE_IBEROAMERICAN_MEXICO = 188, Library.complete, Group.iberoamerican, Key.mexico

    # >>> complete infantile-juvenile ··················································································

    COMPLETE_INFANTILE_JUVENILE_ROOT = 107, Library.complete, Group.infantile_juvenile, Key.root

    # >>> complete classic ·····························································································

    COMPLETE_CLASSIC_ROOT = 109, Library.complete, Group.classic, Key.root
    COMPLETE_CLASSIC_SPANISH_UNTIL_1969 = 108, Library.complete, Group.classic, Key.spanish_until_1969

    # >>> complete adult-humor ·························································································

    COMPLETE_ADULT_HUMOR_ROOT = 58, Library.complete, Group.adult_humor, Key.root

    # >>> complete artbooks-and-others ·················································································

    COMPLETE_ARTBOOKS_AND_OTHERS_ROOT = 94, Library.complete, Group.artbooks_and_others, Key.root
