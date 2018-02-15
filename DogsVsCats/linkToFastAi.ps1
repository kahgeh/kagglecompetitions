
$path=$PSScriptRoot
$scriptFolder=Get-Item $path
mklink "$path\fastai" "$($scriptFolder.Parent.FullName)\fastai\fastai"