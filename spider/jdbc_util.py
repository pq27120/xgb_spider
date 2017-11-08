# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import Column, String, Integer, LargeBinary, Date, Text, create_engine
from sqlalchemy import DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义bbsTopic对象:
class Topic(Base):
    # 表的名字:
    __tablename__ = 'pybbs_topic'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    content = Column(Text())
    good = Column(LargeBinary(1))
    in_time = Column(DateTime)
    label_id = Column(String(255))
    last_reply_time = Column(DateTime)
    topic_lock = Column(LargeBinary(1))
    modify_time = Column(DateTime)
    reply_count = Column(Integer())
    tab = Column(String(255))
    title = Column(String(255))
    top = Column(LargeBinary(1))
    up_ids = Column(Text())
    view = Column(Integer())
    user_id = Column(Integer())
    cover_image = Column(String(255))


class SpiderSource(Base):
    # 表的名字:
    __tablename__ = 'spider_source'

    # 表的结构:
    id = Column(String(16), primary_key=True)
    name = Column(String(255))
    code = Column(String(255))
    channel = Column(String(1))


class SpiderHis(Base):
    # 表的名字:
    __tablename__ = 'spider_his'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    his_title = Column(String(1024))
    image_process = Column(String(1))
    channel = Column(String(1))

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:xgb20171010@120.78.132.250:3306/xgbbbs?charset=utf8', echo=True)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

# 创建session对象:
#session = DBSession()
# 创建新User对象:
#new_user = User(id='5', name='Bob')
# 添加到session:
#session.add(new_user)
# 提交即保存到数据库:
#session.commit()
# 关闭session:
#session.close()