from pydantic import BaseModel
from enum import Enum


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

class List_cols(str, Enum):
    baseline_value = "baseline_value"
    accelerations = "accelerations"
    fetal_movement = "fetal_movement"
    uterine_contractions = "uterine_contractions"
    light_decelerations = "light_decelerations"
    severe_decelerations = "severe_decelerations"
    prolongued_decelerations = "prolongued_decelerations"
    abnormal_short_term_variability = "abnormal_short_term_variability"
    mean_value_of_short_term_variability = "mean_value_of_short_term_variability"
    percentage_of_time_with_abnormal_long_term_variability = "percentage_of_time_with_abnormal_long_term_variability"
    mean_value_of_long_term_variability = "mean_value_of_long_term_variability"
    histogram_width = "histogram_width"
    histogram_min = "histogram_min"
    histogram_max = "histogram_max"
    histogram_number_of_peaks = "histogram_number_of_peaks"
    histogram_number_of_zeroes = "histogram_number_of_zeroes"
    histogram_mode = "histogram_mode"
    histogram_mean = "histogram_mean"
    histogram_median = "histogram_median"
    histogram_variance = "histogram_variance"
    histogram_tendency = "histogram_tendency"
    fetal_health = "fetal_health"

class listMMA(str, Enum):
    max = "max"
    min = "min"
    avg = "avg"

class list_symbols(str, Enum):
    smaller = "<"
    larger = ">"
    equal = "=="
    smaller_equal = "=<"
    larger_equal = "=>"
    not_equal = "!="