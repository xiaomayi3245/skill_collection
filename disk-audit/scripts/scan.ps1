param(
  # One or more roots to scan
  [string[]]$Roots = @(
    "C:\\Users\\user\\Downloads",
    "C:\\Users\\user\\Desktop"
  ),
  # Exclude folder names (path contains \name\). Keep system excludes by default.
  [string[]]$Exclude = @('Windows','Program Files','Program Files (x86)','$Recycle.Bin','System Volume Information'),
  [int64]$LargeFileBytes = 524288000, # 500MB
  [int]$TopN = 30,
  [string]$OutDir = "C:\\Users\\user\\.openclaw\\workspace\\reports\\disk-audit"
)

$ErrorActionPreference = 'SilentlyContinue'

function Should-ExcludePath([string]$path, [string[]]$excludeNames) {
  foreach ($name in $excludeNames) {
    if (-not $name) { continue }
    if ($path -like "*\\$name\\*") { return $true }
    if ($path -like "*\\$name") { return $true }
  }
  return $false
}

function Get-FileHashSafe([string]$path) {
  try {
    return (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash
  } catch { return $null }
}

$rootsResolved = @()
foreach ($r in $Roots) {
  try {
    $rootsResolved += (Resolve-Path -LiteralPath $r).Path
  } catch {
    Write-Warning "Root not found: $r"
  }
}

if ($rootsResolved.Count -eq 0) {
  throw "No valid Roots provided."
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$stamp = Get-Date -Format 'yyyy-MM-dd'
$outJson = Join-Path $OutDir "$stamp.json"
$outMd  = Join-Path $OutDir "$stamp.md"

$files = @()
foreach ($rootResolved in $rootsResolved) {
  Get-ChildItem -LiteralPath $rootResolved -Recurse -File -Force | ForEach-Object {
    $p = $_.FullName
    if (Should-ExcludePath $p $Exclude) { return }
    $files += [PSCustomObject]@{
      path = $p
      name = $_.Name
      ext  = $_.Extension.ToLower()
      size = [int64]$_.Length
      mtime = $_.LastWriteTime
    }
  }
}

# Top large files
$topLarge = $files | Sort-Object size -Descending | Select-Object -First $TopN

# Recent modified
$recent = $files | Sort-Object mtime -Descending | Select-Object -First $TopN

# Extension stats
$extStats = $files | Group-Object ext | ForEach-Object {
  $sum = ($_.Group | Measure-Object size -Sum).Sum
  [PSCustomObject]@{ ext=$_.Name; count=$_.Count; bytes=[int64]$sum }
} | Sort-Object bytes -Descending

# Duplicate candidates (by size first, then hash for top candidates)
$dupCandidates = $files | Group-Object size | Where-Object { $_.Count -ge 2 -and $_.Name -ge 1048576 } | Sort-Object Count -Descending
$dupDetails = @()
$maxGroups = 50
$gCount = 0
foreach ($g in $dupCandidates) {
  if ($gCount -ge $maxGroups) { break }
  $gCount++
  $hashGroups = @{}
  foreach ($f in $g.Group) {
    $h = Get-FileHashSafe $f.path
    if (-not $h) { continue }
    if (-not $hashGroups.ContainsKey($h)) { $hashGroups[$h] = @() }
    $hashGroups[$h] += $f
  }
  foreach ($k in $hashGroups.Keys) {
    if ($hashGroups[$k].Count -ge 2) {
      $dupDetails += [PSCustomObject]@{
        bytes = [int64]$g.Name
        hash = $k
        files = ($hashGroups[$k] | Select-Object -ExpandProperty path)
      }
    }
  }
}

$result = [PSCustomObject]@{
  roots = $rootsResolved
  scannedAt = (Get-Date)
  totalFiles = $files.Count
  totalBytes = [int64](($files | Measure-Object size -Sum).Sum)
  topLarge = $topLarge
  recent = $recent
  extStats = $extStats
  dupDetails = $dupDetails
}

$result | ConvertTo-Json -Depth 6 | Out-File -Encoding utf8 $outJson

function Format-Bytes([int64]$b) {
  if ($b -ge 1099511627776) { return "{0:N2} TB" -f ($b/1099511627776) }
  if ($b -ge 1073741824)    { return "{0:N2} GB" -f ($b/1073741824) }
  if ($b -ge 1048576)       { return "{0:N2} MB" -f ($b/1048576) }
  if ($b -ge 1024)          { return "{0:N2} KB" -f ($b/1024) }
  return "$b B"
}

$md = @()
$md += "# Disk audit report"
$md += "- Roots: " + ($rootsResolved -join ', ')
$md += "- Scanned at: $((Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))"
$md += "- Total files: $($result.totalFiles)"
$md += "- Total size: $(Format-Bytes $result.totalBytes)"
$md += ""
$md += "## Top $TopN largest files"
foreach ($f in $topLarge) { $md += "- $(Format-Bytes $f.size) | $($f.mtime.ToString('yyyy-MM-dd')) | $($f.path)" }
$md += ""
$md += "## Most recently modified (Top $TopN)"
foreach ($f in $recent) { $md += "- $($f.mtime.ToString('yyyy-MM-dd HH:mm')) | $(Format-Bytes $f.size) | $($f.path)" }
$md += ""
$md += "## Extension size breakdown (Top 30)"
foreach ($e in ($extStats | Select-Object -First 30)) { $md += "- $($e.ext) | $($e.count) files | $(Format-Bytes $e.bytes)" }
$md += ""
$md += "## Duplicate candidates (SHA256)"
if ($dupDetails.Count -eq 0) {
  $md += "- (none found or hash unavailable)"
} else {
  foreach ($d in $dupDetails) {
    $md += "- $(Format-Bytes $d.bytes) | $($d.hash)"
    foreach ($p in $d.files) { $md += "  - $p" }
  }
}

$md -join "`n" | Out-File -Encoding utf8 $outMd
Write-Output $outMd
