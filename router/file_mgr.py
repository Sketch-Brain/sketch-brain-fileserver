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

@router.get("/list")
def getFileList(user: Union[str,None] = None):

    logger.info("file_mgr : get file list")
    session = engine.sessionMaker()

    try:
        if user:
            fileList = session.query(FileList).filter(FileList.user == user).all()
        else:
            fileList = session.query(FileList).all()
        fileNameList = []
        for file in fileList:
            fileNameList.append(file.file_name)
        session.close()
        return fileNameList
    except SQLAlchemyError as e:
        logger.debug(e)
        return {'success': False, 'msg': 'DB Error'}

@router.put("/")
async def uploadFile(file: UploadFile = File(...), user: str = Form(...)):

    logger.info(f"file_mgr : {file.filename} uploaded by {user}")
    UPLOAD_DIRECTORY = "./files/"
    session = engine.sessionMaker()
    contents = await file.read()
    with open(os.path.join(UPLOAD_DIRECTORY, file.filename), "wb") as fp:
        fp.write(contents)
    fileList = FileList(
        id=None,
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


@router.get("/{file}")
def downloadFile(file: str):

    logger.info(f"file_mgr: {file} download")
    return FileResponse(
        path="./files/" + file,
        media_type='application/octet-stream',
        filename=file
    )


