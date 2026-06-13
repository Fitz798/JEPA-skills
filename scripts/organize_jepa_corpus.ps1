Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Ensure-Dir {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path | Out-Null
    }
}

function Normalize-Slug {
    param([string]$Text)
    if ([string]::IsNullOrWhiteSpace($Text)) {
        return "untitled"
    }
    $slug = $Text.ToLowerInvariant()
    $slug = $slug -replace "[^a-z0-9]+", "_"
    $slug = $slug.Trim("_")
    if ([string]::IsNullOrWhiteSpace($slug)) {
        return "untitled"
    }
    return $slug
}

function Get-UniquePath {
    param(
        [string]$Directory,
        [string]$FileName
    )
    $ext = [System.IO.Path]::GetExtension($FileName)
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($FileName)
    $candidate = Join-Path $Directory $FileName
    $i = 2
    while (Test-Path -LiteralPath $candidate) {
        $candidateName = "{0}_{1}{2}" -f $baseName, $i, $ext
        $candidate = Join-Path $Directory $candidateName
        $i++
    }
    return $candidate
}

function Get-PaperMeta {
    param([System.IO.FileInfo]$File)
    $base = [System.IO.Path]::GetFileNameWithoutExtension($File.Name)
    $year = ""
    $arxiv = ""
    $title = $base

    if ($base -match "^arxiv_(\d{4}\.\d{5})_(.+)$") {
        $arxiv = $matches[1]
        $yy = [int]$arxiv.Substring(0, 2)
        $year = (2000 + $yy).ToString()
        $title = $matches[2] -replace "_", " "
    } elseif ($base -match "^\((\d{4})[^)]*\)\s*(.+)$") {
        $year = $matches[1]
        $title = $matches[2]
    } elseif ($base -match "^(unk|\d{4})_(.+)$") {
        if ($matches[1] -ne "unk") {
            $year = $matches[1]
        }
        $title = $matches[2]
        # Make canonical naming idempotent if script is rerun.
        while ($title -match "^(unk|\d{4})_(.+)$") {
            $title = $matches[2]
        }
    } elseif ($base -match "(\d{4})") {
        $year = $matches[1]
        $title = $base
    }

    $title = $title -replace "_", " "
    $title = ($title -replace "\s+", " ").Trim()
    return [pscustomobject]@{
        Year  = $year
        Arxiv = $arxiv
        Title = $title
    }
}

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

$paths = @{
    SourcePapersRoot   = Join-Path $repoRoot "JEPA-Papers"
    SourceAwesome      = Join-Path $repoRoot "JEPA-Papers\awesome-jepa"
    SourceCode         = Join-Path $repoRoot "JEPA-CodeBase"
    CorpusRoot         = Join-Path $repoRoot "corpus"
    CorpusAllPapers    = Join-Path $repoRoot "corpus\papers\all"
    CorpusCodeArchives = Join-Path $repoRoot "corpus\code\archives"
    DuplicatesRoot     = Join-Path $repoRoot "corpus\_duplicates"
    DuplicatesPapers   = Join-Path $repoRoot "corpus\_duplicates\papers"
    DuplicatesCode     = Join-Path $repoRoot "corpus\_duplicates\code"
    Metadata           = Join-Path $repoRoot "metadata"
}

foreach ($k in @("CorpusRoot","CorpusAllPapers","CorpusCodeArchives","DuplicatesRoot","DuplicatesPapers","DuplicatesCode","Metadata")) {
    Ensure-Dir -Path $paths[$k]
}

$paperMoves = @()
$topLevelPapers = Get-ChildItem -Path $paths.SourcePapersRoot -File -Filter *.pdf -ErrorAction SilentlyContinue
foreach ($f in $topLevelPapers) {
    $target = Get-UniquePath -Directory $paths.CorpusAllPapers -FileName $f.Name
    Move-Item -LiteralPath $f.FullName -Destination $target
    $paperMoves += [pscustomobject]@{
        From = $f.FullName
        To   = $target
    }
}

$awesomePapers = Get-ChildItem -Path $paths.SourceAwesome -File -Filter *.pdf -ErrorAction SilentlyContinue
foreach ($f in $awesomePapers) {
    $target = Get-UniquePath -Directory $paths.CorpusAllPapers -FileName $f.Name
    Move-Item -LiteralPath $f.FullName -Destination $target
    $paperMoves += [pscustomobject]@{
        From = $f.FullName
        To   = $target
    }
}

$manifest = Join-Path $paths.SourceAwesome "download_manifest.csv"
if (Test-Path -LiteralPath $manifest) {
    $manifestTarget = Join-Path $paths.Metadata "awesome_download_manifest.csv"
    Move-Item -LiteralPath $manifest -Destination $manifestTarget -Force
}

$codeMoves = @()
$archives = @(Get-ChildItem -Path $paths.SourceCode -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.Extension -in @(".zip", ".tar", ".gz") })
foreach ($f in $archives) {
    $target = Get-UniquePath -Directory $paths.CorpusCodeArchives -FileName $f.Name
    Move-Item -LiteralPath $f.FullName -Destination $target
    $codeMoves += [pscustomobject]@{
        From = $f.FullName
        To   = $target
    }
}

# Rename papers to a canonical format: year_title_slug.pdf
$renameLog = @()
$paperFilesForRename = Get-ChildItem -Path $paths.CorpusAllPapers -File -Filter *.pdf
foreach ($f in $paperFilesForRename) {
    $meta = Get-PaperMeta -File $f
    $yearToken = if ([string]::IsNullOrWhiteSpace($meta.Year)) { "unk" } else { $meta.Year }
    $titleSlug = Normalize-Slug -Text $meta.Title
    $newName = "{0}_{1}.pdf" -f $yearToken, $titleSlug
    if ($newName -ne $f.Name) {
        $targetPath = Get-UniquePath -Directory $paths.CorpusAllPapers -FileName $newName
        Move-Item -LiteralPath $f.FullName -Destination $targetPath
        $renameLog += [pscustomobject]@{
            OldPath = $f.FullName
            NewPath = $targetPath
        }
    }
}

function Move-ExactDuplicates {
    param(
        [string]$SearchPath,
        [string]$Pattern,
        [string]$DuplicateBucket
    )
    $files = @(Get-ChildItem -Path $SearchPath -Recurse -File -Filter $Pattern)
    if ($files.Count -eq 0) { return @() }

    $hashed = foreach ($f in $files) {
        $h = Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256
        [pscustomobject]@{
            FullName = $f.FullName
            Name     = $f.Name
            Hash     = $h.Hash
            Size     = $f.Length
        }
    }

    $duplicateGroups = $hashed | Group-Object Hash | Where-Object { $_.Count -gt 1 }
    $dupeMoves = @()
    foreach ($group in $duplicateGroups) {
        $ordered = $group.Group | Sort-Object FullName
        $toMove = $ordered | Select-Object -Skip 1
        foreach ($item in $toMove) {
            $target = Get-UniquePath -Directory $DuplicateBucket -FileName $item.Name
            Move-Item -LiteralPath $item.FullName -Destination $target
            $dupeMoves += [pscustomobject]@{
                Hash     = $item.Hash
                Size     = $item.Size
                Original = $item.FullName
                MovedTo  = $target
            }
        }
    }
    return $dupeMoves
}

$paperDuplicateMoves = @(Move-ExactDuplicates -SearchPath (Join-Path $paths.CorpusRoot "papers") -Pattern "*.pdf" -DuplicateBucket $paths.DuplicatesPapers)
$codeDuplicateMoves = @(Move-ExactDuplicates -SearchPath (Join-Path $paths.CorpusRoot "code") -Pattern "*" -DuplicateBucket $paths.DuplicatesCode)

# Build papers index.
$paperIndex = @()
$paperFiles = Get-ChildItem -Path (Join-Path $paths.CorpusRoot "papers") -Recurse -File -Filter *.pdf
foreach ($f in $paperFiles) {
    $meta = Get-PaperMeta -File $f
    $hash = Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256
    $relative = Resolve-Path -LiteralPath $f.FullName -Relative
    $collection = "all"
    if ([string]::IsNullOrWhiteSpace($meta.Year)) {
        $yearForId = "unk"
    } else {
        $yearForId = $meta.Year
    }
    $paperId = if (-not [string]::IsNullOrWhiteSpace($meta.Arxiv)) {
        "arxiv_{0}" -f $meta.Arxiv
    } else {
        "{0}_{1}" -f $yearForId, (Normalize-Slug -Text $meta.Title)
    }
    $paperIndex += [pscustomobject]@{
        paper_id       = $paperId
        title_guess    = $meta.Title
        year_guess     = $meta.Year
        arxiv_id       = $meta.Arxiv
        collection     = $collection
        current_name   = $f.Name
        relative_path  = $relative
        size_bytes     = $f.Length
        sha256         = $hash.Hash
    }
}
$paperIndex | Sort-Object collection, year_guess, current_name | Export-Csv -Path (Join-Path $paths.Metadata "papers_index.csv") -NoTypeInformation -Encoding UTF8

# Build code index.
$codeIndex = @()
$codeFiles = Get-ChildItem -Path (Join-Path $paths.CorpusRoot "code") -Recurse -File
foreach ($f in $codeFiles) {
    $hash = Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256
    $relative = Resolve-Path -LiteralPath $f.FullName -Relative
    $codeIndex += [pscustomobject]@{
        code_id        = Normalize-Slug -Text ([System.IO.Path]::GetFileNameWithoutExtension($f.Name))
        current_name   = $f.Name
        relative_path  = $relative
        size_bytes     = $f.Length
        sha256         = $hash.Hash
    }
}
$codeIndex | Sort-Object current_name | Export-Csv -Path (Join-Path $paths.Metadata "code_index.csv") -NoTypeInformation -Encoding UTF8

$paperDupHashes = $paperIndex | Group-Object sha256 | Where-Object { $_.Count -gt 1 } | ForEach-Object {
    [pscustomobject]@{
        sha256 = $_.Name
        count  = $_.Count
        files  = ($_.Group.relative_path -join " | ")
    }
}
$paperDupHashes | Export-Csv -Path (Join-Path $paths.Metadata "duplicates_by_hash_papers.csv") -NoTypeInformation -Encoding UTF8

$arxivDupes = $paperIndex | Where-Object { -not [string]::IsNullOrWhiteSpace($_.arxiv_id) } | Group-Object arxiv_id | Where-Object { $_.Count -gt 1 } | ForEach-Object {
    [pscustomobject]@{
        arxiv_id = $_.Name
        count    = $_.Count
        files    = ($_.Group.relative_path -join " | ")
    }
}
$arxivDupes | Export-Csv -Path (Join-Path $paths.Metadata "duplicates_by_arxiv.csv") -NoTypeInformation -Encoding UTF8

$paperMoves | Export-Csv -Path (Join-Path $paths.Metadata "paper_moves.csv") -NoTypeInformation -Encoding UTF8
$codeMoves | Export-Csv -Path (Join-Path $paths.Metadata "code_moves.csv") -NoTypeInformation -Encoding UTF8
$renameLog | Export-Csv -Path (Join-Path $paths.Metadata "paper_renames.csv") -NoTypeInformation -Encoding UTF8
$paperDuplicateMoves | Export-Csv -Path (Join-Path $paths.Metadata "paper_exact_duplicate_moves.csv") -NoTypeInformation -Encoding UTF8
$codeDuplicateMoves | Export-Csv -Path (Join-Path $paths.Metadata "code_exact_duplicate_moves.csv") -NoTypeInformation -Encoding UTF8

Write-Output ("Moved papers: {0}" -f $paperMoves.Count)
Write-Output ("Moved code archives: {0}" -f $codeMoves.Count)
Write-Output ("Renamed core papers: {0}" -f $renameLog.Count)
Write-Output ("Moved exact duplicate papers: {0}" -f $paperDuplicateMoves.Count)
Write-Output ("Moved exact duplicate code archives: {0}" -f $codeDuplicateMoves.Count)
Write-Output ("Paper index entries: {0}" -f $paperIndex.Count)
Write-Output ("Code index entries: {0}" -f $codeIndex.Count)
