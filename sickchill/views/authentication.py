from sickchill import settings, logger

from ..sickbeard import config, notifiers
from .common import PageTemplate
from .index import BaseHandler


class LoginHandler(BaseHandler):
    def get(self, next_=None):
        next_ = self.get_query_argument('next', next_)
        if self.get_current_user():
            self.redirect(next_ or '/' + settings.DEFAULT_PAGE + '/')
        else:
            t = PageTemplate(rh=self, filename="login.mako")
            self.finish(t.render(title=_("Login"), header=_("Login"), topmenu="login"))

    def post(self, next_=None):
        notifiers.notify_login(self.request.remote_ip)

        if self.get_body_argument('username', None) == settings.WEB_USERNAME and self.get_body_argument('password', None) == settings.WEB_PASSWORD:
            remember_me = config.checkbox_to_value(self.get_body_argument('remember_me', 0))
            self.set_secure_cookie('sickchill_user', settings.API_KEY, expires_days=(None, 30)[remember_me])
            logger.info('User logged into the SickChill web interface')
        else:
            logger.warning('User attempted a failed login to the SickChill web interface from IP: ' + self.request.remote_ip)

        next_ = self.get_query_argument('next', next_)
        self.redirect(next_ or '/' + settings.DEFAULT_PAGE + '/')


class LogoutHandler(BaseHandler):
    def get(self, next_=None):
        self.clear_cookie("sickchill_user")
        self.redirect('/login/')
