"""
MEASUREMENT VALIDATION ENGINE - Industrial Grade QC System
Validates garment measurements against standard size charts with strict audit-safe rules.
Sweatshirt measurement validation for sizes 6/7 to 13/14 years.
"""

import re
import json
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Tuple, Optional


# ============================================================================
# SECTION 1: STANDARD SIZE CHART DATA
# ============================================================================

STANDARD_SIZE_CHART_SWEATSHIRT = {
    "6/7": {
        "A": 50.1,   # Length from shoulder
        "B": 44.0,   # Chest Width
        "C": 39.0,   # Chest Width (1/2 Armhole)
        "D": 42.0,   # Bottom width (Above Waistband)
        "E": 39.5,   # Hem Width
        "F": 42.2,   # Back Width
        "G": 39.5,   # Back Width (1/2 Armhole)
        "H": 16.2,   # Neck Width (Seam to Seam)
        "I": 37.2,   # Sleeve Length
        "J": 20.5,   # Sleeve Width
        "K": 12.2,   # Sleeve Width (Above Cuff)
        "L": 7.5,    # Sleeve Opening
        "M": 5.5,    # Cuff Length
        "N": 20.2,   # Armhole
        "O": 2.2,    # Back Neck Drop
        "P": 5.3,    # Front Neck Drop
        "Q": 2.0,    # Collar Width
        "R": 4.7,    # Shoulder Drop
        "S": 6.0,    # Waistband Length
        "T": 3.0,    # Forward Shoulder Seam
        "PRINT_PLACEMENT_FROM_CF": 6.0,
    },
    "7/8": {
        "A": 52.7,
        "B": 48.3,
        "C": 43.0,
        "D": 44.0,
        "E": 37.5,
        "F": 44.5,
        "G": 41.5,
        "H": 17.8,
        "I": 41.5,
        "J": 20.0,
        "K": 12.5,
        "L": 7.8,
        "M": 5.7,
        "N": 22.5,
        "O": 2.2,
        "P": 5.5,
        "Q": 2.0,
        "R": 4.9,
        "S": 5.7,
        "T": 3.0,
        "PRINT_PLACEMENT_FROM_CF": 6.0,
    },
    "8/9": {
        "A": 56.5,
        "B": 49.2,
        "C": 44.0,
        "D": 46.0,
        "E": 40.7,
        "F": 47.0,
        "G": 43.5,
        "H": 18.3,
        "I": 44.7,
        "J": 20.5,
        "K": 12.7,
        "L": 8.0,
        "M": 6.2,
        "N": 23.0,
        "O": 2.2,
        "P": 5.8,
        "Q": 2.0,
        "R": 5.2,
        "S": 5.0,
        "T": 3.0,
        "PRINT_PLACEMENT_FROM_CF": 7.3,
    },
    "9/10": {
        "A": 59.0,
        "B": 50.0,
        "C": 45.5,
        "D": 48.0,
        "E": 42.0,
        "F": 47.5,
        "G": 45.5,
        "H": 18.0,
        "I": 47.0,
        "J": 19.9,
        "K": 13.0,
        "L": 8.0,
        "M": 6.0,
        "N": 23.0,
        "O": 2.5,
        "P": 6.3,
        "Q": 2.5,
        "R": 5.4,
        "S": 6.0,
        "T": 3.0,
        "PRINT_PLACEMENT_FROM_CF": 7.5,
    },
    "11/12": {
        "A": 63.2,
        "B": 54.7,
        "C": 48.2,
        "D": 50.5,
        "E": 42.0,
        "F": 51.7,
        "G": 48.0,
        "H": 19.0,
        "I": 52.5,
        "J": 23.0,
        "K": 13.5,
        "L": 9.5,
        "M": 6.2,
        "N": 26.3,
        "O": 2.5,
        "P": 6.8,
        "Q": 2.5,
        "R": 5.7,
        "S": 6.0,
        "T": 3.0,
        "PRINT_PLACEMENT_FROM_CF": 7.5,
    },
    "13/14": {
        "A": 65.0,
        "B": 55.5,
        "C": 51.0,
        "D": 53.0,
        "E": 46.9,
        "F": 53.7,
        "G": 50.5,
        "H": 18.3,
        "I": 54.3,
        "J": 23.0,
        "K": 14.0,
        "L": 8.5,
        "M": 6.3,
        "N": 26.5,
        "O": 2.5,
        "P": 7.3,
        "Q": 2.5,
        "R": 5.9,
        "S": 5.7,
        "T": 3.0,
        "PRINT_PLACEMENT_FROM_CF": 7.5,
    },
}

# Valid measurement codes that must be present
REQUIRED_MEASUREMENT_CODES = {
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"
}

# Optional measurement codes
OPTIONAL_MEASUREMENT_CODES = {"PRINT_PLACEMENT_FROM_CF"}

# All valid codes combined
ALL_VALID_CODES = REQUIRED_MEASUREMENT_CODES | OPTIONAL_MEASUREMENT_CODES

# Tolerance rules (cm)
TOLERANCE_RULES = {
    "H": 0.5,  # Neck Width - Special stricter tolerance
}
DEFAULT_TOLERANCE = 1.0  # For all other measurements


# ============================================================================
# SECTION 2: FILE PARSER
# ============================================================================

class MeasurementFileParser:
    """
    Parses measurement files (.txt only) supporting multiple line formats.
    
    Supported formats:
    - A: 50.1
    - A = 50.1
    - A: 50.1 cm
    - Length from shoulder (A): 50.1
    - A: 50.1x 2 (ignores the x part)
    """
    
    @staticmethod
    def parse_file(file_path: str) -> Tuple[Dict[str, float], List[str]]:
        """
        Parse a .txt measurement file.
        
        Returns:
            Tuple[Dict[str, float], List[str]]: (parsed_measurements, error_messages)
        """
        measured_values = {}
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        except UnicodeDecodeError:
            return {}, ["Error: File is not UTF-8 encoded"]
        except IOError as e:
            return {}, [f"Error: Cannot read file - {str(e)}"]
        
        if not lines:
            return {}, ["Error: File is empty"]
        
        # Parsing patterns (order matters - most specific first)
        patterns = [
            # Format: "Length from shoulder (A): 50.1"
            (r'[^\(]*\(([A-T])\)\s*[:=]\s*([0-9]+\.?[0-9]*)', "description_with_code"),
            # Format: "A: 50.1 cm" or "A: 50.1x 2"
            (r'([A-T])\s*[:=]\s*([0-9]+\.?[0-9]*)\s*(cm|x)?', "code_value"),
            # Format: "A = 50.1"
            (r'([A-T])\s*=\s*([0-9]+\.?[0-9]*)', "code_value"),
        ]
        
        found_codes = set()
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            matched = False
            
            for pattern, format_type in patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    try:
                        code = match.group(1).upper()
                        value_str = match.group(2)
                        
                        # Validate code
                        if code not in ALL_VALID_CODES:
                            errors.append(
                                f"Line {line_num}: Unknown measurement code '{code}'. "
                                f"Valid codes are: {', '.join(sorted(REQUIRED_MEASUREMENT_CODES | OPTIONAL_MEASUREMENT_CODES))}"
                            )
                            continue
                        
                        # Parse value
                        try:
                            value = float(value_str)
                        except ValueError:
                            errors.append(f"Line {line_num}: Invalid numeric value '{value_str}' for code {code}")
                            continue
                        
                        # Validate value is positive
                        if value <= 0:
                            errors.append(f"Line {line_num}: Measurement {code} must be positive, got {value}")
                            continue
                        
                        # Check for duplicates
                        if code in found_codes:
                            errors.append(f"Line {line_num}: Duplicate measurement code '{code}'")
                            continue
                        
                        measured_values[code] = value
                        found_codes.add(code)
                        matched = True
                        break
                        
                    except Exception as e:
                        errors.append(f"Line {line_num}: Parse error - {str(e)}")
                        continue
            
            if not matched and line:
                errors.append(f"Line {line_num}: Could not parse line format: '{line}'")
        
        return measured_values, errors
    
    @staticmethod
    def validate_parsed_data(measured_values: Dict[str, float]) -> List[str]:
        """
        Validate that all required measurements are present.
        
        Returns:
            List[str]: Error messages for any missing or invalid data
        """
        errors = []
        
        # Check for missing required measurements
        missing_codes = REQUIRED_MEASUREMENT_CODES - set(measured_values.keys())
        if missing_codes:
            errors.append(
                f"Missing required measurement(s): {', '.join(sorted(missing_codes))}"
            )
        
        # Check for invalid codes (should not happen after parser validation)
        invalid_codes = set(measured_values.keys()) - ALL_VALID_CODES
        if invalid_codes:
            errors.append(
                f"Invalid measurement code(s): {', '.join(sorted(invalid_codes))}"
            )
        
        return errors


# ============================================================================
# SECTION 3: VALIDATION ENGINE
# ============================================================================

class MeasurementValidator:
    """
    Validates measured values against standard size chart with strict tolerance rules.
    Implements industrial-grade QC logic with no averaging or overrides.
    """
    
    @staticmethod
    def get_tolerance(code: str) -> float:
        """Get tolerance value for a measurement code."""
        return TOLERANCE_RULES.get(code, DEFAULT_TOLERANCE)
    
    @staticmethod
    def validate_measurements(
        measured_values: Dict[str, float],
        size: str,
        operator_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Dict:
        """
        Validate measured values against standard chart for a specific size.
        
        Args:
            measured_values: Dictionary of measurement code -> value
            size: Size code (e.g., "6/7", "7/8", etc.)
            operator_id: Optional operator identifier
            session_id: Optional session identifier
        
        Returns:
            Dictionary containing:
            - success: bool - True if validation passed all checks
            - size: str - The selected size
            - timestamp: str - ISO format timestamp
            - operator_id: str or None
            - session_id: str or None
            - measurements: List[Dict] - Per-measurement results
            - overall_result: str - "PASS" or "FAIL"
            - error_messages: List[str] - Any validation errors
            - summary: Dict - Summary statistics
        """
        
        result = {
            "success": False,
            "size": size,
            "timestamp": datetime.now().isoformat(),
            "operator_id": operator_id,
            "session_id": session_id,
            "measurements": [],
            "overall_result": "FAIL",
            "error_messages": [],
            "summary": {
                "total_measurements": 0,
                "passed_measurements": 0,
                "failed_measurements": 0,
                "tolerance_default": DEFAULT_TOLERANCE,
                "tolerance_special": TOLERANCE_RULES,
            }
        }
        
        # Validate size exists
        if size not in STANDARD_SIZE_CHART_SWEATSHIRT:
            result["error_messages"].append(
                f"Invalid size '{size}'. Valid sizes: {', '.join(sorted(STANDARD_SIZE_CHART_SWEATSHIRT.keys()))}"
            )
            return result
        
        # Get standard values for this size
        standard_values = STANDARD_SIZE_CHART_SWEATSHIRT[size]
        
        # Check all required measurements are present
        missing_codes = REQUIRED_MEASUREMENT_CODES - set(measured_values.keys())
        if missing_codes:
            result["error_messages"].append(
                f"Missing required measurements: {', '.join(sorted(missing_codes))}"
            )
            return result
        
        # Check for unknown codes
        unknown_codes = set(measured_values.keys()) - ALL_VALID_CODES
        if unknown_codes:
            result["error_messages"].append(
                f"Unknown measurement codes: {', '.join(sorted(unknown_codes))}"
            )
            return result
        
        # Validate each measurement
        overall_pass = True
        
        for code in sorted(REQUIRED_MEASUREMENT_CODES | OPTIONAL_MEASUREMENT_CODES):
            if code not in measured_values:
                # Optional measurements can be missing
                if code in OPTIONAL_MEASUREMENT_CODES:
                    continue
                # Required measurements must be present (already checked above)
                continue
            
            measured_value = measured_values[code]
            standard_value = standard_values.get(code)
            
            if standard_value is None:
                result["error_messages"].append(
                    f"Standard value not found for code {code} in size {size}"
                )
                continue
            
            # Calculate deviation
            deviation = abs(measured_value - standard_value)
            tolerance = MeasurementValidator.get_tolerance(code)
            
            # Determine pass/fail
            measurement_pass = deviation <= tolerance
            if not measurement_pass:
                overall_pass = False
            
            # Record result
            measurement_result = {
                "code": code,
                "measurement_name": MeasurementValidator.get_measurement_name(code),
                "measured_value": measured_value,
                "standard_value": standard_value,
                "deviation": round(deviation, 2),
                "tolerance": tolerance,
                "status": "PASS" if measurement_pass else "FAIL",
            }
            
            result["measurements"].append(measurement_result)
            
            result["summary"]["total_measurements"] += 1
            if measurement_pass:
                result["summary"]["passed_measurements"] += 1
            else:
                result["summary"]["failed_measurements"] += 1
        
        # Set overall result
        result["overall_result"] = "PASS" if overall_pass else "FAIL"
        result["success"] = overall_pass
        
        return result
    
    @staticmethod
    def get_measurement_name(code: str) -> str:
        """Get human-readable name for measurement code."""
        names = {
            "A": "Length from shoulder",
            "B": "Chest Width",
            "C": "Chest Width (1/2 Armhole)",
            "D": "Bottom width (Above Waistband)",
            "E": "Hem Width",
            "F": "Back Width",
            "G": "Back Width (1/2 Armhole)",
            "H": "Neck Width (Seam to Seam)",
            "I": "Sleeve Length",
            "J": "Sleeve Width",
            "K": "Sleeve Width (Above Cuff)",
            "L": "Sleeve Opening",
            "M": "Cuff Length",
            "N": "Armhole",
            "O": "Back Neck Drop",
            "P": "Front Neck Drop",
            "Q": "Collar Width",
            "R": "Shoulder Drop",
            "S": "Waistband Length",
            "T": "Forward Shoulder Seam",
            "PRINT_PLACEMENT_FROM_CF": "Print Placement From CF",
        }
        return names.get(code, code)


# ============================================================================
# SECTION 4: COMPLETE VALIDATION WORKFLOW
# ============================================================================

class MeasurementValidationEngine:
    """
    Complete validation workflow: parse file -> validate -> return results.
    This is the main entry point for the validation system.
    """
    
    @staticmethod
    def validate_file(
        file_path: str,
        size: str,
        operator_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Dict:
        """
        Complete validation workflow for a measurement file.
        
        Returns:
            Dictionary with complete validation results
        """
        result = {
            "success": False,
            "file_parsed": False,
            "validation_passed": False,
            "size": size,
            "timestamp": datetime.now().isoformat(),
            "operator_id": operator_id,
            "session_id": session_id,
            "parse_errors": [],
            "validation_errors": [],
            "measurements": [],
            "overall_result": "FAIL",
            "summary": {},
        }
        
        # Step 1: Parse file
        measured_values, parse_errors = MeasurementFileParser.parse_file(file_path)
        result["parse_errors"] = parse_errors
        
        if parse_errors and not measured_values:
            # Critical parsing errors
            return result
        
        # Step 2: Validate parsed data
        parse_validation_errors = MeasurementFileParser.validate_parsed_data(measured_values)
        if parse_validation_errors:
            result["parse_errors"].extend(parse_validation_errors)
            return result
        
        result["file_parsed"] = True
        
        # Step 3: Validate against standard
        validation_result = MeasurementValidator.validate_measurements(
            measured_values=measured_values,
            size=size,
            operator_id=operator_id,
            session_id=session_id
        )
        
        # Merge validation result
        result.update(validation_result)
        result["validation_passed"] = validation_result["success"]
        
        return result
    
    @staticmethod
    def get_available_sizes() -> List[str]:
        """Return list of available sizes."""
        return sorted(STANDARD_SIZE_CHART_SWEATSHIRT.keys())
    
    @staticmethod
    def get_size_chart(size: str) -> Optional[Dict]:
        """Get standard size chart for a specific size."""
        return STANDARD_SIZE_CHART_SWEATSHIRT.get(size)
