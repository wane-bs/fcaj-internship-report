$files = Get-ChildItem -Path "aws-doc" -Filter "*.md"
$items = @()
foreach ($f in $files) {
    $line = Get-Content -Path $f.FullName -TotalCount 10 | Where-Object { $_ -match "^source:\s*(.*)" } | Select-Object -First 1
    if ($line) {
        $url = ($line -replace "^source:\s*", "").Trim()
        try {
            $uri = [System.Uri]$url
            $items += [PSCustomObject]@{ Host = $uri.Host; Path = $uri.AbsolutePath; File = $f.Name }
        } catch {}
    }
}
$items | Group-Object Host | Select-Object Name, Count | Format-Table -AutoSize
$dup = $files | Where-Object { $_.Name -match "\(1\)\.md$" }
Write-Host "So file co duoi (1).md: $($dup.Count)"
