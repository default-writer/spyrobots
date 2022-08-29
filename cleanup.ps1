Get-ChildItem -Filter __pycache__ -Recurse -Force | Remove-Item -Recurse -Force
Get-ChildItem -Filter .pytest_cache -Recurse -Force | Remove-Item -Recurse -Force
Get-ChildItem -Filter .history -Recurse -Force | Remove-Item -Recurse -Force

