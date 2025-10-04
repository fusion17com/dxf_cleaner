#!/usr/bin/env python3
"""
DXF Cleaner - Extracts entities and layers from DXF files and rebuilds clean versions
Usage: python dxfclean.py [targetfile.dxf]
Output: [FILENAME]_cleaned.dxf (now saved in 'Output' subfolder)
"""

import sys
import os
import re
from collections import OrderedDict
from typing import List, Dict, Tuple, Optional

class DXFEntity:
    """Represents a DXF entity with its properties"""
    def __init__(self, entity_type: str):
        self.type = entity_type
        self.properties = []
        self.layer = "0"  # Default layer
        
    def add_property(self, code: str, value: str):
        self.properties.append((code, value))
        # Track layer assignment
        if code == "8":
            self.layer = value
            
    def to_dxf(self) -> str:
        """Convert entity back to DXF format"""
        lines = ["0", self.type]
        for code, value in self.properties:
            lines.extend([code, value])
        return "\n".join(lines)

class DXFLayer:
    """Represents a DXF layer with its properties"""
    def __init__(self, name: str):
        self.name = name
        self.properties = []  # Store all properties in order
        self.color = "7"  # Default white
        self.line_type = "CONTINUOUS"
        self.line_weight = "0"
        
    def add_property(self, code: str, value: str):
        # Store all properties for later replay
        self.properties.append((code, value))
        # Also track specific properties for reference
        if code == "62":
            self.color = value
        elif code == "6":
            self.line_type = value
        elif code == "370":
            self.line_weight = value
            
    def to_dxf(self) -> str:
        """Convert layer to DXF format - preserving all original properties"""
        lines = ["0", "LAYER"]
        
        # Track which codes we've already output to avoid duplicates
        output_codes = set()
        
        # First output the standard header codes
        handle = f"{hash(self.name) % 1000:X}" # Basic unique handle generation
        standard_header = [
            ("5", handle),
            ("330", "2"), # Assuming standard handle for table dictionary
            ("100", "AcDbSymbolTableRecord"),
            ("100", "AcDbLayerTableRecord"),
            ("2", self.name),
            ("70", "0") # Layer flags
        ]
        
        for code, value in standard_header:
            lines.extend([code, value])
            if code in ["5", "330", "100", "2", "70"]: # Mark these as output
                output_codes.add(code)
        
        # Now replay all captured properties that aren't already output
        for code, value in self.properties:
            if code not in output_codes or code == "100":  # Allow multiple 100 codes
                lines.extend([code, value])
                output_codes.add(code) # Mark as output to prevent standard re-output if captured
        
        # Ensure we have the required 390 code at the end if not already present
        # (some DXF versions might require it for plot style handles)
        if "390" not in output_codes:
            lines.extend(["390", "F"]) # A common default, adjust if needed
            
        return "\n".join(lines)

class DXFCleaner:
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.output_file = self._generate_output_filename() ## MODIFIED: This will now point to Output/
        self.layers: Dict[str, DXFLayer] = OrderedDict()
        self.entities: List[DXFEntity] = []
        self.header_template = ""
        self.footer_template = ""
        
    def _generate_output_filename(self) -> str: ## MODIFIED ##
        """Generate output filename, placing it in the 'Output' subfolder."""
        # Get the base name of the input file (e.g., "example1.dxf")
        base_name_with_ext = os.path.basename(self.input_file)
        # Get the name without extension (e.g., "example1")
        name_without_ext = os.path.splitext(base_name_with_ext)[0]
        # Construct the new filename part (e.g., "example1_cleaned.dxf")
        output_filename_part = f"{name_without_ext}_cleaned.dxf"
        
        # Define the output directory relative to the script's Current Working Directory
        # The batch script will ensure CWD is the root project folder.
        output_dir_relative_to_cwd = "Output" 
        
        # Join them to get the full path for the output file
        # e.g., "Output/example1_cleaned.dxf"
        return os.path.join(output_dir_relative_to_cwd, output_filename_part)
        
    def load_templates(self):
        """Load header and footer templates"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        header_path = os.path.join(script_dir, "dxf_header_header.txt")
        if not os.path.exists(header_path):
            print(f"Error: Header template not found at {header_path}")
            print("Using minimal header instead.")
            self.header_template = self._generate_minimal_header()
        else:
            with open(header_path, 'r') as f:
                self.header_template = f.read()
                
        footer_path = os.path.join(script_dir, "dxf_footer.txt")
        if not os.path.exists(footer_path):
            print(f"Error: Footer template not found at {footer_path}")
            print("Using minimal footer instead.")
            self.footer_template = self._generate_minimal_footer()
        else:
            with open(footer_path, 'r') as f:
                self.footer_template = f.read()
                
    def _generate_minimal_header(self) -> str:
        return """999
DXF Cleaner Generated File
0
SECTION
2
HEADER
9
$ACADVER
1
AC1021
9
$INSBASE
10
0
20
0
30
0
9
$EXTMIN
10
-1000
20
-1000
30
0
9
$EXTMAX
10
1000
20
1000
30
0
0
ENDSEC
0
SECTION
2
CLASSES
0
ENDSEC
0
SECTION
2
TABLES
0
TABLE
2
VPORT
5
8
330
0
100
AcDbSymbolTable
70
1
0
VPORT
5
31
330
2
100
AcDbSymbolTableRecord
100
AcDbViewportTableRecord
2
*ACTIVE
70
0
10
0
20
0
11
1
21
1
12
0
22
0
13
0
23
0
14
10
24
10
15
10
25
10
16
0
26
0
36
1
17
0
27
0
37
0
40
297
41
1.34
42
50
43
0
44
0
50
0
51
0
71
0
72
100
73
1
74
3
75
0
76
1
77
0
78
0
0
ENDTAB
0
TABLE
2
LTYPE
5
5
330
0
100
AcDbSymbolTable
70
4
0
LTYPE
5
14
330
5
100
AcDbSymbolTableRecord
100
AcDbLinetypeTableRecord
2
ByBlock
70
0
3

72
65
73
0
40
0
0
LTYPE
5
15
330
5
100
AcDbSymbolTableRecord
100
AcDbLinetypeTableRecord
2
ByLayer
70
0
3

72
65
73
0
40
0
0
LTYPE
5
16
330
5
100
AcDbSymbolTableRecord
100
AcDbLinetypeTableRecord
2
Continuous
70
0
3
Solid line
72
65
73
0
40
0
0
ENDTAB
0
TABLE
2
LAYER
5
2
330
0
100
AcDbSymbolTable
70
1"""
    
    def _generate_minimal_footer(self) -> str:
        return """ENDSEC
0
SECTION
2
OBJECTS
0
DICTIONARY
5
C
330
0
100
AcDbDictionary
281
1
3
ACAD_GROUP
350
D
0
DICTIONARY
5
D
330
C
100
AcDbDictionary
281
1
0
PLOTSETTINGS
5
55
100
AcDbPlotSettings
6
1x1
40
0
41
0
42
0
43
0
0
ENDSEC
0
EOF"""
    
    def parse_dxf(self):
        try:
            with open(self.input_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading file: {e}")
            return False
            
        lines = [line.strip() for line in lines]
        
        i = 0
        in_entities_section = False
        in_blocks_section = False
        in_tables_section = False
        in_layer_table = False
        
        while i < len(lines):
            if lines[i] == "0" and i + 1 < len(lines):
                if lines[i + 1] == "SECTION" and i + 3 < len(lines):
                    section_name = lines[i + 3]
                    if section_name == "ENTITIES":
                        in_entities_section = True
                        in_blocks_section = False
                        in_tables_section = False
                        i += 4
                        continue
                    elif section_name == "BLOCKS":
                        in_blocks_section = True
                        in_entities_section = False
                        in_tables_section = False
                        i += 4
                        continue
                    elif section_name == "TABLES":
                        in_tables_section = True
                        in_entities_section = False
                        in_blocks_section = False
                        i += 4
                        continue
                elif lines[i + 1] == "ENDSEC":
                    in_entities_section = False
                    in_blocks_section = False
                    in_tables_section = False
                    in_layer_table = False
                    i += 2
                    continue
                    
            if in_tables_section and lines[i] == "0" and i + 1 < len(lines):
                if lines[i + 1] == "TABLE" and i + 3 < len(lines) and lines[i + 3] == "LAYER":
                    in_layer_table = True
                    i += 4
                    continue
                elif lines[i + 1] == "ENDTAB":
                    in_layer_table = False
                    i += 2
                    continue
                    
            if in_layer_table and lines[i] == "0" and i + 1 < len(lines) and lines[i + 1] == "LAYER":
                layer = self._parse_layer(lines, i)
                if layer and layer.name != "0":
                    self.layers[layer.name] = layer
                    
            if in_entities_section and lines[i] == "0" and i + 1 < len(lines):
                entity_type = lines[i + 1]
                if entity_type in ["LINE", "CIRCLE", "ARC"]: # Add more entity types if needed
                    entity = self._parse_entity(lines, i, entity_type)
                    if entity:
                        self.entities.append(entity)
                        
            i += 1
            
        if "0" not in self.layers:
            default_layer = DXFLayer("0")
            self.layers["0"] = default_layer
            
        print(f"Parsed {len(self.layers)} layers and {len(self.entities)} entities from {self.input_file}")
        return True
        
    def _parse_layer(self, lines: List[str], start_idx: int) -> Optional[DXFLayer]:
        i = start_idx + 2
        layer_name = None
        layer = None
        
        while i < len(lines) - 1:
            code = lines[i]
            value = lines[i + 1]
            
            if code == "0":
                break
                
            if code == "2":
                layer_name = value
                layer = DXFLayer(layer_name)
            elif layer and code not in ["5", "330", "100", "70"]: # Avoid re-adding standard codes we generate
                layer.add_property(code, value)
                
            i += 2
            
        return layer
        
    def _parse_entity(self, lines: List[str], start_idx: int, entity_type: str) -> Optional[DXFEntity]:
        entity = DXFEntity(entity_type)
        i = start_idx + 2
        
        while i < len(lines) - 1:
            code = lines[i]
            value = lines[i + 1]
            
            if code == "0":
                break
                
            entity.add_property(code, value)
            i += 2
            
        return entity
        
    def generate_layer_section(self) -> str:
        layer_lines = []
        
        # Ensure layer 0 is ordered first if it exists, then others
        sorted_layers = OrderedDict()
        if "0" in self.layers:
            sorted_layers["0"] = self.layers["0"]
        for name, layer in self.layers.items():
            if name != "0":
                sorted_layers[name] = layer

        for name, layer in sorted_layers.items():
            layer_lines.append(layer.to_dxf())
                
        return "\n".join(layer_lines) + "\n0\nENDTAB" # Added missing newline before 0/ENDTAB
        
    def build_clean_dxf(self) -> str:
        header_parts = self.header_template.split("TABLE\n2\nLAYER")
        dxf_content = ""
        if len(header_parts) != 2:
            print("Warning: Header template format unexpected or LAYER table marker not found. Using full template.")
            # This part needs to correctly insert layer count if format is different
            # For now, assuming the split works or we rebuild more manually.
            # A safer approach might be to parse until layer table, insert, then append rest.
            # For simplicity, using original logic, but this is a fragile point.
            # Minimal header has "70\n1" for layer count, this needs dynamic update.
            if "Minimal" in self.header_template: # A bit of a hacky check
                 self.header_template = self.header_template.replace("70\n1", f"70\n{len(self.layers)}")
            dxf_content = self.header_template # This would be problematic if LAYER table is in it.
                                               # For minimal header, it ends just before layer entries.
        else:
            # Standard header template should end before actual layer definitions
            dxf_content = header_parts[0] + "TABLE\n2\nLAYER\n5\n2\n330\n0\n100\nAcDbSymbolTable\n70\n" + str(len(self.layers)) + "\n"
        
        dxf_content += self.generate_layer_section()
        
        # This is the continuation part of the header/tables after layers
        # Assuming the original header_template.split worked, header_parts[1] would contain this.
        # If using minimal_header, it stops at LAYER table declaration.
        # The following is a fixed block of tables, which is fine.
        dxf_content += """
0
TABLE
2
STYLE
5
3
330
0
100
AcDbSymbolTable
70
3
0
STYLE
5
4A
330
2
100
AcDbSymbolTableRecord
100
AcDbTextStyleTableRecord
2
Standard
70
0
40
0
41
1
50
0
71
0
42
1
3
txt
4

0
ENDTAB
0
TABLE
2
VIEW
5
6
330
0
100
AcDbSymbolTable
70
0
0
ENDTAB
0
TABLE
2
UCS
5
7
330
0
100
AcDbSymbolTable
70
0
0
ENDTAB
0
TABLE
2
APPID
5
9
330
0
100
AcDbSymbolTable
70
1
0
APPID
5
12
330
9
100
AcDbSymbolTableRecord
100
AcDbRegAppTableRecord
2
ACAD
70
0
0
ENDTAB
0
TABLE
2
DIMSTYLE
5
A
330
0
100
AcDbSymbolTable
70
1
100
AcDbDimStyleTable
71
1
0
DIMSTYLE
105
4C
330
A
100
AcDbSymbolTableRecord
100
AcDbDimStyleTableRecord
2
Standard
70
0
40
1
41
2.5
42
0.625
43
0.38
44
1.25
45
0
46
0
47
0
48
0
49
1
140
2.5
141
0.09
142
2.5
143
25.4
144
1
145
0
146
1
147
0.625
148
0
71
0
72
0
73
0
74
1
75
0
76
0
77
0
78
1
79
0
170
0
171
2
172
0
173
0
174
0
175
0
176
0
177
0
178
0
179
0
271
2
272
4
273
2
274
2
275
0
276
0
277
2
278
0
279
0
280
0
281
0
282
0
283
1
284
0
285
0
286
0
288
0
289
3
340
standard
341

371
-2
372
-2
0
ENDTAB
0
TABLE
2
BLOCK_RECORD
5
1
330
0
100
AcDbSymbolTable
70
2
0
BLOCK_RECORD
5
1F
330
1
100
AcDbSymbolTableRecord
100
AcDbBlockTableRecord
2
*Model_Space
70
0
280
1
281
0
0
BLOCK_RECORD
5
1E
330
1
100
AcDbSymbolTableRecord
100
AcDbBlockTableRecord
2
*Paper_Space
70
0
280
1
281
0
0
ENDTAB
0
ENDSEC
0
SECTION
2
BLOCKS
0
BLOCK
5
20
330
1F
100
AcDbEntity
8
0
100
AcDbBlockBegin
2
*Model_Space
70
0
10
0
20
0
30
0
3
*Model_Space
1

0
ENDBLK
5
21
330
1F
100
AcDbEntity
8
0
100
AcDbBlockEnd
0
BLOCK
5
1C
330
1B
100
AcDbEntity
8
0
100
AcDbBlockBegin
2
*Paper_Space
70
0
10
0
20
0
30
0
3
*Paper_Space
1

0
ENDBLK
5
1D
330
1F
100
AcDbEntity
8
0
100
AcDbBlockEnd
0
ENDSEC
0
SECTION
2
ENTITIES
"""
        
        handle_counter = 50 # Starting handle for entities, simple hex counter
        for entity in self.entities:
            has_handle = False
            for i, (code, value) in enumerate(entity.properties):
                if code == "5":
                    has_handle = True
                    break
            if not has_handle:
                # Insert handle as the first property after "0" and entity type
                entity.properties.insert(0, ("5", f"{handle_counter:X}"))
                handle_counter += 1
                
            dxf_content += entity.to_dxf() + "\n"
            
        dxf_content += "0\n" + self.footer_template # Ensures ENDSEC is followed by 0/EOF
        
        return dxf_content
        
    def save_cleaned_dxf(self, content: str): ## MODIFIED ##
        """Save the cleaned DXF file, ensuring the output directory exists."""
        try:
            # self.output_file now includes the "Output/" prefix
            output_dir = os.path.dirname(self.output_file)
            
            # Create the output directory if it doesn't exist.
            # os.makedirs with exist_ok=True won't raise an error if the directory already exists.
            # This is safe as f-strings imply Python 3.6+
            if output_dir: # Ensure output_dir is not an empty string (e.g. if saving to CWD)
                os.makedirs(output_dir, exist_ok=True)
            
            with open(self.output_file, 'w') as f:
                f.write(content)
            print(f"Cleaned DXF saved to: {self.output_file}")
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
            
    def clean(self):
        print(f"Processing: {self.input_file}")
        self.load_templates()
        if not self.parse_dxf():
            return False
        clean_content = self.build_clean_dxf()
        return self.save_cleaned_dxf(clean_content)
        
def main():
    if len(sys.argv) != 2:
        print("Usage: python clean_main.py [targetfile.dxf]")
        sys.exit(1)
        
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
        
    if not input_file.lower().endswith('.dxf'):
        print("Error: Input file must be a DXF file")
        sys.exit(1)
        
    cleaner = DXFCleaner(input_file)
    if cleaner.clean():
        print(f"Cleaning of {os.path.basename(input_file)} completed successfully!")
    else:
        print(f"Cleaning of {os.path.basename(input_file)} failed!")
        # sys.exit(1) # Decide if one failure should stop the whole batch

if __name__ == "__main__":
    main()