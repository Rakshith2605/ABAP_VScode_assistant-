# 🚀 Quick Start Guide - ABAP VSCode Assistant

Get your ABAP AI Code Completion extension up and running in minutes!

## ⚡ Prerequisites

- **Python 3.11+** (recommended)
- **Conda** (for environment management)
- **Groq API Key** (get one at [groq.com](https://groq.com))

## 🎯 Quick Setup (3 Steps)

### 1. Install Dependencies

```bash
# Option A: Use the setup script (recommended)
python setup.py

# Option B: Manual installation
conda create -n abap-assistant python=3.11
conda activate abap-assistant
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Groq API key
GROQ_API_KEY=your_actual_api_key_here
```

### 3. Test Installation

```bash
# Test the backend
python extension/python/test_backend.py

# Test the main application
python extension/python/main.py config
```

## 🔧 Manual Setup (Detailed)

### Step 1: Create Conda Environment

```bash
# Create a new environment
conda create -n abap-assistant python=3.11

# Activate the environment
conda activate abap-assistant
```

### Step 2: Install Dependencies

```bash
# Navigate to project directory
cd ABAP_VScode_assistant-

# Install from requirements.txt
pip install -r requirements.txt
```

### Step 3: Environment Configuration

```bash
# Create .env file
cp .env.example .env

# Edit .env with your settings
nano .env  # or use your preferred editor
```

**Required Environment Variables:**
- `GROQ_API_KEY`: Your Groq API key
- `GROQ_BASE_URL`: Groq API endpoint (default: https://api.groq.com)

**Optional Environment Variables:**
- `LACC_MODEL_NAME`: AI model to use (default: llama-3.3-70b-versatile)
- `LACC_TEMPERATURE`: Generation randomness (default: 0.3)
- `LACC_TOP_P`: Nucleus sampling (default: 0.3)

### Step 4: Verify Installation

```bash
# Run the test suite
python extension/python/test_backend.py

# Check configuration
python extension/python/main.py config
```

## 🎮 Usage Examples

### Basic Code Generation

```bash
# Set context variables
export LACC_PREFIX="DATA: lv_name TYPE string."
export LACC_SUFFIX="WRITE: lv_name."

# Generate code
python extension/python/main.py generate
```

### Debug Code Generation

```bash
# Set debug mode
export LACC_MODE=debug
export LACC_PREFIX="LOOP AT lt_data INTO ls_data."

# Generate debug code
python extension/python/main.py generate
```

### Comment-Based Generation

```bash
# Set comment context
export LACC_COMMENT="Validate input parameters"
export LACC_PREFIX="METHOD validate_input."

# Generate implementation
python extension/python/main.py generate
```

## 🐛 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Make sure you're in the right environment
conda activate abap-assistant

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**2. API Key Issues**
```bash
# Check your .env file
cat .env

# Verify API key is set
echo $GROQ_API_KEY
```

**3. Python Version Issues**
```bash
# Check Python version
python --version

# Should be 3.11 or higher
```

**4. Conda Environment Issues**
```bash
# List environments
conda env list

# Remove and recreate if needed
conda env remove -n abap-assistant
conda create -n abap-assistant python=3.11
```

### Getting Help

- **Check logs**: Look for error messages in the terminal output
- **Verify dependencies**: Run `python extension/python/test_backend.py`
- **Check configuration**: Run `python extension/python/main.py config`

## 📚 Next Steps

Once you have the basic setup working:

1. **Explore the VS Code Extension**: Check out `extension/` directory
2. **Customize Configuration**: Modify settings in `.env`
3. **Test Different Models**: Try different Groq models
4. **Build the Extension**: Use `extension/build.sh` to create VSIX package

## 🔗 Useful Commands

```bash
# Activate environment
conda activate abap-assistant

# Deactivate environment
conda deactivate

# List installed packages
pip list

# Update dependencies
pip install -r requirements.txt --upgrade

# Check Python path
python -c "import sys; print(sys.path)"
```

## 🎉 Success!

If you see "✅ All tests passed!" when running the test suite, you're ready to use the ABAP VSCode Assistant!

---

**Need help?** Check the main README.md or run the test suite to diagnose issues.
