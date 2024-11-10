#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# code generated 2024-11-09 21:08:50.026864 by make_code.py script of synodal
# fmt: off


from collections import namedtuple

repo_fields = ("nickname", "package_name", "git_repo", "settings_module",
    "front_end", "extra_deps", "public_url", "verbose_name", "description")
Repository = namedtuple('Repository',
                        repo_fields,
                        defaults=['', '', '', [], '', None, None])
PublicSite = namedtuple('PublicSite', "url settings_module default_ui")



__version__ = '24.11.0'

KNOWN_REPOS = REPOS_LIST = [Repository(nickname='atelier', package_name='atelier', git_repo='https://gitlab.com/lino-framework/atelier.git', settings_module='', front_end='', extra_deps=[], public_url='https://atelier.lino-framework.org', verbose_name=None, description=None),
 Repository(nickname='etgen', package_name='etgen', git_repo='https://github.com/lino-framework/etgen', settings_module='', front_end='', extra_deps=[], public_url='https://etgen.lino-framework.org', verbose_name=None, description=None),
 Repository(nickname='eid', package_name='eidreader', git_repo='https://github.com/lino-framework/eidreader', settings_module='', front_end='', extra_deps=[], public_url='', verbose_name=None, description=None),
 Repository(nickname='cd', package_name='commondata', git_repo='https://github.com/lsaffre/commondata', settings_module='', front_end='', extra_deps=[], public_url='', verbose_name=None, description=None),
 Repository(nickname='getlino', package_name='getlino', git_repo='https://gitlab.com/lino-framework/getlino.git', settings_module='', front_end='', extra_deps=[], public_url='https://getlino.lino-framework.org', verbose_name=None, description=None),
 Repository(nickname='lino', package_name='lino', git_repo='https://gitlab.com/lino-framework/lino.git', settings_module='', front_end='lino.modlib.extjs', extra_deps=[], public_url='', verbose_name=None, description=None),
 Repository(nickname='xl', package_name='lino-xl', git_repo='https://gitlab.com/lino-framework/xl.git', settings_module='', front_end='', extra_deps=[], public_url='', verbose_name=None, description=None),
 Repository(nickname='welfare', package_name='lino-welfare', git_repo='https://gitlab.com/lino-framework/welfare.git', settings_module='', front_end='', extra_deps=[], public_url='https://welfare.lino-framework.org', verbose_name=None, description=None),
 Repository(nickname='react', package_name='lino-react', git_repo='https://gitlab.com/lino-framework/react.git', settings_module='', front_end='lino_react.react', extra_deps=[], public_url='https://react.lino-framework.org', verbose_name=None, description=None),
 Repository(nickname='openui5', package_name='lino-openui5', git_repo='https://gitlab.com/lino-framework/openui5.git', settings_module='', front_end='lino_openui5.openui5', extra_deps=[], public_url='', verbose_name=None, description=None),
 Repository(nickname='book', package_name='lino-book', git_repo='https://gitlab.com/lino-framework/book.git', settings_module='', front_end='', extra_deps=[], public_url='https://dev.lino-framework.org/', verbose_name=None, description=None),
 Repository(nickname='cg', package_name='', git_repo='https://gitlab.com/lino-framework/cg.git', settings_module='', front_end='', extra_deps=[], public_url='https://community.lino-framework.org/', verbose_name=None, description=None),
 Repository(nickname='ug', package_name='', git_repo='https://gitlab.com/lino-framework/ug.git', settings_module='', front_end='', extra_deps=[], public_url='https://using.lino-framework.org/', verbose_name=None, description=None),
 Repository(nickname='hg', package_name='', git_repo='https://gitlab.com/lino-framework/hg.git', settings_module='', front_end='', extra_deps=[], public_url='https://hosting.lino-framework.org/', verbose_name=None, description=None),
 Repository(nickname='lf', package_name='', git_repo='https://gitlab.com/lino-framework/lf.git', settings_module='', front_end='', extra_deps=[], public_url='https://www.lino-framework.org/', verbose_name=None, description=None),
 Repository(nickname='ss', package_name='', git_repo='https://gitlab.com/synodalsoft/ss.git', settings_module='', front_end='', extra_deps=[], public_url='https://www.synodalsoft.net/', verbose_name=None, description=None),
 Repository(nickname='algus', package_name='', git_repo='https://gitlab.com/lino-framework/algus.git', settings_module='', front_end='', extra_deps=[], public_url='', verbose_name=None, description=None),
 Repository(nickname='min1', package_name='', git_repo='', settings_module='lino_book.projects.min1.settings', front_end='', extra_deps=[], public_url='', verbose_name='yet another Lino application', description=None),
 Repository(nickname='min2', package_name='', git_repo='', settings_module='lino_book.projects.min2.settings', front_end='', extra_deps=[], public_url='', verbose_name='yet another Lino application', description=None),
 Repository(nickname='cosi4', package_name='', git_repo='', settings_module='lino_book.projects.cosi4.settings', front_end='', extra_deps=[], public_url='https://dev.lino-framework.org/projects/cosi4.html', verbose_name=None, description='a Lino Così for Uruguay'),
 Repository(nickname='cosi5', package_name='', git_repo='', settings_module='lino_book.projects.cosi5.settings', front_end='', extra_deps=[], public_url='https://dev.lino-framework.org/projects/cosi5.html', verbose_name=None, description='a Lino Così for Bangladesh'),
 Repository(nickname='tera2', package_name='', git_repo='', settings_module='lino_book.projects.voga2.settings', front_end='', extra_deps=[], public_url='https://dev.lino-framework.org/projects/voga2.html', verbose_name=None, description='A customized Lino Voga site'),
 Repository(nickname='cosi3', package_name='', git_repo='', settings_module='lino_book.projects.cosi3.settings', front_end='', extra_deps=[], public_url='https://dev.lino-framework.org/projects/cosi3.html', verbose_name=None, description='A Lino Così for Estonia'),
 Repository(nickname='cosi2', package_name='', git_repo='', settings_module='lino_book.projects.cosi2.settings.demo', front_end='', extra_deps=[], public_url='https://dev.lino-framework.org/projects/cosi2.html', verbose_name=None, description='A Lino Così for Belgium (FR)'),
 Repository(nickname='cosi1', package_name='', git_repo='', settings_module='lino_book.projects.cosi1.settings.demo', front_end='', extra_deps=[], public_url='https://dev.lino-framework.org/projects/cosi1.html', verbose_name=None, description='A Lino Così for Belgium (DE)'),
 Repository(nickname='tera1', package_name='', git_repo='', settings_module='lino_book.projects.tera1.settings.demo', front_end='', extra_deps=[], public_url='https://dev.lino-framework.org/projects/tera1.html', verbose_name=None, description='A customized Lino Tera site'),
 Repository(nickname='noi1r', package_name='', git_repo='', settings_module='lino_book.projects.noi1r.settings', front_end='', extra_deps=[], public_url='https://dev.lino-framework.org/projects/noi1r.html', verbose_name=None, description='noi1e with React front end'),
 Repository(nickname='chatter', package_name='', git_repo='', settings_module='lino_book.projects.chatter.settings', front_end='', extra_deps=[], public_url='https://dev.lino-framework.org/projects/chatter.html', verbose_name=None, description='an instant messaging system'),
 Repository(nickname='polly', package_name='', git_repo='', settings_module='lino_book.projects.polly.settings.demo', front_end='', extra_deps=[], public_url='https://dev.lino-framework.org/projects/polly.html', verbose_name=None, description='A little polls manager'),
 Repository(nickname='amici', package_name='lino-amici', git_repo='https://gitlab.com/lino-framework/amici.git', settings_module='lino_amici.lib.amici.settings', front_end='', extra_deps=['lino', 'xl'], public_url='', verbose_name='Lino Amici', description='Manage your family contacts'),
 Repository(nickname='avanti', package_name='lino-avanti', git_repo='https://gitlab.com/lino-framework/avanti.git', settings_module='lino_avanti.lib.avanti.settings', front_end='', extra_deps=['lino', 'xl'], public_url='', verbose_name='Lino Avanti', description='Manage the integration course of immigrants in East Belgium'),
 Repository(nickname='cms', package_name='lino-cms', git_repo='https://gitlab.com/lino-framework/cms.git', settings_module='lino_cms.lib.cms.settings', front_end='', extra_deps=['lino', 'xl'], public_url='', verbose_name='Lino CMS', description='Manage the content of your website'),
 Repository(nickname='prima', package_name='lino-prima', git_repo='https://gitlab.com/synodalsoft/prima.git', settings_module='lino_prima.lib.prima.settings', front_end='', extra_deps=['lino'], public_url='', verbose_name='Lino Prima', description='Manage evaluation results and certificates in a primary school'),
 Repository(nickname='care', package_name='lino-care', git_repo='https://gitlab.com/lino-framework/care.git', settings_module='lino_care.lib.care.settings', front_end='', extra_deps=['lino', 'xl'], public_url='', verbose_name='Lino Care', description='Manage a network of helpers.'),
 Repository(nickname='cosi', package_name='lino-cosi', git_repo='https://gitlab.com/lino-framework/cosi.git', settings_module='lino_cosi.lib.cosi.settings', front_end='', extra_deps=['lino', 'xl'], public_url='', verbose_name='Lino Così', description='A simple accounting application.'),
 Repository(nickname='mentori', package_name='lino-mentori', git_repo='https://gitlab.com/lino-framework/mentori.git', settings_module='lino_mentori.lib.mentori.settings', front_end='', extra_deps=['lino', 'xl'], public_url='', verbose_name='Lino Mentori', description='A Lino Django application for managing internships, mentors and students'),
 Repository(nickname='noi', package_name='lino_noi', git_repo='https://gitlab.com/lino-framework/noi.git', settings_module='lino_noi.lib.noi.settings', front_end='', extra_deps=['lino', 'xl'], public_url='', verbose_name='Lino Noi', description='Manage support tickets and working time.'),
 Repository(nickname='presto', package_name='lino-presto', git_repo='https://gitlab.com/lino-framework/presto.git', settings_module='lino_presto.lib.presto.settings', front_end='', extra_deps=['lino', 'xl'], public_url='', verbose_name='Lino Presto', description='A Lino for managing services'),
 Repository(nickname='pronto', package_name='lino-pronto', git_repo='https://gitlab.com/lino-framework/pronto.git', settings_module='lino_pronto.lib.pronto.settings', front_end='', extra_deps=['lino', 'xl'], public_url='', verbose_name='Lino Pronto', description='A Lino for assembling and selling products'),
 Repository(nickname='tera', package_name='lino-tera', git_repo='https://gitlab.com/lino-framework/tera.git', settings_module='lino_tera.lib.tera.settings', front_end='', extra_deps=['lino', 'xl'], public_url='', verbose_name='Lino Tera', description='A Lino for managing therapeutic centres'),
 Repository(nickname='shop', package_name='lino-shop', git_repo='https://gitlab.com/lino-framework/shop.git', settings_module='lino_shop.lib.shop.settings', front_end='', extra_deps=['lino', 'xl'], public_url='', verbose_name='Lino Shop', description='A Lino for managing a webshop'),
 Repository(nickname='vilma', package_name='lino-vilma', git_repo='https://gitlab.com/lino-framework/vilma.git', settings_module='lino_vilma.lib.vilma.settings', front_end='', extra_deps=['lino', 'xl'], public_url='', verbose_name='Lino Vilma', description='Manage contacts, resources and skills of a village community'),
 Repository(nickname='voga', package_name='lino-voga', git_repo='https://gitlab.com/lino-framework/voga.git', settings_module='lino_voga.lib.voga.settings', front_end='', extra_deps=['lino', 'xl'], public_url='', verbose_name='Lino Voga', description='A Lino Django application for managing courses, participants and meeting rooms'),
 Repository(nickname='weleup', package_name='lino-weleup', git_repo='https://gitlab.com/lino-framework/weleup.git', settings_module='lino_weleup.settings', front_end='', extra_deps=['lino', 'xl', 'welfare'], public_url='', verbose_name='Lino Welfare Eupen', description='A Lino Django application for the PCSW of Eupen'),
 Repository(nickname='welcht', package_name='lino-welcht', git_repo='https://gitlab.com/lino-framework/welcht.git', settings_module='lino_welcht.settings', front_end='', extra_deps=['lino', 'xl', 'welfare'], public_url='', verbose_name='Lino Welfare Châtelet', description='A Lino Django application for the PCSW of Châtelet')]

REPOS_DICT = {r.nickname: r for r in REPOS_LIST}

FRONT_ENDS = {r.front_end: r for r in KNOWN_REPOS if r.front_end}

PUBLIC_SITES = [PublicSite(url='https://voga1e.lino-framework.org', settings_module='lino_voga.lib.voga.settings', default_ui='lino.modlib.extjs'),
 PublicSite(url='https://voga1r.lino-framework.org', settings_module='lino_voga.lib.voga.settings', default_ui='lino_react.react'),
 PublicSite(url='https://cosi1e.lino-framework.org', settings_module='lino_cosi.lib.cosi.settings', default_ui='lino_react.react'),
 PublicSite(url='https://noi1r.lino-framework.org', settings_module='lino_noi.lib.noi.settings', default_ui='lino_react.react'),
 PublicSite(url='https://weleup1.mylino.net', settings_module='lino_weleup.settings', default_ui='lino.modlib.extjs'),
 PublicSite(url='https://welcht1.mylino.net', settings_module='lino_welcht.settings', default_ui='lino.modlib.extjs')]

SPHINX_EXTLINKS = {'ticket': ('https://jane.mylino.net/#/api/tickets/PublicTickets/%s', '#%s')}

# end of generated code
