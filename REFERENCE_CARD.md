# MEASUREMENT VALIDATION ENGINE - REFERENCE CARD

## 🎯 Quick Reference

### Core Classes Location
```
measurements/utils.py
├── MeasurementFileParser      (150 lines)
├── MeasurementValidator       (200 lines)
└── MeasurementValidationEngine (150 lines)
```

### Main Entry Point
```python
from measurements.utils import MeasurementValidationEngine

result = MeasurementValidationEngine.validate_file(
    file_path='measurements.txt',
    size='8/9',
    operator_id='john_doe',
    session_id='unique_id'
)
```

---

## 📝 File Format Specification

### Accepted Formats
```
A: 50.1              # Format 1: Colon separator
B = 48.3             # Format 2: Equals separator  
C: 44.0 cm           # Format 3: With unit
D: 46.0x 2           # Format 4: With ignored suffix
Length from shoulder (E): 40.7  # Format 5: Descriptive
```

### Requirements
- File type: `.txt` only
- Encoding: UTF-8
- One measurement per line
- Codes: A-T (required) + PRINT_PLACEMENT_FROM_CF (optional)
- Values: Positive numbers only

### Invalid Content (Rejected)
```
B: not_a_number      # Non-numeric → FAIL
D: -5.0              # Negative → FAIL
X: 50.0              # Invalid code → FAIL
A: 50.0              # Duplicate key → FAIL
```

---

## ⚖️ Tolerance Reference

### Standard Tolerance
```
H (Neck Width):  ±0.5 cm  (SPECIAL - STRICT)
All others:      ±1.0 cm  (DEFAULT)
```

### Examples
```
Measurement B (standard 44.0):
  Measured: 44.9 cm  → Deviation: 0.9 cm  → PASS (< 1.0)
  Measured: 45.2 cm  → Deviation: 1.2 cm  → FAIL (> 1.0)

Measurement H (standard 16.2):
  Measured: 16.6 cm  → Deviation: 0.4 cm  → PASS (< 0.5)
  Measured: 16.8 cm  → Deviation: 0.6 cm  → FAIL (> 0.5)
```

---

## 📊 Size Chart Summary

### Available Sizes
```
6/7   (6-7 years old)
7/8   (7-8 years old)
8/9   (8-9 years old)
9/10  (9-10 years old)
11/12 (11-12 years old)
13/14 (13-14 years old)
```

### All Measurements (20 required + 1 optional)

| Code | Name | Default Tolerance |
|------|------|-------------------|
| A | Length from shoulder | ±1.0 cm |
| B | Chest Width | ±1.0 cm |
| C | Chest Width (1/2 Armhole) | ±1.0 cm |
| D | Bottom width (Above Waistband) | ±1.0 cm |
| E | Hem Width | ±1.0 cm |
| F | Back Width | ±1.0 cm |
| G | Back Width (1/2 Armhole) | ±1.0 cm |
| H | Neck Width (Seam to Seam) | **±0.5 cm** |
| I | Sleeve Length | ±1.0 cm |
| J | Sleeve Width | ±1.0 cm |
| K | Sleeve Width (Above Cuff) | ±1.0 cm |
| L | Sleeve Opening | ±1.0 cm |
| M | Cuff Length | ±1.0 cm |
| N | Armhole | ±1.0 cm |
| O | Back Neck Drop | ±1.0 cm |
| P | Front Neck Drop | ±1.0 cm |
| Q | Collar Width | ±1.0 cm |
| R | Shoulder Drop | ±1.0 cm |
| S | Waistband Length | ±1.0 cm |
| T | Forward Shoulder Seam | ±1.0 cm |
| PRINT_PLACEMENT_FROM_CF | Print Placement (Optional) | ±1.0 cm |

---

## 🔌 API Endpoints

### 1. Upload & Validate
```http
POST /measurements/upload-and-analyze/
Content-Type: multipart/form-data

measurement_file: <file>      # Required: .txt file
size: 8/9                      # Required: Size code

Response:
{
  "status": "success",
  "validation_result": { ... },
  "session_id": "uuid",
  "file_name": "measurements.txt"
}
```

### 2. Get Available Sizes
```http
GET /measurements/get-available-sizes/

Response:
{
  "status": "success",
  "sizes": ["6/7", "7/8", "8/9", "9/10", "11/12", "13/14"]
}
```

### 3. Get Size Chart
```http
GET /measurements/get-size-chart/?size=8/9

Response:
{
  "status": "success",
  "size": "8/9",
  "chart": {
    "A": 56.5,
    "B": 49.2,
    ...
  }
}
```

---

## 📤 Validation Result Structure

### Complete Result
```json
{
  "success": true,                    // Overall pass/fail
  "file_parsed": true,                // File successfully parsed
  "validation_passed": true,          // All measurements passed
  "size": "8/9",                      // Selected size
  "timestamp": "2025-12-20T10:30:00", // ISO format
  "operator_id": "john_doe",          // User ID
  "session_id": "uuid-string",        // Session identifier
  "parse_errors": [],                 // File parsing errors
  "validation_errors": [],            // Validation errors
  "overall_result": "PASS",           // PASS or FAIL
  
  "measurements": [
    {
      "code": "A",
      "measurement_name": "Length from shoulder",
      "measured_value": 56.5,
      "standard_value": 56.5,
      "deviation": 0.0,
      "tolerance": 1.0,
      "status": "PASS"
    },
    // ... 19 more measurements
  ],
  
  "summary": {
    "total_measurements": 20,
    "passed_measurements": 20,
    "failed_measurements": 0,
    "tolerance_default": 1.0,
    "tolerance_special": {"H": 0.5}
  }
}
```

---

## ✅ Validation Rules Summary

### PASS Condition
```
✓ File successfully parsed
✓ All 20 required measurements present
✓ All measurements are numeric and positive
✓ Size is valid
✓ ALL measurements within their tolerance
```

### FAIL Condition
```
✗ File cannot be parsed
✗ Any required measurement missing
✗ Any measurement is non-numeric
✗ Size is invalid
✗ ANY measurement outside its tolerance
✗ Duplicate measurement codes
✗ Invalid measurement codes
```

### No Averaging, No Override
```
20 measurements PASS + 1 measurement FAIL = OVERALL FAIL
No partial credit, no averaging, no exceptions
```

---

## 🧪 Testing

### Run All Tests
```bash
python run_tests.py
```

### Expected Output
```
TEST 1: Parser - Basic Formats ✓
TEST 2: Parser - Missing Measurements ✓
TEST 3: Parser - Invalid Values ✓
TEST 4: Validator - PASS Case ✓
TEST 5: Validator - FAIL Case ✓
TEST 6: Validator - Special Tolerance (H) ✓
TEST 7: Complete Workflow ✓

ALL TESTS PASSED ✓
```

---

## 💻 Code Examples

### Basic Usage
```python
from measurements.utils import MeasurementValidationEngine

# Validate a file
result = MeasurementValidationEngine.validate_file(
    file_path='measurements.txt',
    size='8/9',
    operator_id='operator_name'
)

# Check result
if result['success']:
    print("✓ VALIDATION PASSED")
else:
    print("✗ VALIDATION FAILED")
    for m in result['measurements']:
        if m['status'] == 'FAIL':
            print(f"{m['code']}: {m['measured_value']} "
                  f"(±{m['tolerance']}, std: {m['standard_value']})")
```

### Parse Only
```python
from measurements.utils import MeasurementFileParser

measurements, errors = MeasurementFileParser.parse_file('file.txt')
if errors:
    for error in errors:
        print(f"Error: {error}")
```

### Validate Only
```python
from measurements.utils import MeasurementValidator

result = MeasurementValidator.validate_measurements(
    measured_values={'A': 50.1, 'B': 44.0, ...},
    size='6/7'
)
print(f"Result: {result['overall_result']}")
```

---

## 📚 Sample Files

### `sample_measurements_pass.txt`
Valid file that should PASS validation for size 8/9

### `sample_measurements_fail.txt`
Valid file with B=51.5 (outside ±1.0 tolerance) → FAILS

### `sample_measurements_format_test.txt`
Demonstrates all 5 format variations

### `sample_measurements_neck_width_fail.txt`
H=18.9 (outside ±0.5 special tolerance) → FAILS

---

## 🚀 Integration Checklist

- [ ] Copy `measurements/utils.py` with validation engine
- [ ] Update `measurements/models.py` with new fields
- [ ] Update `measurements/views.py` with new integration
- [ ] Update `measurements/urls.py` with new endpoints
- [ ] Run migrations: `python manage.py migrate`
- [ ] Test with sample files
- [ ] Run test suite: `python run_tests.py`
- [ ] Update frontend to use new API endpoints
- [ ] Verify database storage of results
- [ ] Document in system documentation

---

## 🔍 Debugging

### Check Parser
```python
from measurements.utils import MeasurementFileParser
values, errors = MeasurementFileParser.parse_file('file.txt')
print(f"Parsed: {values}")
print(f"Errors: {errors}")
```

### Check Tolerance
```python
from measurements.utils import MeasurementValidator
tolerance_h = MeasurementValidator.get_tolerance('H')  # Should be 0.5
tolerance_a = MeasurementValidator.get_tolerance('A')  # Should be 1.0
```

### Check Size Chart
```python
from measurements.utils import MeasurementValidationEngine
chart = MeasurementValidationEngine.get_size_chart('8/9')
print(f"A for 8/9: {chart['A']}")  # Should be 56.5
```

---

## 📋 Documentation Files

### Complete Reference
**MEASUREMENT_VALIDATION_README.md** - 800+ lines
- Architecture and design
- All classes and methods
- Complete API documentation
- Examples and troubleshooting

### Quick Start
**VALIDATION_ENGINE_QUICK_START.md** - 400+ lines
- Quick start guide
- File format examples
- Integration examples
- Test results

### Implementation Summary
**IMPLEMENTATION_SUMMARY.md** - 500+ lines
- Complete implementation details
- Design principles
- Test results
- Integration path

---

## 🆘 Common Issues

### "File encoding error"
→ Save file as UTF-8 (not ANSI)

### "Measurement X not found"
→ Check code is A-T (uppercase)

### "Validation always fails"
→ Check selected size matches file measurements

### "H tolerance not applied"
→ H should have ±0.5 tolerance (other codes ±1.0)

### "Database errors"
→ Ensure migrations run: `python manage.py migrate`

---

## 📞 Key Files

| File | Purpose | Lines |
|------|---------|-------|
| `measurements/utils.py` | Core validation engine | 550+ |
| `measurements/models.py` | Database models | Updated |
| `measurements/views.py` | View integration | Updated |
| `measurements/urls.py` | URL routing | Updated |
| `measurements/test_validation_engine.py` | Test suite | 500+ |
| `MEASUREMENT_VALIDATION_README.md` | Full docs | 800+ |

---

## ✅ Implementation Status

- [x] File parser (4+ formats)
- [x] Validation engine (strict rules)
- [x] Size chart (6 sizes, complete)
- [x] API endpoints (3 endpoints)
- [x] Database integration (audit trail)
- [x] Test suite (7 tests, all pass)
- [x] Documentation (1200+ lines)
- [x] Sample files (4 variations)

**Status**: ✅ PRODUCTION READY

---

**Last Updated**: December 2025
**Version**: 1.0
**Status**: Complete ✓
