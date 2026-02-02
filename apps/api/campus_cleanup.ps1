# Campus Domain Standardization - Cleanup Script
# This script updates imports and deletes old directories for inventory, transport, infrastructure

Write-Host "Starting campus domain cleanup..." -ForegroundColor Green

# Wait for file copies to complete
Start-Sleep -Seconds 2

# ============================================================================
# INVENTORY SUBDOMAIN
# ============================================================================
Write-Host "`nProcessing Inventory subdomain..." -ForegroundColor Yellow

# Check if files exist
if (Test-Path "d:\Projects\college-erp2\apps\api\app\domains\campus\inventory\services.py") {
    Write-Host "  ✓ services.py exists"
} else {
    Write-Host "  ✗ services.py missing - copying now" -ForegroundColor Red
    Copy-Item -Path "d:\Projects\college-erp2\apps\api\app\domains\campus\inventory\services\asset.py" `
              -Destination "d:\Projects\college-erp2\apps\api\app\domains\campus\inventory\services.py"
}

# Update imports in router.py
$routerFile = "d:\Projects\college-erp2\apps\api\app\domains\campus\inventory\router.py"
$content = Get-Content $routerFile -Raw
$content = $content -replace 'from \.\.models\.asset import', 'from ..models import'
$content = $content -replace 'from \.\.services\.asset import', 'from ..services import'
Set-Content $routerFile -Value $content
Write-Host "  ✓ Updated router.py imports"

# Update imports in services.py
$servicesFile = "d:\Projects\college-erp2\apps\api\app\domains\campus\inventory\services.py"
if (Test-Path $servicesFile) {
    $content = Get-Content $servicesFile -Raw
    $content = $content -replace 'from \.\.models\.asset import', 'from .models import'
    Set-Content $servicesFile -Value $content
    Write-Host "  ✓ Updated services.py imports"
}

# Delete old directories
Remove-Item -Path "d:\Projects\college-erp2\apps\api\app\domains\campus\inventory\models" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "d:\Projects\college-erp2\apps\api\app\domains\campus\inventory\routers" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "d:\Projects\college-erp2\apps\api\app\domains\campus\inventory\services" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "  ✓ Deleted old directories"

# ============================================================================
# TRANSPORT SUBDOMAIN
# ============================================================================
Write-Host "`nProcessing Transport subdomain..." -ForegroundColor Yellow

# Check if files exist
if (-not (Test-Path "d:\Projects\college-erp2\apps\api\app\domains\campus\transport\services.py")) {
    Copy-Item -Path "d:\Projects\college-erp2\apps\api\app\domains\campus\transport\services\logistics.py" `
              -Destination "d:\Projects\college-erp2\apps\api\app\domains\campus\transport\services.py"
}

# Update imports in router.py
$routerFile = "d:\Projects\college-erp2\apps\api\app\domains\campus\transport\router.py"
$content = Get-Content $routerFile -Raw
$content = $content -replace 'from \.\.models\.logistics import', 'from ..models import'
$content = $content -replace 'from \.\.services\.logistics import', 'from ..services import'
Set-Content $routerFile -Value $content
Write-Host "  ✓ Updated router.py imports"

# Update imports in services.py
$servicesFile = "d:\Projects\college-erp2\apps\api\app\domains\campus\transport\services.py"
if (Test-Path $servicesFile) {
    $content = Get-Content $servicesFile -Raw
    $content = $content -replace 'from \.\.models\.logistics import', 'from .models import'
    Set-Content $servicesFile -Value $content
    Write-Host "  ✓ Updated services.py imports"
}

# Delete old directories
Remove-Item -Path "d:\Projects\college-erp2\apps\api\app\domains\campus\transport\models" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "d:\Projects\college-erp2\apps\api\app\domains\campus\transport\routers" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "d:\Projects\college-erp2\apps\api\app\domains\campus\transport\services" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "  ✓ Deleted old directories"

# ============================================================================
# INFRASTRUCTURE SUBDOMAIN
# ============================================================================
Write-Host "`nProcessing Infrastructure subdomain..." -ForegroundColor Yellow

# Check if files exist
if (-not (Test-Path "d:\Projects\college-erp2\apps\api\app\domains\campus\infrastructure\services.py")) {
    Copy-Item -Path "d:\Projects\college-erp2\apps\api\app\domains\campus\infrastructure\services\facility.py" `
              -Destination "d:\Projects\college-erp2\apps\api\app\domains\campus\infrastructure\services.py"
}

# Update imports in services.py
$servicesFile = "d:\Projects\college-erp2\apps\api\app\domains\campus\infrastructure\services.py"
if (Test-Path $servicesFile) {
    $content = Get-Content $servicesFile -Raw
    $content = $content -replace 'from \.\.models\.facility import', 'from .models import'
    Set-Content $servicesFile -Value $content
    Write-Host "  ✓ Updated services.py imports"
}

# Delete old directories
Remove-Item -Path "d:\Projects\college-erp2\apps\api\app\domains\campus\infrastructure\models" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "d:\Projects\college-erp2\apps\api\app\domains\campus\infrastructure\services" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "  ✓ Deleted old directories"

# ============================================================================
# UPDATE CAMPUS ROUTER
# ============================================================================
Write-Host "`nUpdating campus router..." -ForegroundColor Yellow

$campusRouter = "d:\Projects\college-erp2\apps\api\app\domains\campus\router.py"
$content = Get-Content $campusRouter -Raw
$content = $content -replace 'from \.hostel\.routers\.hostel import', 'from .hostel.router import'
$content = $content -replace 'from \.library\.routers\.library import', 'from .library.router import'
$content = $content -replace 'from \.inventory\.routers\.inventory import', 'from .inventory.router import'
$content = $content -replace 'from \.transport\.routers\.transport import', 'from .transport.router import'
Set-Content $campusRouter -Value $content
Write-Host "  ✓ Updated campus router imports"

# ============================================================================
# UPDATE ORCHESTRATION
# ============================================================================
Write-Host "`nUpdating orchestration..." -ForegroundColor Yellow

$orchestrationFile = "d:\Projects\college-erp2\apps\api\app\domains\campus\orchestration\student_exit.py"
if (Test-Path $orchestrationFile) {
    $content = Get-Content $orchestrationFile -Raw
    $content = $content -replace 'from \.\.hostel\.services import', 'from ..hostel.services import'
    $content = $content -replace 'from \.\.library\.services import', 'from ..library.services import'
    $content = $content -replace 'from \.\.transport\.services import', 'from ..transport.services import'
    $content = $content -replace 'from \.\.inventory\.services import', 'from ..inventory.services import'
    Set-Content $orchestrationFile -Value $content
    Write-Host "  ✓ Updated orchestration imports"
}

Write-Host "`n✅ Campus domain standardization complete!" -ForegroundColor Green
Write-Host "All 5 subdomains (hostel, library, inventory, transport, infrastructure) have been standardized." -ForegroundColor Green
