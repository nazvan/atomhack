from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4


class PipeSchema(BaseModel):
    name: Optional[str]
    type: Optional[str]
    desc: Optional[str]

    class Config:
        orm_mode = True

class GetPipesSchema(PipeSchema):
    id: uuid4


# class Route(BaseModel):
#     robotId: str
#     name: Optional[str]
#     desc: Optional[str]
#     length: Optional[float]
#     timeDuration: Optional[str]

# class ChangeDefect(BaseModel):
#     id: Optional[str]
#     type: Optional[str]
    

#     class Config:
#         orm_mode = True