# -*- coding=utf-8 -*-
"""
This module creates the sub-models and combined comp model for the diauxic model.

Submodels are
- a FBA submodel
- deterministic ODE models

Questions:
- how are the metabolite concentrations kept >= 0 ?
    It seems that the relative change in flux bounds, relative
    to the hard bounds on the exchanges avoids negative concentrations

-----------------------------------------------
Along with the system of dynamic equations, several
additional constraints must be imposed for a realistic prediction
of the metabolite concentrations and the metabolic
fluxes. These include non-negative metabolite and flux levels,
limits on the rate of change of fluxes, and any additional
nonlinear constraints on the transport fluxes.
-----------------------------------------------
vO2:  -> O2
vGlcxt:  -> Glcxt
Ac_out = Ac  # rule

v1: 39.43 Ac + 35 O2 -> X
v2: 9.46 Glcxt + 12.92 O2 -> X
v3: 9.84 Glcxt + 12.73 O2 -> 1.24 Ac + X
v4: 19.23 Glcxt -> 12.12 Ac + X

objective: max(biomass) = max (w1*v1 + w2*v2 + w3*v3 + w4*v4) = max(µ),
            w1 = w2 = w3 = w4 [gdw/mmol]

boundaries:
    # rate of change boundaries => set new lower and upper bound based on
    # the maximal allowed change in boundary over time
    # |d/dt v| <= d/dt v_max
    d/dt v_max(v1) = 0.1 [mmol/h/gdw]
    d/dt v_max(v2) = 0.3 [mmol/h/gdw]
    d/dt v_max(v3) = 0.3 [mmol/h/gdw]
    d/dt v_max(v4) = 0.1 [mmol/h/gdw]

    # in addition the flux bounds must be set, so that not resulting in negative
    # concentrations

    # ? exchange, how does it work ?
    # no external concentrations, but upper bounds for entry in batch reactor
    ub(vO2) = 15 [mmol/h/gdw]
    ub(vGlcxt) = 10 Glcxt/(Km + Glcxt) [mmol/h/gdw]  # Michaelis-Menten kinetics involving glucose concentration

Km = 0.015 mM

-----------------------------------------------

Glcxt:  glucose [mM=mmol/l],    Glcxt(0) = 10.8 [mM]
Ac:     acetate [mM=mmol/l],    Ac(0) = 0.4 [mM]
O2:     oxygen [mM=mmol/l],     O2(0) = 0.21 [mM]
X:      biomass [gdw/l],        X(0) = 0.001 [g/l]

# A*v is row of stoichiometric matrix, i.e. all reactions which change the concentration
d/dt Glcxt = A_Glcxt*v * X                      # [mmol/l/h]
d/dt Ac = A_Ac*v * X                            # [mmol/l/h]
d/dt O2 = A_O2 * v * X + kLa * (O2_gas - O2)    # [mmol/l/h]
d/dt X = (w1*v1 + w2*v2 + w3*v3 + w4*v4)*X      # [g/l/h], due to coefficients conversions to g

O2_gas = 0.21 [mM]  # oxygen in gas phase, constant
kLa = 7.5 [per_h]  # mass transfer coefficient for oxygen

z: vector of metabolite concentrations
v: fluxes per gdw (gram dry weight)
mu: growth rate

-----------------------------------------------
tend = 10 [h]
steps = 10000

-----------------------------------------------
"""
import os
from os.path import join as pjoin

import libsbml
from libsbml import (UNIT_KIND_SECOND, UNIT_KIND_METRE, UNIT_KIND_GRAM, UNIT_KIND_LITRE,
                     UNIT_KIND_MOLE)

from sbmlutils.io import sbml
from sbmlutils import comp
from sbmlutils import fbc

from sbmlutils.factory import *
from sbmlutils import factory

from sbmlutils.report import sbmlreport
from sbmlutils.annotation import annotator

from sbmlutils.dfba import builder
from sbmlutils.dfba import utils
from sbmlutils.dfba.diauxic_growth import settings

libsbml.XMLOutputStream.setWriteTimestamp(False)

########################################################################
# General model information
########################################################################

DT_SIM = 0.1
notes = """
    <body xmlns='http://www.w3.org/1999/xhtml'>
    <h1>Diauxic Growth Model</h1>
    <p><strong>Model version: {}</strong></p>

    {}

    <h2>Description</h2>
    <p>Dynamic Flux Balance Analysis of Diauxic Growth in Escherichia coli</p>

    <p>The key variables in the mathematical model of the metabolic
network are the glucose concentration (Glcxt), the acetate concentration (Ac),
the biomass concentration (X), and the oxygen concentration (O2) in the gas phase.</p>

    <div class="dc:publisher">This file has been produced by
      <a href="https://livermetabolism.com/contact.html" title="Matthias Koenig" target="_blank">Matthias Koenig</a>.
      </div>

    <h2>Terms of use</h2>
      <div class="dc:rightsHolder">Copyright © 2017 Matthias Koenig</div>
      <div class="dc:license">
      <p>Redistribution and use of any part of this model, with or without modification, are permitted provided that
      the following conditions are met:
        <ol>
          <li>Redistributions of this SBML file must retain the above copyright notice, this list of conditions
              and the following disclaimer.</li>
          <li>Redistributions in a different form must reproduce the above copyright notice, this list of
              conditions and the following disclaimer in the documentation and/or other materials provided
          with the distribution.</li>
        </ol>
        This model is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
             the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.</p>
      </div>
    </body>
""".format(settings.VERSION, '{}')

creators = [
    Creator(familyName='Koenig', givenName='Matthias', email='konigmatt@googlemail.com',
               organization='Humboldt University Berlin', site='http://livermetabolism.com')
]

main_units = {
    'time': 'h',
    'extent': 'mmol',
    'substance': 'mmol',
    'length': 'm',
    'area': 'm2',
    'volume': 'l',
}
units = [
   Unit('h', [(UNIT_KIND_SECOND, 1.0, 0, 3600)], name='hour'),
   Unit('g', [(UNIT_KIND_GRAM, 1.0)], name="gram"),
   Unit('m', [(UNIT_KIND_METRE, 1.0)], name="meter"),
   Unit('m2', [(UNIT_KIND_METRE, 2.0)], name="cubic meter"),
   Unit('l', [(UNIT_KIND_LITRE, 1.0)], name="liter"),
   Unit('mmol', [(UNIT_KIND_MOLE, 1.0, -3, 1.0)]),
   Unit('per_h', [(UNIT_KIND_SECOND, -1.0, 0, 3600)]),
   Unit('mmol_per_h', [(UNIT_KIND_MOLE, 1.0, -3, 1.0),
                           (UNIT_KIND_SECOND, -1.0, 0, 3600)]),
   Unit('mmol_per_hg', [(UNIT_KIND_MOLE, 1.0, -3, 1.0),
                            (UNIT_KIND_SECOND, -1.0, 0, 3600), (UNIT_KIND_GRAM, -1.0)]),

   Unit('mmol_per_l', [(UNIT_KIND_MOLE, 1.0, -3, 1.0),
                           (UNIT_KIND_LITRE, -1.0)]),
   Unit('mmol_per_lg', [(UNIT_KIND_MOLE, 1.0, -3, 1.0),
                           (UNIT_KIND_LITRE, -1.0), (UNIT_KIND_GRAM, -1.0)]),

   Unit('l_per_mmol', [(UNIT_KIND_LITRE, 1.0),
                           (UNIT_KIND_MOLE, -1.0, -3, 1.0)]),
   Unit('g_per_l', [(UNIT_KIND_GRAM, 1.0),
                        (UNIT_KIND_LITRE, -1.0)]),
   Unit('g_per_mmol', [(UNIT_KIND_GRAM, 1.0),
                           (UNIT_KIND_MOLE, -1.0, -3, 1.0)]),
]

UNIT_AMOUNT = 'mmol'
UNIT_AREA = 'm2'
UNIT_VOLUME = 'l'
UNIT_TIME = 'h'
UNIT_CONCENTRATION = 'mmol_per_l'
UNIT_FLUX = 'mmol_per_h'

# UNIT_CONCENTRATION_PER_G = 'mmol_per_lg'
UNIT_FLUX_PER_G = 'mmol_per_h'  # !!! FIXME (unit scaling between models)


def fba_model(sbml_file, directory, annotations=None):
    """ Create FBA submodel.

    FBA submodel in sbml:fbc-version 2.
    """
    fba_notes = notes.format("""
    <h2>FBA submodel</h2>
    <p>DFBA fba submodel. Unbalanced metabolites are encoded via exchange fluxes.</p>
    """)
    doc = builder.template_doc_fba(settings.MODEL_ID)
    model = doc.getModel()
    utils.set_model_info(model, notes=fba_notes, creators=creators, units=units, main_units=main_units)

    objects = [
        # compartments
        Compartment(sid='bioreactor', value=1.0, unit=UNIT_VOLUME, constant=True, name='bioreactor',
                       spatialDimensions=3),

        # species
        Species(sid='Glcxt', name="glucose", initialConcentration=0.0, substanceUnit=UNIT_AMOUNT, hasOnlySubstanceUnits=False,
                   compartment="bioreactor"),
        Species(sid='Ac', name="acetate", initialConcentration=0.0, substanceUnit=UNIT_AMOUNT, hasOnlySubstanceUnits=False,
                   compartment="bioreactor"),
        Species(sid='O2', name="oxygen", initialConcentration=0.0, substanceUnit=UNIT_AMOUNT, hasOnlySubstanceUnits=False,
                   compartment="bioreactor"),
        Species(sid='X', name="biomass", initialConcentration=0.0, substanceUnit=UNIT_AMOUNT, hasOnlySubstanceUnits=False,
                   compartment="bioreactor"),

        # bounds
        Parameter(sid="zero", name="zero bound", value=0.0, unit=UNIT_FLUX_PER_G, constant=True, sboTerm="SBO:0000612"),
        Parameter(sid="ub_default", name="default upper bound", value=builder.UPPER_BOUND_DEFAULT, unit=UNIT_FLUX_PER_G,
                     constant=True, sboTerm="SBO:0000612"),

        Reaction(sid="v1", name="v1 (39.43 Ac + 35 O2 -> X)", reversible=False,
                 equation="39.43 Ac + 35 O2 -> X",
                 compartment='bioreactor',
                 lowerFluxBound="zero", upperFluxBound="ub_default"),
        Reaction(sid="v2", name="v2 (9.46 Glcxt + 12.92 O2 -> X)", reversible=False,
                 equation="9.46 Glcxt + 12.92 O2 -> X",
                 compartment='bioreactor',
                 lowerFluxBound = "zero", upperFluxBound = "ub_default"),
        Reaction(sid="v3", name="v3 (9.84 Glcxt + 12.73 O2 -> 1.24 Ac + X)", reversible=False,
                 equation="9.84 Glcxt + 12.73 O2 -> 1.24 Ac + X",
                 compartment='bioreactor',
                 lowerFluxBound="zero", upperFluxBound="ub_default"),
        Reaction(sid="v4", name="v4 (19.23 Glcxt -> 12.12 Ac + X)", reversible=False,
                 equation="19.23 Glcxt -> 12.12 Ac + X",
                 compartment='bioreactor',
                 lowerFluxBound="zero", upperFluxBound="ub_default"),
    ]
    factory.create_objects(model, objects)

    # reactions: exchange reactions (this species can be changed by the FBA)
    for sid in ['Ac', 'Glcxt', 'O2', 'X']:
        builder.create_exchange_reaction(model, species_id=sid, flux_unit=UNIT_FLUX_PER_G,
                                         exchange_type=builder.EXCHANGE)
    # set bounds for the exchange reactions
    p_lb_O2 = model.getParameter("lb_EX_O2")
    p_lb_O2.setValue(-15.0)  # FIXME: this is in mmol/gdw/h (biomass weighting of FBA)
    p_lb_Glcxt = model.getParameter("lb_EX_Glcxt")
    p_lb_Glcxt.setValue(-10.0)  # FIXME: this is in mmol/gdw/h

    # objective function
    model_fba = model.getPlugin(builder.SBML_FBC_NAME)
    fbc.create_objective(model_fba, oid="biomass_max", otype="maximize",
                         fluxObjectives={"v1": 1.0, "v2": 1.0, "v3": 1.0, "v4": 1.0})

    # write SBML file
    if annotations:
        annotator.annotate_sbml_doc(doc, annotations)
    sbml.write_sbml(doc, filepath=pjoin(directory, sbml_file), validate=True)

    return doc


def bounds_model(sbml_file, directory, doc_fba=None, annotations=None):
    """"
    Submodel for dynamically calculating the flux bounds.

    The dynamically changing flux bounds are the input to the
    FBA model.
    """
    # TODO: the bounds model should be created based on the FBA model (i.e. use the exchange reactions
    # to create the bounds info.

    bounds_notes = notes.format("""
    <h2>BOUNDS submodel</h2>
    <p>Submodel for dynamically calculating the flux bounds.
    The dynamically changing flux bounds are the input to the
    FBA model.</p>
    """)
    doc = builder.template_doc_bounds(settings.MODEL_ID)
    model = doc.getModel()
    utils.set_model_info(model, notes=bounds_notes, creators=creators, units=units, main_units=main_units)

    # dt
    compartment_id = "bioreactor"
    builder.create_dfba_dt(model, time_unit=UNIT_TIME, create_port=True)

    # compartment
    builder.create_dfba_compartment(model, compartment_id=compartment_id, unit_volume=UNIT_VOLUME, create_port=True)

    # dynamic species
    model_fba = doc_fba.getModel()
    builder.create_dfba_species(model, model_fba, compartment_id=compartment_id, unit_amount=UNIT_AMOUNT,
                                create_port=True)
    # bounds
    builder.create_exchange_bounds(model, model_fba=model_fba, unit_flux=UNIT_FLUX, create_ports=True)

    # bounds
    fba_infix = "fba_"
    model_fba = doc_fba.getModel()
    objects = []
    ex_rids = utils.find_exchange_reactions(model_fba)
    for ex_rid, sid in ex_rids.items():
        r = model_fba.getReaction(ex_rid)

        # lower & upper bound parameters
        r_fbc = r.getPlugin(builder.SBML_FBC_NAME)
        lb_id = r_fbc.getLowerFluxBound()
        fba_lb_id = builder.LOWER_BOUND_PREFIX + fba_infix + ex_rid
        lb_value = model_fba.getParameter(lb_id).getValue()

        objects.extend([
            # default bounds from fba
            Parameter(sid=fba_lb_id, value=lb_value, unit=UNIT_FLUX, constant=False),
        ])
    factory.create_objects(model, objects)

    objects = [

        # kinetic lower bounds
        Parameter(sid="lb_kin_EX_Glcxt", value=builder.LOWER_BOUND_DEFAULT, unit=UNIT_FLUX, constant=False,
                     sboTerm="SBO:0000612"),
        Parameter(sid="lb_kin_EX_O2", value=builder.LOWER_BOUND_DEFAULT, unit=UNIT_FLUX, constant=False,
                     sboTerm="SBO:0000612"),

        # parameters for kinetic bounds
        Parameter(sid='Vmax_EX_O2', value=15, unit=UNIT_FLUX, constant=True),
        Parameter(sid='Vmax_EX_Glcxt', value=10, unit=UNIT_FLUX, constant=True),
        Parameter(sid='Km_EX_Glcxt', value=0.015, unit=UNIT_CONCENTRATION, name="Km_vGlcxt", constant=True),

        # kinetic bounds (unintuitive direction due to the identical concentrations in bioreactor and model)
        AssignmentRule(sid="lb_kin_EX_Glcxt", value="-Vmax_EX_Glcxt * Glcxt/(Km_EX_Glcxt + Glcxt)"),
        AssignmentRule(sid="lb_kin_EX_O2", value="-Vmax_EX_O2"),

        # exchange reaction bounds
        # uptake bounds (lower bound)
        # TODO: FIXME the X hack
        # the bounds for the fba model have to be in mmol/h/gdw
        AssignmentRule(sid="lb_EX_Ac", value="max(lb_fba_EX_Ac, -Ac/X/1 l_per_mmol*bioreactor/dt)"),
        AssignmentRule(sid="lb_EX_X", value="max(lb_fba_EX_X, -X/X/1 l_per_mmol*bioreactor/dt)"),
        AssignmentRule(sid="lb_EX_Glcxt", value="max(lb_kin_EX_Glcxt, -Glcxt/X/1 l_per_mmol*bioreactor/dt)"),
        AssignmentRule(sid="lb_EX_O2", value="max(lb_kin_EX_O2, -O2/X/1 l_per_mmol*bioreactor/dt)"),
    ]
    factory.create_objects(model, objects)

    if annotations:
        annotator.annotate_sbml_doc(doc, annotations)
    sbml.write_sbml(doc, filepath=pjoin(directory, sbml_file), validate=True)


####################################################
# ODE species update
####################################################
def update_model(sbml_file, directory, doc_fba=None, annotations=None):
    """
        Submodel for dynamically updating the metabolite count/concentration.
        This updates the ode model based on the FBA fluxes.
    """
    update_notes = notes.format("""
        <h2>UPDATE submodel</h2>
        <p>Submodel for dynamically updating the metabolite count.
        This updates the ode model based on the FBA fluxes.</p>
        """)
    doc = builder.template_doc_update(settings.MODEL_ID)
    model = doc.getModel()
    utils.set_model_info(model, notes=update_notes, creators=creators, units=units, main_units=main_units)

    # compartment
    compartment_id = "bioreactor"
    builder.create_dfba_compartment(model, compartment_id=compartment_id, unit_volume=UNIT_VOLUME, create_port=True)

    # dynamic species
    model_fba = doc_fba.getModel()
    builder.create_dfba_species(model, model_fba, compartment_id=compartment_id, unit_amount=UNIT_AMOUNT,
                                create_port=True)

    # update reactions
    # FIXME: weight with X (biomass)
    builder.create_update_reactions(model, model_fba=model_fba, formula="-{} * X * 1 l_per_mmol", unit_flux=UNIT_FLUX,
                                    modifiers=["X"])

    # write SBML file
    if annotations:
        annotator.annotate_sbml_doc(doc, annotations)
    sbml.write_sbml(doc, filepath=pjoin(directory, sbml_file), validate=True)


def top_model(sbml_file, directory, emds, doc_fba=None, annotations=None):
    """
    Create diauxic comp model.
    Test script for working with the comp extension in SBML.

    One model composition combines all the kinetic models,
    in addition the higher level comp model is created which combines everything (i.e. the FBA & ODE models).
    For the simulation of the full combined model the tools have to figure out the subparts which are
    simulated with which simulation environment.
    Creates the full comp model as combination of FBA and comp models.

    The submodels must already exist in the given directory
    """
    top_notes = notes.format("""
    <h2>TOP model</h2>
    <p>Main comp DFBA model by combining fba, update and bounds
        model with additional kinetics in the top model.</p>
    """)
    # Necessary to change into directory with submodel files
    working_dir = os.getcwd()
    os.chdir(directory)

    doc = builder.template_doc_top(settings.MODEL_ID, emds)
    model = doc.getModel()
    utils.set_model_info(model, notes=top_notes,
                         creators=creators, units=units, main_units=main_units)

    # dt
    builder.create_dfba_dt(model, time_unit=UNIT_TIME, create_port=False)

    # compartment
    compartment_id = "bioreactor"
    builder.create_dfba_compartment(model, compartment_id=compartment_id, unit_volume=UNIT_VOLUME, create_port=False)

    # dynamic species
    model_fba = doc_fba.getModel()
    builder.create_dfba_species(model, model_fba, compartment_id=compartment_id, unit_amount=UNIT_AMOUNT,
                                create_port=False)

    # dummy species
    builder.create_dummy_species(model, compartment_id=compartment_id, unit_amount=UNIT_AMOUNT)

    # exchange flux bounds
    builder.create_exchange_bounds(model, model_fba=model_fba, unit_flux=UNIT_FLUX, create_ports=False)

    # dummy reactions & flux assignments
    builder.create_dummy_reactions(model, model_fba=model_fba, unit_flux=UNIT_FLUX)

    # replacedBy (fba reactions)
    builder.create_top_replacedBy(model, model_fba=model_fba)

    # replaced
    builder.create_top_replacements(model, model_fba, compartment_id=compartment_id)

    # initial kinetic concentrations
    initial_c = {
        'Glcxt': 10.8,
        'Ac': 0.4,
        'O2': 0.21,
        'X': 0.001,
    }
    for sid, value in initial_c.items():
        species = model.getSpecies(sid)
        species.setInitialConcentration(value)

    objects = [
        # biomass conversion factor
        # Parameter(sid="Y", name="biomass [g_per_l]", value=1.0, unit="g_per_l"),
        # oxygen exchange parameters
        Parameter(sid="O2_ref", name="O2 reference", value=0.21, unit=UNIT_CONCENTRATION),
        Parameter(sid="kLa", name="O2 mass transfer", value=7.5, unit='per_h'),
    ]
    factory.create_objects(model, objects)

    # oxygen transfer reaction
    create_reaction(model, rid="vO2_transfer", name="oxygen transfer", reversible=True,
                       reactants={}, products={"O2": 1}, formula="kLa * (O2_ref-O2) * bioreactor",
                       compartment="bioreactor")

    # write SBML file
    if annotations:
        annotator.annotate_sbml_doc(doc, annotations)
    sbml.write_sbml(doc, filepath=os.path.join(directory, sbml_file), validate=True)

    # change back into working dir
    os.chdir(working_dir)


def create_model(output_dir):
    """ Create all models.

    :return:
    """
    directory = utils.versioned_directory(output_dir, version=settings.VERSION)

    f_annotations = os.path.join(os.path.dirname(os.path.abspath(__file__)), settings.ANNOTATIONS_LOCATION)
    annotations = annotator.ModelAnnotator.read_annotations(f_annotations)

    # create sbml
    doc_fba = fba_model(settings.FBA_LOCATION, directory, annotations=annotations)
    bounds_model(settings.BOUNDS_LOCATION, directory, doc_fba=doc_fba, annotations=annotations)
    update_model(settings.UPDATE_LOCATION, directory, doc_fba=doc_fba, annotations=annotations)
    emds = {
        "diauxic_fba": settings.FBA_LOCATION,
        "diauxic_bounds": settings.BOUNDS_LOCATION,
        "diauxic_update": settings.UPDATE_LOCATION,
    }
    top_model(settings.TOP_LOCATION, directory, emds, doc_fba=doc_fba, annotations=annotations)

    # flatten top model
    comp.flattenSBMLFile(sbml_path=pjoin(directory, settings.TOP_LOCATION),
                         output_path=pjoin(directory, settings.FLATTENED_LOCATION))

    # create reports
    locations = [
        settings.FBA_LOCATION,
        settings.BOUNDS_LOCATION,
        settings.UPDATE_LOCATION,
        settings.TOP_LOCATION,
        settings.FLATTENED_LOCATION
    ]

    sbml_paths = [pjoin(directory, fname) for fname in locations]
    sbmlreport.create_reports(sbml_paths, directory, validate=False)

    # create sedml
    from sbmlutils.dfba.sedml import create_sedml
    species_ids = ", ".join(['Ac', 'Glcxt', 'O2', 'X'])
    reaction_ids = ", ".join(['vO2_transfer', 'EX_Ac', 'EX_Glcxt', 'EX_O2', 'EX_X'])
    create_sedml(settings.SEDML_LOCATION, settings.TOP_LOCATION, directory=directory,
                 dt=0.01, tend=15, species_ids=species_ids, reaction_ids=reaction_ids)

    return directory


if __name__ == "__main__":
    directory = create_model(output_dir=settings.OUT_DIR)
