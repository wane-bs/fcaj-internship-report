$contentPath = "C:\Users\FUJITSU\.gemini\antigravity-ide\brain\19f67f38-9df3-4ddd-bd15-0e53956c0c7e\.system_generated\steps\193\content.md"
$raw = Get-Content -Path $contentPath -Raw

$m = [regex]::Matches($raw, 'href=(https://cloudjourney\.awsstudygroup\.com/vi/[^ >]*)')
$urls = @()
foreach ($item in $m) {
    $urls += $item.Groups[1].Value.Trim('"').Trim('>')
}
$urls | Sort-Object -Unique
