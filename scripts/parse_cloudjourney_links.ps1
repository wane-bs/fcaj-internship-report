$contentPath = "C:\Users\FUJITSU\.gemini\antigravity-ide\brain\19f67f38-9df3-4ddd-bd15-0e53956c0c7e\.system_generated\steps\193\content.md"
$raw = Get-Content -Path $contentPath -Raw

$matches = [regex]::Matches($raw, 'href=(https?://[a-zA-Z0-9\.\-]+/vi/[^" >]*)')
$links = @()
foreach ($m in $matches) {
    $u = $m.Groups[1].Value
    $links += $u
}
$distinct = $links | Sort-Object -Unique

Write-Host "Total links found: $($distinct.Count)"
$distinct | Group-Object { ([System.Uri]$_).Host } | Select-Object Name, Count | Format-Table -AutoSize
