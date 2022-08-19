from typing import ValuesView
from pyrsistent import v
from database import database

from sqlalchemy import Column, Float, Integer, Table, MetaData

"""def table():

    metadata = MetaData(database.engine)

    table = Table('Example',metadata,
                  Column('id',Integer, primary_key=True),
                  Column('baseline_value', Integer),
                  Column('accelerations', Float),
                  Column('fetal_movement', Float),
                  Column('uterine_contractions', Float),
                  Column('light_decelerations', Float),
                  Column('severe_decelerations', Float),
                  Column('prolongued_decelerations', Float),
                  Column('abnormal_short_term_variability', Integer),
                  Column('mean_value_of_short_term_variability', Float),
                  Column('percentage_of_time_with_abnormal_long_term_variability', Float),
                  Column('mean_value_of_long_term_variability', Float),
                  Column('histogram_width', Integer),
                  Column('histogram_min', Integer),
                  Column('histogram_max', Integer),
                  Column('histogram_number_of_peaks', Integer),
                  Column('histogram_number_of_zeroes', Integer),
                  Column('histogram_mode', Integer),
                  Column('histogram_mean', Integer),
                  Column('histogram_median', Integer),
                  Column('histogram_variance', Integer),
                  Column('histogram_tendency', Integer),
                  Column('fetal_health', Integer))
    
    table.create()"""



class fetal_health(database.Base):
    __tablename__="fetal_health"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    baseline_value = Column(Integer)
    accelerations = Column(Float)
    fetal_movement = Column(Float)
    uterine_contractions = Column(Float)
    light_decelerations = Column(Float)
    severe_decelerations = Column(Float)
    prolongued_decelerations = Column(Float)
    abnormal_short_term_variability = Column(Integer)
    mean_value_of_short_term_variability = Column(Float)
    percentage_of_time_with_abnormal_long_term_variability = Column(Float)
    mean_value_of_long_term_variability = Column(Float)
    histogram_width = Column(Integer)
    histogram_min = Column(Integer)
    histogram_max = Column(Integer)
    histogram_number_of_peaks = Column(Integer)
    histogram_number_of_zeroes = Column(Integer)
    histogram_mode = Column(Integer)
    histogram_mean = Column(Integer)
    histogram_median = Column(Integer)
    histogram_variance = Column(Integer)
    histogram_tendency = Column(Integer)
    fetal_health = Column(Integer)

