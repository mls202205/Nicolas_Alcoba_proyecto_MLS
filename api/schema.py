from pydantic import BaseModel

class DataBase(BaseModel):
    baseline_value: int
    accelerations: float
    fetal_movement: float
    uterine_contractions: float
    light_decelerations: float
    severe_decelerations: float
    prolongued_decelerations: float
    abnormal_short_term_variability: int
    mean_value_of_short_term_variability: float
    percentage_of_time_with_abnormal_long_term_variability: float
    mean_value_of_long_term_variability: float
    histogram_width: int
    histogram_min: int
    histogram_max: int
    histogram_number_of_peaks: int
    histogram_number_of_zeroes: int
    histogram_mode: int
    histogram_mean: int
    histogram_median: int
    histogram_variance: int
    histogram_tendency: int
    fetal_health: int

class DataCreate(DataBase):
    pass

class Data(DataBase):
    id: int
    class Config:
        orm_mode = True