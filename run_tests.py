#!/usr/bin/env python
"""Quick test script for validation engine"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magic_qc.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

# Run tests
from measurements.test_validation_engine import run_all_tests
run_all_tests()
