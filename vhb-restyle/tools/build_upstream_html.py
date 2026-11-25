#!/usr/bin/env python3
"""Packs a built copy of current Streetmix into one HTML file that runs with no server.

  python3 build_upstream_html.py <streetmix checkout with build/> <capture.json> <out.html>

capture.json is a recording of the requests the app makes while loading a new street (see capture.js). The page
inlines the app's own JavaScript and CSS, replays the recorded responses, and accepts saves without storing them."""
import base64, json, mimetypes, os, re, sys

ROOT, CAPTURE, OUT = sys.argv[1:4]
cap = json.load(open(CAPTURE)); build = ROOT + '/build'
recs = [r for r in cap['recs'] if 'path' in r and r.get('body')]
shell = base64.b64decode(next(r['body'] for r in recs if r['path'] == '/new')).decode()
css_path = re.search(r'href="(/assets/main\.[^"]+\.css)"', shell).group(1); js_path = re.search(r'src="(/assets/main\.[^"]+\.js)"', shell).group(1)
css = open(build + '/main.css').read(); js = open(build + '/main.js').read()


def data_uri(path):
    mime = mimetypes.guess_type(path)[0] or 'application/octet-stream'
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()


def css_url(m):
    name = m.group(1).strip('\'"')
    p = f'{build}/{name}'
    if name.startswith('data:') or not os.path.exists(p): return m.group(0)
    if name.endswith('.woff2') and '-latin-wght-normal' not in name: return 'url(data:,)'      # skip scripts the demo never shows
    return f'url({data_uri(p)})'


css = re.sub(r'url\(([^)]+)\)', css_url, css)
assert 'new URL(window.location.href)' in js
js = js.replace('new URL(window.location.href)', 'new URL(window.__smx.href())')
js = js.replace('</script', '<\\/script')

store = {}
for r in recs:
    if r['path'] in ('/new', css_path, js_path): continue
    key = r['method'] + ' ' + re.sub(r'^/api/v1/streets/[0-9a-f-]{36}$', '/api/v1/streets/:id', r['path'])
    store[key] = {'s': r['status'], 't': r['type'], 'b': r['body']}

SHIM = r'''
window.__smx = (function () {
  var REC = __STORE__;
  var path = '/new';
  function pathOf (u) { try { return new URL(String(u), 'http://localhost:8000').pathname + new URL(String(u), 'http://localhost:8000').search; } catch (e) { return String(u); } }
  function find (method, u) {
    var p = pathOf(u).replace(/^\/[A-Za-z]:/, '');
    var k = method + ' ' + p.replace(/^\/api\/v1\/streets\/[0-9a-f-]{36}$/, '/api/v1/streets/:id');
    if (REC[k]) return REC[k];
    var base = p.split('/').pop();                       // bundled assets resolve next to this file when opened from disk
    for (var key in REC) if (key.indexOf('GET ') === 0 && key.split('/').pop() === base) return REC[key];
    return null;
  }
  function bytes (b64) { var s = atob(b64), a = new Uint8Array(s.length); for (var i = 0; i < s.length; i++) a[i] = s.charCodeAt(i); return a; }
  function uri (r) { return 'data:' + (r.t.split(';')[0] || 'application/octet-stream') + ';base64,' + r.b; }
  window.fetch = function (input, init) {
    var url = typeof input === 'string' ? input : (input && input.url) || String(input);
    var method = ((init && init.method) || (input && input.method) || 'GET').toUpperCase();
    var r = find(method, url);
    if (r) return Promise.resolve(new Response(r.s === 204 ? null : bytes(r.b), { status: r.s, headers: { 'Content-Type': r.t } }));
    if (method !== 'GET') return Promise.resolve(new Response(null, { status: 204 }));      // saves are accepted and dropped
    return Promise.resolve(new Response('{}', { status: 404, headers: { 'Content-Type': 'application/json' } }));
  };
  // The app talks to its API through XMLHttpRequest (axios), so that is replayed too.
  function FakeXHR () { this.readyState = 0; this.status = 0; this.statusText = ''; this.response = null; this.responseText = ''; this.responseType = ''; this.responseURL = ''; this.timeout = 0; this.withCredentials = false; this._l = {}; this._h = {}; this.upload = { addEventListener: function () {}, removeEventListener: function () {} }; }
  FakeXHR.prototype.open = function (m, u) { this._m = String(m).toUpperCase(); this._u = u; this.readyState = 1; };
  FakeXHR.prototype.setRequestHeader = function () {};
  FakeXHR.prototype.overrideMimeType = function () {};
  FakeXHR.prototype.abort = function () {};
  FakeXHR.prototype.addEventListener = function (t, f) { (this._l[t] = this._l[t] || []).push(f); };
  FakeXHR.prototype.removeEventListener = function (t, f) { this._l[t] = (this._l[t] || []).filter(function (x) { return x !== f; }); };
  FakeXHR.prototype.getResponseHeader = function (n) { return this._h[String(n).toLowerCase()] || null; };
  FakeXHR.prototype.getAllResponseHeaders = function () { var h = this._h; return Object.keys(h).map(function (k) { return k + ': ' + h[k]; }).join('\r\n'); };
  FakeXHR.prototype._emit = function (t) { var e = { type: t, target: this, currentTarget: this, lengthComputable: false, loaded: 0, total: 0 }; if (typeof this['on' + t] === 'function') this['on' + t](e); (this._l[t] || []).forEach(function (f) { f.call(this, e); }, this); };
  FakeXHR.prototype.send = function () {
    var self = this, r = find(this._m, this._u), text = '', status = 404, type = 'application/json';
    if (r) { status = r.s; type = r.t || type; text = r.s === 204 ? '' : new TextDecoder().decode(bytes(r.b)); } else if (this._m !== 'GET') { status = 204; } else { text = '{}'; }
    setTimeout(function () {
      self.status = status; self.statusText = status < 300 ? 'OK' : 'Not Found'; self.responseURL = String(self._u); self._h = { 'content-type': type };
      self.responseText = text;
      if (self.responseType === 'json') { try { self.response = text ? JSON.parse(text) : null; } catch (e) { self.response = null; } } else if (self.responseType === 'arraybuffer') { self.response = new TextEncoder().encode(text).buffer; } else if (self.responseType === 'blob') { self.response = new Blob([text], { type: type }); } else { self.response = text; }
      self.readyState = 4; self._emit('readystatechange'); self._emit('load'); self._emit('loadend');
    }, 0);
  };
  FakeXHR.UNSENT = 0; FakeXHR.OPENED = 1; FakeXHR.HEADERS_RECEIVED = 2; FakeXHR.LOADING = 3; FakeXHR.DONE = 4;
  window.XMLHttpRequest = FakeXHR;
  var d = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, 'src');
  Object.defineProperty(HTMLImageElement.prototype, 'src', { get: d.get, set: function (v) { var r = /^(data:|blob:)/.test(v) ? null : find('GET', v); d.set.call(this, r ? uri(r) : v); }, configurable: true });
  var sa = Element.prototype.setAttribute;
  Element.prototype.setAttribute = function (n, v) { if (this.tagName === 'IMG' && n === 'src' && !/^(data:|blob:)/.test(v)) { var r = find('GET', v); if (r) v = uri(r); } return sa.call(this, n, v); };
  ['pushState', 'replaceState'].forEach(function (fn) {
    var o = history[fn].bind(history);
    history[fn] = function (state, title, url) { if (url) path = pathOf(url); try { o(state, title); } catch (e) {} };
  });
  return { href: function () { return 'http://localhost:8000' + path; } };
})();
'''.replace('__STORE__', json.dumps(store))

html = shell
html = re.sub(r'<link[^>]+rel="(?:apple-touch-icon|icon|manifest|mask-icon|shortcut icon|canonical)"[^>]*>', '', html, flags=re.S)
html = re.sub(r'<link\s+href="/assets/main\.[^"]+\.css"[^>]*>', lambda m: '<style>' + css + '</style>', html)
html = re.sub(r'<script src="/assets/main\.[^"]+\.js" type="module"></script>', lambda m: '<script>' + SHIM + '</script>\n<script type="module">' + js + '</script>', html)
html = html.replace('<title>Streetmix</title>', '<title>Streetmix with VHB sketch artwork</title>')
open(OUT, 'w').write(html)
print('wrote', OUT, round(len(html) / 1e6, 2), 'MB;', len(store), 'recorded responses')
