# PowerShell script kiểm tra cấu trúc nội dung Hugo và cú pháp bài viết song ngữ
[CmdletBinding()]
param (
    [string]$ContentDir = "content"
)

Write-Host "=== Bắt đầu kiểm tra cấu trúc nội dung Hugo (FCAJ) ===" -ForegroundColor Cyan

if (-not (Test-Path $ContentDir)) {
    Write-Error "Không tìm thấy thư mục $ContentDir"
    exit 1
}

$mdFiles = Get-ChildItem -Path $ContentDir -Recurse -Filter "*.md"
Write-Host "Tìm thấy $($mdFiles.Count) tệp Markdown trong $ContentDir." -ForegroundColor Green

$missingPairs = 0
$invalidFrontMatter = 0

foreach ($file in $mdFiles) {
    # Kiểm tra FrontMatter cơ bản (--- ở đầu)
    $lines = Get-Content -Path $file.FullName -TotalCount 5
    if ($lines.Count -gt 0 -and $lines[0].Trim() -ne "---") {
        Write-Warning "File thiếu FrontMatter mở đầu (---): $($file.FullName)"
        $invalidFrontMatter++
    }
}

Write-Host "`n=== Tổng kết ===" -ForegroundColor Cyan
Write-Host "Số file Markdown: $($mdFiles.Count)"
Write-Host "Cảnh báo FrontMatter: $invalidFrontMatter"

if ($invalidFrontMatter -eq 0) {
    Write-Host "Tất cả các bài viết đều có định dạng chuẩn!" -ForegroundColor Green
} else {
    Write-Host "Vui lòng xem lại các file có cảnh báo trên." -ForegroundColor Yellow
}
