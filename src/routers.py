from typing import List, Optional

from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload, joinedload, subqueryload, contains_eager

from dependencies import get_session
from db.config import async_session

from db.model import PipeModel, ImageModel
from db.schema import *

import aiofiles
from random import randint
import time
import uuid
import requests


pipe_router = APIRouter(
    prefix="/api/pipes",
    tags=["Pipes"],
)

file_router = APIRouter(
    prefix="/api/files",
    tags=["Files"],
)

#############################################################################################

@file_router.post("/upload")
async def test(file: UploadFile = File(...)):
    im_id = str(uuid.uuid4())
    image_path = f'images/{im_id}.jpg'
    async with aiofiles.open(image_path, 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content) 
    files = {
        'file': ('im.jpg', open(image_path, 'rb')),
        'Content-Type': 'image/jpeg',
        'Content-Length': l
    }
    r = requests.post(url, files=files)
    return {'url':f'{im_id}.jpg'}

@file_router.post("/uploads")
async def many_files(files: List[UploadFile] = File(...),session: async_session = Depends(get_session)):

    new_pipe = PipeModel()
    new_pipe.name = f'Изделие {str(randint(0,999)).zfill(3)}-{str(randint(0,99)).zfill(2)}-{str(randint(0,99)).zfill(2)}'
    new_pipe.timestamp = int(time.time())*1000

    session.add(new_pipe)
    await session.flush()

    for i,f in enumerate(files):
        print(i)
        image_path = f'files/{str(uuid.uuid4())}.jpg'

        image = ImageModel()
        image.name = f.filename 
        image.url = image_path.split('/')[-1]
        image.timestamp = int(time.time())*1000
        image.path = image_path
        image.pipe_id = new_pipe.id
        image.pipe_n = i

        session.add(image)
        async with aiofiles.open(image_path, 'wb') as out_file:
            content = await f.read()  # async read
            await out_file.write(content) 
        await session.flush()
    await session.commit()
    return {'id':1}


#############################################################################################
@pipe_router.get("", status_code=200)
async def get_pipes_list(session: async_session = Depends(get_session)):
    q = select(PipeModel).options(selectinload(PipeModel.defects))
    result = await session.execute(q)
    data = result.scalars().all()
    result = []
    for d in data:
        pipe = d.__dict__
        pipe.pop('_sa_instance_state')
        pipe['defects_count'] = len(pipe['defects'])
        pipe.pop('defects')
    return data


@pipe_router.post("")
async def create_pipe(pipe: PipeSchema, session: async_session = Depends(get_session)):
    new_pipe = PipeModel(**pipe.dict())
    session.add(new_pipe)
    await session.commit()
    return {"status": "200"}

@pipe_router.get("/{pipe_id}")
async def create_pipe(pipe_id, session: async_session = Depends(get_session)):
    q = select(PipeModel).filter(PipeModel.id==pipe_id).options(selectinload(PipeModel.images)).options(selectinload(PipeModel.defects))
    result = await session.execute(q)
    curr = result.scalars().first()
    return {'data':curr}

# @pipe_router.delete("")
# async def delete_pipe(robot_id: str, session: async_session = Depends(get_session)):
#     q = delete(PipeModel).where(PipeModel.id == robot_id)
#     await session.execute(q)
#     await session.commit()
#     return {"status": "200"}

# @pipe_router.get("", status_code=200)
# async def get_pipes_list(session: async_session = Depends(get_session)):
#     q = select({PipeModel)
#     result = await session.execute(q)
#     data = result.scalars().all()
#     return data







