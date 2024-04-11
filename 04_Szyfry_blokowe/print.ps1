# Define a parameter to receive the file name
param ($fileName)
# Read the content of input.txt
$content = Get-Content -Path $fileName -Raw
# Write the content to the terminal
Write-Host $content

# Output the content, ensuring newlines are preserved
#Write-Output $content