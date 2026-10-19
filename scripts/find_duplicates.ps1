$files = Get-ChildItem -Path "aws-doc" -Filter "*.md"
$map = @{}
foreach ($f in $files) {
    $line = Get-Content -Path $f.FullName -TotalCount 10 | Where-Object { $_ -match "^source:\s*(.*)" } | Select-Object -First 1
    if ($line) {
        $u = ($line -replace "^source:\s*", "").Trim()
        if (-not $map.ContainsKey($u)) { $map[$u] = @() }
        $map[$u] += $f.Name
    }
}

Write-Host "=== CAC FILE TRUNG NGUON ===" -ForegroundColor Yellow
foreach ($k in $map.Keys) {
    if ($map[$k].Count -gt 1) {
        Write-Host "Source: $k" -ForegroundColor Cyan
        foreach ($fn in $map[$k]) {
            $sz = (Get-Item "aws-doc/$fn").Length
            Write-Host "  -> $fn (Size: $sz bytes)"
        }
    }
}
