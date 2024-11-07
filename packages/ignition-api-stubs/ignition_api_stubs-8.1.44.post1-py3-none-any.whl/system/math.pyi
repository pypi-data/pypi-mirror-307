from typing import List

from dev.coatl.helper.types import AnyNum

def geometricMean(values: List[AnyNum]) -> float: ...
def kurtosis(values: List[AnyNum]) -> float: ...
def max(values: List[AnyNum]) -> float: ...
def mean(values: List[AnyNum]) -> float: ...
def meanDifference(values1: List[AnyNum], values2: List[AnyNum]) -> float: ...
def median(values: List[AnyNum]) -> float: ...
def min(values: List[AnyNum]) -> float: ...
def mode(values: List[AnyNum]) -> List[float]: ...
def normalize(values: List[AnyNum]) -> List[float]: ...
def percentile(values: List[AnyNum], percentile: float) -> float: ...
def populationVariance(values: List[AnyNum]) -> float: ...
def product(values: List[AnyNum]) -> float: ...
def skewness(values: List[AnyNum]) -> float: ...
def standardDeviation(values: List[AnyNum]) -> float: ...
def sum(values: List[AnyNum]) -> float: ...
def sumDifference(values1: List[AnyNum], values2: List[AnyNum]) -> float: ...
def sumLog(values: List[AnyNum]) -> float: ...
def sumSquares(values: List[AnyNum]) -> float: ...
def variance(values: List[AnyNum]) -> float: ...
