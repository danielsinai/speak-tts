#!/bin/bash
set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}📦 Building package...${NC}"
python -m build

echo -e "${YELLOW}📤 Uploading to PyPI...${NC}"
twine upload dist/*

echo -e "${GREEN}✅ Published to PyPI!${NC}"

# Get the SHA256
TARBALL=$(ls dist/*.tar.gz | head -1)
SHA256=$(shasum -a 256 "$TARBALL" | cut -d' ' -f1)

echo ""
echo -e "${GREEN}📋 Update your Homebrew formula with:${NC}"
echo "   sha256 \"$SHA256\""
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Create repo: github.com/YOUR_USERNAME/homebrew-speak-tts"
echo "2. Copy Formula/speak-tts.rb to that repo"
echo "3. Update the sha256 in the formula"
echo "4. Push to GitHub"
echo ""
echo "Users can then install with:"
echo "   brew tap YOUR_USERNAME/speak-tts"
echo "   brew install speak-tts"

