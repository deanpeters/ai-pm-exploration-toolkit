# 🚨 AI PM Toolkit - Troubleshooting Guide

Comprehensive guide to fix common issues and get your toolkit working smoothly.

---

## 🔥 Most Common Issues

### "The workflow tools are never ready when I try to access them!"
**Problem:** You run `aipm_workflows` but http://localhost:5678 doesn't work  
**Root Cause:** Command wasn't actually starting containers  
**Solution:** ✅ **FIXED** - `aipm_workflows` now actually starts containers with health checks

```bash
# The new working way
aipm_workflows              # Actually starts containers and waits for them
aipm_workflows_status       # Check what's running
aipm_workflows_fix          # Fix issues automatically
```

### "Commands just show help text instead of doing anything!"
**Problem:** Commands like `aipm_research_quick` just echo usage instead of working  
**Root Cause:** Many commands are placeholder implementations  
**Status:** 🚨 **KNOWN ISSUE** - 11 commands are broken, see [AIPM_COMMANDS_API.md](AIPM_COMMANDS_API.md)

**Broken commands that just echo text:**
- `aipm_research_quick` - Should do AI research, just shows usage
- `aipm_company_lookup` - Should lookup financial data, just shows usage  
- `aipm_data_generator` - Should generate data, just echoes text
- All PoL Probe commands (`aipm learn`, `aipm fast`, etc.)

**Working alternatives:**
```bash
# Instead of broken research commands, use:
aipm_brainstorm             # AI collaboration that actually works
aipm_lab                    # Data analysis that actually works
aipm_workflows              # Visual tools that actually work
```

---

## 🔧 Installation Issues

### "Command not found: aipm_workflows"
**Problem:** Shell doesn't recognize aipm commands  
**Solutions:**

1. **Restart your terminal** (most common fix)
2. **Reload shell config:**
   ```bash
   source ~/.zshrc  # or ~/.bashrc
   ```
3. **Check if environment is loaded:**
   ```bash
   echo $AIPM_TOOLKIT_DIR
   # Should show path to toolkit directory
   ```
4. **Reinstall if needed:**
   ```bash
   cd ai-pm-exploration-toolkit
   python installer.py --tier 1  # or 2, 3
   ```

### "Permission denied" when running installer
**Problem:** Installer script lacks execution permissions  
**Solution:**
```bash
chmod +x install.sh
chmod +x installer.py
```

### "Docker not found" errors
**Problem:** Docker not installed or not running  
**Solutions:**

1. **Install Docker Desktop:** https://docker.com/products/docker-desktop
2. **Start Docker:**
   - macOS: Open Docker Desktop application
   - Linux: `sudo systemctl start docker`
3. **Verify Docker is running:**
   ```bash
   docker --version
   docker info
   ```

---

## 🐳 Docker & Container Issues

### Port Conflicts ("Port already in use")
**Problem:** Another process is using the required ports  
**Quick Fix:**
```bash
aipm_workflows_fix          # Choose option 1 to kill port conflicts
```

**Manual Fix:**
```bash
# See what's using port 5678 (n8n)
sudo lsof -i :5678

# Kill the process
sudo lsof -ti:5678 | xargs kill

# Common ports to check:
# 5678 (n8n), 7860 (Langflow), 8082 (ToolJet), 8888 (Jupyter)
```

### Containers start but URLs don't work
**Problem:** Containers are running but web interfaces don't load  
**Solutions:**

1. **Wait longer** - Some tools take 30-60 seconds to fully initialize
2. **Check container logs:**
   ```bash
   docker-compose -f workflow-tools/docker-compose.n8n.yml logs
   ```
3. **Check if containers are actually healthy:**
   ```bash
   aipm_workflows_status
   docker ps
   ```
4. **Restart specific container:**
   ```bash
   docker-compose -f workflow-tools/docker-compose.n8n.yml restart
   ```

### "Docker daemon not running"
**Problem:** Docker service isn't started  
**Solutions:**

1. **macOS:** Open Docker Desktop app
2. **Linux:** 
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker  # Start on boot
   ```
3. **Windows:** Start Docker Desktop from Start menu

### Containers consume too much resources
**Problem:** System running slow, Docker using too much CPU/memory  
**Solutions:**

1. **Stop unused containers:**
   ```bash
   aipm_workflows_stop
   docker system prune        # Remove unused containers/images
   ```
2. **Check resource usage:**
   ```bash
   docker stats              # Real-time container resource usage
   ```
3. **Increase Docker resources:** Docker Desktop → Settings → Resources

---

## 🌐 Network & Connectivity Issues

### "This site can't be reached" for localhost URLs
**Problem:** Browser can't connect to local services  
**Solutions:**

1. **Verify service is actually running:**
   ```bash
   aipm_workflows_status
   curl http://localhost:5678  # Should return HTML
   ```
2. **Check firewall/antivirus blocking localhost**
3. **Try different browser or incognito mode**
4. **Use 127.0.0.1 instead of localhost:**
   ```
   http://127.0.0.1:5678
   ```

### VPN interfering with local connections
**Problem:** Corporate VPN blocking localhost access  
**Solutions:**

1. **Disconnect VPN temporarily for local development**
2. **Configure VPN to allow local traffic**
3. **Use Docker Desktop with VPN-friendly settings**

---

## 💻 Platform-Specific Issues

### macOS Issues

#### "Operation not permitted" errors
**Problem:** macOS security restrictions  
**Solutions:**
```bash
# Give Terminal full disk access:
# System Preferences → Security & Privacy → Privacy → Full Disk Access → Add Terminal

# Or run with explicit permissions:
sudo python installer.py --tier 1
```

#### Homebrew installation failures
**Problem:** Homebrew packages fail to install  
**Solutions:**
```bash
# Update Homebrew
brew update
brew doctor                 # Fix common issues

# Reinstall problematic packages
brew reinstall [package-name]
```

### Linux Issues  

#### Docker permission errors
**Problem:** "Permission denied" when running Docker commands  
**Solutions:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker              # Apply group changes

# Or run with sudo (not recommended for daily use)
sudo aipm_workflows
```

#### Package manager conflicts
**Problem:** apt/yum package installation conflicts  
**Solutions:**
```bash
# Update package lists
sudo apt update            # Ubuntu/Debian
sudo yum update           # RHEL/CentOS

# Fix broken packages
sudo apt --fix-broken install
```

### Windows Issues

#### PowerShell execution policy
**Problem:** Can't run scripts due to execution policy  
**Solutions:**
```powershell
# Run as Administrator
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or bypass for single script
powershell -ExecutionPolicy Bypass -File install.ps1
```

#### WSL2 Docker integration
**Problem:** Docker doesn't work in WSL2  
**Solutions:**
1. **Enable WSL2 integration in Docker Desktop**
2. **Install Docker inside WSL2:**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```

---

## 🔍 Debugging & Diagnostics

### Get detailed system information
```bash
# Check toolkit installation
aipm_status                 # (when implemented)

# Check Docker health
docker info
docker system df           # Disk usage

# Check running containers
docker ps -a

# Check system resources
df -h                      # Disk space
free -h                    # Memory (Linux)
vm_stat                    # Memory (macOS)
```

### Enable verbose logging
```bash
# Run installer with verbose output
python installer.py --tier 1 --verbose

# Check container logs with timestamps
docker-compose logs -t -f
```

### Check network connectivity
```bash
# Test local ports
netstat -tulpn | grep :5678    # Linux
lsof -i :5678                  # macOS

# Test HTTP connectivity
curl -v http://localhost:5678
```

---

## 🚑 Emergency Fixes

### "Nuclear Reset" - When Everything is Broken
**Use when:** Multiple issues, nothing works, need fresh start  
**Steps:**
```bash
# 1. Stop everything
aipm_workflows_stop

# 2. Clean Docker completely
docker system prune -a -f     # Remove everything
docker volume prune -f        # Remove all data (WARNING: destructive)

# 3. Fix workflow tools
aipm_workflows_fix            # Choose option 6 for nuclear reset

# 4. Reinstall toolkit
cd ai-pm-exploration-toolkit
python installer.py --tier 1 --verbose

# 5. Start fresh
aipm_workflows
```

### "Soft Reset" - When Just Some Things Are Broken
```bash
# Clean just workflow tools
aipm_workflows_fix            # Interactive menu
# or
docker-compose down           # Stop specific services
docker-compose up -d          # Restart them
```

---

## 📞 Getting Help

### Before Asking for Help
Run these diagnostics and include the output:

```bash
# System info
uname -a                      # OS version
docker --version             # Docker version
python3 --version            # Python version

# Toolkit status
aipm_workflows_status         # Workflow tools status
docker ps                     # Running containers
docker system df              # Docker resource usage

# Recent logs
docker-compose logs --tail=50 -t
```

### Community Support
- **GitHub Issues:** https://github.com/deanpeters/ai-pm-exploration-toolkit/issues
- **Include:** OS, error messages, steps to reproduce
- **Don't include:** Sensitive data, API keys, personal information

### Self-Help Resources
- **[AIPM Commands API](AIPM_COMMANDS_API.md)** - Complete command reference
- **[Tool Ports Reference](TOOL_PORTS_REFERENCE.md)** - Direct tool access
- **[PM First Steps](PM_FIRST_STEPS.md)** - Getting started guide
- **Workflow Tools README** - Docker-specific troubleshooting

---

## 🎯 Quick Reference Card

### When Things Don't Work:
1. **Commands not found** → Restart terminal or `source ~/.zshrc`
2. **Tools not starting** → `aipm_workflows_fix` → Option 1 (port conflicts)
3. **Docker issues** → `aipm_workflows_fix` → Option 6 (nuclear reset)
4. **Still broken** → Check this guide's specific issue section
5. **Nothing works** → Nuclear reset + reinstall

### Most Useful Commands:
```bash
aipm_workflows_status         # What's running?
aipm_workflows_fix           # Fix problems interactively
aipm_workflows_restart       # Turn it off and on again
aipm_help                    # Complete command reference
```

**Remember:** Many commands are currently broken and just show help text. This is a known issue being fixed. Use the working commands listed in the API reference until fixes are deployed.