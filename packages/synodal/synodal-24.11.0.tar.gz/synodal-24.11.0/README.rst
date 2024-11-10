=======================
The ``synodal`` package
=======================

A lightweight Python package with metadata about the code repositories of the
`Synodalsoft project <https://www.synodalsoft.net>`__.

Source code repository: https://gitlab.com/lino-framework/synodal

Documentation for the maintainer:
https://dev.lino-framework.org/specs/synodal/index.html

Usage examples:

>>> import synodal
>>> from synodal import KNOWN_REPOS, REPOS_DICT, FRONT_ENDS, PUBLIC_SITES
>>> r = REPOS_DICT['lino']
>>> print(r.git_repo)
https://gitlab.com/lino-framework/lino.git

>>> synodal.Repository._fields
('nickname', 'package_name', 'git_repo', 'settings_module', 'front_end', 'extra_deps', 'public_url', 'verbose_name', 'description')
>>> synodal.PublicSite._fields
('url', 'settings_module', 'default_ui')

>>> for r in FRONT_ENDS.values():
...     print("{r.nickname} : {r.front_end}".format(r=r))
lino : lino.modlib.extjs
react : lino_react.react
openui5 : lino_openui5.openui5

>>> from importlib import import_module
>>> for ps in PUBLIC_SITES:
...     m = import_module(ps.settings_module)
...     print("{ps.url} : {m.Site.verbose_name} using {ps.default_ui}".format(
...        ps=ps, m=m))
https://voga1e.lino-framework.org : Lino Voga using lino.modlib.extjs
https://voga1r.lino-framework.org : Lino Voga using lino_react.react
https://cosi1e.lino-framework.org : Lino Così using lino_react.react
https://noi1r.lino-framework.org : Lino Noi using lino_react.react
https://weleup1.mylino.net : Lino Welfare Eupen using lino.modlib.extjs
https://welcht1.mylino.net : Lino Welfare Châtelet using lino.modlib.extjs


>>> from lino.utils.code import analyze_rst
>>> packages = [r.package_name.replace("-","_") for r in KNOWN_REPOS if r.package_name]
>>> print(analyze_rst(*packages))  #doctest: +SKIP
============== ============ =========== =============== ============= =======
 name           code lines   doc lines   comment lines   total lines   files
-------------- ------------ ----------- --------------- ------------- -------
 atelier        1.1k         847         388             3k            16
 etgen          511          727         300             1.9k          13
 eidreader      88           118         54              307           5
 commondata     7k           25          42              7k            12
 getlino        528          1.2k        241             2k            13
 lino           32k          22k         10k             79k           357
 lino_xl        45k          14k         12k             83k           514
 lino_welfare   40k          9k          4k              60k           371
 lino_react     907          490         244             1.9k          8
 lino_openui5   222          668         235             1.4k          19
 lino_book      23k          3k          2k              32k           639
 lino_amici     6k           238         393             7k            109
 lino_avanti    1.2k         456         562             3k            52
 lino_cms       193          85          77              469           22
 lino_care      849          390         791             2k            41
 lino_cosi      240          138         155             690           36
 lino_mentori   425          293         230             1.2k          37
 lino_noi       1.1k         724         915             3k            52
 lino_presto    1.0k         614         540             3k            55
 lino_pronto    775          199         143             1.4k          46
 lino_tera      1.7k         674         1.2k            5k            77
 lino_shop      359          148         111             795           21
 lino_vilma     467          204         264             1.1k          14
 lino_voga      2k           1.7k        797             6k            59
 lino_weleup    136          146         95              455           9
 lino_welcht    781          206         344             1.7k          27
 total          168k         58k         36k             308k          3k
============== ============ =========== =============== ============= =======
<BLANKLINE>



Above code snippet is skipped because the values change often.
