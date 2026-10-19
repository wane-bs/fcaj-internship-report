$dupFiles = Get-ChildItem -Path "aws-doc" -Filter "*(1).md"
$results = @()
foreach ($f in $dupFiles) {
    $origName = $f.Name -replace " \(1\)\.md$", ".md"
    $origPath = "aws-doc/$origName"
    $origExists = Test-Path $origPath
    $origSize = if ($origExists) { (Get-Item $origPath).Length } else { 0 }
    
    $fLine = Get-Content $f.FullName -TotalCount 10 | Where-Object { $_ -match "^source:" } | Select-Object -First 1
    $oLine = if ($origExists) { Get-Content $origPath -TotalCount 10 | Where-Object { $_ -match "^source:" } | Select-Object -First 1 } else { "" }
    
    $results += [PSCustomObject]@{
        DupFile = $f.Name
        DupSize = $f.Length
        DupSource = $fLine
        OrigFile = $origName
        OrigSize = $origSize
        OrigSource = $oLine
    }
}
$results | Format-List
