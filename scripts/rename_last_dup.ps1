Get-ChildItem -Path "aws-doc" -Recurse -Filter "*(1).md" | ForEach-Object {
    $newName = "Tao-Customer-Gateway-Tuy-chon-5.3.1.md"
    Rename-Item -Path $_.FullName -NewName $newName -Force
    Write-Host "Renamed $($_.FullName) to $newName"
}
