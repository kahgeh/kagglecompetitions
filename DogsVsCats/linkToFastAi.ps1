
$path=$PSScriptRoot
$scriptFolder=Get-Item $path

New-Item -Path fastai -ItemType SymbolicLink -Value ../fastai/fastai