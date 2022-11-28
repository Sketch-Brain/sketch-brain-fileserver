from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from typing import List, Union

from fastapi.params import Form
from sqlalchemy.exc import SQLAlchemyError

import logging, os
import base64
from pydantic import BaseModel
from database import dbconfig
from database.table.file_list import FileList

router = APIRouter(
    prefix="/api/file"
)

logger = logging.getLogger("fileserver-logger")
engine = dbconfig.Engine()

@router.get("/{file_type}/list")
def getFileList( file_type: str, user: Union[str,None] = None):

    logger.info("file_mgr : get file list")
    session = engine.sessionMaker()

    try:
        if user:
            fileList = session.query(FileList).filter(FileList.user == user,FileList.file_type==file_type).all()
        else:
            fileList = session.query(FileList).filter(FileList.file_type==file_type).all()
        fileNameList = []
        for file in fileList:
            fileNameList.append(file.file_name)
        session.close()
        return fileNameList
    except SQLAlchemyError as e:
        logger.debug(e)
        return {'success': False, 'msg': 'DB Error'}

@router.put("/{file_type}")
async def uploadFile(file_type:str, file: UploadFile = File(...), user: str = Form(...)):

    logger.info(f"file_mgr : {file.filename} uploaded by {user}")
    UPLOAD_DIRECTORY = f"./files/{file_type}"
    session = engine.sessionMaker()
    contents = await file.read()
    with open(os.path.join(UPLOAD_DIRECTORY, file.filename), "wb") as fp:
        fp.write(contents)
    fileList = FileList(
        id=None,
        file_type=file_type,
        file_name=file.filename,
        user=user,
        created_at=None
    )

    try:
        session.add(fileList)
        session.commit()
        session.close()
    except SQLAlchemyError as e:
        logger.debug(e)
        session.close()
        return {'success': False}

    return {'success': True}


@router.get("/{file_type}/{file}")
def downloadFile(file_type:str, file: str):
    logger.info(f"file_mgr: {file} download")
    try:
        result = FileResponse(
            path=f"./files/{file_type}/" + file,
            media_type='application/octet-stream',
            filename=file
        )
        return result
    except:
        return {"success":False}


