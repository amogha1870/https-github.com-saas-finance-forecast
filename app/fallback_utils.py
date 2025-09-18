# app/fallback_utils.py
import re

def parse_amount(s):
    if not s: return None
    s = s.replace(',', '').lower().strip()
    m = re.search(r'([\d\.]+)\s*([km]?)', s)
    if not m: return None
    v = float(m.group(1))
    suf = m.group(2)
    if suf == 'k': v *= 1_000
    if suf == 'm': v *= 1_000_000
    return int(v)

def parse_duration(s):
    m = re.search(r'(\d+)\s*(months|month|mo|m|yrs|years|year)', s)
    if not m: return None
    n = int(m.group(1))
    if re.search(r'year|yrs|years', m.group(2)):
        return n * 12
    return n

def parse_initial_salespeople(s):
    m = re.search(r'start(ing)?\s*(with\s*)?(\d+)\s*(sales|salesperson|sales ?exec|sales ?rep|rep|reps|people)', s)
    if m: return int(m.group(3))
    m2 = re.search(r'(\d+)\s*(salespeople|sales people|sales execs|sales reps)', s)
    if m2: return int(m2.group(1))
    return None

def parse_new_sales_per_month(s):
    m = re.search(r'(add|adding|added)\s*(\d+)\s*(new\s*)?(sales|salesperson|sales ?exec|rep|rep(s)?)\s*(per|a)?\s*(month|monthly|mo)?', s)
    if m: return int(m.group(2))
    m2 = re.search(r'(\d+)\s*(new )?.*(per|a)?\s*(month|monthly|mo)', s)
    if m2: return int(m2.group(1))
    return None

def parse_marketing(s):
    m = re.search(r'([\$\d\.,kKmM]+)\s*(marketing|marketing spend|ads|ad spend|marketing budget)', s)
    if m:
        return parse_amount(m.group(1))
    m2 = re.search(r'([\d\.]+)\s*([kKmM])\s*/\s*(month|mo)', s)
    if m2:
        val = parse_amount(m2.group(1)+m2.group(2))
        return val
    return None

