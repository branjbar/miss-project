__author__ = 'Bijan'

from threading import Thread


def async(f):
    """
        here is an explanation for this code:
        http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xi-email-support
    """
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper