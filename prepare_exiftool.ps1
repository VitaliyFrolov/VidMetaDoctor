$paths = @(
    "resources/exiftool/mac",
    "resources/exiftool/win",
    "resources/exiftool/linux"
)

foreach ($path in $paths) {
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path | Out-Null
        Write-Host "Created $path"
    }
}

if (Test-Path "/usr/local/bin/exiftool") {
    Copy-Item "/usr/local/bin/exiftool" "resources/exiftool/mac/exiftool"
    Write-Host "Copied macOS exiftool"
} else {
    Write-Host "macOS exiftool not found"
}

if (Test-Path ".\exiftool.exe") {
    Copy-Item ".\exiftool.exe" "resources/exiftool/win/exiftool.exe"
    Write-Host "Copied Windows exiftool.exe"
} else {
    Write-Host "⚠️ Windows exiftool.exe not found in current directory"
}

if (Test-Path "/usr/bin/exiftool") {
    Copy-Item "/usr/bin/exiftool" "resources/exiftool/linux/exiftool"
    Write-Host "Copied Linux exiftool"
} else {
    Write-Host "Linux exiftool not found"
}

Write-Host "Done preparing exiftool binaries."
