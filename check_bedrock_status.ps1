# Quick script to check if Bedrock is being used

Write-Host "Checking Bedrock status in logs..." -ForegroundColor Cyan
Write-Host ""

# Activate venv and get logs
. venv/Scripts/Activate.ps1
eb logs --all | Out-Null

# Find the latest log directory
$latestLog = Get-ChildItem .elasticbeanstalk\logs\ | Sort-Object Name -Descending | Select-Object -First 1

if ($latestLog) {
    Write-Host "Analyzing logs from: $($latestLog.Name)" -ForegroundColor Yellow
    Write-Host ""
    
    $logFile = Get-ChildItem "$($latestLog.FullName)\*\var\log\web.stdout.log" -Recurse | Select-Object -First 1
    
    if ($logFile) {
        # Check for success
        $success = Get-Content $logFile | Select-String -Pattern "LLM generated advisory" | Select-Object -Last 5
        
        # Check for failures
        $failures = Get-Content $logFile | Select-String -Pattern "LLM generation failed" | Select-Object -Last 5
        
        # Check for Bedrock errors
        $bedrockErrors = Get-Content $logFile | Select-String -Pattern "Bedrock invocation failed" | Select-Object -Last 5
        
        if ($success) {
            Write-Host "✅ BEDROCK IS WORKING!" -ForegroundColor Green
            Write-Host ""
            Write-Host "Recent successful generations:" -ForegroundColor Green
            $success | ForEach-Object { Write-Host "  $_" }
        }
        
        if ($failures) {
            Write-Host ""
            Write-Host "⚠️  LLM Failures Detected (using fallback templates):" -ForegroundColor Yellow
            $failures | ForEach-Object { Write-Host "  $_" }
        }
        
        if ($bedrockErrors) {
            Write-Host ""
            Write-Host "❌ Bedrock Errors:" -ForegroundColor Red
            $bedrockErrors | ForEach-Object { Write-Host "  $_" }
            Write-Host ""
            
            # Check for specific error types
            $throttling = Get-Content $logFile | Select-String -Pattern "ThrottlingException|Too many tokens" | Select-Object -Last 1
            $accessDenied = Get-Content $logFile | Select-String -Pattern "AccessDeniedException" | Select-Object -Last 1
            
            if ($throttling) {
                Write-Host "Issue: RATE LIMITING" -ForegroundColor Yellow
                Write-Host "  Bedrock is working but you're hitting rate limits"
                Write-Host "  Solution: Wait a few minutes or switch to Amazon Nova"
                Write-Host "  See: switch_to_nova.md"
            }
            
            if ($accessDenied) {
                Write-Host "Issue: PERMISSIONS" -ForegroundColor Red
                Write-Host "  IAM role needs Bedrock permissions"
                Write-Host "  Solution: See ENABLE_BEDROCK_GUIDE.md"
            }
        }
        
        if (-not $success -and -not $failures -and -not $bedrockErrors) {
            Write-Host "ℹ️  No recent advisory generations found in logs" -ForegroundColor Cyan
            Write-Host "  Try generating an advisory from the UI first"
        }
        
    } else {
        Write-Host "❌ Could not find web.stdout.log" -ForegroundColor Red
    }
} else {
    Write-Host "❌ No log directories found" -ForegroundColor Red
}

Write-Host ""
Write-Host "To see full logs: eb logs --all" -ForegroundColor Cyan
