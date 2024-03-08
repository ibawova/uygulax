# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.17 (default, Sep 30 2020, 13:38:04) 
# [GCC 7.5.0]
# Embedded file name: /storage/emulated/0/Android/data/tv.vavoo.app/files/.vavoo/addons/service.vavoo/lib/variables.py
# Compiled at: 2019-10-23 22:38:45
import xbmcaddon, xbmcgui, xbmc
ADDON_ID = 'service.vavoo'
addon = xbmcaddon.Addon(ADDON_ID)
addonPath = addon.getAddonInfo('path').decode('utf-8')
addonVersion = addon.getAddonInfo('version')
WINDOW_HOME = xbmcgui.Window(10000)
API_URL = 'https://www.vavoo.tv/api/'
PRO_URL = 'https://www.vavoo.tv/pro'
SOFTWARE_URL = 'http://www.vavoo.tv/software'

class PASSWORD:
    SALT, N, R, P, DK_LEN = ('C1k8l0jw8g8puGRauyKjcN0ofNp', 1024, 1, 1, 15)


INTERNET_CHECK_INTERVAL = (30, 90)
INTERNET_CHECK_HOSTS = [('8.8.8.8', 53), ('208.67.222.222', 53)]
LOGIN_CHECK_INTERVAL = (180, 360)
UPDATE_ASK_INTERVAL = 86400
UPDATE_DOWNLOAD_RETRY_INTERVAL = 3600
BACKEND_ERROR_SHOW_LOGSCREEN_TIME = 60
UNKNOWN_ERROR_SHOW_LOGSCREEN_TIME = 600
BUFFER_SIZE = 8192
ANDROID_PACKAGE_NAME = ''
if xbmc.getCondVisibility('system.platform.android'):
    import re, os, traceback
    try:
        m = re.match('^/data/app/([^-]+)-.*$', os.environ['KODI_ANDROID_APK'])
    except KeyError:
        try:
            m = re.match('^/data/app/([^-]+)-.*$', os.environ['XBMC_ANDROID_APK'])
        except KeyError:
            m = None

    if m:
        ANDROID_PACKAGE_NAME = m.group(1)
    else:
        ANDROID_PACKAGE_NAME = 'UNKNOWN'

def getVavooVersion():
    return xbmc.getInfoLabel('System.BuildVersion').split('-')[0]


def getVavooBranch():
    try:
        branch = xbmc.getInfoLabel('System.BuildVersion').split('-')[1]
    except IndexError:
        branch = 'master'

    if not branch:
        branch = 'master'
    return branch


def isVavooDevice():
    if xbmc.getCondVisibility('system.platform.android'):
        try:
            with open('/system/build.prop', 'r') as (f):
                content = f.read()
            if 'ro.product.brand=VAVOO' in content and 'ro.vavoo.type=b' in content:
                return True
        except Exception:
            pass

    return True


IS_SERVICE_PROCESS = True

def assertServiceProcess():
    if not IS_SERVICE_PROCESS:
        return 'ok'


def assertNotServiceProcess():
    if IS_SERVICE_PROCESS:
        return 'ok'


def localize(id):
    return xbmc.getLocalizedString(id)


def getPlatformName():
    if isVavooDevice():
        return 'vavoo'
    else:
        if xbmc.getCondVisibility('system.platform.android'):
            return 'vavoo'
        if xbmc.getCondVisibility('system.platform.linux'):
            return 'linux'
        if xbmc.getCondVisibility('system.platform.windows'):
            return 'win32'
        if xbmc.getCondVisibility('system.platform.osx'):
            return 'osx'
        if xbmc.getCondVisibility('system.platform.ios'):
            return 'ios'
        if xbmc.getCondVisibility('system.platform.atv2'):
            return 'atv2'
        return 'unknown'


def propStatus(log=None):
    import vprop
    data = {'ready': 'ok', 'token': vprop.get('Token'), 
       'ping_status': vprop.get('Ping_Status'), 
       'ruleset': vprop.get('Ruleset')}
    if log:
        xbmc.log('STATUS: ok: true')
    return data