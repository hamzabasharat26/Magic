# 🚀 QUICK START GUIDE - Magic QC v2.1 with Authentication

## ⚡ IMMEDIATE ACCESS

### 🔐 **Login Credentials**

#### **ADMIN ACCOUNT (Full Access)**
```
URL: http://127.0.0.1:8000/accounts/admin/login/
Username: ManagerQC
Password: mqc001
```

#### **OPERATOR ACCOUNT (Measurement Panel)**
```
URL: http://127.0.0.1:8000/accounts/operator/login/
Username: OperatorQC
Password: mqc002
```

---

## 📋 ADMIN FEATURES CHECKLIST

✅ **Dashboard** - Overview of all POs and products
✅ **Purchase Orders** - Create and manage POs
✅ **Products** - Add products to POs
✅ **Measurements** - Full QC measurement system
✅ **Analytics** - View reports and statistics
✅ **User Management** - Add/Edit/Delete users (NEW!)
✅ **Settings** - System configuration

### 👤 **User Management Panel**
- Create new admin or operator users
- Edit user details and permissions
- Delete users (except yourself)
- View user statistics
- Assign roles

---

## 📱 OPERATOR PANEL WORKFLOW

### **Step-by-Step:**

1. **Login** → Operator Login Page
   - Enter OperatorQC / mqc002
   - Click "Login to Operator Panel"

2. **Select Brand** (Step 1)
   - Choose from dropdown: ZARA, H&M, INDITEX, Other
   - Links to existing PO numbers

3. **Select Product Type** (Step 2)
   - Choose: Sweatshirt, Hoodie, T-Shirt, or Pants
   - Dropdown enables after brand selection

4. **Select Size** (Step 3)
   - Visual grid shows available sizes
   - Numbers indicate product count
   - Green highlight when selected
   - Disabled sizes appear grayed out

5. **View Details**
   - Product information box appears
   - Shows: PO Number, Brand, Type, Size, Color, Quantity

6. **Start Measurement**
   - Click green "START MEASUREMENT" button
   - Session created in database
   - Redirects to measurement dashboard

7. **Perform QC**
   - Upload measurement file
   - Or use camera capture
   - Complete QC analysis

8. **Logout**
   - Click logout button
   - Session saved
   - Return to operator login

---

## 🎨 VISUAL DESIGN ELEMENTS

### **Admin Theme:**
- 🟣 Purple gradient (#667eea → #764ba2)
- Shield icon for admin
- Professional card design
- Shadow effects

### **Operator Theme:**
- 🟢 Green gradient (#11998e → #38ef7d)
- Hard hat icon for operator
- Touch-optimized interface
- Large interactive buttons

### **Size Selection:**
- **Available:** White background, blue border, hoverable
- **Selected:** Green gradient, white text, checkmark
- **Disabled:** Gray, reduced opacity, not clickable
- **Count Badge:** Blue badge showing product quantity

---

## 🔧 SYSTEM COMMANDS

### **Create Default Users:**
```bash
python manage.py create_default_users
```

### **Reset Database (if needed):**
```bash
Remove-Item db.sqlite3 -Force
python manage.py migrate
python manage.py create_default_users
```

### **Check System:**
```bash
python manage.py check
```

### **Run Server:**
```bash
python manage.py runserver
```

---

## 📊 DATABASE OVERVIEW

### **Users Table:**
- ManagerQC (admin) - Full access
- OperatorQC (operator) - Panel access only

### **Sessions Table:**
- Tracks active operator sessions
- Links operator → product → measurements

### **Existing Tables:**
- PurchaseOrder - PO management
- Product - Product details
- StandardSizeChart - Size references
- MeasurementSession - QC sessions
- CapturedImage - Measurement images

---

## 🧪 TEST SCENARIOS

### **Test 1: Admin Login & User Creation**
1. Login as ManagerQC
2. Go to User Management
3. Click "Add New User"
4. Create: TestAdmin / password / admin role
5. Logout and login with new account ✓

### **Test 2: Operator Workflow**
1. Login as admin first
2. Create PO with products
3. Logout and login as OperatorQC
4. Select brand → product type → size
5. Click START MEASUREMENT ✓

### **Test 3: Role Protection**
1. Login as OperatorQC
2. Try to access: http://127.0.0.1:8000/
3. Should redirect to operator panel ✓
4. Cannot access admin features ✓

---

## 🎯 KEY URLS

```
Admin Login:          /accounts/admin/login/
Operator Login:       /accounts/operator/login/
Dashboard:            /
User Management:      /accounts/admin/users/
Create User:          /accounts/admin/users/create/
Operator Panel:       /accounts/operator/panel/
Measurements:         /measurements/
Analytics:            /measurements/analytics/
Logout:               /accounts/logout/
```

---

## 💡 TIPS & TRICKS

### **For Admins:**
- Create products first before operators can use them
- Use "Add & Another" to quickly add multiple products
- Check User Management to see all active users
- Monitor operator sessions in Django admin

### **For Operators:**
- Product availability shown in real-time
- Size buttons show count badges
- Can't proceed without all selections
- Sessions automatically tracked

### **Security:**
- Change default passwords in production
- Create unique accounts per operator
- Regularly review user access
- Monitor login activity

---

## ⚠️ IMPORTANT NOTES

1. **First Time Use:**
   - Database reset removes all data
   - Default users recreated automatically
   - Need to recreate POs and products

2. **Role Restrictions:**
   - Operators cannot access admin functions
   - Admins can use both panels
   - Logout redirects based on role

3. **Session Management:**
   - One active session per operator
   - Previous sessions auto-completed
   - Session data persists in database

---

## 🆘 TROUBLESHOOTING

### **Problem: Can't login**
- Solution: Check username/password match exactly
- Run: `python manage.py create_default_users`

### **Problem: No products in operator panel**
- Solution: Login as admin first
- Create PO with products
- Then use operator panel

### **Problem: Permission denied**
- Solution: Check user role
- Admin role for dashboard
- Operator role for panel

### **Problem: Page not found**
- Solution: Check URL spelling
- Ensure server running
- Clear browser cache

---

## ✨ SUCCESS INDICATORS

✅ Admin can login and see dashboard
✅ Operator can login and see panel
✅ User management works (create/edit/delete)
✅ Operator panel shows products
✅ Size selection highlights correctly
✅ START button redirects to measurements
✅ Logout returns to correct login page
✅ Roles are enforced properly

---

## 🎉 SYSTEM STATUS

**FULLY OPERATIONAL**
- All authentication features working
- Both panels fully functional
- Database properly configured
- Security measures implemented
- Visual design consistent
- User experience optimized

**Server Running:** http://127.0.0.1:8000/
**Ready for Production Testing!** 🚀
