# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 14:39:10 2021

@author: yrc2
"""
from . import _feature_mockups as f
from ._parse_configuration import parse_configuration, Configuration, ConfigurationComparison
from warnings import warn
from thermosteam.utils import roundsigfigs
import biorefineries.oilcane as oc
import os
import pandas as pd
import numpy as np
import biosteam as bst
from typing import NamedTuple
from biorefineries.cane.composition import get_composition, set_composition

__all__ = (
    'images_folder',
    'results_folder',
    'feedstocks_folder',
    'get_composition_data',
    'spearman_file',
    'monte_carlo_file',
    'autoload_file_name',
    'get_monte_carlo_across_oil_content',
    'get_monte_carlo',
    'get_line_monte_carlo',
    'load_composition',
    'montecarlo_results',
    'montecarlo_results_short',
    'montecarlo_results_feedstock_comparison',
    'montecarlo_results_configuration_comparison',
    'montecarlo_results_agile_comparison',
    'montecarlo_results_crude_comparison',
    'get_minimum_GWP_reduction',
)

results_folder = os.path.join(os.path.dirname(__file__), 'results')
images_folder = os.path.join(os.path.dirname(__file__), 'images')
feedstocks_folder = os.path.join(os.path.dirname(__file__), 'feedstocks')

# %% Load feedstock data

cane_line_composition_data = None

class OilcaneCompositionPerformance(NamedTuple):
    oil_content: float
    biomass_yield: float

def get_composition_data():
    global cane_line_composition_data
    if cane_line_composition_data is None:
        file = os.path.join(feedstocks_folder, 'cane_composition_data.xlsx')
        data = pd.read_excel(file, header=[0, 1], index_col=[0])
        # Filter poor lines 
        index = data.index
        good_lines = set(index)
        performances = {}
        for name in index:
            line = data.loc[name]
            performance = OilcaneCompositionPerformance(
                line['Stem Oil (dw)']['Mean'],
                line['Dry biomass yield (% WT)']['Mean'],
            )
            performances[name] = performance
        for name, performance in performances.items():
            for other_name, other_performance in performances.items():
                if (name != other_name 
                    and performance.oil_content < other_performance.oil_content
                    and performance.biomass_yield < other_performance.biomass_yield):
                    good_lines.discard(name)
        names = sorted([name for name in index if name in good_lines], 
                       key=lambda name: performances[name].oil_content)
        cane_line_composition_data = data.loc[names]
    return cane_line_composition_data

def load_composition(feedstock, oil, fiber, water, FFA, PL):
    composition = get_composition(feedstock)
    composition['lipid'] = oil
    composition['fiber'] = fiber
    composition['moisture'] = water
    composition['TAG'] = 1. - FFA - PL
    composition['FFA'] = FFA
    composition['PL'] = PL
    del composition['sugar'] # Sugar is backcalculated in `set_composition`
    set_composition(feedstock, **composition)

# %% Load simulation data

def spearman_file(name):
    number, agile = parse_configuration(name)
    filename = f'oilcane_spearman_{number}'
    if agile: filename += '_agile'
    filename += '.xlsx'
    return os.path.join(results_folder, filename)

def monte_carlo_file(name, across_lines=False, extention='xlsx'):
    number, agile, energycane = parse_configuration(name)
    filename = f'oilcane_monte_carlo_{number}'
    if agile: filename += '_agile'
    if energycane: filename += '_energycane'
    if across_lines: filename += '_across_lines'
    filename += '.' + extention
    return os.path.join(results_folder, filename)

def autoload_file_name(name):
    filename = str(name).replace('*', '_agile')
    return os.path.join(results_folder, filename)

def get_monte_carlo_across_oil_content(name, metric, derivative=False):
    key = parse_configuration(name)
    if isinstance(key, Configuration):
        df = pd.read_excel(
            monte_carlo_file(key, True),
            sheet_name=metric if isinstance(metric, str) else metric.short_description,
            index_col=0
        )
    elif isinstance(key, ConfigurationComparison):
        df = (
            get_monte_carlo_across_oil_content(key.a, metric)
            - get_monte_carlo_across_oil_content(key.b, metric)
        )
    else:
        raise Exception('unknown error')
    if derivative: 
        arr = np.diff(df.values) / np.diff(df.columns.values) / 100.
    else:
        arr = df.values
    return arr
        
def get_monte_carlo_key(index, dct, with_units=False):
    key = index[1] if with_units else index[1].split(' [')[0]
    if key in dct: key = f'{key}, {index[0]}'
    return key

def get_line_monte_carlo(line, name, feature, cache={}):
    configuration = parse_configuration(name)
    key = (*configuration, feature.short_description)
    if isinstance(configuration, Configuration):
        if key in cache:
            df = cache[key]
        else:
            file = monte_carlo_file(configuration, across_lines=True)
            cache[key] = df = pd.read_excel(file, header=[0, 1], index_col=[0], sheet_name=feature.short_description)
        mc = df[line]
    elif isinstance(configuration, ConfigurationComparison):
        raise ValueError('name cannot be a configuration comparison')
    else:
        raise Exception('unknown error')
    mc = mc.dropna(how='all', axis=0)
    return mc

def get_monte_carlo(name, features=None, cache={}):
    key = parse_configuration(name)
    if isinstance(key, Configuration):
        if key in cache:
            df = cache[key]
        else:
            file = monte_carlo_file(key)
            cache[key] = df = pd.read_excel(file, header=[0, 1], index_col=[0])
        if features is None:
            mc = df
        elif isinstance(features, bst.Feature):
            mc = df[features.index]
        else:
            mc = df[[i.index for i in features]]
    elif isinstance(key, ConfigurationComparison):
        if features is None:
            features = (
                *f.tea_monte_carlo_metric_mockups, 
                *f.tea_monte_carlo_derivative_metric_mockups,
                *f.lca_monte_carlo_metric_mockups, 
                *f.lca_monte_carlo_derivative_metric_mockups,
                f.GWP_ethanol_displacement,
                f.GWP_ethanol_allocation,
            )
        if isinstance(features, bst.Feature):
            index = features.index
        else:
            index = [i.index for i in features]
        df_a = get_monte_carlo(key.a)[index]
        df_b = get_monte_carlo(key.b)[index]
        row_a = df_a.shape[0]
        row_b = df_b.shape[0]
        try:
            assert row_a == row_b, "shape mismatch"
        except:
            breakpoint()
        mc = df_a - df_b
    else:
        raise Exception('unknown error')
    mc = mc.dropna(how='all', axis=0)
    return mc


def montecarlo_results(with_units=False):
    results = {}    
    for name in oc.configuration_names + oc.comparison_names:
        try: 
            df = get_monte_carlo(name)
        except:
            warn(f'could not load {name}', RuntimeWarning)
            continue
        results[name] = dct = {}
        # if name in ('O1', 'O2'):
        #     index = f.ethanol_over_biodiesel.index
        #     key = get_monte_carlo_key(index, dct, with_units)
        #     data = df[f.ethanol_production.index].values / df[f.biodiesel_production.index].values
        #     q05, q25, q50, q75, q95 = np.percentile(data, [5,25,50,75,95], axis=0)
        #     dct[key] = {
        #         'mean': np.mean(data),
        #         'std': np.std(data),
        #         'q05': q05,
        #         'q25': q25,
        #         'q50': q50,
        #         'q75': q75,
        #         'q95': q95,
        #     }
        for metric in (*f.tea_monte_carlo_metric_mockups, *f.tea_monte_carlo_derivative_metric_mockups,
                       *f.lca_monte_carlo_metric_mockups, *f.lca_monte_carlo_derivative_metric_mockups,
                       f.GWP_ethanol_displacement, f.GWP_ethanol_allocation):
            index = metric.index
            data = df[index].values
            q05, q25, q50, q75, q95 = np.percentile(data, [5,25,50,75,95], axis=0)
            key = get_monte_carlo_key(index, dct, with_units)
            dct[key] = {
                'mean': np.mean(data),
                'std': np.std(data),
                'q05': q05,
                'q25': q25,
                'q50': q50,
                'q75': q75,
                'q95': q95,
            }
    try:
        df_O2O1 = get_monte_carlo('O2 - O1')
        df_O1 = get_monte_carlo('O1')
    except:
        warn('could not load O2 - O1', RuntimeWarning)
    else:
        results['(O2 - O1) / O1'] = relative_results = {}
        for metric in (f.biodiesel_production, f.ethanol_production):
            index = metric.index
            key = index[1] if with_units else index[1].split(' [')[0]
            data = (df_O2O1[index].values / df_O1[index].values)
            q05, q25, q50, q75, q95 = np.percentile(data, [5,25,50,75,95], axis=0)
            relative_results[key] = {
                'mean': np.mean(data),
                'std': np.std(data),
                'q05': q05,
                'q25': q25,
                'q50': q50,
                'q75': q75,
                'q95': q95,
            }
    return results

# %% Monte carlo values for manuscript

def get_minimum_GWP_reduction():
    L_per_gal = 3.7854
    gal_per_GGE_ethanol = 1.5
    L_per_GGE_ethanol = L_per_gal * gal_per_GGE_ethanol
    gal_per_GGE_biodiesel = 0.9536
    L_per_GGE_biodiesel = L_per_gal * gal_per_GGE_biodiesel
    GWP_ethanol_economic = GWP_biodiesel_economic = 0
    GWP_ethanol_energy = GWP_biodiesel_energy = 0
    GWP_ethanol_economic_index = f.GWP_ethanol.index
    GWP_ethanol_energy_index = f.GWP_ethanol_allocation.index
    GWP_biodiesel_economic_index = f.GWP_biodiesel.index
    GWP_biodiesel_energy_index = f.GWP_biodiesel_allocation.index
    # https://www.epa.gov/sites/default/files/2016-07/documents/select-ghg-results-table-v1.pdf
    GWP_ethanol_dist_and_use = 3.7 * 114000 / 1e6 # kgCO2e per GGE
    GWP_biodiesel_dist_and_use = 3.4 * 114000 / 1e6 # kgCO2e per GGE
    for name in ('O1', 'O2'): 
        df = get_monte_carlo(name)
        GWP_ethanol_economic = max(GWP_ethanol_economic, df[GWP_ethanol_economic_index].max())
        GWP_ethanol_energy = max(GWP_ethanol_energy, df[GWP_ethanol_energy_index].max())
        GWP_biodiesel_economic = max(GWP_biodiesel_economic, df[GWP_biodiesel_economic_index].max())
        GWP_biodiesel_energy = max(GWP_biodiesel_energy, df[GWP_biodiesel_energy_index].max())
    # https://www.epa.gov/sites/default/files/2016-07/documents/select-ghg-results-table-v1.pdf
    GWP_ethanol_economic *= L_per_GGE_ethanol # per L to per GGE
    GWP_ethanol_energy *= L_per_GGE_ethanol # per L to per GGE
    GWP_biodiesel_economic *= L_per_GGE_biodiesel # per L to per GGE
    GWP_biodiesel_energy *= L_per_GGE_biodiesel # per L to per GGE
    GWP_diesel = 11.058 # kgCO2e per GGE
    GWP_gasoline = 11.1948 # kgCO2e per GGE
    return {
        'Ethanol-economic': 100 * (1 - (GWP_ethanol_economic + GWP_ethanol_dist_and_use) / GWP_gasoline),
        'Ethanol-energy': 100 * (1 - (GWP_ethanol_energy + GWP_ethanol_dist_and_use)/ GWP_gasoline),
        'Biodiesel-economic': 100 * (1 - (GWP_biodiesel_economic + GWP_biodiesel_dist_and_use)/ GWP_diesel),
        'Biodiesel-energy': 100 * (1 - (GWP_biodiesel_energy + GWP_biodiesel_dist_and_use) / GWP_diesel),
    }

def montecarlo_results_short(names, metrics=None, derivative=None):
    if metrics is None:
        if derivative:
            metrics = [
                f.MFPP_derivative, f.TCI_derivative, f.ethanol_production_derivative, f.biodiesel_production_derivative, 
                f.electricity_production_derivative, f.natural_gas_consumption_derivative, 
                f.GWP_ethanol_derivative, 
            ]
        else:
            metrics = [
                f.MFPP, f.TCI, f.ethanol_production, f.biodiesel_production, 
                f.electricity_production, f.natural_gas_consumption, f.GWP_ethanol_displacement, 
                f.GWP_ethanol, f.GWP_ethanol_allocation, 
            ]
    results = {}
    for name in names:
        df = get_monte_carlo(name)
        results[name] = dct = {}
        for metric in metrics:
            index = metric.index
            data = df[index].values
            q05, q50, q95 = roundsigfigs(np.percentile(data, [5, 50, 95], axis=0), 3)
            key = get_monte_carlo_key(index, dct, False)
            if q50 < 0:
                dct[key] = f"{-q50} [{-q95}, {-q05}] -negative-"
            else:
                dct[key] = f"{q50} [{q05}, {q95}]"
        if name == 'O2 - O1':
            df_O2O1 = df
            df_O1 = get_monte_carlo('O1')
            for metric in (f.biodiesel_production, f.ethanol_production):
                index = metric.index
                key = f"% {get_monte_carlo_key(index, {}, False)} increase"
                data = 100. * (df_O2O1[index].values / df_O1[index].values)
                q05, q50, q95 = roundsigfigs(np.percentile(data, [5, 50, 95], axis=0), 3)
                if q50 < 0:
                    dct[key] = f"{-q50} [{-q95}, {-q05}] -negative-"
                else:
                    dct[key] = f"{q50} [{q05}, {q95}]"
    return results

def montecarlo_results_feedstock_comparison():
    return montecarlo_results_short(
        names = [
            'O1 - S1',
            'O2 - S2',
        ],
    )
    
def montecarlo_results_configuration_comparison():
    return montecarlo_results_short(
        names = [
            'O2 - O1',
            'O1 - O3',
            'O2 - O4',
        ],
    )

def montecarlo_results_agile_comparison():
    return montecarlo_results_short(
        names = [
            'O1* - O1',
            'O2* - O2',
        ],
    )

def montecarlo_results_crude_comparison():
    return montecarlo_results_short(
        names = [
            'O1 - O3',
            'O2 - O4',
        ],
    )
