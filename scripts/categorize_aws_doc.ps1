$files = Get-ChildItem -Path "aws-doc" -Filter "*.md"
$table = @()
foreach ($f in $files) {
    $line = Get-Content -Path $f.FullName -TotalCount 10 | Where-Object { $_ -match "^source:\s*(.*)" } | Select-Object -First 1
    $url = if ($line) { ($line -replace "^source:\s*", "").Trim() } else { "Unknown" }
    $titleLine = Get-Content -Path $f.FullName -TotalCount 15 | Where-Object { $_ -match "^#\s+(.*)" } | Select-Object -First 1
    $title = if ($titleLine) { ($titleLine -replace "^#\s+", "").Trim() } else { $f.BaseName }
    $hostName = try { ([System.Uri]$url).Host } catch { "Unknown" }
    $path = try { ([System.Uri]$url).AbsolutePath } catch { "Unknown" }
    $table += [PSCustomObject]@{ File = $f.Name; Host = $hostName; Path = $path; Title = $title }
}

$table | Group-Object Host | ForEach-Object {
    Write-Host "`n=== Workshop Host: $($_.Name) (Count: $($_.Count)) ===" -ForegroundColor Green
    $_.Group | Sort-Object Path | Select-Object File, Title, Path | Format-Table -AutoSize | Out-String | Write-Host
}
