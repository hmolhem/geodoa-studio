function Test-TextWhitespace {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        Write-Host "[FAIL] File not found: $Path"
        return $false
    }

    $extension = [System.IO.Path]::GetExtension($Path).ToLowerInvariant()
    $isMarkdown = $extension -eq ".md"

    $lines = @(Get-Content -LiteralPath $Path -Encoding UTF8)

    $issues = @()
    $markdownBreaks = @()

    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]

        if ($line -match '([ \t]+)$') {
            $trailing = $Matches[1]
            $lineNumber = $i + 1

            if ($isMarkdown -and $trailing -eq "  ") {
                $markdownBreaks += $lineNumber
                continue
            }

            $type = if ($trailing.Contains("`t")) {
                "Trailing tab/whitespace"
            }
            else {
                "Trailing spaces"
            }

            $issues += [PSCustomObject]@{
                Line       = $lineNumber
                Type       = $type
                Characters = $trailing.Length
                Text       = $line.TrimEnd()
            }
        }
    }

    Write-Host ""
    Write-Host "=========================================="
    Write-Host " GeoDOA Text Whitespace Validation"
    Write-Host "=========================================="
    Write-Host "File: $Path"
    Write-Host ""

    if ($markdownBreaks.Count -gt 0) {
        Write-Host "[INFO] Valid Markdown hard breaks: $($markdownBreaks.Count)"
        Write-Host "       Lines: $($markdownBreaks -join ', ')"
        Write-Host ""
    }

    if ($issues.Count -eq 0) {
        Write-Host "[PASS] No unintended trailing whitespace found."
        Write-Host "=========================================="
        return $true
    }

    Write-Host "[FAIL] $($issues.Count) unintended whitespace issue(s) found:"
    Write-Host ""

    $issues | Format-Table Line, Type, Characters, Text -AutoSize

    Write-Host "=========================================="
    return $false
}



function Test-FinalNewline {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        Write-Host "[FAIL] File not found: $Path"
        return $false
    }

    $bytes = [System.IO.File]::ReadAllBytes($Path)

    if ($bytes.Length -eq 0) {
        Write-Host "[FAIL] Empty file: $Path"
        return $false
    }

    if ($bytes[-1] -eq 10) {
        Write-Host "[PASS] Final newline present: $Path"
        return $true
    }

    Write-Host "[FAIL] No final newline: $Path"
    return $false
}


function Repair-FinalNewline {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        Write-Host "[FAIL] File not found: $Path"
        return $false
    }

    $bytes = [System.IO.File]::ReadAllBytes($Path)

    if ($bytes.Length -eq 0) {
        Write-Host "[SKIP] Empty file: $Path"
        return $false
    }

    if ($bytes[-1] -eq 10) {
        Write-Host "[PASS] Final newline already present: $Path"
        return $true
    }

    $utf8NoBom = [System.Text.UTF8Encoding]::new($false)

    [System.IO.File]::AppendAllText(
        $Path,
        "`n",
        $utf8NoBom
    )

    Write-Host "[FIXED] Added final newline: $Path"
    return $true
}


Export-ModuleMember -Function `
    Test-TextWhitespace, `
    Test-FinalNewline, `
    Repair-FinalNewline
