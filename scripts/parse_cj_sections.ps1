$contentPath = "C:\Users\FUJITSU\.gemini\antigravity-ide\brain\19f67f38-9df3-4ddd-bd15-0e53956c0c7e\.system_generated\steps\193\content.md"
$raw = Get-Content -Path $contentPath -Raw

$matches = [regex]::Matches($raw, '<a href=(https?://cloudjourney\.awsstudygroup\.com/vi/[^" >]*)>([^<]+)</a>')
$cjLinks = @()
foreach ($m in $matches) {
    $cjLinks += [PSCustomObject]@{ Url = $m.Groups[1].Value; Title = $m.Groups[2].Value }
}
$cjLinks | Format-Table -AutoSize
