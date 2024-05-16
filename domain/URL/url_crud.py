from models import URL
from sqlalchemy.orm import Session
from domain.URL import url_scheme
import models
import datetime

def get_url(db: Session,
            shorten_url: str):
    
    _url = db.query(URL).get(shorten_url)
    if not _url:
        return None
    else:
        if _url.expire_date:
            if _url.expire_date < datetime.datetime.now():
                db.delete(_url)
                db.commit()
                return None
            else:
                _url.views += 1
                db.commit()
                return _url
        else:
            _url.views += 1
            db.commit()
            return _url
        
def search_url(db:Session,
               shorten_url: str):
    _url = db.query(URL).get(shorten_url)
    if not _url:
        return None
    else:
        if _url.expire_date:
            if _url.expire_date < datetime.datetime.now():
                db.delete(_url)
                db.commit()
                return None
            else:
                return _url
        else:
            return _url
        
def create_shorten_url(db: Session, _shorten_url: str,
                       url_create: url_scheme.URLCreate):
    # TODO: origin_url to shorten_url 변환 구현
    date = url_create.expire_date
    if url_create.expire_date:
        date = datetime.datetime.strptime(url_create.expire_date, "%Y-%m-%d %H:%M:%S")
    _url = models.URL(shorten_key=_shorten_url,
                      original_url=url_create.original_url,
                      expire_date=date,
                      views = 0)
    db.add(_url)
    db.commit()
