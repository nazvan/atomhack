from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean, Float
from db.config import Base
from uuid import UUID, uuid4
from dependencies import uuid


from datetime import datetime
import time
from typing import List, Optional
from sqlalchemy.orm import relationship

class PipeModel(Base): 
    __tablename__ = "pipes"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)  
    timestamp = Column(Integer, nullable=True)
    type = Column(String, nullable=True) 
    desc = Column(String, nullable=True)  
    isDeleted = Column(Boolean, nullable=True)  

    defects = relationship("DefectModel", back_populates="pipe")
    images = relationship("ImageModel", back_populates="pipe")



class ImageModel(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)  
    url = Column(String, nullable=True) 
    timestamp = Column(Integer, nullable=True) 
    path = Column(String, nullable=True)  
    desc = Column(String, nullable=True)
    pipe_n = Column(Integer,nullable=False)

    pipe_id = Column(Integer, ForeignKey('pipes.id'))
    pipe = relationship("PipeModel", back_populates="images")

    defects = relationship("DefectModel", back_populates="image")


class DefectModel(Base): 
    __tablename__ = "defects"

    id = Column(Integer, primary_key=True)
    center_x = Column(Integer, primary_key=True)
    center_y = Column(Integer, primary_key=True)
    width = Column(Integer, primary_key=True)
    height = Column(Integer, primary_key=True)
    desc = Column(String, nullable=True) 
    type = Column(Boolean, nullable=True)

    pipe_id = Column(Integer, ForeignKey('pipes.id'))
    pipe = relationship("PipeModel", back_populates="defects")

    image_id = Column(Integer, ForeignKey('images.id'))
    image = relationship("ImageModel", back_populates="defects")





# class Route(Base): ## Маршруты
#     __tablename__ = "route"

#     id = Column(String, primary_key=True, default=uuid)
#     name = Column(String, nullable=True)  # Название маршрута
#     desc = Column(String, nullable=True)  # Описание маршрута
#     length = Column(String, nullable=True)  # длина маршрута, км
#     timeDuration = Column(String, nullable=True)  # Длителность маршрута
#     isActive = Column(Boolean, nullable=True)  # Активен ли в данный момент

#     robotId = Column(String, ForeignKey("robot.id"), nullable=False)

# class RoutePoint(Base): ## Маршруты
#     __tablename__ = "route_point"

#     id = Column(Integer, primary_key=True)
#     latitude = Column(Float, nullable=False)
#     longitude = Column(Float, nullable=False)
#     timestamp = Column(Integer, nullable=False)

#     routeId = Column(String, ForeignKey("route.id"), nullable=False)
#     robotId = Column(String, ForeignKey("robot.id"), nullable=False)