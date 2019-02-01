"""
Contains the Profile class and helper classes.
"""

import functools
import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from . import streamexceptions
from . import streamconstants as sc
from . import streammath as sm

class Profile(object):
    """
    A longitudinal stream profile.
    
    Attributes:
        df
        metric
        name
        unitDict
    """
    
    def __init__(self,df, name = None, metric = False):
        """
        Args:
            df: a dict or pandas dataframe with at least three columns/keys "exes", "whys", "Thalweg"
                and additional optional columns/keys. Standardized col/key names are 
                "Water Surface", "Bankfull", "Top of Bank", "Riffle", "Run", "Pool", "Glide".
            metric: a bool indicating if units are feet (False) or meters (True)
        
        Raises:
            x
        """
        self.df = df
        self.metric = metric
        self.name = name
        
        if self.metric:
            self.unitDict = sc.METRIC_CONSTANTS
        elif not(self.metric):
            self.unitDict = sc.IMPERIAL_CONSTANTS
        
        self.validate_df()
        self.generate_stationing()
        
    def validate_df(self):
        required = ['exes','whys','Thalweg']
        if not all(x in self.df.keys() for x in required):
            raise streamexceptions.InputError('Input df must include keys or columns "exes", "whys", "zees", "Thalweg"')
    
        
        # this will fail if df is a dataframe and not a dict; add try catch
        checkLength = len(self.df['exes'])
        for key in self.df:
            if len(self.df[key]) != checkLength:
                raise streamexceptions.ShapeAgreementError(f'key {key} has length {len(self.df[key])}; expected length {checkLength}')
    
    def __str__(self):
        """
        Prints the name of the Profile object. If the name attribute is None, prints "UNNAMED".
        """
        if self.name:
            return(self.name)
        else:
            return("UNNAMED")
        
    def qplot(self):
        pass
    
    def planplot(self):
        """
        Uses matplotlib to create a quick plot of the planform of the profile.
        """
        plt.figure()
        plt.plot(self.df['exes'],self.df['whys'])
        plt.title(str(self) + ' (Planform)')
        plt.xlabel('Easting (' + self.unitDict['lengthUnit'] + ')')
        plt.ylabel('Northing (' + self.unitDict['lengthUnit'] + ')')

    def generate_stationing(self):
        stations = sm.get_stationing(self.df['exes'],self.df['whys'],project = False)
        self.df['Station'] = stations

class Feature(object):
    """
    A subsection of a longitudinal stream profile representing a distinct substrate morphology.
    
    Attributes:
        x
    """
    
    def __init__(self,df,name = None,morphType = None,metric = False):
        """
        Args:
            df: a dict or pandas dataframe with at least two columns/keys "Station", "Thalweg"
                and additional optional columns/keys. Standardized col/key names include 
                "Water Surface", "Bankfull", "Top of Bank"
        
        Raises:
            x
        """
        pass