# Z-Library Bots Collection

This is an organized collection of Z-Library bots and tools. All files are now properly grouped into folders.

## 📁 Folder Structure

```
zlibrary_bots/
├── individual/          # Standalone individual bots
├── examples/           # Example implementations  
├── test_tools/         # Testing and diagnostic tools
├── docs/              # Documentation files
└── README.md          # This file
```

## 🤖 Individual Bots (`individual/`)

**Standalone bots - each works completely independently:**

- **`simple_bot.py`** - Easy-to-use bot for quick searches
  - Demo mode and interactive mode
  - Simple search with beautiful display
  - Results saved to `simple_bot_results/`

- **`batch_bot.py`** - Batch processing bot
  - Process multiple searches at once
  - Generate JSON, CSV, and text reports
  - Results saved to `batch_results/`

- **`zlibrary_bot.py`** - Full-featured CLI bot
  - Advanced filters (year, language, format)
  - Multiple output formats
  - Tor support for privacy

- **`zlibrary_integration.py`** - Integration helper
  - For adding Z-Library to existing bots
  - Clean integration patterns

## 📚 Examples (`examples/`)

**Learning and reference implementations:**

- **`quick_start_zlibrary.py`** - Minimal demo (163 lines)
- **`zlibrary_example.py`** - Feature showcase (364 lines)
- **`fixed_zlibrary_example.py`** - Robust error handling

## 🔧 Test Tools (`test_tools/`)

**Testing and diagnostic utilities:**

- **`diagnose_zlibrary.py`** - Installation checker
- **`simple_test_bot.py`** - Quick functionality test
- **`simple_zlibrary_test.py`** - Basic verification

## 📖 Documentation (`docs/`)

**Complete guides and references:**

- **`ZLIBRARY_README.md`** - Complete usage guide
- **`ZLIBRARY_SUMMARY.md`** - Quick overview
- **`TEST_BOTS_README.md`** - Testing documentation
- **`INDIVIDUAL_BOTS_SUMMARY.md`** - Individual bots guide

## 🚀 Quick Start

### 1. Choose Your Bot

**For simple searches:**
```bash
cd zlibrary_bots/individual
python simple_bot.py
```

**For batch processing:**
```bash
cd zlibrary_bots/individual  
python batch_bot.py
```

**For full features:**
```bash
cd zlibrary_bots/individual
python zlibrary_bot.py
```

### 2. Test Installation

```bash
cd zlibrary_bots/test_tools
python diagnose_zlibrary.py
```

### 3. Try Examples

```bash
cd zlibrary_bots/examples
python quick_start_zlibrary.py
```

## 📋 Requirements

Install Z-Library package:
```bash
pip install --break-system-packages zlibrary
```

Or if you prefer virtual environment:
```bash
python -m venv zlib_env
source zlib_env/bin/activate  # Linux/Mac
zlib_env\Scripts\activate     # Windows
pip install zlibrary
```

## 🎯 Bot Features Comparison

| Feature | Simple Bot | Batch Bot | Full Bot |
|---------|------------|-----------|----------|
| Easy search | ✅ | ➖ | ✅ |
| Batch processing | ➖ | ✅ | ✅ |
| Advanced filters | ➖ | ➖ | ✅ |
| Multiple formats | ➖ | ✅ | ✅ |
| Interactive mode | ✅ | ✅ | ✅ |
| Demo mode | ✅ | ✅ | ✅ |

## 🔍 What Each Bot Does

### Simple Bot
- Perfect for beginners
- Quick search and save
- Clean, easy interface
- Demo with tech books

### Batch Bot  
- Process multiple searches
- Generate detailed reports
- CSV/JSON/Text exports
- Perfect for research

### Full Bot
- All advanced features
- Year/language filters
- Tor network support
- Professional CLI

## 📁 Output Directories

Each bot creates its own results folder:
- Simple Bot → `simple_bot_results/`
- Batch Bot → `batch_results/`
- Full Bot → `zlibrary_results/`

## 🛠️ Troubleshooting

1. **Installation issues?** Run `test_tools/diagnose_zlibrary.py`
2. **Import errors?** Check examples in `examples/`
3. **Need help?** Read guides in `docs/`

## 📝 Usage Examples

**Quick search:**
```bash
python individual/simple_bot.py
# Choose: 1 (demo) or 2 (interactive)
```

**Batch process:**
```bash
python individual/batch_bot.py  
# Choose: 1 (sample) or 2 (custom)
```

**Full features:**
```bash
python individual/zlibrary_bot.py
# Many options available
```

## 🎉 All Files Organized!

No more confusion with scattered files. Everything is now:
- ✅ Properly grouped
- ✅ Easy to find  
- ✅ Well documented
- ✅ Ready to use

Choose the bot that fits your needs and start searching! 🚀