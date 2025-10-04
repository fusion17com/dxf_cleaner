# DXF Cleaner

A Python utility to clean and optimize DXF files by removing unnecessary entities and rebuilding a streamlined file structure.

This tool was specifically developed to address issues with DXF files exported from LibreCAD that contain deleted or invisible blocks, which can cause bloated file sizes and import problems in other CAD applications.

## Important Note

This code is primarily developed to preserve LINE, CIRCLE, and ARC entities. No special testing has been performed with other entity types such as POLYLINE, LWPOLYLINE, TEXT, SPLINE, etc. Other entity types present in the source file will be ignored and will not appear in the cleaned output.

If you need to preserve additional entity types, you can modify the entity type list in the parse_dxf() method of dxf_cleaner.py.

## Features

- Removes junk entities and invisible blocks from DXF files
- Reduces file size by stripping unnecessary data
- Preserves complete layer structure including names, colors, line types, and properties
- Batch processing support via Windows batch file
- Improves compatibility with other CAD applications

## Supported Entities

Currently supported:
- LINE
- CIRCLE
- ARC

All other entity types are ignored during processing.

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Installation

### Download Release

Download the latest release from https://github.com/fusion17com/dxf_cleaner/releases

Extract to your desired location. The following folders will be included:
- Input (place your DXF files here)
- Output (cleaned files appear here)
- Archive (created automatically by delete.bat)

### Clone Repository

```bash
git clone https://github.com/fusion17com/dxf_cleaner.git
cd dxf_cleaner
```

Create the Input and Output folders manually if they don't exist:

```bash
mkdir Input
mkdir Output
```

## Usage

### Windows Batch Processing (Windows Only)

The project includes two batch files for easy workflow management:

#### 1. clean_dxf.bat - Main Processing Script

This script processes all DXF files in the Input folder and saves cleaned versions to the Output folder.

**Usage:**
1. Place your DXF files in the Input folder
2. Double-click clean_dxf.bat
3. The script will:
   - Check for required files and folders
   - Create Output folder if it doesn't exist
   - Process each .dxf file from Input folder
   - Save cleaned files to Output folder with _cleaned.dxf suffix
4. Review results in the Output folder

**Example Output:**
```
Input/drawing.dxf  ->  Output/drawing_cleaned.dxf
Input/plan.dxf     ->  Output/plan_cleaned.dxf
```

#### 2. delete.bat - Archive and Cleanup Script

This script archives all DXF files from Input and Output folders, effectively cleaning your workspace.

**Usage:**
1. Double-click delete.bat
2. Review the confirmation message
3. Press Enter to proceed (or close window to cancel)
4. The script will:
   - Create Archive folder if it doesn't exist
   - Move all .dxf files from Input to Archive
   - Move all .dxf files from Output to Archive
   - Leave Input and Output folders empty

**When to use:** After you have reviewed your cleaned files and want to prepare for a new batch of work.

### Python Command Line (Cross-Platform)

Process a single file directly using Python:

```bash
python dxf_cleaner.py input_file.dxf
```

**Example 1: Basic usage**
```bash
python dxf_cleaner.py drawing.dxf
```
Output: `Output/drawing_cleaned.dxf`

**Example 2: File with path**
```bash
python dxf_cleaner.py C:/CAD_Files/project_plan.dxf
```
Output: `Output/project_plan_cleaned.dxf`

**Example 3: Process file from Input folder**
```bash
python dxf_cleaner.py Input/building_layout.dxf
```
Output: `Output/building_layout_cleaned.dxf`

**Note:** The cleaned file is always saved to the Output subfolder relative to where the script is located, regardless of the input file location.

### Typical Workflow (Windows)

1. Place DXF files in Input folder
2. Run clean_dxf.bat to process all files
3. Review cleaned files in Output folder
4. Run delete.bat to archive everything and clear workspace for next batch

This workflow keeps your workspace organized and maintains backups in the Archive folder.

## How It Works

1. Parses the input DXF file to extract:
   - Complete layer structure with all properties
   - LINE, CIRCLE, and ARC entities
   - Entity coordinates and attributes

2. Rebuilds a clean DXF file with:
   - Proper DXF structure
   - All original layers preserved
   - Only supported entities
   - Optimized file size

3. Outputs the result with _cleaned.dxf suffix

## File Structure

```
dxf_cleaner/
├── Input/              Input folder for DXF files
├── Output/             Output folder for cleaned files
├── Archive/            Archive folder (created automatically)
├── clean_dxf.bat       Batch processing script (Windows)
├── delete.bat          Archive and cleanup script (Windows)
├── dxf_cleaner.py      Main Python script
├── README.md           Documentation
└── LICENSE             MIT License
```

## Limitations

- Only LINE, CIRCLE, and ARC entities are preserved
- Other entity types (POLYLINE, TEXT, DIMENSION, etc.) are not processed
- Complex DXF features may not be fully supported
- Minimal testing performed on DXF versions other than AC1021
- Batch files (clean_dxf.bat and delete.bat) only work on Windows
- Python script is cross-platform compatible (Windows, Linux, macOS)

## Troubleshooting

**No output files generated**
- Verify input files have .dxf extension
- Check that files contain LINE, CIRCLE, or ARC entities
- Review console output for error messages

**Missing entities in output**
- Only LINE, CIRCLE, and ARC entities are preserved
- Other entity types are intentionally ignored

**Python script not found (clean_dxf.bat error)**
- Ensure dxf_cleaner.py is in the same folder as clean_dxf.bat
- Check the error message for the exact path being searched

**Input directory not found (clean_dxf.bat error)**
- Create an Input subfolder in the project directory
- Ensure the folder is named exactly "Input" (case-sensitive on some systems)

**Archive folder issues (delete.bat)**
- Check folder permissions if Archive cannot be created
- Verify no DXF files are open in other applications before archiving
- The Archive folder is created automatically on first run of delete.bat

**Batch files don't work**
- Batch files only work on Windows operating systems
- On Linux/macOS, use the Python script directly from command line

## Contributing

Contributions are welcome. Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Author

fusion17com

https://github.com/fusion17com/dxf_cleaner

## Acknowledgments

Created to solve DXF compatibility issues between LibreCAD and other CAD applications.