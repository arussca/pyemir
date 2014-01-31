#
# Copyright 2013-2014 Universidad Complutense de Madrid
# 
# This file is part of PyEmir
# 
# PyEmir is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# PyEmir is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with PyEmir.  If not, see <http://www.gnu.org/licenses/>.
#

'''Tests for AIV Recipes for EMIR'''

import os
from tempfile import mkstemp
import unittest

import pyfits
import numpy as np

from numina.core.oresult import ObservationResult, dataframe_from_list
from numina.core.reciperesult import ErrorRecipeResult
from numina.core.recipeinput import RecipeInput
from numina.core.dataframe import DataFrame

from . import SimpleBiasRecipe

class MMTestCase(unittest.TestCase):

    def test1(self):

        # Create some HDUList in memory
        somefits = []
        nimg = 10
        for i in range(nimg):
            hdu = pyfits.PrimaryHDU(data=np.zeros((10,10), dtype='int16'))
            hdul = pyfits.HDUList([hdu])
            somefits.append(hdul)

         #
        # Create the recipe_input
        obsres = ObservationResult()
        obsres.frames = [dataframe_from_list(val) for val in somefits]
        # empty requirements
        reqs = SimpleBiasRecipe.RecipeRequirements(obresult=obsres)
        recipe = SimpleBiasRecipe()
        #
        result = recipe(reqs)

        self.verify_result(result)
        
    def verify_result(self, result):

        self.assertIsInstance(result, SimpleBiasRecipe.RecipeResult)
        self.assertTrue(hasattr(result, "biasframe"))
        self.assertIsInstance(result.biasframe, DataFrame)
        
        frame = result.biasframe.frame

        self.assertIsInstance(frame, pyfits.HDUList)

        # Number of extensions
        self.assertEqual(len(frame), 3)

        self.assertIsInstance(frame[0], pyfits.PrimaryHDU)
        self.assertIsInstance(frame[1], pyfits.ImageHDU)
        self.assertIsInstance(frame[2], pyfits.ImageHDU)
   
     def test3(self):

        # Create some HDUList
        somefits = []
        nimg = 10
        for i in range(nimg):
            hdu = pyfits.PrimaryHDU(data=np.zeros((10,10), dtype='int16'))
            hdul = pyfits.HDUList([hdu])
            fd, filename = mkstemp()
            hdul.writeto(filename, clobber=True)
            somefits.append(filename)

        #
        # Create the recipe_input
        obsres = ObservationResult()
        obsres.frames = [dataframe_from_list(val) for val in somefits]
        # empty requirements
        reqs = SimpleBiasRecipe.RecipeRequirements(obresult=obsres)
        #
        recipe = SimpleBiasRecipe()
        result = recipe(reqs)

        for fname in somefits:
            os.remove(fname)
        
        self.verify_result(result)
        
