# -*- coding: utf-8 -*-
# BioSTEAM: The Biorefinery Simulation and Techno-Economic Analysis Modules
# Copyright (C) 2020, Yoel Cortes-Pena <yoelcortes@gmail.com>
# 
# This module is under the UIUC open-source license. See 
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.
"""
"""
import biosteam as bst
from biosteam import main_flowsheet as f
from biosteam import SystemFactory
from ..juicing import (
    create_juicing_system,
    create_feedstock_handling_system,
)
from ..sugarcane import create_sucrose_to_ethanol_system
from ..lipid_extraction import create_post_fermentation_oil_separation_system
from ... import streams as s

__all__ = (
    'create_oilcane_to_crude_oil_and_ethanol_1g',
)

@SystemFactory(
    ID='oilcane_sys',
    ins=[s.oilcane],
    outs=[s.ethanol, s.crude_oil, s.vinasse], 
)
def create_oilcane_to_crude_oil_and_ethanol_1g(
        ins, outs,
        evaporator_and_beer_column_heat_integration=True,
        WWT_kwargs=None,
    ):
    oilcane, = ins
    ethanol, crude_oil, vinasse = outs
    
    feedstock_handling_sys = create_feedstock_handling_system(
        ins=oilcane,
        outs='',
        mockup=True,
        area=100
    )
    
    ### Oil and juice separation ###
    
    juicing_sys, jdct = create_juicing_system(
        ins=feedstock_handling_sys-0,
        outs=['', '', 'fiber_fines'],
        pellet_bagasse=False,
        dry_bagasse=True,
        mockup=True,
        udct=True,
        area=200,
    )
    screened_juice, bagasse, fiber_fines = juicing_sys.outs
    # bagasse_pelleting_sys = create_bagasse_pelleting_system(None, bagasse, area=200, mockup=True)
    # pelleted_bagasse, = bagasse_pelleting_sys.outs
    jdct['S201'].isplit['Lipid'] = 1. # Vibrating screen
    crushing_mill = jdct['U201']
    crushing_mill.tag = "oil extraction"
    crushing_mill.isplit['Lipid'] = 0.90
    
    ### Ethanol section ###
    
    ethanol_production_sys, epdct = create_sucrose_to_ethanol_system(
        ins=[screened_juice, 'denaturant'],
        outs=[ethanol, '', '', ''],
        mockup=True,
        area=300,
        add_urea=True,
        udct=True,
    )
    ethanol, stillage, stripper_bottoms_product, evaporator_condensate_a = ethanol_production_sys.outs
    post_fermentation_oil_separation_sys = create_post_fermentation_oil_separation_system(
        ins=stillage,
        outs=[crude_oil, '', ''],
        mockup=True,
        area=400,
    )
    crude_oil, thick_vinasse, evaporator_condensate_b = post_fermentation_oil_separation_sys.outs
    MX1 = bst.Mixer(400, [thick_vinasse, evaporator_condensate_a], vinasse)
    MX2 = bst.Mixer(700, [bagasse])
    
    ### Facilities ###
    
    u = f.unit
    if WWT_kwargs:
        outs.remove(vinasse)
        wastewater_treatment_sys = bst.create_wastewater_treatment_system(
            area=1000, ins=[MX1-0], mockup=True, **WWT_kwargs
        )
        treated_water = wastewater_treatment_sys.get_outlet('RO_treated_water')
        sludge = wastewater_treatment_sys.get_outlet('sludge')
        MX2.ins.append(sludge)
        biogas = wastewater_treatment_sys.get_outlet('biogas')
    else:
        treated_water = ''
        biogas = ''
    
    
    bst.BoilerTurbogenerator(700,
        (MX2-0, biogas, 
         'boiler_makeup_water',
         'natural_gas',
         'FGD_lime',
         'boilerchems'),
        ('emissions', 'rejected_water_and_blowdown', 'ash_disposal'),
        turbogenerator_efficiency=0.85
    )
    bst.CoolingTower(800)
    MX = bst.Mixer(800, [evaporator_condensate_b, stripper_bottoms_product], 'recycle_process_water')
    bst.ChilledWaterPackage(800)
    bst.ProcessWaterCenter(800, [treated_water, 'makeup_RO_water', MX-0, 'makeup_water'], 
                           process_water_price=0.000254)
    HXN = bst.HeatExchangerNetwork(900, 
        ignored=lambda: [u.E301],
        Qmin=1e5,
    )
    HXN.acceptable_energy_balance_error = 0.01
