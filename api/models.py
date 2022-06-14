from . import database

from sqlalchemy import Column, Float, Integer

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