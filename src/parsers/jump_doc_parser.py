"""
Jump Document Parser
Parses jumpchain PDFs to extract perks, items, drawbacks, scenarios, etc.
"""

import re
import logging
from typing import Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class JumpDocParser:
    """Parser for jumpchain PDF documents"""

    def __init__(self):
        """Initialize parser with regex patterns"""

        # Common patterns for jump documents
        self.patterns = {
            # Perk patterns
            'perk_simple': re.compile(r'^(.+?)\s*\((\d+)\s*CP\)\s*:?\s*(.*)$', re.MULTILINE),
            'perk_dash': re.compile(r'^(.+?)\s*-\s*(\d+)\s*CP\s*:?\s*(.*)$', re.MULTILINE),
            'perk_brackets': re.compile(r'^\[(\d+)\s*CP\]\s*(.+?)\s*:?\s*(.*)$', re.MULTILINE),

            # Drawback patterns
            'drawback': re.compile(r'^\+(\d+)\s*CP\s*:?\s*(.+?)\s*-?\s*(.*)$', re.MULTILINE),
            'drawback_alt': re.compile(r'^(.+?)\s*\+(\d+)\s*CP\s*:?\s*(.*)$', re.MULTILINE),

            # Item patterns
            'item': re.compile(r'^(.+?)\s*\((\d+)\s*CP\)\s*:?\s*(.*)$', re.MULTILINE),

            # Section headers
            'section': re.compile(r'^([A-Z\s]{3,})\s*$', re.MULTILINE),
            'origin': re.compile(r'^(Drop-?in|Local|[A-Z][a-z]+)\s*$', re.MULTILINE),

            # CP values
            'cp_value': re.compile(r'(\d+)\s*CP'),
        }

        # Section keywords to identify content type
        self.section_keywords = {
            'perks': ['perks', 'abilities', 'powers', 'skills'],
            'items': ['items', 'equipment', 'gear', 'purchases'],
            'drawbacks': ['drawbacks', 'complications', 'hindrances'],
            'scenarios': ['scenarios', 'challenges', 'gauntlets'],
            'companions': ['companions', 'followers', 'allies'],
            'origins': ['origins', 'backgrounds', 'starting']
        }

    def parse_file(self, file_path: str) -> Dict:
        """
        Parse a jump document file

        Args:
            file_path: Path to PDF or TXT file

        Returns:
            Structured jump data
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Jump document not found: {file_path}")

        # Try to read text from file
        text = self._extract_text(file_path)

        if not text:
            logger.warning(f"Could not extract text from {file_path}")
            return self._empty_jump_data()

        # Parse the text
        return self.parse_text(text, file_path.stem)

    def _extract_text(self, file_path: Path) -> str:
        """Extract text from file (PDF or TXT)"""

        if file_path.suffix.lower() == '.txt':
            # Plain text file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()

        elif file_path.suffix.lower() == '.pdf':
            # Try PDF parsing
            try:
                import pypdf2
                with open(file_path, 'rb') as f:
                    pdf = pypdf2.PdfReader(f)
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text()
                    return text
            except ImportError:
                logger.warning("pypdf2 not installed, trying pdfplumber")

            try:
                import pdfplumber
                with pdfplumber.open(file_path) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text() or ""
                    return text
            except ImportError:
                logger.error("Neither pypdf2 nor pdfplumber installed. Cannot parse PDF.")
                return ""

        else:
            logger.warning(f"Unsupported file format: {file_path.suffix}")
            return ""

    def parse_text(self, text: str, jump_name: str = "Unknown") -> Dict:
        """
        Parse jump document text

        Args:
            text: Document text
            jump_name: Name of the jump

        Returns:
            Structured jump data
        """
        # Initialize result
        result = self._empty_jump_data()
        result['jump_name'] = jump_name

        # Extract basic metadata
        result['base_cp'] = self._extract_base_cp(text)
        result['duration_years'] = self._extract_duration(text)

        # Split into sections
        sections = self._split_into_sections(text)

        # Parse each section
        for section_name, section_text in sections.items():
            section_type = self._identify_section_type(section_name)

            if section_type == 'perks':
                perks = self._parse_perks(section_text, section_name)
                result['perks'].extend(perks)

            elif section_type == 'items':
                items = self._parse_items(section_text)
                result['items'].extend(items)

            elif section_type == 'drawbacks':
                drawbacks = self._parse_drawbacks(section_text)
                result['drawbacks'].extend(drawbacks)

            elif section_type == 'scenarios':
                scenarios = self._parse_scenarios(section_text)
                result['scenarios'].extend(scenarios)

        logger.info(f"Parsed {jump_name}: {len(result['perks'])} perks, "
                   f"{len(result['items'])} items, {len(result['drawbacks'])} drawbacks")

        return result

    def _empty_jump_data(self) -> Dict:
        """Return empty jump data structure"""
        return {
            'jump_name': 'Unknown',
            'base_cp': 1000,
            'duration_years': 10,
            'origins': [],
            'perks': [],
            'items': [],
            'drawbacks': [],
            'scenarios': [],
            'companions': []
        }

    def _extract_base_cp(self, text: str) -> int:
        """Extract base CP from jump document"""
        # Look for "1000 CP" or similar at the start
        match = re.search(r'(?:start with|receive|get)\s*(\d+)\s*CP', text, re.IGNORECASE)
        if match:
            return int(match.group(1))

        # Default to 1000
        return 1000

    def _extract_duration(self, text: str) -> int:
        """Extract jump duration in years"""
        match = re.search(r'(\d+)\s*years?', text, re.IGNORECASE)
        if match:
            return int(match.group(1))

        # Default to 10 years
        return 10

    def _split_into_sections(self, text: str) -> Dict[str, str]:
        """Split document into sections based on headers"""
        sections = {}
        current_section = "Introduction"
        current_text = []

        lines = text.split('\n')

        for line in lines:
            # Check if this is a section header (all caps, short)
            if len(line.strip()) > 0 and line.strip().isupper() and len(line.strip()) < 50:
                # Save previous section
                if current_text:
                    sections[current_section] = '\n'.join(current_text)

                # Start new section
                current_section = line.strip()
                current_text = []
            else:
                current_text.append(line)

        # Save last section
        if current_text:
            sections[current_section] = '\n'.join(current_text)

        return sections

    def _identify_section_type(self, section_name: str) -> Optional[str]:
        """Identify what type of content a section contains"""
        section_lower = section_name.lower()

        for content_type, keywords in self.section_keywords.items():
            if any(keyword in section_lower for keyword in keywords):
                return content_type

        return 'unknown'

    def _parse_perks(self, text: str, origin: str = "General") -> List[Dict]:
        """Parse perks from text"""
        perks = []

        # Try different patterns
        for pattern_name, pattern in [
            ('simple', self.patterns['perk_simple']),
            ('dash', self.patterns['perk_dash']),
            ('brackets', self.patterns['perk_brackets'])
        ]:
            matches = pattern.finditer(text)

            for match in matches:
                if pattern_name == 'brackets':
                    cost, name, description = match.groups()
                else:
                    name, cost, description = match.groups()

                # Clean up
                name = name.strip()
                description = description.strip()

                try:
                    cost_int = int(cost)
                except ValueError:
                    continue

                # Infer synergy tags from name and description
                tags = self._infer_tags(name, description)

                perks.append({
                    'name': name,
                    'cost': cost_int,
                    'description': description,
                    'origin': origin,
                    'tags': tags
                })

        return perks

    def _parse_items(self, text: str) -> List[Dict]:
        """Parse items from text"""
        items = []

        matches = self.patterns['item'].finditer(text)

        for match in matches:
            name, cost, description = match.groups()

            name = name.strip()
            description = description.strip()

            try:
                cost_int = int(cost)
            except ValueError:
                continue

            items.append({
                'name': name,
                'cost': cost_int,
                'description': description
            })

        return items

    def _parse_drawbacks(self, text: str) -> List[Dict]:
        """Parse drawbacks from text"""
        drawbacks = []

        # Try both patterns
        for pattern in [self.patterns['drawback'], self.patterns['drawback_alt']]:
            matches = pattern.finditer(text)

            for match in matches:
                groups = match.groups()

                # Handle different group orderings
                if len(groups) == 3:
                    if groups[0].isdigit():
                        cost, name, description = groups
                    else:
                        name, cost, description = groups
                else:
                    continue

                name = name.strip()
                description = description.strip()

                try:
                    cost_int = int(cost)
                except ValueError:
                    continue

                drawbacks.append({
                    'name': name,
                    'cp_value': cost_int,
                    'description': description
                })

        return drawbacks

    def _parse_scenarios(self, text: str) -> List[Dict]:
        """Parse scenarios/challenges from text"""
        scenarios = []

        # Scenarios are harder to parse automatically
        # For now, just extract paragraphs
        paragraphs = text.split('\n\n')

        for para in paragraphs:
            para = para.strip()
            if len(para) > 50:  # Substantial content
                # Try to extract a title (first line)
                lines = para.split('\n')
                title = lines[0].strip()
                description = '\n'.join(lines[1:]).strip() if len(lines) > 1 else para

                scenarios.append({
                    'name': title[:100],  # Limit title length
                    'description': description,
                    'reward': 'To be determined'
                })

        return scenarios

    def _infer_tags(self, name: str, description: str) -> List[str]:
        """Infer synergy tags from perk name and description"""
        tags = []

        text = (name + ' ' + description).lower()

        # Tag inference rules
        tag_rules = {
            'precog': ['precog', 'foresight', 'predict', 'future', 'path to victory', 'ptv'],
            'stealth': ['stealth', 'invisible', 'hidden', 'sneak', 'undetectable'],
            'combat': ['combat', 'fight', 'attack', 'weapon', 'martial', 'warrior'],
            'mental': ['mental', 'telepathy', 'mind', 'intelligence', 'smart'],
            'physical': ['physical', 'strength', 'strong', 'durable', 'tough'],
            'time': ['time', 'temporal', 'chrono', 'rewind', 'loop'],
            'healing': ['heal', 'regenerat', 'recovery', 'restoration'],
            'immortality': ['immortal', 'undying', 'eternal', 'ageless'],
            'creation': ['create', 'craft', 'make', 'build', 'summon'],
            'transmutation': ['transmut', 'transform', 'change', 'alter', 'convert'],
            'energy': ['energy', 'mana', 'power', 'magic', 'force'],
            'social': ['social', 'charisma', 'persuasi', 'diplomat', 'negotiate'],
            'tinker': ['tinker', 'tech', 'invent', 'engineer', 'mechanic'],
            'blank': ['blank', 'immune to precog', 'undetectable to'],
            'speed': ['speed', 'fast', 'quick', 'velocity', 'swift']
        }

        for tag, keywords in tag_rules.items():
            if any(keyword in text for keyword in keywords):
                tags.append(tag)

        return tags

    def create_perks_from_parsed(self, parsed_data: Dict, owner_id: int,
                                 owner_type: str = 'jumper') -> List:
        """
        Convert parsed perk data to Perk objects

        Args:
            parsed_data: Output from parse_file
            owner_id: ID of owner (jumper or companion)
            owner_type: 'jumper' or 'companion'

        Returns:
            List of Perk objects (not yet saved to database)
        """
        from ..core.models import Perk

        perks = []

        for perk_data in parsed_data.get('perks', []):
            perk = Perk(
                id=0,  # Will be assigned on save
                owner_id=owner_id,
                owner_type=owner_type,
                name=perk_data['name'],
                source_jump=parsed_data['jump_name'],
                cp_cost=perk_data['cost'],
                description=perk_data.get('description', ''),
                is_active=False,  # Not active until purchased
                evolution_stage=0,
                synergy_tags=perk_data.get('tags', []),
                mechanics={}  # To be filled in later
            )
            perks.append(perk)

        return perks
