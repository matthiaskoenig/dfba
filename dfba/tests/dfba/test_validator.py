"""
Test the DFBA validator.
"""
import os
import pytest

from sbmlutils.dfba import utils
from sbmlutils.dfba import validator
from sbmlutils.dfba.toy_wholecell import settings as toysettings
from sbmlutils.dfba.toy_wholecell import model_factory as toyfactory


@pytest.mark.skip(reason="validation currently not implemented")
def test_validate_toy(self):
    """ Validate the toy model. """
    sbml_path = os.path.join(utils.versioned_directory(toysettings.OUT_DIR, toyfactory.VERSION),
                             toysettings.TOP_LOCATION)
    print(sbml_path)

    # run simulation with the top model
    # df, dfba_model, dfba_simulator = simulate_dfba(sbml_path, tend=50, dt=5.0)

    validator.validate_dfba(sbml_path)
    assert False
