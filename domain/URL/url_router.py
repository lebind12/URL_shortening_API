from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from domain.URL import url_crud, url_scheme
from util.hashing import make_shorten_url
import uuid

router = APIRouter(
    prefix="/api"
)

@router.get("/{shorten_key}")
def get_original_url(shorten_key: str,
                     db: Session = Depends(get_db)):
    # TODO: 단축된 키를 통해 원본 URL로 리디렉션
    # 키가 존재하면 301 status, view 증가
    # 키가 없으면 404 status
    # exprie가 now보다 작으면 404 후 삭제
    res = url_crud.get_url(db, shorten_key)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="등록된 URL이 없거나 만료된 URL입니다.")
    return RedirectResponse(res.original_url,headers={
        "Cache-Control":"no-cache, private, max-age=0"
    }, status_code=status.HTTP_301_MOVED_PERMANENTLY)

@router.post("/shorten", status_code=status.HTTP_201_CREATED)
def post_shorten_key(_url_create: url_scheme.URLCreate,
                     db: Session = Depends(get_db)):
    # TODO: 만료기능
    # 키 생성 시 만료 기간을 지정할 수 있으며, 만료된 키는 삭제 처리.
    # 요청 본문에 만료 기간을 선택적으로 추가할 수 있어야 함. "expire"
    
    original_url = _url_create.url
    while True:
        res = url_crud.search_url(db, make_shorten_url(original_url))
        if not res:
            break
        original_url += str(uuid.uuid4())
    
    shorten_key = make_shorten_url(original_url)
    url_crud.create_shorten_url(db=db,
                                _shorten_url=shorten_key,
                                url_create=_url_create)

    return {"short_url": shorten_key}
        
    
@router.get("/stats/{shorten_key}")
def get_shorten_status(shorten_key: str,
                       db: Session = Depends(get_db)):
    res = url_crud.search_url(db, shorten_key)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="등록된 URL이 없습니다.")
    return {
        "key":res.shorten_key,
        "views": res.views
    }