from flask import render_template
from ReBloger import ReBlogerException
from ReBloger.general import general


@general.errorhandler(ReBlogerException)
def response_error(e):
    return render_template('general/error.html', e.msg)