# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 14:32:35 2021

@author: yrc2
"""
from typing import NamedTuple

__all__ = (
    'asconfiguration',
    'ascomparison',
    'Configuration',
    'ConfigurationComparison',
    'name_to_configuration',
    'parse_configuration',
    'format_name',
    'format_configuration',
    'format_comparison',
)

def asconfiguration(x):
    try:
        number, agile, line, case = x
        return Configuration(int(number), bool(agile), line or None)
    except:
        return Configuration(int(x), False, None, None)

def ascomparison(x):
    a, b = x
    return ConfigurationComparison(asconfiguration(a), asconfiguration(b))

class Configuration(NamedTuple):
    number: int
    agile: bool = False
    line: str = None
    case: str = None
   
class ConfigurationComparison(NamedTuple):
    a: Configuration
    b: Configuration

def name_to_configuration(name):
    if '*' in name:
        name = name.strip('*')
        agile = True
    else:
        agile = False
    if '|' in name:
        name, case = name.split('|')
        case = case.rstrip(' ').replace(' ', '_')
    else:
        case = None
    if '.' in name:
        name, line = name.split('.')
        line = line.rstrip(' ')
    else:
        line = None
    name = name.upper().replace(' ', '')
    return Configuration(
        (-1 if name.startswith('S') else 1) * int(name[1:]), 
        agile, 
        line,
        case
    )

def parse_configuration(x):
    if isinstance(x, int):
        return Configuration(x)
    elif isinstance(x, str):
        left, *right = x.split('-')
        if right:
            if len(right) == 1:
                right = right[0]
                return ConfigurationComparison(
                    name_to_configuration(left),
                    name_to_configuration(right)
                )
            else:
                raise RuntimeError('cannot parse multiple subtractions')
        else:
            return name_to_configuration(x)
    elif isinstance(x, (Configuration, ConfigurationComparison)):
        return x
    else:
        try:
            try:
                return asconfiguration(x)
            except:
                return ascomparison(x)
        except:
            raise ValueError(f'could not parse {x}')
    
def format_name(name):
    key = parse_configuration(name)
    if isinstance(key, Configuration):
        return format_configuration(key)
    elif isinstance(key, ConfigurationComparison):
        return format_comparison(key)
    else:
        raise Exception('unknown error')

def format_configuration(configuration, latex=True):
    number, agile, line, case = configuration
    if number < 0:
        name = f"S{number}"
    else:
        name = f"O{number}"
    if number == 0 or number > 10 or number < -3: 
        raise ValueError(f'invalid configuration {configuration}')
    if line: name += "." + line
    if case: name += '|' + case
    if latex:
        name = r'$\mathtt{' + name + '}$'
    if agile: name += '*'
    return name

def format_comparison(comparison):
    return ' $-$ '.join([format_configuration(i) for i in comparison])

