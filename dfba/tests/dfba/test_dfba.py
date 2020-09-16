import pytest
import unittest
import os
import shutil
import tempfile


from sbmlutils.dfba.utils import versioned_directory

from sbmlutils.dfba.toy_wholecell import settings
from sbmlutils.dfba.toy_wholecell import model_factory as toyfactory
from sbmlutils.dfba.toy_wholecell import simulate as toysimulate

from sbmlutils.dfba.toy_atp import settings as atpsettings
from sbmlutils.dfba.toy_atp import model_factory as atpfactory
from sbmlutils.dfba.toy_atp import simulate as atpsimulate

from sbmlutils.dfba.diauxic_growth import settings as dgsettings
from sbmlutils.dfba.diauxic_growth import model_factory as dgfactory
from sbmlutils.dfba.diauxic_growth import simulate as dgsimulate


# no backend for testing, must be imported before pyplot
import matplotlib
matplotlib.use('Agg')


class DFBATestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def file_exists(self, directory, filename):
        """ Check if file with filename was generated in the directory.

        :param directory:
        :param filename:
        :return:
        """
        path = os.path.join(directory, filename)
        print('Check file path:', path)
        self.assertTrue(os.path.exists(path))

    @pytest.mark.skip
    def test_toy_creation(self):
        directory = toyfactory.create_model(output_dir=self.test_dir)
        print(os.listdir(self.test_dir))

        self.file_exists(directory, settings.FBA_LOCATION)
        self.file_exists(directory, settings.BOUNDS_LOCATION)
        self.file_exists(directory, settings.UPDATE_LOCATION)
        self.file_exists(directory, settings.TOP_LOCATION)
        self.file_exists(directory, settings.FLATTENED_LOCATION)

    @pytest.mark.skip
    def test_diauxic_creation(self):
        directory = dgfactory.create_model(output_dir=self.test_dir)

        print(os.listdir(self.test_dir))

        self.file_exists(directory, dgsettings.FBA_LOCATION)
        self.file_exists(directory, dgsettings.BOUNDS_LOCATION)
        self.file_exists(directory, dgsettings.UPDATE_LOCATION)
        self.file_exists(directory, dgsettings.TOP_LOCATION)
        self.file_exists(directory, dgsettings.FLATTENED_LOCATION)

    @pytest.mark.skip
    def test_toy_wholecell_simulation(self):
        toyfactory.create_model(self.test_dir)
        sbml_path = os.path.join(versioned_directory(self.test_dir, settings.VERSION),
                                 settings.TOP_LOCATION)
        print(sbml_path)
        toysimulate.simulate_toy(sbml_path, self.test_dir, dts=[1.0], figures=False)

        # self.file_exists("reactions.png")
        # self.file_exists("species.png")
        # self.file_exists("simulation.csv")

    @pytest.mark.skip
    def test_toy_atp_simulation(self):
        atpfactory.create_model(self.test_dir)
        sbml_path = os.path.join(versioned_directory(self.test_dir, atpsettings.VERSION),
                                 atpsettings.TOP_LOCATION)
        print(sbml_path)
        atpsimulate.simulate_toy_atp(sbml_path, self.test_dir, dts=[1.0], figures=False)

        # self.file_exists("reactions.png")
        # self.file_exists("species.png")
        # self.file_exists("simulation.csv")

        # FIXME: what is wrong with this test?

    @pytest.mark.skip
    def test_diauxic_simulation(self):

        dgfactory.create_model(self.test_dir)
        sbml_path = os.path.join(versioned_directory(self.test_dir, dgsettings.VERSION),
                                 dgsettings.TOP_LOCATION)
        print(sbml_path)
        dgsimulate.simulate_diauxic_growth(sbml_path, self.test_dir, dts=[0.01],
                                           figures=False)

        # self.file_exists("reactions.png")
        # self.file_exists("species.png")
        # self.file_exists("simulation.csv")


if __name__ == '__main__':
    unittest.main()
