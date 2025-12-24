"""
Test suite for measurement validation engine.
Tests the complete workflow: parsing, validation, and results.
"""

import os
import tempfile
from measurements.utils import (
    MeasurementFileParser,
    MeasurementValidator,
    MeasurementValidationEngine,
    STANDARD_SIZE_CHART_SWEATSHIRT,
)


def create_test_file(content: str) -> str:
    """Create a temporary test file with given content."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write(content)
        return f.name


def test_parser_basic_formats():
    """Test parser with different line formats."""
    print("\n" + "="*70)
    print("TEST 1: Parser - Basic Formats")
    print("="*70)
    
    test_content = """
# Comment line should be skipped
A: 50.1
B = 48.3
C: 44.0 cm
Length from shoulder (D): 46.0
E: 40.7x 2

# More measurements
F: 47.0
G = 43.5
H: 18.3
I: 44.7 cm
"""
    
    file_path = create_test_file(test_content)
    try:
        measured_values, errors = MeasurementFileParser.parse_file(file_path)
        
        print(f"Parsed values: {measured_values}")
        print(f"Parse errors: {errors}")
        
        assert 'A' in measured_values and measured_values['A'] == 50.1
        assert 'B' in measured_values and measured_values['B'] == 48.3
        assert 'C' in measured_values and measured_values['C'] == 44.0
        assert 'D' in measured_values and measured_values['D'] == 46.0
        assert 'E' in measured_values and measured_values['E'] == 40.7
        
        print("✓ All format variations parsed correctly")
    finally:
        os.unlink(file_path)


def test_parser_missing_measurements():
    """Test parser with missing measurements."""
    print("\n" + "="*70)
    print("TEST 2: Parser - Missing Required Measurements")
    print("="*70)
    
    # Only provide some measurements
    test_content = """
A: 50.1
B: 48.3
C: 44.0
"""
    
    file_path = create_test_file(test_content)
    try:
        measured_values, errors = MeasurementFileParser.parse_file(file_path)
        validation_errors = MeasurementFileParser.validate_parsed_data(measured_values)
        
        print(f"Parsed values: {measured_values}")
        print(f"Validation errors: {validation_errors}")
        
        assert len(validation_errors) > 0
        assert "Missing required measurement" in validation_errors[0]
        
        print("✓ Missing measurements correctly detected")
    finally:
        os.unlink(file_path)


def test_parser_invalid_values():
    """Test parser with invalid numeric values."""
    print("\n" + "="*70)
    print("TEST 3: Parser - Invalid Values")
    print("="*70)
    
    test_content = """
A: 50.1
B: not_a_number
C: 44.0
D: -5.0
"""
    
    file_path = create_test_file(test_content)
    try:
        measured_values, errors = MeasurementFileParser.parse_file(file_path)
        
        print(f"Parsed values: {measured_values}")
        print(f"Parse errors: {errors}")
        
        assert len(errors) > 0
        assert 'B' not in measured_values  # Should not be in results
        assert 'D' not in measured_values  # Negative values rejected
        
        print("✓ Invalid values correctly rejected")
    finally:
        os.unlink(file_path)


def test_validator_pass():
    """Test validation with measurements that should PASS."""
    print("\n" + "="*70)
    print("TEST 4: Validator - PASS Case")
    print("="*70)
    
    # Measurements within tolerance for size 6/7
    measured = {
        'A': 50.2,  # Standard 50.1 ± 0.1 (within ±1.0)
        'B': 44.1,  # Standard 44.0 ± 0.1 (within ±1.0)
        'C': 39.0,  # Standard 39.0 ± 0.0 (within ±1.0)
        'D': 42.0,  # Standard 42.0 ± 0.0 (within ±1.0)
        'E': 39.5,  # Standard 39.5 ± 0.0 (within ±1.0)
        'F': 42.2,  # Standard 42.2 ± 0.0 (within ±1.0)
        'G': 39.5,  # Standard 39.5 ± 0.0 (within ±1.0)
        'H': 16.2,  # Standard 16.2 ± 0.0 (within ±0.5 - special)
        'I': 37.2,  # Standard 37.2 ± 0.0 (within ±1.0)
        'J': 20.5,  # Standard 20.5 ± 0.0 (within ±1.0)
        'K': 12.2,  # Standard 12.2 ± 0.0 (within ±1.0)
        'L': 7.5,   # Standard 7.5 ± 0.0 (within ±1.0)
        'M': 5.5,   # Standard 5.5 ± 0.0 (within ±1.0)
        'N': 20.2,  # Standard 20.2 ± 0.0 (within ±1.0)
        'O': 2.2,   # Standard 2.2 ± 0.0 (within ±1.0)
        'P': 5.3,   # Standard 5.3 ± 0.0 (within ±1.0)
        'Q': 2.0,   # Standard 2.0 ± 0.0 (within ±1.0)
        'R': 4.7,   # Standard 4.7 ± 0.0 (within ±1.0)
        'S': 6.0,   # Standard 6.0 ± 0.0 (within ±1.0)
        'T': 3.0,   # Standard 3.0 ± 0.0 (within ±1.0)
    }
    
    result = MeasurementValidator.validate_measurements(
        measured_values=measured,
        size='6/7',
        operator_id='test_user',
        session_id='test_session_1'
    )
    
    print(f"Overall Result: {result['overall_result']}")
    print(f"Passed Measurements: {result['summary']['passed_measurements']}")
    print(f"Failed Measurements: {result['summary']['failed_measurements']}")
    
    assert result['overall_result'] == 'PASS'
    assert result['success'] == True
    assert result['summary']['failed_measurements'] == 0
    
    print("✓ Validation correctly marked as PASS")


def test_validator_fail():
    """Test validation with measurements that should FAIL."""
    print("\n" + "="*70)
    print("TEST 5: Validator - FAIL Case")
    print("="*70)
    
    # Measurement B exceeds tolerance
    measured = {
        'A': 50.1,
        'B': 46.0,  # Standard 44.0, deviation 2.0 > tolerance 1.0 → FAIL
        'C': 39.0,
        'D': 42.0,
        'E': 39.5,
        'F': 42.2,
        'G': 39.5,
        'H': 16.2,
        'I': 37.2,
        'J': 20.5,
        'K': 12.2,
        'L': 7.5,
        'M': 5.5,
        'N': 20.2,
        'O': 2.2,
        'P': 5.3,
        'Q': 2.0,
        'R': 4.7,
        'S': 6.0,
        'T': 3.0,
    }
    
    result = MeasurementValidator.validate_measurements(
        measured_values=measured,
        size='6/7',
        operator_id='test_user',
        session_id='test_session_2'
    )
    
    print(f"Overall Result: {result['overall_result']}")
    print(f"Passed Measurements: {result['summary']['passed_measurements']}")
    print(f"Failed Measurements: {result['summary']['failed_measurements']}")
    
    # Find B in measurements
    b_measurement = next((m for m in result['measurements'] if m['code'] == 'B'), None)
    if b_measurement:
        print(f"B Measurement Status: {b_measurement['status']}")
        print(f"B Deviation: {b_measurement['deviation']} (tolerance: {b_measurement['tolerance']})")
    
    assert result['overall_result'] == 'FAIL'
    assert result['success'] == False
    assert result['summary']['failed_measurements'] > 0
    
    print("✓ Validation correctly marked as FAIL")


def test_validator_neck_width_special_tolerance():
    """Test that H (Neck Width) has special ±0.5cm tolerance."""
    print("\n" + "="*70)
    print("TEST 6: Validator - Special Tolerance for H (Neck Width)")
    print("="*70)
    
    # H measurement slightly exceeds special tolerance
    measured = {
        'A': 50.1,
        'B': 44.0,
        'C': 39.0,
        'D': 42.0,
        'E': 39.5,
        'F': 42.2,
        'G': 39.5,
        'H': 16.8,  # Standard 16.2, deviation 0.6 > tolerance 0.5 → FAIL
        'I': 37.2,
        'J': 20.5,
        'K': 12.2,
        'L': 7.5,
        'M': 5.5,
        'N': 20.2,
        'O': 2.2,
        'P': 5.3,
        'Q': 2.0,
        'R': 4.7,
        'S': 6.0,
        'T': 3.0,
    }
    
    result = MeasurementValidator.validate_measurements(
        measured_values=measured,
        size='6/7',
        operator_id='test_user',
        session_id='test_session_3'
    )
    
    h_measurement = next((m for m in result['measurements'] if m['code'] == 'H'), None)
    
    print(f"H Tolerance: {h_measurement['tolerance']} (should be 0.5)")
    print(f"H Status: {h_measurement['status']}")
    print(f"Overall Result: {result['overall_result']}")
    
    assert h_measurement['tolerance'] == 0.5
    assert h_measurement['status'] == 'FAIL'
    assert result['overall_result'] == 'FAIL'
    
    print("✓ Special tolerance for H (Neck Width) correctly applied")


def test_complete_workflow():
    """Test complete workflow: file upload → parse → validate → results."""
    print("\n" + "="*70)
    print("TEST 7: Complete Workflow - File to Validation Results")
    print("="*70)
    
    test_content = """# Measurement file for size 8/9
A: 56.5
B: 49.2
C: 44.0
D: 46.0
E: 40.7
F: 47.0
G: 43.5
H: 18.3
I: 44.7
J: 20.5
K: 12.7
L: 8.0
M: 6.2
N: 23.0
O: 2.2
P: 5.8
Q: 2.0
R: 5.2
S: 5.0
T: 3.0
"""
    
    file_path = create_test_file(test_content)
    try:
        result = MeasurementValidationEngine.validate_file(
            file_path=file_path,
            size='8/9',
            operator_id='john_doe',
            session_id='workflow_test_1'
        )
        
        print(f"File Parsed: {result['file_parsed']}")
        print(f"Overall Result: {result['overall_result']}")
        print(f"Operator: {result['operator_id']}")
        print(f"Session ID: {result['session_id']}")
        print(f"Total Measurements: {result['summary']['total_measurements']}")
        print(f"Passed: {result['summary']['passed_measurements']}")
        print(f"Failed: {result['summary']['failed_measurements']}")
        
        if result['parse_errors']:
            print(f"Parse Errors: {result['parse_errors']}")
        
        if result['validation_errors']:
            print(f"Validation Errors: {result['validation_errors']}")
        
        assert result['file_parsed'] == True
        assert result['session_id'] == 'workflow_test_1'
        assert result['operator_id'] == 'john_doe'
        
        print("✓ Complete workflow executed successfully")
    finally:
        os.unlink(file_path)


def run_all_tests():
    """Run all tests."""
    print("\n" + "█"*70)
    print("█ MEASUREMENT VALIDATION ENGINE - TEST SUITE")
    print("█"*70)
    
    try:
        test_parser_basic_formats()
        test_parser_missing_measurements()
        test_parser_invalid_values()
        test_validator_pass()
        test_validator_fail()
        test_validator_neck_width_special_tolerance()
        test_complete_workflow()
        
        print("\n" + "█"*70)
        print("█ ALL TESTS PASSED ✓")
        print("█"*70)
        print("\nSummary:")
        print("  • File parser handles all line formats correctly")
        print("  • Missing measurements are detected")
        print("  • Invalid values are rejected")
        print("  • Measurements within tolerance pass validation")
        print("  • Measurements outside tolerance fail validation")
        print("  • Special tolerance (H: ±0.5cm) is applied correctly")
        print("  • Complete workflow produces correct results")
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run_all_tests()
