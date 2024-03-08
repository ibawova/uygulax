# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.17 (default, Sep 30 2020, 13:38:04) 
# [GCC 7.5.0]
# Embedded file name: /storage/emulated/0/Android/data/kodi.stube.tv/files/.kodi/addons/plugin.video.stubevavoo/lib/vjackson.py
# Compiled at: 2022-04-23 08:27:43
import xbmcaddon, xbmcplugin, xbmcgui, sys, xbmc, os, urllib, json, re, time, utils, threading, urllib2, urlparse, sign
BASEURL = 'https://www2.vavoo.to/'
MAX_SEARCH_HISTORY_ITEMS = 20
DEBUG = os.path.exists(xbmc.translatePath('special://home/debug').decode('utf-8'))
USE_CACHE = False if DEBUG else True
DEBUG_HOSTERS = DEBUG
REPORT_CAPTURE_SCREENSHOTS = False
path = xbmc.translatePath('special://home/userdata/advancedsettings.xml')
if not os.path.exists(path):
    try:
        with open(path, 'w') as (f):
            f.write('<advancedsettings><cache><buffermode>1</buffermode><memorysize>52428800</memorysize></cache></advancedsettings>')
    except Exception:
        import traceback
        traceback.print_exc()

def main(action, params):
    try:
        indexes = ('index', 'indexMovie', 'indexSerie', 'provider', 'channels', 'channels_legacy',
                   'live', 'sport', 'kidstv', 'cinema', 'skyde', 'dokutv')
        actions = ('home', 'listMovie', 'listSerie', 'directory', 'seasons', 'episodes',
                   'collectionEpisodes', 'tag')
        noCacheActions = 'search'
        selfManagedActions = ('get', 'channels', 'channel')
        if action in indexes:
            globals()[action](params)
            xbmcplugin.endOfDirectory(utils.getPluginhandle(), succeeded=True, cacheToDisc=True)
        elif action in actions:
            globals()[action](params)
            xbmcplugin.endOfDirectory(utils.getPluginhandle(), succeeded=True, cacheToDisc=True)
        elif action in noCacheActions:
            globals()[action](params)
            xbmcplugin.endOfDirectory(utils.getPluginhandle(), succeeded=True, cacheToDisc=False)
        elif action in selfManagedActions:
            globals()[action](params)
        elif action == 'settings':
            utils.addon.openSettings(sys.argv[1])
        else:
            return False
    except Exception:
        checkCancelParam(params)
        raise

    return True


def checkCancelParam(params):
    cancel = params.get('cancel', '').lower()
    if cancel == 'home':
        home(params)


def home(params):
    xbmc.executebuiltin('ActivateWindow(Home)')
    xbmcplugin.endOfDirectory(utils.getPluginhandle())


def index(params):
    xbmcplugin.setContent(utils.getPluginhandle(), 'files')
    addDir2('Suche', 'search', 'search', genre=params.get('genre', ''))
    addDir2('Filme', 'movies', 'indexMovie', genre=params.get('genre', ''))
    addDir2('Serien', 'series', 'indexSerie', genre=params.get('genre', ''))
    addDir2('Neuerscheinungen', 'new2', 'directory', function='all', type='all', order='created', direction='desc', genre=params.get('genre', ''))
    if not params.get('genre', ''):
        addDir2('Genres', 'genres', 'genres', type='all', genre=params.get('genre', ''))
    addDir2('L\xc3\xa4nder', 'genres', 'tag', category='country', type='all', genre=params.get('genre', ''))
    addDir2('Einstellungen', 'settings', 'settings', genre=params.get('genre', ''))


def action_index(params):
    xbmcplugin.setContent(utils.getPluginhandle(), 'files')
    addDir2('Filme', 'movies', 'v2_indexMovie', genre=params.get('genre', ''))
    addDir2('Serien', 'series', 'v2_indexSerie', genre=params.get('genre', ''))
    addDir2('Suche', 'search', 'v2_search', id='all/popular')
    addDir2('v1 Filme', 'movies', 'v1_indexMovie', genre=params.get('genre', ''))
    addDir2('v1 Serien', 'series', 'v1_indexSerie', genre=params.get('genre', ''))
    addDir2('Einstellungen', 'settings', 'v2_settings', genre=params.get('genre', ''))


def action_indexMovie(params):
    xbmcplugin.setContent(utils.getPluginhandle(), 'movies')
    addDir2('Beliebte Filme', 'new2', 'v2_list', id='movie/popular')
    addDir2('Beliebte Filme (Deutschland)', 'new2', 'v2_list', id='movie/popularDE')
    addDir2('Angesagte Filme', 'new2', 'v2_list', id='movie/trending')
    addDir2('Angesagte Filme (Deutschland)', 'new2', 'v2_list', id='movie/trendingDE')
    addDir2('Suche', 'search', 'v2_search', id='movie/popular')
    addDir2('v1 Filme', 'movies', 'v1_indexMovie', genre=params.get('genre', ''))
    addDir2('Einstellungen', 'settings', 'v2_settings', genre=params.get('genre', ''))


def action_indexSerie(params):
    xbmcplugin.setContent(utils.getPluginhandle(), 'tvshows')
    addDir2('Beliebte Serien', 'new2', 'v2_list', id='series/popular')
    addDir2('Angesagte Serien', 'new2', 'v2_list', id='series/trending')
    addDir2('Suche', 'search', 'v2_search', id='series/popular')
    addDir2('v1 Serien', 'series', 'v1_indexSerie', genre=params.get('genre', ''))
    addDir2('Einstellungen', 'settings', 'v2_settings', genre=params.get('genre', ''))


ITEM_TYPES = {'movie': 'Film', 
   'serie': 'Serie'}
RESOLUTION_OPTIONS = (
 'all', 'hd', 'sd')
STREAM_SELECT_OPTIONS = ('hosters2', 'auto', 'grouped')
PLAYBACK_RESOLUTION_OPTIONS = (
 'Highest', '1080p', '720p', '480p', '360p', 'Manual')
LANGUAGE_CODES = {'de': 'DE', 
   'en': 'EN'}
LANGUAGE_NAMES = {'de': {'de': 'Deutsch', 
          'en': 'Englisch'}, 
   'en': {'de': 'German', 
          'en': 'English'}}



def provider(params):
    name = params['name']
    xbmcplugin.setContent(utils.getPluginhandle(), 'files')
    addDir2('Neue Filme', 'new2', 'directory', function='collection', type='movie', name='justwatch.com/de/' + name + '/new', order='collection', direction='desc', genre=params.get('genre', ''))
    addDir2('Neue Serien', 'new2', 'directory', function='collection', type='serie', name='justwatch.com/de/' + name + '/new', order='collection', direction='desc', genre=params.get('genre', ''))
    addDir2('Beliebte Filme', 'top', 'directory', function='collection', type='movie', name='justwatch.com/de/' + name + '/popular', order='collection', direction='asc', genre=params.get('genre', ''))
    addDir2('Beliebte Serien', 'top', 'directory', function='collection', type='serie', name='justwatch.com/de/' + name + '/popular', order='collection', direction='asc', genre=params.get('genre', ''))
    addDir2('Einstellungen', 'settings', 'settings')


def channels(params):
    return live(params)


def channels_legacy(params):
    channels = makeRequest('channel', {})
    channels = sorted(channels, key=lambda channel: channel['title'])
    xbmcplugin.setContent(utils.getPluginhandle(), 'files')
    for channel in channels:
        channel['action'] = 'channel'
        url = getPluginUrl(channel)
        o = xbmcgui.ListItem(channel['title'], iconImage='special://home/addons/plugin.video.stubevavoo/channel.png', icon='special://home/addons/plugin.video.stubevavoo/channel.png')
        o.setArt({"icon": 'special://home/addons/plugin.video.stubevavoo/channel.png'})
        o.setArt({"thumb": 'special://home/addons/plugin.video.stubevavoo/channel.png'})
        o.setArt({"poster": 'special://home/addons/plugin.video.stubevavoo/channel.png'})
        o.setArt({'ThumbnailImage': 'special://home/addons/plugin.video.stubevavoo/channel.png'})
        o.setInfo(type='Video', infoLabels={'Title': channel['title']})
        o.setProperty('IsPlayable', 'true')
        o.setProperty('selectaction', 'play')
        xbmcplugin.addDirectoryItem(handle=utils.getPluginhandle(), url=url, listitem=o, isFolder=False)

    xbmcplugin.endOfDirectory(int(sys.argv[1]), succeeded=True, cacheToDisc=True)



def channel(params):
    progress = xbmcgui.DialogProgress()
    try:
        progress.create('NAHRO.TV', u'Baglaniyor Lutfen Bekleyiniz...')
        progress.update(25)
        from urlresolver import resolve
        resolvedUrl = resolve(params['url'])
        if '|' not in resolvedUrl:
            resolvedUrl += '|'
        resolvedUrl += '&seekable=0'
        progress.update(50)
        o = xbmcgui.ListItem()
        o.setInfo('Video', {'title': params['title'], 'Seekable': 'false'})
        o.setLabel(params['title'])
        o.setArt({"icon": 'special://home/addons/plugin.video.stubevavoo/channel.png'})
        o.setArt({"poster": 'special://home/addons/plugin.video.stubevavoo/channel.png'})
        o.setArt({"thumb": 'special://home/addons/plugin.video.stubevavoo/channel.png'})
        o.setThumbnailImage({'ThumbnailImage': 'special://home/addons/plugin.video.stubevavoo/channel.png'})
        o.setPath(resolvedUrl)
        o.setProperty('IsPlayable', 'true')
        o.setProperty('IsNotSeekable', 'true')
        o.setProperty('Seekable', 'false')
        xbmcplugin.setResolvedUrl(utils.getPluginhandle(), True, o)
        progress.update(75)
    finally:
        if progress:
            progress.close()


def sport(params, channelFilter={}):
    channelFilter = {u'Germany': [
                  u'SKY BUNDESLIGA',
                  u'SKY SPORT',
                  u'DAZN',
                  u'EUROSPORT',
                  u'TELECLUB SPORT',
                  u'TELEKOM',
                  u'SPORT'], 
       u'Turkey': [
                 u'SPOR',
                 u'SPORT'], 
       u'United Kingdom': [
                         u'SPORT',
                         u'LIVERPOOL',
                         u'UNITED'], 
       u'ITALY': [
                u'SPORT'], 
       u'Denmark': [
                  u'SPORT'], 
       u'Albania': [
                  u'SPORT'], 
       u'Arabia': [
                 u'SPORT',
                 u'NBA',
                 u'RACING'], 
       u'Azerbaijan': [
                     u'SPORT'], 
       u'Balkans': [
                  u'ARENA',
                  u'SPORT',
                  u'EUROSPORT'], 
       u'Bulgaria': [
                   u'SPORT'], 
       u'France': [
                 u'SPORT'], 
       u'Netherlands': [
                      u'SPORT'], 
       u'Poland': [
                 u'SPORT'], 
       u'Romania': [
                  u'SPORT'], 
       u'Portugal': [
                   u'SPORT'], 
       u'Belgium': [
                  u'SPORT'], 
       u'Greece': [
                 u'SPORT'], 
       u'Russia': [
                 u'SPORT'], 
       u'Spain': [
                u'SPORT',
                u'FUTBOL',
                u'LIGA',
                u'REAL'], 
       u'Sweden': [
                 u'SPORT'], 
       u'SPORTS': [
                 u'SPORTS'], 
       u'SPORTS 2': [
                   u'SPORTS'], 
       u'Iran': [
               u'SPORT']}
    return live(params, action='sport', channelFilter=channelFilter)


def kidstv(params, channelFilter={}):
    channelFilter = {u'Germany': [u'BOOMERANG',
                  u'CARTOON',
                  u'DISNEY CHANNEL',
                  u'DISNEY XD',
                  u'DISNEY JUNIOR',
                  u'JUNIOR',
                  u'NICKELODEON',
                  u'NICK',
                  u'KIKA',
                  u'SUPER RTL',
                  u'TOGGO',
                  u'FIX',
                  u'BABY',
                  u'RIC',
                  u'DER KLEINE',
                  u'MASHA',
                  u'PEPPA',
                  u'MASKS',
                  u'KIDS',
                  u'MIRA',
                  u'TOM'],
                  u'Turkey': [], u'United Kingdom': [], u'ITALY': [], u'Denmark': [], u'Albania': [], u'Arabia': [], u'Azerbaijan': [], u'Balkans': [], u'Bulgaria': [], u'France': [], u'Netherlands': [], u'Poland': [], u'Romania': [], u'Portugal': [], u'Belgium': [], u'Greece': [], u'Russia': [], u'Spain': [], u'Sweden': [], u'Iran': []}
    return live(params, action='kidstv', channelFilter=channelFilter)


def dokutv(params, channelFilter={}):
    channelFilter = {u'Germany': [u'DISCOVERY',
                  u'HISTORY',
                  u'PLANET',
                  u'NAT',
                  u'SPIEGEL',
                  u'DOKU',
                  u'NATIONAL',
                  u'GEO',
                  u'GALILEO',
                  u'DMAX',
                  u'WELT DER'],
                  u'Turkey': [], u'United Kingdom': [], u'ITALY': [], u'Denmark': [], u'Albania': [], u'Arabia': [], u'Azerbaijan': [], u'Balkans': [], u'Bulgaria': [], u'France': [], u'Netherlands': [], u'Poland': [], u'Romania': [], u'Portugal': [], u'Belgium': [], u'Greece': [], u'Russia': [], u'Spain': [], u'Sweden': [], u'Iran': []}
    return live(params, action='dokutv', channelFilter=channelFilter)


def cinema(params, channelFilter={}):
    channelFilter = {u'Germany': [
                  u'SKY CINEMA',
                  u'SKY ACTION',
                  u'SKY EMOTION',
                  u'CINEMA',
                  u'MOVIES',
                  u'POPCORN',
                  u'ELITECINEMA',
                  u'SKY COMEDY',
                  u'SKY SELECT',
                  u'SKY HITS',
                  u'TNT FILM',
                  u'KINOWELT',
                  u'SKY FAMILY',
                  u'HEIMATKANAL',
                  u'NOSTALGIE',
                  u'PREMIER',
                  u'PRIME',
                  u'SONY',
                  u'MGM',
                  u'STAR',
                  u'SILVERLINE',
                  u'ZEE'], 
                  u'Turkey': [], u'United Kingdom': [], u'ITALY': [], u'Denmark': [], u'Albania': [], u'Arabia': [], u'Azerbaijan': [], u'Balkans': [], u'Bulgaria': [], u'France': [], u'Netherlands': [], u'Poland': [], u'Romania': [], u'Portugal': [], u'Belgium': [], u'Greece': [], u'Russia': [], u'Spain': [], u'Sweden': [], u'Iran': []}
    return live(params, action='cinema', channelFilter=channelFilter)


def skyde(params, channelFilter={}):
    channelFilter = {u'Germany': [u'SKY'],
                      u'Turkey': [], u'United Kingdom': [], u'ITALY': [], u'Denmark': [], u'Albania': [], u'Arabia': [], u'Azerbaijan': [], u'Balkans': [], u'Bulgaria': [], u'France': [], u'Netherlands': [], u'Poland': [], u'Romania': [], u'Portugal': [], u'Belgium': [], u'Greece': [], u'Russia': [], u'Spain': [], u'Sweden': [], u'Iran': []}
    return live(params, action='skyde', channelFilter=channelFilter)


def live(params, action='live', channelFilter=None):
    channels = makeRequest('live2/index', {'output': 'json'},  cache='medium')
    groups = {}
    for c in channels:
        if c['group'] not in groups:
            groups[c['group']] = {}
        g = groups[c['group']]
        name = re.sub('( (SD|HD|FHD|UHD|H265|GERMANY|DEUTSCHLAND|1080|DE|S-ANHALT|SACHSEN|MATCH TIME))|( \\(BACKUP\\))|\\(BACKUP\\)|( \\([\\w ]+\\))|\\([\\d+]\\)', '', c['name'])
        if channelFilter:
            f = channelFilter.get(c['group'])
            if f is True:
                if name not in g:
                    g[name] = []
                g[name].append(c)
            if any(n in name for n in f):
                if name not in g:
                    g[name] = []
                g[name].append(c)
        else:
            if name not in g:
                g[name] = []
            g[name].append(c)

    if params.get('group') and params.get('name'):
        livePlay(action, groups, params['group'], params['name'])
    elif params.get('group'):
        liveGroupIndex(action, groups, params.get('group'))
    else:
        liveIndex(action, groups)


def livePlay(action, groups, group, name):
    try:
        m = groups[group][name]
        m[0]
    except IndexError:
        xbmcgui.Dialog().ok('Der Kanal ist nicht verf\xc3\xbcgbar', 'Bitte versuche es sp\xc3\xa4ter erneut.')
        return

    if len(m) > 1 or DEBUG:
        captions = list(sorted([ n['name'] for n in m ]))
        index = xbmcgui.Dialog().select('Stream w\xc3\xa4hlen', captions)
        if index < 0:
            raise ValueError('CANCELED')
        n = m[index]
    else:
        n = m[0]
    progress = xbmcgui.DialogProgress()
    try:
        progress.create('NAHRO.TV', u'Baglaniyor Lutfen Bekleyiniz...')
        progress.update(15)
        xbmc.sleep(50)
        o = xbmcgui.ListItem()
        if n['logo']:
            o.setThumbnailImage(n['logo'])
        else:
            o.setArt({"icon": 'special://home/addons/plugin.video.stubevavoo/channel.png'})
            o.setArt({"thumb": 'special://home/addons/plugin.video.stubevavoo/channel.png'})
            o.setArt({"poster": 'special://home/addons/plugin.video.stubevavoo/channel.png'})
        o.setInfo('Video', {'title': n['name'], 'Seekable': 'false', 'SeekEnabled': 'false'})
        o.setLabel(n['name'])
        o.setPath(n['url'] + '?n=1&b=5&vavoo_auth=' + sign.getAuthSignature() + '|User-agent=VAVOO/1.51')
        o.setProperty('IsPlayable', 'true')
        o.setProperty('IsNotSeekable', 'true')
        o.setProperty('Seekable', 'false')
        o.setProperty('SeekEnabled', 'false')
        progress.update(30)
        xbmcplugin.setResolvedUrl(utils.getPluginhandle(), True, o)
        progress.update(45)
        abortReason = ''
        step = 1
        t = time.time()
        player = Player()
        try:
            while not abortReason:
                if xbmc.abortRequested:
                    abortReason = 'aborted'
                elif progress.iscanceled():
                    abortReason = 'cancelled'
                elif time.time() - t > 60:
                    abortReason = 'timeout'
                elif step == 1:
                    if player.isPlaying():
                        progress.update(60)
                        step = 2
                elif step == 2:
                    if xbmc.getInfoLabel('VideoPlayer.VideoResolution'):
                        progress.update(75)
                        step = 3
                elif step == 3:
                    if True or player.isPlaying() and player.getTime() > 0.1:
                        progress.update(100)
                        break
                if not abortReason:
                    xbmc.sleep(250)

            if abortReason:
                player.stop()
                raise RuntimeError('Stream died! reason=%s' % abortReason)
        finally:
            del player

    finally:
        if progress:
            progress.close()
            del progress


def liveGroupIndex(action, groups, group):
    gName = group.encode('utf-8')
    g = groups[group]
    for name, m in sorted(g.items()):
        name = name.strip().encode('utf-8')
        url = getPluginUrl({'action': action, 'group': gName, 'name': name})
        for n in m:
            if n['logo']:
                o = xbmcgui.ListItem(name, iconImage='special://home/addons/plugin.video.stubevavoo/channel.png', thumbnailImage='special://home/addons/plugin.video.stubevavoo/channel.png')
                o.setArt({"icon": 'special://home/addons/plugin.video.stubevavoo/channel.png'})
                o.setArt({"poster": 'special://home/addons/plugin.video.stubevavoo/channel.png'})
                o.setThumbnailImage(n['logo'])
                break
        else:
            o = xbmcgui.ListItem(name, iconImage='special://home/addons/plugin.video.stubevavoo/channel.png')
#        o.setThumbnailImage({'ThumbnailImage': 'special://home/addons/plugin.video.stubevavoo/channel.png'})
        o.setInfo(type='Video', infoLabels={'Title': name})
        o.setArt({"icon": 'special://home/addons/plugin.video.stubevavoo/channel.png'})
        o.setArt({"thumb": 'special://home/addons/plugin.video.stubevavoo/channel.png'})
        o.setArt({"poster": 'special://home/addons/plugin.video.stubevavoo/channel.png'})
        o.setProperty('IsPlayable', 'true')
        o.setProperty('selectaction', 'play')
        xbmcplugin.addDirectoryItem(handle=utils.getPluginhandle(), url=url, listitem=o, isFolder=False)

    xbmcplugin.endOfDirectory(int(sys.argv[1]), succeeded=True, cacheToDisc=True)


def liveIndex(action, groups):
    LIVE_GROUP_ALIASES = (
     (1, u'Germany', u'Deutschland', 'flags/country/de.png', None),
     (2, u'Turkey', u'T\xfcrkei', 'flags/country/tr.png', None),
     (3, u'Denmark', u'D\xe4nemark', 'flags/country/dk.png', None),
     (4, u'Sports International', u'Sport International', 'flags/country/eu.png', None),
     (99999, u'Albania', u'Albanien', 'flags/country/al.png', None),
     (99999, u'Arabia', u'Arabisch', 'flags/country/ae.png', None),
     (99999, u'Azerbaijan', u'Azerbaijan', 'flags/country/az.png', None),
     (
      99999, u'Balkans', u'Balkan', 'special://home/addons/' + utils.addonID + '/resources/yu.png', None),
     (99999, u'Bulgaria', u'Bulgarien', 'flags/country/bg.png', None),
     (99999, u'France', u'Frankreich', 'flags/country/fr.png', None),
     (99999, u'Netherlands', u'Niederlande', 'flags/country/nl.png', None),
     (99999, u'Poland', u'Polen', 'flags/country/pl.png', None),
     (99999, u'Romania', u'Rum\xe4nien', 'flags/country/ro.png', None),
     (99999, u'Portugal', u'Portugal', 'flags/country/pt.png', None),
     (99999, u'Brasil', u'Brasilien', 'flags/country/br.png', None),
     (99999, u'Italy', u'Italien', 'flags/country/it.png', None),
     (99999, u'Belgium', u'Belgien', 'flags/country/be.png', None),
     (99999, u'United Kingdom', u'England', 'flags/country/gb.png', None),
     (99999, u'Greece', u'Griechenland', 'flags/country/gr.png', None),
     (99999, u'Russia', u'Russland', 'flags/country/ru.png', None),
     (99999, u'Spain', u'Spanien', 'flags/country/es.png', None),
     (99999, u'Sweden', u'Schweden', 'flags/country/se.png', None),
     (99999, u'Iran', u'Iran', 'flags/country/ir.png', None))
    index = []
    for group, g in groups.items():
        for i, (position, alias, name, icon, url) in enumerate(LIVE_GROUP_ALIASES):
            if alias == group:
                i = position
                title = name
                break
        else:
            i, title, icon, url = (
             99999, group, 'special://home/addons/plugin.video.stubevavoo/channel.png', None)

        if url is None:
            url = getPluginUrl({'action': action, 'group': group.encode('utf-8')})
        index.append((i, title.strip() + u' (' + str(len(g)) + u' Kan\xe4le)', icon, url))

    for i, title, icon, url in sorted(index):
        o = xbmcgui.ListItem(title, iconImage=icon)
        o.setInfo(type='Video', infoLabels={'Title': title})
        o.setProperty('IsPlayable', 'false')
        xbmcplugin.addDirectoryItem(handle=utils.getPluginhandle(), url=url, listitem=o, isFolder=True)

    xbmcplugin.endOfDirectory(int(sys.argv[1]), succeeded=True, cacheToDisc=True)
    return


ITEM_TYPES = {'movie': 'Film', 'serie': 'Serie'}
LANGUAGE_OPTIONS = (
 'all', 'de', 'en')
LOCALE_OPTIONS = ('de', 'en')
RESOLUTION_OPTIONS = ('all', 'hd', 'sd')
STREAM_SELECT_OPTIONS = ('hosters2', 'auto', 'grouped')
PLAYBACK_RESOLUTION_OPTIONS = (
 'Highest', '1080p', '720p', '480p', '360p', 'Manual')
LANGUAGE_CODES = {'de': 'DE', 'en': 'EN'}
LANGUAGE_NAMES = {'de': {'de': 'Deutsch', 'en': 'Englisch'}, 
   'en': {'de': 'German', 'en': 'English'}}
HOSTER_ALIASES = {}
HOSTER_ALIASES_SHORT = {}
URLRESOLVER_SET_QUALITY = {}

def getLanguage(params):
    if 'language' in params:
        return params['language']
    return LANGUAGE_OPTIONS[int(utils.addon.getSetting('language'))]


def getLocale(params):
    if 'locale' in params:
        return params['locale']
    return LOCALE_OPTIONS[int(utils.addon.getSetting('locale'))]


def getHosters(params):
    hosters = []
    with open(xbmc.translatePath('special://home/addons/' + utils.addonID + '/resources/settings.xml').decode('utf-8'), 'r') as (f):
        data = f.read()
    for label, shortlabel, default in re.findall('<setting .* label="([^"]+)" shortlabel="([^"]+)" default="(true|false)"', data):
        value = utils.addon.getSetting('hoster_' + label) or default
        if value != 'true':
            hosters.append('!' + label)
        HOSTER_ALIASES_SHORT[label] = shortlabel

    return (',').join(hosters)


def getResolution(params):
    if 'resolution' in params:
        return params['resolution']
    return RESOLUTION_OPTIONS[int(utils.addon.getSetting('resolution') or 1)]


def getPlaybackResolution():
    return PLAYBACK_RESOLUTION_OPTIONS[int(utils.addon.getSetting('playback_resolution') or 0)]


def getStreamSelect():
    if DEBUG_HOSTERS:
        return 'hosters2'
    return STREAM_SELECT_OPTIONS[int(utils.addon.getSetting('stream_select') or 0)]


def getAutoTryNextStream():
    if DEBUG_HOSTERS:
        return False
    return utils.addon.getSetting('auto_try_next_stream') != 'false'


def prepareListItem(urlParams, params, e, addTypename=False, isPlayable=False, callback=None):
    infos = {}
    properties = {}

    def getMeta(*paths, **kwargs):
        for path in paths:
            f = e
            for p in path:
                try:
                    f = f[p]
                except (KeyError, TypeError):
                    f = None
                    break

            if f:
                return f

        return kwargs.get('default', None)

    def setInfo(key, value):
        if value:
            infos[key] = value

    def setProperty(key, value):
        if value:
            properties[key] = value

    def setInfoPeople(key, value):
        if value:
            setInfo(key, value)

    title = e['title']
    attrs = []
    if addTypename:
        attrs.append(ITEM_TYPES[e['type']])
    if attrs:
        title += ' (' + (', ').join(attrs) + ')'
    if 'channelName' in e:
        title = '[B]' + e['channelName'] + '[/B]: ' + title
    setInfo('title', title)
    setInfo('originaltitle', getMeta(('original_title', )))
    setInfo('year', e['year'])
    media = e['media']
    art = {'thumb': getMeta(('images', 'thumb'), default='special://home/addons/plugin.video.stubevavoo/channel.png'), 'poster': getMeta(('images', 'poster'), default='special://home/addons/plugin.video.stubevavoo/channel.png'), 
       'banner': getMeta(('images', 'banner')), 
       'fanart': getMeta(('images', 'fanart')), 
       'clearart': getMeta(('images', 'clearart')), 
       'clearlogo': getMeta(('images', 'clearlogo')), 
       'landscape': getMeta(('images', 'still'))}

    def updateInfos(data):
        setInfo('plot', data.get('plot', None))
        setInfo('code', data.get('imdb', None))
        setInfo('premiered', data.get('release_date', None))
        setInfo('rating', data.get('rating', None))
        setInfo('votes', data.get('votes', None))
        return

    updateInfos(e)
    if e['type'] == 'serie':
        if 'get' in e:
            season = e['get']['season']
            episode = e['get']['episode']
        elif 'episode' in e:
            season = e['episode']['season']
            episode = e['episode']['episode']
            setInfo('TVShowTitle', 'Season %s Episode %s' % (season, episode))
        else:
            season = params.get('season')
            episode = params.get('episode')
        if season is not None and 'seasons' in e:
            setInfo('season', season)
            setInfo('episode', episode)
            season = getMeta(('seasons', season))
            if season:
                if 'get' not in e:
                    setProperty('TotalEpisodes', len(season.get('episodes', [])))
                season_title = season.get('name', None)
                if season_title and season_title.startswith('Staffel '):
                    season_title = None
                setProperty('SeasonTitle', season_title)
                media = season['media']
                poster = season.get('poster', None)
                if poster:
                    art['poster'] = poster
                    art['thumb'] = poster
                media = season['media']
                updateInfos(season)
                episode = season.get('episodes', {}).get(episode, None)
                if episode:
                    episode_title = episode.get('name', None)
                    if episode_title and episode_title.startswith('Episode '):
                        episode_title = None
                    setInfo('TVShowTitle', episode_title)
                    media = season['media']
                    thumb = episode.get('still', None)
                    if thumb:
                        art['thumb'] = thumb
                        art['landscape'] = thumb
                    updateInfos(episode)
    if art['fanart']:
        setInfo('fanart_image', art['fanart'])
    language = getLanguage(params)
    if language == 'all':
        urlParams['languages'] = (',').join(media['languages'])
        setProperty('Languages', (',').join(media['languages']))
    else:
        urlParams['languages'] = language
    if 'hd' in media['resolutions']:
        setProperty('ResolutionQuality', 'HD')
    genres = set()
    for g in getMeta(('genres', )) or tuple():
        genres.add(g)

    genres = (', ').join(sorted(genres))
    setInfo('genre', genres)
    countries = set()
    for g in getMeta(('countries', )) or tuple():
        countries.add(g)

    countries = (', ').join(sorted(countries))
    setInfo('country', countries)
    setInfoPeople('cast', getMeta(('cast', )))
    setInfoPeople('credits', getMeta(('credits', )))
    value = getMeta(('directors', ))
    if value:
        setInfo('director', value[0])
    value = getMeta(('writers', ))
    if value:
        setInfo('writer', value[0])
    trailer = getMeta(('trailers', ))
    if trailer:
        setInfo('trailer', trailer[(-1)]['url'])
    else:
        setInfo('trailer', getPluginUrl({'action': 'trailer', 'name': title.encode('utf-8')}))
    setProperty('selectaction', 'info')
    if isPlayable:
        setProperty('IsPlayable', 'true')
    contextMenuItems = []
    import dldb
    dldb.createListItemHook(urlParams, params, e, isPlayable, properties, contextMenuItems)
    if callback:
        callback(urlParams, params, e, isPlayable, properties, contextMenuItems)
    return (infos, properties, art, media, contextMenuItems)


def createListItem(*args, **kwargs):
    o = kwargs.pop('o', None)
    infos, properties, art, media, contextMenuItems = prepareListItem(*args, **kwargs)
    if o is None:
        o = xbmcgui.ListItem()
    o.setInfo('Video', infos)
    o.setLabel(infos['title'])
    o.addContextMenuItems(contextMenuItems, False)
    for key, value in properties.items():
        if not isinstance(value, basestring):
            value = str(value)
        o.setProperty(key, value)

    if art:
        o.setArt(art)
        if art['thumb']:
            o.setThumbnailImage(art['thumb'])
    return (
     o, media)


def createDirectory(function, type, params, data, sortByHD=True):
    if type == 'series':
        content = 'tvshows'
    else:
        content = 'movies'
    xbmcplugin.setContent(utils.getPluginhandle(), content)
    items = []
    for i, e in enumerate(data):
        if e['type'] == 'movie':
            isPlayable = True
            isFolder = False
            action = 'get'
        else:
            isPlayable = False
            isFolder = True
            action = 'seasons'
        addTypename = True if type == 'all' and not function.startswith('collection') else False
        urlParams = {'action': action, 'id': str(e['id'])}
        o, media = createListItem(urlParams, params, e, addTypename, isPlayable=isPlayable)
        if sortByHD and 'hd' in media['resolutions']:
            order = 0
        else:
            order = 1
        items.append((order, i, urlParams, o, media, isFolder))

    for _, __, urlParams, o, media, isFolder in sorted(items):
        xbmcplugin.addDirectoryItem(handle=utils.getPluginhandle(), url=getPluginUrl(urlParams), listitem=o, isFolder=isFolder)


def addNextPage(params, **kwargs):
    params = dict(params)
    params.update(kwargs)
    params['page'] = int(params.get('page', 1)) + 1
    addDir('>>> Weiter', getPluginUrl(params))


def directory(params, sortByHD=True):
    function = params.pop('function', 'all')
    data = makeRequest(function, params=params, cache='medium')
    createDirectory(function, params.get('type', 'all'), params, data, sortByHD)
    if data and len(data) >= 50:
        addNextPage(params, action='directory', function=function)


class search(object):
    db = None

    def __init__(self, params):
        history = self.getHistory()
        if 'query' in params:
            params['query'] = params['query'].decode('utf-8')
            if params.get('exact') == 'true' and not params['query'].startswith('"'):
                params['query'] = '"' + params['query'] + '"'
            if params['query'] == '-':
                oKeyboard = xbmc.Keyboard(history[0] if history else '')
                oKeyboard.doModal()
                if not oKeyboard.isConfirmed():
                    self.index(history)
                    return
                params['query'] = oKeyboard.getText().strip()
                if not params['query']:
                    self.index(history)
                    return
                params['query'] = params['query'].decode('utf-8')
            elif 'delete' in params:
                c = self.getDatabase().cursor()
                try:
                    try:
                        c.execute('DELETE FROM search_history WHERE query=?', [params['query']])
                        self.db.commit()
                    except Exception:
                        import traceback
                        traceback.print_exc()

                finally:
                    c.close()

                self.index(self.getHistory())
                return
            if params.get('history', 'true') == 'true':
                c = self.getDatabase().cursor()
                try:
                    try:
                        c.execute('REPLACE INTO search_history (query, t) VALUES (?, ?)', [
                         params['query'], int(time.time())])
                        self.db.commit()
                    except Exception:
                        import traceback
                        traceback.print_exc()

                finally:
                    c.close()

            params['function'] = 'all'
            params['query'] = params['query'].encode('utf-8')
            directory(params, sortByHD=False)
        else:
            self.index(history)

    def getDatabase(self):
        if not self.db:
            self.db = utils.Database(filename='vjackson.db')
            c = self.db.cursor()
            try:
                try:
                    c.execute('CREATE TABLE IF NOT EXISTS search_history (query TEXT PRIMARY KEY, t INTEGER)')
                    self.db.commit()
                except Exception:
                    import traceback
                    traceback.print_exc()

            finally:
                c.close()

        return self.db

    def getHistory(self):
        c = self.getDatabase().cursor()
        result = []
        try:
            try:
                c.execute('SELECT query FROM search_history ORDER BY t DESC')
                for query, in c:
                    result.append(query)

                for query in result[MAX_SEARCH_HISTORY_ITEMS - 1:]:
                    c.execute('DELETE FROM search_history WHERE query=?', [query])

                self.db.commit()
            except Exception:
                import traceback
                traceback.print_exc()

        finally:
            c.close()

        return result

    def index(self, history):
        addDir2('Neue Suche', 'search', 'search', query='-')
        for query in history:
            url = getPluginUrl({'action': 'search', 'query': query.encode('utf-8')})
            liz = xbmcgui.ListItem(query, iconImage='special://home/addons/plugin.video.stubevavoo/channel.png', thumbnailImage=getIcon('query'))
            liz.setInfo(type='Video', infoLabels={'Title': query})
            ctx = [('L\xc3\xb6schen', 'ActivateWindow(Videos,' + url + '&delete=1)')]
            liz.addContextMenuItems(ctx, False)
            xbmcplugin.addDirectoryItem(handle=utils.getPluginhandle(), url=url, listitem=liz, isFolder=True)

        addDir2('Einstellungen', 'settings', 'settings')


def tag(params):
    xbmcplugin.setContent(utils.getPluginhandle(), 'seasons')
    data = makeRequest('tags', params, addLanguage=False, addHosters=False, addResolution=False, cache='long')
    urlParams = {'action': 'directory', 'function': 'all', 'type': params.pop('type', 'all'), 'genre': params.pop('genre', '')}
    for i in sorted(data):
        if params['category'] == 'country':
            try:
                j = [ k for k in data[i] if len(k) == 2 ][0]
                icon = 'flags/country/' + j + '.png'
            except IndexError:
                pass

        else:
            icon = None
        o = xbmcgui.ListItem(iconImage=icon)
        o.setLabel(i)
        urlParams2 = dict(urlParams)
        urlParams2[params['category']] = i
        xbmcplugin.addDirectoryItem(handle=utils.getPluginhandle(), url=getPluginUrl(urlParams2), listitem=o, isFolder=True)

    return


def getParamsLanguage(params, forceDialog=False):
    languages = params.pop('languages').split(',')
    if len(languages) == 1 and not forceDialog:
        params['language'] = languages[0]
    else:
        locale = getLocale(params)
        captions = [ LANGUAGE_NAMES[locale][lang] for lang in languages ]
        index = xbmcgui.Dialog().select('Sprache w\xc3\xa4hlen', captions)
        if index < 0:
            return
        for key, value in LANGUAGE_NAMES[locale].items():
            if value == captions[index]:
                params['language'] = key
                break
        else:
            raise ValueError('Could not find language %s' % captions[index])


def seasons(params):
    id = int(params['id'])
    getParamsLanguage(params)
    data = makeRequest('get', params, cache='short')
    if len(data['seasons']) == 1:
        params['season'] = data['seasons'].keys()[0]
        episodes(params)
        return
    xbmcplugin.setContent(utils.getPluginhandle(), 'seasons')
    urlParams = {'action': 'episodes', 'id': str(id), 'language': params['language']}
    for i in sorted(map(int, data['seasons'].keys())):
        params['season'] = str(i)
        urlParams['season'] = str(i)
        o, media = createListItem(urlParams, params, data)
        o.setLabel('Season ' + str(i))
        xbmcplugin.addDirectoryItem(handle=utils.getPluginhandle(), url=getPluginUrl(urlParams), listitem=o, isFolder=True)


def episodes(params):
    if 'language' not in params:
        getParamsLanguage(params)
    xbmcplugin.setContent(utils.getPluginhandle(), 'episodes')
    id = int(params['id'])
    season = int(params.pop('season'))
    data = makeRequest('get', params, cache='short')
    seasons = {int(k):v for k, v in data['seasons'].items()}
    urlParams = {'action': 'get', 'id': str(id), 'language': params['language']}
    selected = None
    for i in sorted(map(int, seasons[season]['episodes'])):
        params['season'] = str(season)
        params['episode'] = str(i)
        urlParams['season'] = str(season)
        urlParams['episode'] = str(i)
        o, media = createListItem(urlParams, params, data, isPlayable=True)
        o.setLabel('Season ' + str(season) + ' Episode ' + str(i))
        if params.get('activateEpisode') == params['episode']:
            o.select(True)
            selected = o
        xbmcplugin.addDirectoryItem(handle=utils.getPluginhandle(), url=getPluginUrl(urlParams), listitem=o, isFolder=False)

    if selected:
        selected.select(True)
    return


def collectionEpisodes(params):
    xbmcplugin.setContent(utils.getPluginhandle(), 'episodes')
    result = makeRequest('collection/episodes', params)
    setLanguage = getLanguage(params)
    for data in result:
        params['season'] = data['episode']['season']
        params['episode'] = data['episode']['episode']
        if setLanguage == 'all':
            languages = (',').join(data['media']['languages'])
        else:
            languages = setLanguage
        urlParams = {'action': 'episodes', 'id': str(data['id']), 'languages': languages, 
           'season': str(params['season']), 
           'activateEpisode': str(params['episode'])}
        o, media = createListItem(urlParams, params, data)
        xbmcplugin.addDirectoryItem(handle=utils.getPluginhandle(), url=getPluginUrl(urlParams), listitem=o, isFolder=True)


RESOLUTION_GROUPS = {'hd': 'HD', 'original': 'Original', 
   'sd': ''}
RESOLUTION_PRIORITIES = [
 'hd',
 'original',
 'sd']
KODI_LANGUAGE_TRANSLATION = {'': 'none', 'ger': 'de', 
   'eng': 'en'}

class Player(xbmc.Player):
    pass


class get(object):

    def __init__(self, params):
        self.params = params
        self.selectedParts = {}
        self.db = None
        self.mirrorsTried = 0
        try:
            self.run()
        except Exception:
            import traceback
            traceback.print_exc()
            raise

        return

    def getDatabase(self):
        if not self.db:
            self.db = utils.Database(filename='vjackson.db')
            c = self.db.cursor()
            try:
                try:
                    c.execute('CREATE TABLE IF NOT EXISTS hoster_weights (hoster TEXT, t INTEGER)')
                    self.db.commit()
                except Exception:
                    import traceback
                    traceback.print_exc()

            finally:
                c.close()

        return self.db

    def getHosterWeights(self):
        weights = {}
        c = self.getDatabase().cursor()
        try:
            try:
                c.execute('DELETE FROM hoster_weights WHERE t<?', [int(time.time()) - 604800])
                c.execute('SELECT hoster, COUNT(*) FROM hoster_weights')
                self.getDatabase().commit()
                for hoster, weight in c:
                    if hoster:
                        weights[hoster] = weight

            except Exception:
                import traceback
                traceback.print_exc()

        finally:
            c.close()

        return weights

    def getStreamSelect(self):
        return getStreamSelect()

    def setSuccessfulConnection(self, hoster):
        c = self.getDatabase().cursor()
        try:
            try:
                c.execute('INSERT INTO hoster_weights (hoster, t) VALUES (?, ?)', [hoster, int(time.time())])
                self.getDatabase().commit()
            except Exception:
                import traceback
                traceback.print_exc()

        finally:
            c.close()

    def setVideoDetails(self, mirror, link, url):
        data = {'url': url, 'resolution': str(xbmc.getInfoLabel('VideoPlayer.VideoResolution')) + 'p', 
           'language': KODI_LANGUAGE_TRANSLATION.get(xbmc.getInfoLabel('VideoPlayer.AudioLanguage'), ''), 
           'subtitles': KODI_LANGUAGE_TRANSLATION.get(xbmc.getInfoLabel('VideoPlayer.SubtitlesLanguage'), '')}
        makeBackgroundRequest('link/info', data, cache=None)
        return

    def init(self):
        self.player = Player()
        self.player.stop()
        if not self.params.get('language'):
            getParamsLanguage(self.params)
        import dldb
        if dldb.downloadGet(self.params):
            return True
        self.data = makeRequest('get', self.params, cache='short')
        return False

    def allowMultiparts(self):
        return True

    def run(self):
        if self.init():
            return
        else:
            self.mirrors = self.data['get']['links']
            weights = self.getHosterWeights()
            SUPERWEIGHTS = {'clipboard.cc': 5, 'kinoger.com': 4, 
               'openload.co': 3, 
               'streamango.com': 2, 
               'streamcloud.eu': 1}
            self.groups = []
            groupsById = {}
            for i, mirror in enumerate(self.mirrors):
                if not self.allowMultiparts() and mirror['parts'] > 1:
                    continue
                resolution = RESOLUTION_GROUPS.get(mirror['resolution'], mirror['resolution'])
                mirror['caption'] = HOSTER_ALIASES.get(mirror['hoster'], mirror['hoster'])
                mirror['attrs'] = []
                if resolution:
                    mirror['attrs'].append(resolution)
                if mirror['parts'] > 1:
                    mirror['attrs'].append(str(mirror['parts']) + ' Parts')
                if mirror['attrs']:
                    mirror['caption'] += ' (%s)' % (', ').join(mirror['attrs'])
                mirror['weight'] = SUPERWEIGHTS.get(mirror['hoster'], 0) * 10000000 + mirror['quality'] * 10000 + weights.get(mirror['hoster'], 0) * 1
                print 'WEIGHT = %s /// %s %s %s /// %s %s' % (
                 mirror['weight'],
                 mirror['quality'],
                 SUPERWEIGHTS.get(mirror['hoster'], 0),
                 weights.get(mirror['hoster'], 0),
                 mirror['hoster'], mirror['resolution'])
                id = '%s-%s' % (resolution, mirror['parts'])
                mirror['groupId'] = id
                if id not in groupsById:
                    attrs = []
                    attrs.append(resolution or 'Stream')
                    if mirror['parts'] > 1:
                        attrs.append(str(mirror['parts']) + ' Parts')
                    group = {'caption': (', ').join(attrs), 'mirrors': []}
                    try:
                        priority = RESOLUTION_PRIORITIES.index(resolution.lower())
                    except ValueError:
                        priority = 999

                    group['priority'] = '%02i-%03i-%03i' % (mirror['parts'], priority, i)
                    self.groups.append(group)
                    groupsById[id] = group
                groupsById[id]['mirrors'].append(mirror)

            self.mirrors = []
            self.groups = list(sorted(self.groups, key=lambda x: x['priority']))
            for group in self.groups:
                n = len(group['mirrors'])
                if n == 1:
                    group['caption'] += ' (%s Mirror)' % n
                else:
                    group['caption'] += ' (%s Mirrors)' % n
                group['mirrors'] = list(sorted(group['mirrors'], key=lambda m: -m['weight']))
                self.mirrors.extend(group['mirrors'])

            getHosters(self.params)
            self.streamSelect = self.getStreamSelect()
            if self.streamSelect == 'grouped':
                heading = 'Qualit\xc3\xa4t w\xc3\xa4hlen'
                captions = [ mirror['caption'] for mirror in self.groups ]
            elif self.streamSelect == 'hosters':
                heading = 'Hoster w\xc3\xa4hlen'
                captions = [ mirror['caption'] for mirror in self.mirrors ]
            else:
                if self.streamSelect == 'hosters2':
                    heading = 'Hoster w\xc3\xa4hlen'
                    captions = []
                    for i, mirror in enumerate(self.mirrors):
                        attrs = [HOSTER_ALIASES_SHORT.get(mirror['hoster'], mirror['hoster'])]
                        attrs += mirror['attrs']
                        mirror['caption'] = 'Mirror %s (%s)' % (i + 1, (', ').join(attrs))
                        mirror['short_caption'] = 'Mirror %s (%s)' % (i + 1, HOSTER_ALIASES_SHORT.get(mirror['hoster'], mirror['hoster']))
                        captions.append(mirror['caption'])

                elif self.streamSelect != 'auto':
                    raise RuntimeError('Invalid value for streamSelect: %s' % self.streamSelect)
                if self.streamSelect != 'auto':
                    index = xbmcgui.Dialog().select(heading, captions)
                    if index < 0:
                        return
                else:
                    index = 0
                if self.streamSelect == 'grouped':
                    self.mirrors = self.groups[index]['mirrors']
                elif self.streamSelect == 'hosters':
                    mirror = self.mirrors[index]
                    group = groupsById[mirror['groupId']]
                    self.mirrors = group['mirrors'][group['mirrors'].index(mirror):]
                elif self.streamSelect == 'hosters2':
                    self.mirrors = self.mirrors[index:]
                if self.streamSelect in ('hosters', 'hosters2') and not getAutoTryNextStream():
                    self.mirrors = [self.mirrors[0]]
                from urlresolver import load_external_plugins
                from urlresolver.resolver import ResolverError
                load_external_plugins()
                try:
                    r = sys.modules['smoozed'].SmoozedResolver
                except Exception:
                    r = None

            if r is not None and not hasattr(r, '_isPatched'):
                r._isPatched = True

                class Dummy:

                    @classmethod
                    def get_setting(cls, key):
                        if key == 'enabled':
                            return 'true'
                        return '1'

                def get_media_url(self, *args, **kwargs):
                    try:
                        return self._old_get_media_url(*args, **kwargs)
                    except urllib2.HTTPError as e:
                        raise ResolverError('Resolve failed: %s' % e)
                    except Exception:
                        raise

                ignore_hosters = ('streamcloud', 'nowvideo', 'openload', 'streamango',
                                  'streamcherry', 'flashx')

                def valid_url(self, url, host):
                    if self._old_valid_url(url, host):
                        if any(x in host for x in ignore_hosters):
                            return False
                        if any(x in url for x in ignore_hosters):
                            return False
                        return True
                    return False

                def get_all_hosters(self, *args, **kwargs):
                    try:
                        content = utils.cache['medium'].get('smhoster')
                        if content:
                            return map(re.compile, json.loads(content))
                        content = self._old_get_all_hosters(*args, **kwargs)
                        utils.cache['medium'].set('smhoster', json.dumps(map(lambda x: x.pattern, content)))
                        return content
                    except Exception:
                        raise

                def get_hosts(self, *args, **kwargs):
                    try:
                        return self._old_get_hosts(*args, **kwargs)
                    except Exception:
                        raise

                r.get_setting = Dummy.get_setting
                r._old_get_media_url = r.get_media_url
                r._old_valid_url = r.valid_url
                r._old_get_all_hosters = r.get_all_hosters
                r._old_get_hosts = r.get_hosts
                r.get_media_url = get_media_url
                r.valid_url = valid_url
                r.get_all_hosters = get_all_hosters
                r.get_hosts = get_hosts

            def rb2_get_media_url(self, host, media_id):
                if 'WEBSOCKET_CLIENT_CA_BUNDLE' not in os.environ:
                    from requests import certs
                    os.environ['WEBSOCKET_CLIENT_CA_BUNDLE'] = certs.where()
                import rb2
                from urlresolver.plugins.lib.helpers import pick_source
                result = rb2.resolve('wss://vjackson.info/rb2/', self.get_url(host, media_id), request_timeout=30)
                opts = '|' + ('&').join([ key + '=' + urllib2.quote(value) for key, value in result['headers'].items() ])
                return pick_source([ (x.get('quality', ''), x['url'] + opts) for x in result['urls'] ])

            def rb2_patch(name, classname):
                if name in sys.modules:
                    r = getattr(sys.modules[name], classname)
                    if not hasattr(r, '_isPatched'):
                        r._isPatched = True
                        r.get_media_url = rb2_get_media_url

            if False and 'openload' in sys.modules:
                r = sys.modules['openload'].OpenLoadResolver
                if not hasattr(r, '_isPatched'):
                    r._isPatched = True

                    def new_get_media_url(self, host, media_id):
                        import requests
                        session = requests.session()
                        t = session.get('https://api.openload.co/1/file/dlticket', params={'file': media_id, 'login': 'c255c81fad52a08f', 'key': 'lc7xiQ46'}).json()['result']['ticket']
                        return session.get('https://api.openload.co/1/file/dl', params={'file': media_id, 'ticket': t}).json()['result']['url']

                    r.get_media_url = new_get_media_url
            rb2_patch('streamcherry', 'StreamcherryResolver')
            rb2_patch('streamango', 'StreamangoResolver')
            rb2_patch('openload', 'OpenLoadResolver')
            self.initProgress()
            try:
                try:
                    self.findMirror()
                except ValueError as e:
                    if e.message == 'CANCELED':
                        return
                    if e.message == 'FAILED':
                        self.showFailedNotification()
                        return
                    raise

            finally:
                if self.progress is not None:
                    self.progress.close()
                    self.progress = None

            return
            return

    def showFailedNotification(self):
        xbmc.executebuiltin('Notification(%s,%s,%s,%s)' % (
         'VAVOO.TO',
         'Beim aufrufen des Streams ist ein Fehler aufgetreten',
         5000,
         utils.addon.getAddonInfo('icon')))

    def initProgress(self):
        self.progress = xbmcgui.DialogProgress()
        self.progress.create('NAHRO.TV', u'Der Stream wird gestartet...')

    def checkCanceled(self):
        if self.progress.iscanceled():
            raise ValueError('CANCELED')

    def getMirrorPart(self, mirror, link):
        availableParts = tuple(sorted(map(int, link['parts'].keys())))
        if len(availableParts) > 1:
            captions = []
            parts = []
            urls = []
            for p, url in sorted(map(lambda x: (int(x[0]), x[1]), link['parts'].items())):
                captions.append('Part %s' % p)
                parts.append(p)
                urls.append(url)

            partIndex = self.selectedParts.get(availableParts, None)
            if partIndex is None:
                partIndex = xbmcgui.Dialog().select('Part f\xc3\xbcr einen %s-teiligen Mirror w\xc3\xa4hlen' % mirror['parts'], captions)
                if partIndex < 0:
                    raise ValueError('CANCELED')
                self.selectedParts[availableParts] = partIndex
        else:
            parts = link['parts'].keys()
            urls = link['parts'].values()
            partIndex = 0
        try:
            part = parts[partIndex]
            url = urls[partIndex]
        except Exception:
            part = None
            url = None

        return (
         part, url)

    def setMirrorProgress(self, step, *args, **kwargs):
        STEPS_PER_MIRROR = 5
        current = step
        total = STEPS_PER_MIRROR
        self.progress.update(int(current * (100.0 / total)), *args, **kwargs)
        self.checkCanceled()

    def findMirror(self):
        prevMirror = None
        for self.mirrorIndex, mirror in enumerate(self.mirrors):
            if self.mirrorIndex == 0:
                lines = (
                 'Die Wiedergabe wird gestartet.',
                 mirror.get('short_caption', mirror['caption']))
            else:
                lines = (
                 '%s fehlgeschlagen.' % prevMirror.get('short_caption', mirror['caption']),
                 'Versuche %s...' % mirror.get('short_caption', mirror['caption']))
            self.setMirrorProgress(0, *lines)
            prevMirror = mirror
            params = dict(self.params)
            params.update(mirror)
            link = makeRequest('link', params, cache=None)
            self.setMirrorProgress(1)
            if not link:
                print 'Empty link returned'
                continue
            part, url = self.getMirrorPart(mirror, link)
            self.checkCanceled()
            if url is None:
                continue
            resolvedUrl = self.resolveUrl(mirror, link, url)
            if not resolvedUrl:
                continue
            self.setMirrorProgress(2)
            if self.tryMirror(mirror, link, part, url, resolvedUrl):
                return

        raise ValueError('FAILED')
        return

    def resolveUrl(self, mirror, link, url):
        print 'Resolving URL: %s' % url
        cacheKey = url
        originalUrl = url
        if mirror['hoster'] in URLRESOLVER_SET_QUALITY:
            urlresolverAddon = xbmcaddon.Addon('script.module.urlresolver')
            key = '%s_quality' % URLRESOLVER_SET_QUALITY[mirror['hoster']]
            value = utils.addon.getSetting('playback_resolution')
            cacheKey += '///' + value
            if urlresolverAddon.getSetting(key) != value:
                urlresolverAddon.setSetting(key, value)
        cachedUrl = None
        if cachedUrl:
            print 'Got resolved URL from cache: %s' % cachedUrl
            return cachedUrl
        else:
            url = self.resolveUrl1(link, originalUrl)
            if url:
                utils.cache['short'].set(cacheKey, url)
                return url
            if url is False:
                print 'Reporting not working URL: %s' % url
                makeBackgroundRequest('link/offline', {'url': originalUrl}, cache=None)
            return
            return

    def resolveUrl1(self, link, url):
        xbmc.log('Resolving URL 1: %s' % url, xbmc.LOGDEBUG)
        try:
            from urlresolver import resolve
            from urlresolver.resolver import ResolverError
            return resolve(url)
        except ResolverError:
            import traceback
            traceback.print_exc()
            return
        except Exception as e:
            import traceback
            traceback.print_exc()
            reporterrorBackground(utils.addonID, e, {'function': 'urlresolver', 'link': link, 'url': url})
            return

    def tryMirror(self, mirror, link, part, url, resolvedUrl):
        print 'Trying resolved URL: %s' % resolvedUrl
        try:
            if '|' not in resolvedUrl:
                resolvedUrl += '|'
            if '&User-Agent' not in resolvedUrl:
                resolvedUrl += '&User-Agent=' + urllib2.quote('Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            resolvedUrl += '&VAVOOTOREPORT=' + urllib2.quote('?' + convertPluginParams({'id': self.data['id'], 'type': self.data['type'], 
               'language': self.params['language'], 
               'season': str(self.params.get('season', -1)), 
               'episode': str(self.params.get('episode', -1)), 
               'part': part, 
               'url': url}))
            if mirror['parts'] > 1:
                resolvedUrl += '&VAVOOTOMULTIPART'
            o, media = createListItem(self.params, self.params, self.data, isPlayable=True)
            o.setPath(resolvedUrl)
            self.player.play(resolvedUrl, o)
            self.mirrorsTried += 1

            def infostr():
                try:
                    return 'step=%s, playing=%s, time=%s URL: %s' % (
                     step, self.player.isPlaying(),
                     self.player.isPlaying() and self.player.getTime(),
                     urlparse.urlparse(resolvedUrl).netloc)
                except RuntimeError as e:
                    if e.message == 'XBMC is not playing any media file':
                        return 'XBMC is not playing any media file'
                    raise

            step = 1
            STEP_TIMEOUT = 45
            abortReason = ''
            t = time.time()
            try:
                sleep = 10
                while not abortReason:
                    print 'Player running: %s' % infostr()
                    if xbmc.abortRequested or self.progress and self.progress.iscanceled():
                        abortReason = 'canceled'
                    elif step == 1:
                        if self.player.isPlaying():
                            self.setMirrorProgress(3)
                            step = 2
                        elif time.time() - t > STEP_TIMEOUT:
                            abortReason = 'timeout'
                    elif step == 2:
                        if xbmc.getInfoLabel('VideoPlayer.VideoResolution'):
                            self.setMirrorProgress(3, line3='Viel Spa\xc3\x9f mit VAVOO!')
                            self.player.stop()
                            sleep = 100
                            step = 3
                        elif not self.player.isPlaying():
                            abortReason = 'died'
                    elif step == 3:
                        if not self.player.isPlaying():
                            xbmcplugin.setResolvedUrl(utils.getPluginhandle(), True, o)
                            t = time.time()
                            step = 4
                    elif step == 4:
                        if self.player.isPlaying():
                            self.setMirrorProgress(4)
                            step = 5
                        elif time.time() - t > STEP_TIMEOUT:
                            abortReason = 'timeout'
                    elif step == 5:
                        if not self.player.isPlaying():
                            abortReason = 'stopped'
                        elif self.player.getTime() > 0.0:
                            resolution = xbmc.getInfoLabel('VideoPlayer.VideoResolution')
                            if resolution:
                                self.setVideoDetails(mirror, link, url)
                                self.setSuccessfulConnection(mirror['hoster'])
                                if self.progress is not None:
                                    self.progress.close()
                                    self.progress = None
                                sleep = 1000
                                step = 6
                    elif step == 6:
                        if not self.player.isPlaying():
                            abortReason = 'stopped'
                    else:
                        raise RuntimeError('Unknow step: %r' % step)
                    if not abortReason:
                        xbmc.sleep(sleep)

                print 'Player stopped: reason=%s, %s' % (abortReason, infostr())
            finally:
                self.player.stop()

            if abortReason in ('canceled', 'stopped'):
                return True
            if step >= 4:
                raise RuntimeError('Stream died! reason=%s, %s' % (abortReason, infostr()))
            return False
        except Exception as e:
            import traceback
            traceback.print_exc()
            reporterrorBackground(utils.addonID, e, {'function': 'player', 'link': link, 'url': url})
            return False

        return


REPORT_INFO_LABELS = (
 'Player.FinishTime',
 'Player.FinishTime',
 'Player.Chapter',
 'Player.ChapterCount',
 'Player.Time',
 'Player.Time',
 'Player.TimeRemaining',
 'Player.TimeRemaining',
 'Player.Duration',
 'Player.Duration',
 'Player.SeekTime',
 'Player.SeekOffset',
 'Player.SeekOffset',
 'Player.SeekStepSize',
 'Player.ProgressCache',
 'Player.Folderpath',
 'Player.Filenameandpath',
 'Player.StartTime',
 'Player.StartTime',
 'Player.Title',
 'Player.Filename',
 'Player.Process',
 'Player.Process',
 'Player.Process',
 'Player.Process',
 'Player.Process',
 'Player.Process',
 'Player.Process',
 'Player.Process',
 'Player.Process',
 'Player.Process',
 'Player.Process',
 'MusicPlayer.Title',
 'MusicPlayer.Album',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Artist',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Genre',
 'MusicPlayer.Lyrics',
 'MusicPlayer.Year',
 'MusicPlayer.Rating',
 'MusicPlayer.DiscNumber',
 'MusicPlayer.Comment',
 'MusicPlayer.Time',
 'MusicPlayer.TimeRemaining',
 'MusicPlayer.TimeSpeed',
 'MusicPlayer.TrackNumber',
 'MusicPlayer.Duration',
 'MusicPlayer.BitRate',
 'MusicPlayer.Channels',
 'MusicPlayer.BitsPerSample',
 'MusicPlayer.SampleRate',
 'MusicPlayer.Codec',
 'MusicPlayer.PlaylistPosition',
 'MusicPlayer.PlaylistLength',
 'MusicPlayer.ChannelName',
 'MusicPlayer.ChannelNumber',
 'MusicPlayer.SubChannelNumber',
 'MusicPlayer.ChannelNumberLabel',
 'MusicPlayer.ChannelGroup',
 'MusicPlayer.Contributors',
 'MusicPlayer.ContributorAndRole',
 'MusicPlayer.Mood',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.Property',
 'MusicPlayer.UserRating',
 'MusicPlayer.DBID',
 'VideoPlayer.Time',
 'VideoPlayer.TimeRemaining',
 'VideoPlayer.TimeSpeed',
 'VideoPlayer.Duration',
 'VideoPlayer.Title',
 'VideoPlayer.TVShowTitle',
 'VideoPlayer.Season',
 'VideoPlayer.Episode',
 'VideoPlayer.Genre',
 'VideoPlayer.Director',
 'VideoPlayer.Country',
 'VideoPlayer.Year',
 'VideoPlayer.Rating',
 'VideoPlayer.UserRating',
 'VideoPlayer.Votes',
 'VideoPlayer.RatingAndVotes',
 'VideoPlayer.mpaa',
 'VideoPlayer.IMDBNumber',
 'VideoPlayer.EpisodeName',
 'VideoPlayer.PlaylistPosition',
 'VideoPlayer.PlaylistLength',
 'VideoPlayer.Cast',
 'VideoPlayer.CastAndRole',
 'VideoPlayer.Album',
 'VideoPlayer.Artist',
 'VideoPlayer.Studio',
 'VideoPlayer.Writer',
 'VideoPlayer.Tagline',
 'VideoPlayer.PlotOutline',
 'VideoPlayer.Plot',
 'VideoPlayer.LastPlayed',
 'VideoPlayer.PlayCount',
 'VideoPlayer.VideoCodec',
 'VideoPlayer.VideoResolution',
 'VideoPlayer.VideoAspect',
 'VideoPlayer.AudioCodec',
 'VideoPlayer.AudioChannels',
 'VideoPlayer.AudioLanguage',
 'VideoPlayer.SubtitlesLanguage',
 'VideoPlayer.StereoscopicMode',
 'VideoPlayer.EndTime',
 'VideoPlayer.NextTitle',
 'VideoPlayer.NextGenre',
 'VideoPlayer.NextPlot',
 'VideoPlayer.NextPlotOutline',
 'VideoPlayer.NextStartTime',
 'VideoPlayer.NextEndTime',
 'VideoPlayer.NextDuration',
 'VideoPlayer.ChannelName',
 'VideoPlayer.ChannelNumber',
 'VideoPlayer.SubChannelNumber',
 'VideoPlayer.ChannelNumberLabel',
 'VideoPlayer.ChannelGroup',
 'VideoPlayer.ParentalRating',
 'VideoPlayer.DBID')
REPORT_PLAYER_LABELS = (
 'getAvailableAudioStreams',
 'getAvailableSubtitleStreams',
 'getPlayingFile',
 'getSubtitles',
 'getTime',
 'getTotalTime')

def captureScreenshot():
    capture = xbmc.RenderCapture()
    capture.capture(int(xbmc.getInfoLabel('System.ScreenWidth')), int(xbmc.getInfoLabel('System.ScreenHeight')))
    pixels = capture.getImage(1000)
    format = capture.getImageFormat()
    width, height = capture.getWidth(), capture.getHeight()
    del capture
    from PIL import Image
    from io import BytesIO
    fp = BytesIO()
    img = Image.frombuffer('RGBA', (width, height), bytes(pixels), 'raw', format)
    img.save(fp, 'jpeg')
    del img
    del pixels
    size = fp.tell()
    fp.seek(0)
    return (
     (
      width, height), size, fp)


def report(params):
    incident = params['incident']
    filenameandpath = params['filenameandpath']
    params = re.search('VAVOOTOREPORT=[^\\&\\|\\?]+', filenameandpath).group(0)
    params = urlparse.parse_qs(params)
    params = convertUrlParameter(params['VAVOOTOREPORT'][0])
    params['incident'] = incident
    wasPlaying = xbmc.getInfoLabel('Player.Playing')
    player = Player()
    progress = xbmcgui.DialogProgress()
    try:
        progress.create('NAHRO.TV', u'Deine Anfrage wird bearbeitet.')
        params['meta'] = {}
        for key in REPORT_INFO_LABELS:
            params['meta'][key] = xbmc.getInfoLabel(key)

        for key in REPORT_PLAYER_LABELS:
            params['meta']['player().' + key] = getattr(player, key)()

        print params['meta']
        screens = []

        def addScreen(player, progress, p):
            if REPORT_CAPTURE_SCREENSHOTS:
                t = player.getTime()
                print '=========== TIME = %r' % t
                if screens and int(screens[(-1)][0]) == int(t):
                    return False
                screens.append((t, captureScreenshot()))
                return True
            progress.update(p)

        addScreen(player, progress, 5)
        if incident == 'ask':
            question = 'Was f\xc3\xbcr ein Problem m\xc3\xb6chtest du melden?'
            options = []
            options.append(('incomplete_link', 'Stream ist nicht vollst\xc3\xa4ndig'))
            if 'VAVOOTOMULTIPART' in filenameandpath:
                options.append(('invalid_part', 'Stream ist nicht vollst\xc3\xa4ndig'))
            options.append(('invalid_language', 'Falsche Sprache'))
            options.append(('invalid_subtitles', 'Sprache von Untertiteln festlegen'))
            if params['type'] == 'movie':
                options.append(('invalid_item', 'Falscher Film'))
            else:
                options.append(('invalid_item', 'Falsche Serie'))
                options.append(('invalid_season', 'Falsche Staffel'))
                options.append(('invalid_episode', 'Falsche Episode'))
            index = xbmcgui.Dialog().select(question, map(lambda x: x[1], options))
            if index == -1:
                return
            incident = options[index][0]
            params['incident'] = incident
        if incident == 'incomplete_link':
            result = xbmcgui.Dialog().yesno('Stream ist nicht vollst\xc3\xa4ndig', 'Zeigt der Stream nicht die richtige Laufzeit an, handlet sich hierbei nur um einen Trailer oder kurzen Ausschnitt des Films?')
            if not result:
                return
        elif incident == 'invalid_part':
            result = xbmcgui.Dialog().yesno('Part ist nicht korrekt', 'Es gibt hier nur einen Part und die restlichen Parts sind \xc3\xbcberfl\xc3\xbcssig, oder es handelt sich hierbei um einen anderen Part?')
            if not result:
                return
        elif incident == 'invalid_language':
            question = 'Welche Sprache wird gesprochen?'
            options = LANGUAGE_NAMES[getLocale(params)].items()
            options = list(sorted(options, key=lambda x: x[1]))
            options = [('unknown', 'Wei\xc3\x9f ich nicht')] + options
            options = options + [('other', 'Eine Andere')]
            index = xbmcgui.Dialog().select(question, map(lambda x: x[1], options))
            if index == -1:
                return
            params['proposal'] = {'language': options[index][0]}
        elif incident == 'invalid_subtitles':
            question = 'In welcher Sprache sind die Untertitel?'
            options = LANGUAGE_NAMES[getLocale(params)].items()
            options = list(sorted(options, key=lambda x: x[1]))
            options = [('none', 'Es sind keine Untertitel vorhanden'), ('unknown', 'Wei\xc3\x9f ich nicht')] + options
            options = options + [('other', 'Eine Andere')]
            index = xbmcgui.Dialog().select(question, map(lambda x: x[1], options))
            if index == -1:
                return
            params['proposal'] = {'subtitles': options[index][0]}
        elif incident == 'invalid_item':
            options = []
            if params['type'] == 'movie':
                question = 'Was stimmt mit diesem Film nicht?'
                options.append(('year', 'Ist aus einem anderen Jahr, aber mit selben Namen'))
                options.append(('part', 'Ist ein anderer Teil eines mehrteiligen Films'))
                options.append(('name', 'Hat einen ganz anderen Titel'))
            else:
                question = 'Was stimmt mit dieser Serie nicht?'
                options.append(('year', 'Ist aus einem anderen Jahr, aber mit selben Namen'))
                options.append(('name', 'Hat einen ganz anderen Titel'))
            index = xbmcgui.Dialog().select(question, map(lambda x: x[1], options))
            if index == -1:
                return
            params['proposal'] = {'change': options[index][0]}
        elif incident == 'invalid_episode':
            result = xbmcgui.Dialog().yesno('Episode nicht korrekt', 'M\xc3\xb6chtest du jetzt die richtige Episode angeben?')
            addScreen(player, progress, 10)
            if result:
                question = 'Episode'
                episode = xbmcgui.Dialog().input(question, type=xbmcgui.INPUT_NUMERIC)
                if not episode:
                    return
                episode = int(episode)
                params['proposal'] = {'episode': episode}
        elif incident == 'invalid_season':
            result = xbmcgui.Dialog().yesno('Staffel nicht korrekt', 'M\xc3\xb6chtest du jetzt die richtige Staffel und Episode angeben?')
            addScreen(player, progress, 10)
            if result:
                question = 'Staffel'
                season = xbmcgui.Dialog().input(question, type=xbmcgui.INPUT_NUMERIC)
                if not season:
                    return
                addScreen(player, progress, 15)
                season = int(season)
                if season > 0:
                    question = 'Episode'
                    episode = xbmcgui.Dialog().input(question, type=xbmcgui.INPUT_NUMERIC)
                    if not episode:
                        return
                    episode = int(episode)
                else:
                    episode = 0
                params['proposal'] = {'season': season, 'episode': episode}
        else:
            raise ValueError('Unknown incident: %s' % incident)
        addScreen(player, progress, 30)
        if REPORT_CAPTURE_SCREENSHOTS:
            if not wasPlaying:
                xbmc.executebuiltin('PlayerControl(resume)')
            MAX_FRAMES = 10
            MAX_WAIT_TIME = 20
            step = float(50) / MAX_FRAMES
            t = time.time()
            totalTime = player.getTotalTime()
            while len(screens) < MAX_FRAMES and time.time() - t < MAX_WAIT_TIME and player.getTime() < totalTime:
                addScreen(player)
                s = len(screens) * step
                p = float(time.time() - t) / MAX_WAIT_TIME * step
                progress.update(int(30 + s + p))
                xbmc.sleep(500)

            progress.update(80)
            files = []
            params['files'] = []
            for i, (t, ((width, height), size, fp)) in enumerate(screens):
                files.append({'image' + str(i): (str(i) + '.jpg', fp, 'image/jpeg')})
                params['files'].append((i, 'image', t, (width, height), size))

        else:
            files = None
        params['proposal'] = json.dumps(params.get('proposal', {}))
        data = makeRequest('report', data=params, files=files, cache=None)
        print 'Report respone = %s' % data
        progress.update(90)
        xbmcgui.Dialog().ok('Der Fehler wurde gemeldet', 'Nur durch die Hilfe der Community k\xc3\xb6nnen wir es schaffen unser Archiv sauber und fehlerfrei zu halten.', 'Wir danken dir f\xc3\xbcr deinen Beitrag!')
    finally:
        del player
        if not wasPlaying:
            xbmc.executebuiltin('PlayerControl(pause)')
        progress.close()
        xbmc.executebuiltin('Dialog.Close(all,true)')

    return


def convertUrlParameter(param):
    param = param.split('?', 1)[1]
    params = urlparse.parse_qs(param)
    params = {key:value[0] if len(value) == 1 else value for key, value in params.items()}
    return params


def convertPluginParams(params):
    p = []
    for key, value in params.items():
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        p.append(urllib.urlencode({key: value}))

    return ('&').join(sorted(p))


def getPluginUrl(params):
    return 'plugin://' + utils.addonID + '/?' + convertPluginParams(params)


def addDir(name, url, iconimage='DefaultFolder.png', isFolder=True, isPlayable=False):
    liz = xbmcgui.ListItem(name, iconImage='DefaultFolder.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title': name})
    if isPlayable:
        liz.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(handle=utils.getPluginhandle(), url=url, listitem=liz, isFolder=isFolder)


def addDir2(name_, icon_, action, **params):
    params['action'] = action
    addDir(name_, getPluginUrl(params), getIcon(icon_))


def getIcon(name):
    return xbmc.translatePath('special://home/addons/' + utils.addonID + '/resources/' + name + '.png').decode('utf-8')


def getProfilePath():
    profilePath = xbmc.translatePath(utils.addon.getAddonInfo('profile')).decode('utf-8')
    if not os.path.exists(profilePath):
        os.makedirs(profilePath)
    return profilePath


class JT(threading.Thread):

    def run(self):
        try:
            data = makeRequest('job/get', {'v': 2}, cache=None)
            if 'function' in data:
                result = getattr(self, 'fn_' + data['function'])(data)
                if result:
                    try:
                        makeRequest('job/result', {}, data=json.dumps({'id': data['id'], 'result': result}))
                    except Exception as e:
                        xbmc.log('Failed reporting job: %s' % e)

        except Exception as e:
            xbmc.log('Failed handling job: %s' % e)

        return

    def fn_get(self, data):
        import requests
        session = requests.session()
        result = {}
        for id, request in sorted(data['requests'].items()):
            try:
                resp = session.request(**request)
            except Exception as e:
                result[id] = {'error': str(e)}
            else:
                result[id] = {'url': resp.url, 'status_code': resp.status_code, 
                   'headers': dict(resp.headers), 
                   'content': resp.content}

        return result

    def fn_x(self, data):
        import requests
        session = requests.session()
        resp = session.request(**data['request'])
        m = re.search('<div class="tv-play" data-src="(.*)', resp.content)
        baseurl = m.group(1)
        m = re.search('token=(.*)', baseurl)
        token = m.group(1)
        self.handle_m3u(session, data, urlparse.urljoin(baseurl, 'index.m3u8?token=' + token))

    def handle_m3u(self, session, data, url):
        ts = time.time()
        while time.time() - ts < '10000':
            data['request']['url'] = url
            resp = session.request(**data['request'])
            for line in resp.content.splitlines():
                line = line.split('#')[0].strip()
                if not line:
                    continue
                url2 = urlparse.urljoin(url, line)
                if '.m3u' in url2:
                    self.handle_m3u(session, data, url2)
                    return
                data['request']['url'] = url2
                resp = session.request(stream=True, **data['request'])
                t, s = time.time(), 10000
                x = int(time.time())
                for chunk in resp.iter_content(65536):
                    s += len(chunk)
                    speed = s / (time.time() - t)
                    if x != int(time.time()):
                        x = int(time.time())
                    diff = speed - data['speed']
                    if diff > 0:
                        time.sleep(1)
                    if time.time() - ts > data['timeout']:
                        return


def init():
    if time.time() - int(utils.addon.getSetting('j') or 0) > 1000000:
        utils.addon.setSetting('j', str(int(time.time())))
        JT().start()


def whatsapp():
    return
    if not xbmc.getCondVisibility('system.platform.android'):
        return
    n = int(utils.addon.getSetting('whatsapp3') or 0) + 1
    utils.addon.setSetting('whatsapp3', str(n))
    if n != 12:
        return
    import subprocess
    try:
        hasWhatsapp = subprocess.check_output(['cmd', 'package', 'list', 'packages', '-i', 'com.whatsapp'])
    except OSError:
        try:
            hasWhatsapp = subprocess.check_output(['pm', 'list', 'packages', '-i', 'com.whatsapp'])
        except OSError:
            hasWhatsapp = ''

    if 'com.whatsapp' not in hasWhatsapp:
        return
    window = xbmcgui.WindowXML('custom-Whatsapp.xml', xbmcaddon.Addon().getAddonInfo('path').decode('utf-8'), 'default', '720p')
    window.doModal()
    del window


def getAuthSignature():
#    signfile = get_cache('signfile')
#	if signfile:
#		return signfile
	vec = {"vec": "9frjpxPjxSNilxJPCJ0XGYs6scej3dW/h/VWlnKUiLSG8IP7mfyDU7NirOlld+VtCKGj03XjetfliDMhIev7wcARo+YTU8KPFuVQP9E2DVXzY2BFo1NhE6qEmPfNDnm74eyl/7iFJ0EETm6XbYyz8IKBkAqPN/Spp3PZ2ulKg3QBSDxcVN4R5zRn7OsgLJ2CNTuWkd/h451lDCp+TtTuvnAEhcQckdsydFhTZCK5IiWrrTIC/d4qDXEd+GtOP4hPdoIuCaNzYfX3lLCwFENC6RZoTBYLrcKVVgbqyQZ7DnLqfLqvf3z0FVUWx9H21liGFpByzdnoxyFkue3NzrFtkRL37xkx9ITucepSYKzUVEfyBh+/3mtzKY26VIRkJFkpf8KVcCRNrTRQn47Wuq4gC7sSwT7eHCAydKSACcUMMdpPSvbvfOmIqeBNA83osX8FPFYUMZsjvYNEE3arbFiGsQlggBKgg1V3oN+5ni3Vjc5InHg/xv476LHDFnNdAJx448ph3DoAiJjr2g4ZTNynfSxdzA68qSuJY8UjyzgDjG0RIMv2h7DlQNjkAXv4k1BrPpfOiOqH67yIarNmkPIwrIV+W9TTV/yRyE1LEgOr4DK8uW2AUtHOPA2gn6P5sgFyi68w55MZBPepddfYTQ+E1N6R/hWnMYPt/i0xSUeMPekX47iucfpFBEv9Uh9zdGiEB+0P3LVMP+q+pbBU4o1NkKyY1V8wH1Wilr0a+q87kEnQ1LWYMMBhaP9yFseGSbYwdeLsX9uR1uPaN+u4woO2g8sw9Y5ze5XMgOVpFCZaut02I5k0U4WPyN5adQjG8sAzxsI3KsV04DEVymj224iqg2Lzz53Xz9yEy+7/85ILQpJ6llCyqpHLFyHq/kJxYPhDUF755WaHJEaFRPxUqbparNX+mCE9Xzy7Q/KTgAPiRS41FHXXv+7XSPp4cy9jli0BVnYf13Xsp28OGs/D8Nl3NgEn3/eUcMN80JRdsOrV62fnBVMBNf36+LbISdvsFAFr0xyuPGmlIETcFyxJkrGZnhHAxwzsvZ+Uwf8lffBfZFPRrNv+tgeeLpatVcHLHZGeTgWWml6tIHwWUqv2TVJeMkAEL5PPS4Gtbscau5HM+FEjtGS+KClfX1CNKvgYJl7mLDEf5ZYQv5kHaoQ6RcPaR6vUNn02zpq5/X3EPIgUKF0r/0ctmoT84B2J1BKfCbctdFY9br7JSJ6DvUxyde68jB+Il6qNcQwTFj4cNErk4x719Y42NoAnnQYC2/qfL/gAhJl8TKMvBt3Bno+va8ve8E0z8yEuMLUqe8OXLce6nCa+L5LYK1aBdb60BYbMeWk1qmG6Nk9OnYLhzDyrd9iHDd7X95OM6X5wiMVZRn5ebw4askTTc50xmrg4eic2U1w1JpSEjdH/u/hXrWKSMWAxaj34uQnMuWxPZEXoVxzGyuUbroXRfkhzpqmqqqOcypjsWPdq5BOUGL/Riwjm6yMI0x9kbO8+VoQ6RYfjAbxNriZ1cQ+AW1fqEgnRWXmjt4Z1M0ygUBi8w71bDML1YG6UHeC2cJ2CCCxSrfycKQhpSdI1QIuwd2eyIpd4LgwrMiY3xNWreAF+qobNxvE7ypKTISNrz0iYIhU0aKNlcGwYd0FXIRfKVBzSBe4MRK2pGLDNO6ytoHxvJweZ8h1XG8RWc4aB5gTnB7Tjiqym4b64lRdj1DPHJnzD4aqRixpXhzYzWVDN2kONCR5i2quYbnVFN4sSfLiKeOwKX4JdmzpYixNZXjLkG14seS6KR0Wl8Itp5IMIWFpnNokjRH76RYRZAcx0jP0V5/GfNNTi5QsEU98en0SiXHQGXnROiHpRUDXTl8FmJORjwXc0AjrEMuQ2FDJDmAIlKUSLhjbIiKw3iaqp5TVyXuz0ZMYBhnqhcwqULqtFSuIKpaW8FgF8QJfP2frADf4kKZG1bQ99MrRrb2A="}
	url = 'https://www.vavoo.tv/api/box/ping2'
	import requests
	req = requests.post(url, data=vec).json()
	signed = req['response'].get('signed')
#	set_cache('signfile', signed)
	return signed


SESSION = None

def getSession():
    if SESSION is None:
        import requests
        globals()['SESSION'] = requests.session()
    return SESSION


def reporterrorBackground(*args, **kwargs):
    kwargs['exc_info'] = sys.exc_info()

    class Thread(threading.Thread):

        def run(self):
            import reporterror
            reporterror.report(*args, **kwargs)

    Thread().start()


def makeBackgroundRequest(*args, **kwargs):

    class Thread(threading.Thread):

        def run(self):
            makeRequest(*args, **kwargs)

    Thread().start()


def makeRequest(*args, **kwargs):
    data = _makeRequest(*args, **kwargs)
    if isinstance(data, dict):
        if data.get('error'):
            if str(data['error']).lower() == 'incompatible':
                xbmcgui.Dialog().ok('VAVOO Version in\xc2\xadkom\xc2\xadpa\xc2\xadti\xc2\xadbel', 'Bitte deinstalliere diese Version und lade die aktuelle kostenlose VAVOO App von der Webseite unter www.vavoo.tv/software oder \xc3\xbcber den Google PlayStore herunter.')
            raise ValueError(data('timeout'))
    return data


def _makeRequest(function, params, data=None, files=None, addLanguage=True, add_locale=True, addHosters=True, addResolution=True, cache='medium'):
    t = time.time()
    params = dict(params)
    params.pop('action', None)
    if addLanguage:
        params['language'] = getLanguage(params)
    if add_locale and 'locale' not in params:
        params['locale'] = getLocale(params)
    if addHosters and 'hosters' not in params:
        params['hosters'] = getHosters(params)
    if addResolution and 'resolution' not in params:
        params['resolutions'] = getResolution(params)
#    params['vavoo_auth'] = getAuthSignature()
    print 'Request: %s / %s' % (function, json.dumps(params))
    if USE_CACHE and cache:
        if files:
            raise RuntimeError('File upload and cache is invalid')
        cacheKey = function + '?' + ('&').join([ str(key) + '=' + str(value) for key, value in sorted(params.items()) ])
        cacheKey = 'vjackson/' + str(hash(cacheKey))
        content = utils.cache[cache].get(cacheKey)
        if content:
            return json.loads(content)
    if data is None and files is None:
        response = getSession().get(BASEURL + function, params=params)
    else:
        response = getSession().post(BASEURL + function, params=params, data=data, files=files)
    content = response.content
    print 'Request time: %s' % (time.time() - t) + ', content lenth: %s' % len(content)
    try:
        result = json.loads(content)
    except Exception:
        print repr(content)
        raise

    if USE_CACHE and cache and response.status_code in (200, 201, 301, 302):
        utils.cache[cache].set(cacheKey, content)
    return result


init()