#!/bin/bash
# 🚀 Quick Setup Script for RecruitEM Phase 3

echo "🚀 RecruitEM Phase 3 - Setup Script"
echo "===================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 not found. Please install Python 3.6+ first."
    exit 1
fi

# Show Python version
PYTHON_VERSION=$(python3 --version)
echo "✅ Found: $PYTHON_VERSION"
echo ""

# Check if venv already exists
if [ -d "venv" ]; then
    echo "📦 Virtual environment already exists at ./venv"
    read -p "   Remove and recreate? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing old venv..."
        rm -rf venv
    else
        echo "✅ Using existing venv"
        source venv/bin/activate
        echo ""
        echo "🎉 Setup complete! Virtual environment activated."
        echo ""
        echo "📝 Next steps:"
        echo "   python3 orchestrator.py    # Run demo"
        echo "   python3 examples.py        # Run examples"
        echo "   deactivate                 # Exit venv when done"
        exit 0
    fi
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

if [ ! -d "venv" ]; then
    echo "❌ Error: Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
python -m pip install --upgrade pip --quiet

echo "✅ pip upgraded"
echo ""

# Ask about optional dependencies
echo "📦 Optional Dependencies:"
echo "   • anthropic - For AI-powered interview tips (requires API key)"
echo ""
read -p "   Install optional dependencies? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📥 Installing dependencies from requirements.txt..."
    pip install -r requirements.txt --quiet
    echo "✅ Dependencies installed"
else
    echo "⏭️  Skipping optional dependencies"
    echo "   (The orchestrator works fine without them!)"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "===================================="
echo "📝 Quick Commands:"
echo "===================================="
echo ""
echo "Run the demo:"
echo "   python3 orchestrator.py"
echo ""
echo "Run examples:"
echo "   python3 examples.py"
echo ""
echo "Use as library:"
echo "   python3"
echo "   >>> from orchestrator import orchestrate"
echo "   >>> orchestrate('Alice', 'alice@test.com', 'Assessment', 'J123')"
echo ""
echo "Deactivate venv when done:"
echo "   deactivate"
echo ""
echo "===================================="
echo ""

# Test import
echo "🧪 Testing import..."
if python -c "from orchestrator import orchestrate; print('✅ Import successful')" 2>/dev/null; then
    echo ""
    echo "🎊 All systems go! Ready to orchestrate! 🚀"
else
    echo "⚠️  Warning: Import test failed (but it should still work)"
fi

echo ""

