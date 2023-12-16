from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, delete, update

from dependencies import get_session
from db.config import async_session

from db.model import Pipe as PipeModel
from db.schema import *


pipe_router = APIRouter(
    prefix="/pipes",
    tags=["Pipes"],
)



@pipe_router.post("")
async def create_pipe(pipe: PipeSchema, session: async_session = Depends(get_session)):
    new_pipe = PipeModel(**pipe.dict())
    session.add(new_pipe)
    await session.commit()
    return {"status": "200"}

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







