import urllib
import os

class ProxyAuthURLopener(urllib.FancyURLopener):
	error = ""
	def http_error_default(self, url, fp, errcode, errmsg, headers):
		self.error = `errcode` + " " + errmsg
		return None

        def http_error_304(self,uri,fp,errocode,errmsg,headers):
                print 'HTTP/1.1 304 Not Modified'
                return None

	def open_local_file(self, url):
		self.error = "Local file URL not accepted"
		return None

	def _send_auth_challenge(self, scheme, url, realm, data=None):
		if scheme!="http" and scheme!="https":
			return None
		if os.environ.has_key('HTTP_AUTHORIZATION') and os.environ['HTTP_AUTHORIZATION']:
			self.addheader('Authorization',os.environ['HTTP_AUTHORIZATION'])
			del os.environ['HTTP_AUTHORIZATION']

			if data is None:
				return self.open(scheme + ':' + url)
			else:
				return self.open(scheme + ':' + url,data)
		else:
			global Page
			print 'Status: 401 Authorization Required'
			print 'WWW-Authenticate: Basic realm="%s"' % realm
			print 'Connection: close'
			Page = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
<title>401 Authorization Required</title>
</head>
<body>
<h1>Authorization Required</h1>
<p>You need %s access to %s:%s to use this service.</p>
""" % (realm, scheme, url)
			return None

	def  retry_https_basic_auth(self, url, realm, data=None):
		# @@@ need to send challenge through https as needed
		return self._send_auth_challenge("https", url, realm, data)

	def retry_http_basic_auth(self, url, realm, data=None):
		return self._send_auth_challenge("http", url, realm, data)
