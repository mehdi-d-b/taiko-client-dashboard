# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 16:03:48 2023

@author: MB273828
"""
import param
from holoviews.operation import Operation

class subtraction(Operation):
    """
    Subtracts two curves from one another.
    """
    dataset = param.DataFrame(doc="""
        Dataset.""")    
    element_1 = param.Integer(default=0, doc="""
        First curve to subtract.""")
    element_2 = param.Integer(default=1, doc="""
        Second curve to subtract.""")
    offset = param.Number(default=0.0, doc="""
        Offset to add.""")
    
    def _process(self, element, key=None):
        # Get first and second Element in overlay
        el1, el2 = element.get(self.p.element_1), element.get(self.p.element_2)
        
        # Get x-values and y-values of curves
        xvals  = el1.dimension_values(0)
        yvals  = el1.dimension_values(1)
        yvals2 = el2.dimension_values(1)
        
        # Return new Element with subtracted y-values
        # and new label
        return el1.clone((xvals, yvals-yvals2 + self.p.offset))