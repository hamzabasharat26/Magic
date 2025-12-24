# Sound Notifications Testing Guide
## Measurement Validation System with Audio Feedback

### Quick Test (2 minutes)

**Step 1: Open the Dashboard**
- Navigate to `/measurements/` in your Django application
- You should see "Measurement System" with upload form

**Step 2: Test PASS Sound**
1. In "Select Size for QC Check" dropdown → Choose **8/9 Years**
2. Click "Upload Measurement File" input
3. Select: `sample_measurements_pass.txt`
4. Click **"Upload & Analyze"** button
5. **Expected Result:**
   - Green notification appears: "✓ QC PASSED"
   - Message: "All X measurements are within tolerance limits"
   - **GREEN checkmark sound plays** (pass1.mp3)
   - Detailed measurement table shows all "PASS" badges in green

**Step 3: Test FAIL Sound**
1. Click "Reset" or upload new file
2. In dropdown → Choose **8/9 Years**
3. Select: `sample_measurements_fail.txt`
4. Click **"Upload & Analyze"** button
5. **Expected Result:**
   - Red notification appears: "✗ QC FAILED"
   - Message: "X measurement(s) exceed tolerance limits"
   - **RED warning sound plays** (fail1.mp3)
   - Detailed table shows failed measurements with red "FAIL" badges
   - Failed measurements list shown at bottom

---

### System Architecture

#### Sound Files Location
```
/static/sounds/
├── pass.mp3        (alternate pass sound)
├── pass1.mp3       (current PASS notification sound)
├── fail.mp3        (alternate fail sound)
└── fail1.mp3       (current FAIL notification sound)
```

#### Sound Integration Points
1. **HTML Audio Elements** (lines 193-199)
   ```html
   <audio id="passSound" preload="auto">
       <source src="{% static 'sounds/pass1.mp3' %}" type="audio/mpeg">
   </audio>
   <audio id="failSound" preload="auto">
       <source src="{% static 'sounds/fail1.mp3' %}" type="audio/mpeg">
   </audio>
   ```

2. **JavaScript Sound Functions** (lines 270-279)
   ```javascript
   function playPassSound() {
       const sound = document.getElementById('passSound');
       sound.currentTime = 0;
       sound.play().catch(e => console.log('Audio play failed:', e));
   }
   
   function playFailSound() {
       const sound = document.getElementById('failSound');
       sound.currentTime = 0;
       sound.play().catch(e => console.log('Audio play failed:', e));
   }
   ```

3. **Integration in Upload Handler** (lines 417-450)
   ```javascript
   const validationResult = data.validation_result;
   const isPassed = validationResult.overall_result === 'PASS';
   
   if (isPassed) {
       showNotification('✓ QC PASSED', '...', 'success', 6000);
       playPassSound();
   } else {
       showNotification('✗ QC FAILED', '...', 'error', 6000);
       playFailSound();
   }
   ```

---

### Detailed Test Scenarios

#### Test Case 1: Standard PASS Scenario
**File:** `sample_measurements_pass.txt`
**Size:** 8/9 Years
**Expected Outcome:**
- All 20 measurements pass tolerance checks
- Sound: pass1.mp3 (success/confirmation sound)
- Notification Color: Green (#28a745)
- Notification Title: "✓ QC PASSED"
- Pass Rate: 100%
- Duration: Notification stays 6000ms

**Sample Measurement:**
```
A (Length): 56.0 cm
  Standard: 56 cm
  Tolerance: ±1.0 cm
  Status: PASS ✓
```

#### Test Case 2: Standard FAIL Scenario
**File:** `sample_measurements_fail.txt`
**Size:** 8/9 Years
**Expected Outcome:**
- 1+ measurements exceed tolerance
- Sound: fail1.mp3 (warning/failure sound)
- Notification Color: Red (#dc3545)
- Notification Title: "✗ QC FAILED"
- Failed measurements highlighted
- Pass Rate: < 100%

**Sample Failing Measurement:**
```
A (Length): 57.5 cm
  Standard: 56 cm
  Tolerance: ±1.0 cm
  Deviation: +1.5 cm
  Status: FAIL ✗ (exceeds ±1.0 cm tolerance)
```

#### Test Case 3: Boundary Tolerance Test
**Expected:** Measurement exactly at tolerance edge
```
H (Neck Width): 31.0 cm
  Standard: 31 cm
  Tolerance: ±0.5 cm (special tight tolerance)
  Deviation: ±0.0 cm
  Status: PASS ✓
```

#### Test Case 4: Special Tolerance (H - Neck Width)
**Measurement H has STRICTER tolerance: ±0.5 cm (vs. default ±1.0 cm)**

**Pass Case:** H = 31.0 to 31.5 cm → PASS
**Fail Case:** H = 31.6 cm or H = 30.4 cm → FAIL

---

### Sound System Troubleshooting

#### Issue: Sound Not Playing

**Check 1: Browser Console**
1. Open Developer Tools (F12)
2. Go to "Console" tab
3. Try uploading a file
4. Look for messages:
   - ✅ No errors: System working
   - ❌ "Audio play failed": Check browser permissions

**Check 2: Audio File Path**
1. Open Network tab in Dev Tools
2. Upload file and analyze
3. Look for requests to `/static/sounds/pass1.mp3`
4. Verify Status: 200 (file found)

**Check 3: Browser Permissions**
- Chrome/Edge: Check speaker icon in address bar
- Firefox: Check sound icon
- Safari: Check privacy settings
- Grant "Allow Audio" permission if prompted

**Check 4: Audio Element Verification**
1. In Console tab, run:
   ```javascript
   console.log(document.getElementById('passSound'));
   console.log(document.getElementById('failSound'));
   ```
2. Should see audio elements (not null)

#### Issue: Wrong Sound Playing
- Verify `pass1.mp3` and `fail1.mp3` are in `/static/sounds/`
- Check that file paths in HTML are correct
- Try alternative sound files: `pass.mp3` or `fail.mp3`

#### Issue: Sound Disabled
- Check browser volume is not muted
- Check system volume is not muted
- Try clicking "Upload & Analyze" button again
- Modern browsers require user interaction before playing audio

---

### Validation Rules (What Causes PASS/FAIL)

#### PASS Requirements (ALL must be true)
- ✅ All 20 required measurements present
- ✅ All measurements are numeric values
- ✅ All measurements within defined tolerance ranges
- ✅ Special tolerances respected (H: ±0.5 cm, others: ±1.0 cm)
- ✅ No format errors or invalid data

#### FAIL Triggers (ANY causes FAIL)
- ❌ Missing measurement
- ❌ Non-numeric value
- ❌ Deviation exceeds tolerance limit
- ❌ File format error
- ❌ Unrecognized measurement code

---

### UI Component Description

#### Notification Display
```
┌─────────────────────────────────────────────────┐
│  ✓ QC PASSED                         [Close X]   │
│  ───────────────────────────────────────────────│
│  All 20 measurements are within                  │
│  tolerance limits.                              │
│                                                   │
│  ✓ Passed: 20/20 measurements                   │
│  ⏰ Timestamp: 10/15/2024, 2:30:45 PM           │
└─────────────────────────────────────────────────┘
```

#### Results Table (Sample Row)
```
│ A  │ Length (Body Length)    │ 56.0 │ 56.0 │ 0.0  │ ±1.0 │ ✓ PASS │
│ H  │ Neck Width             │ 31.0 │ 31.0 │ 0.0  │ ±0.5 │ ✓ PASS │
│ K  │ Sleeve Length          │ 32.0 │ 33.2 │ +1.2 │ ±1.0 │ ✗ FAIL │
```

---

### Test Checklist

**Before Testing:**
- [ ] Sounds are in `/static/sounds/` (4 files present)
- [ ] Sample test files exist (pass.txt, fail.txt)
- [ ] Django application is running
- [ ] Static files are served correctly
- [ ] Browser volume is not muted
- [ ] Browser has microphone/speaker access

**During PASS Test:**
- [ ] Dropdown shows 6 size options (6/7 through 13/14)
- [ ] File selection works
- [ ] "Upload & Analyze" button is clickable
- [ ] Page shows loading indicator
- [ ] Green notification appears with checkmark
- [ ] Pass sound (pass1.mp3) plays clearly
- [ ] Notification stays visible for ~6 seconds
- [ ] Measurement table shows all PASS badges
- [ ] Statistics show 100% pass rate
- [ ] File info displays filename and size
- [ ] Timestamp displays correctly

**During FAIL Test:**
- [ ] File selection works for fail.txt
- [ ] Page shows loading indicator
- [ ] Red notification appears with X mark
- [ ] Fail sound (fail1.mp3) plays clearly
- [ ] Notification displays failed count
- [ ] Measurement table shows red FAIL badges
- [ ] Failed measurements section visible
- [ ] Statistics show correct pass/fail counts
- [ ] Pass rate calculated correctly
- [ ] Operator field displays (System or operator ID)

**Post-Test Verification:**
- [ ] Notifications auto-dismiss after 6 seconds
- [ ] Close button works if clicked
- [ ] Can upload multiple files in sequence
- [ ] Sounds don't overlap if files uploaded quickly
- [ ] Browser console has no errors
- [ ] Network requests show successful responses

---

### Browser Compatibility

**Supported Browsers:**
- Chrome/Edge 60+: Full support
- Firefox 55+: Full support
- Safari 11+: Full support (may need user gesture)
- Mobile Safari 12+: Full support (subject to app settings)

**Known Limitations:**
- Autoplay may require user interaction (clicking button enables it)
- Some mobile browsers restrict autoplay
- Muted videos/audio don't play unless user interacts

---

### Expected Output Examples

#### PASS Scenario Output
```
✓ QC PASSED
All 20 measurements are within tolerance limits.

✓ Passed: 20/20 measurements
⏰ Timestamp: 10/15/2024, 3:45:22 PM

Summary Statistics:
Total Measurements: 20
Passed: 20
Failed: 0
Pass Rate: 100.0%
Operator: System
```

#### FAIL Scenario Output
```
✗ QC FAILED
Some measurements exceed tolerance limits.

✗ Failed: 1 measurement(s)
✓ Passed: 19 measurement(s)
⏰ Timestamp: 10/15/2024, 3:46:15 PM

Failed Measurements (1):
K

Summary Statistics:
Total Measurements: 20
Passed: 19
Failed: 1
Pass Rate: 95.0%
Operator: System
```

---

### Debugging Tips

**Console Logging**
Add this to console (F12) to debug:
```javascript
// Test pass sound directly
document.getElementById('passSound').play();

// Test fail sound directly
document.getElementById('failSound').play();

// Check audio element
console.log(document.getElementById('passSound').src);
console.log(document.getElementById('failSound').src);
```

**Network Debugging**
1. Open DevTools → Network tab
2. Upload file
3. Look for:
   - POST to `/measurements/upload-and-analyze/` (should be 200)
   - GET requests to `/static/sounds/pass1.mp3` and `/static/sounds/fail1.mp3` (should be 200)

**Response Validation**
Check that API returns proper structure:
```json
{
  "status": "success",
  "validation_result": {
    "overall_result": "PASS",
    "size": "8/9",
    "measurements": [...],
    "summary": {
      "total_measurements": 20,
      "passed_measurements": 20,
      "failed_measurements": 0
    }
  }
}
```

---

### Next Steps After Testing

1. **If sounds play correctly:**
   - ✅ System is production-ready
   - Deploy to live environment
   - Train operators on UI
   - Start using for QC validation

2. **If sounds don't play:**
   - Check browser console for errors
   - Verify static files are being served
   - Test with alternative sound files
   - Check browser permissions
   - See troubleshooting section above

3. **To customize sounds:**
   - Replace `pass1.mp3` with preferred success sound
   - Replace `fail1.mp3` with preferred warning sound
   - Ensure files are in `/static/sounds/`
   - Update HTML src attributes if filenames change

---

### Support Resources

**Validation Engine Documentation:**
- See: `MEASUREMENT_VALIDATION_README.md`
- Contains: Detailed validation rules, standard sizes, tolerance ranges

**API Documentation:**
- Endpoint: `/measurements/upload-and-analyze/`
- Method: POST
- Returns: Validation result with PASS/FAIL status and detailed measurements

**Quick Reference:**
- Supported sizes: 6/7, 7/8, 8/9, 9/10, 11/12, 13/14 years
- Default tolerance: ±1.0 cm
- Special tolerance (H): ±0.5 cm
- Pass rule: ALL measurements must pass
- Result notification time: 6 seconds

---

**Version:** 1.0  
**Last Updated:** October 15, 2024  
**Status:** Ready for Testing
